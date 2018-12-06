import redis
import random
from time import sleep


class QueueLock(object):
    """
    Функция декоратор для блокировки и последовательного исполнения функций в разных потоках.
    Проверяет в редисе ключ LOCK_ + имя_функции + string_to_uniq + field_to_uniq,
    если он есть, то ждет, если его нет, устанавливает и выполняет функцию.

    Параметры:
    ttl_in_sec     - Сколько хранить ключ в редисе. По умолчанию 10 минут.
                     Внимание! Если это значение меньше чем время выполнения функции, логика работы будет нарушена.
    timeout_in_sec - По истечении этого времени попытки установить блокировку прекращаются, и кидается исключение.
    string_to_uniq - Любое значение которое поможет вам идентифицировать функцию(например имя сервиса.)
    field_to_uniq  - Тип list. Определяет какие пары ключ:значение словаря kwargs записывать в ключ редиса.
                     Рекомендуется указывать поля которые меняют логику работы функции(например имя аккаунта).
    redis_settings - Тип dict. Настройки подлючения к редису. По умолчанию равен {'host': 's1.meta.vmc.loc', 'port': 6379, 'db': 0}
    """

    def __init__(self, timeout_in_sec, ttl_in_sec=600, string_to_uniq='', field_to_uniq=None, redis_settings:dict=None):
        if not redis_settings:
            redis_settings = {'host': 's1.meta.vmc.loc', 'port': 6379, 'db': 0}

        self.ttl_in_sec     = ttl_in_sec
        self.timeout_in_sec = timeout_in_sec
        self.string_to_uniq = string_to_uniq
        self.field_to_uniq  = field_to_uniq
        self.redis_storage  = redis.StrictRedis(**redis_settings)

    def __call__(self, func):
        w_self = self

        def wrapper(*args, **kwargs):
            waiting_time = random.randrange(1, 3)
            redis_key = 'LOCK_' + func.__qualname__ + w_self.string_to_uniq

            if w_self.field_to_uniq and kwargs:
                for key, value in kwargs.items():
                    if key in w_self.field_to_uniq:
                        redis_key += '_{0}={1}'.format(key, value)

            while (w_self.timeout_in_sec - waiting_time) > 0:
                if w_self.redis_storage.get(redis_key):
                    sleep(waiting_time)
                else:
                    try:
                        is_set = self.redis_storage.set(name=redis_key, value=True, ex=w_self.ttl_in_sec, nx=True)
                        if not is_set:
                            continue
                        result = func(*args, **kwargs)
                    finally:
                        w_self.redis_storage.delete(redis_key)
                    return result
            else:
                raise Exception
        return wrapper




