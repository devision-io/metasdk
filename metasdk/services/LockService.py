import random
import time
import redis
from contextlib import contextmanager

from metasdk.exceptions import LockServiceError


class LockService:
    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
        self.__redis_storage = None
        self.__unique_name = None
        self.__key = None
        self.__names = None

    def __connect_to_redis(self):
        if not self.__redis_storage:
            url_parts = self.__app.redis_url.split(':')
            self.__redis_storage = redis.Redis(host=url_parts[0], port=url_parts[1], db=url_parts[2])

    @contextmanager
    def lock(self, key: str, ttl_in_sec: int, timeout_in_sec: int, queue_width: int = 1):
        is_set = None
        self.__connect_to_redis()
        waiting_time = random.randint(1, 3)
        time.sleep(0.0001 * waiting_time)
        key = key + str(random.randint(1, queue_width))

        try:
            while timeout_in_sec > 0:
                is_set = self.__redis_storage.set(name=key, value=True, ex=ttl_in_sec, nx=True)
                if is_set:
                    yield
                    break
                else:
                    time.sleep(waiting_time)
                    timeout_in_sec -= waiting_time
            else:
                # Этот "else" относится к "while" и выполнится если не отработает "break"
                msg = "Функция с ключом {}, не смогла захватить лок за отведенное время".format(key)
                self.__app.log.warning(msg)
                raise LockServiceError(msg)

        except redis.exceptions.ConnectionError as e:
            error_msg = ("Ошибка подключения к redis", {"e": e})
            self.__app.log.error(*error_msg)
            raise LockServiceError(*error_msg)
        finally:
            if is_set:
                self.__redis_storage.delete(key)

    def lock_decorator(self, key: str, ttl_in_sec: int, timeout_in_sec: int, queue_width: int = 1, field_to_uniq=None):
        self.__key = key

        def decorator(func):
            def wrapper(*args, **kwargs):
                self.__unique_name = self.__key

                if field_to_uniq and kwargs:
                    for key, value in kwargs.items():
                        if key in field_to_uniq:
                            self.__unique_name += '_{0}-{1}'.format(key, value)

                with self.lock(key=self.__unique_name, ttl_in_sec=ttl_in_sec, timeout_in_sec=timeout_in_sec, queue_width=queue_width):
                    return func(*args, **kwargs)

            return wrapper
        return decorator

