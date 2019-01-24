import random
import time
import redis
from contextlib import contextmanager


class LockService:
    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
        parts = app.redis_url.split(':')
        self.redis = redis.Redis(host=parts[0], port=parts[1])

    @contextmanager
    def lock(self, key, ttl_in_sec, timeout_in_sec):
        is_set = False
        try:
            waiting_time = random.randrange(1, 3)
            remaining_waiting_time = timeout_in_sec

            while remaining_waiting_time > 0:
                is_set = self.redis.set(name=key, value=True, ex=ttl_in_sec, nx=True)
                if is_set:
                    yield is_set
                    break
                else:
                    print("sleep")
                    time.sleep(waiting_time)
                    remaining_waiting_time -= waiting_time
            else:
                raise Exception
        finally:
            if is_set:
                self.redis.delete(key)
