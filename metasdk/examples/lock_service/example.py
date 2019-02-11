import time
import threading

from metasdk import MetaApp

Meta = MetaApp()
lock = Meta.LockService.lock

TIME_TO_SLEEP = 20
TIMEOUT = 50
TTL = 50
KEY = "gogo"
WIDTH = 2
FIELD_TO_UNIQUE_DECORATOR = ["x"]

def lock_via_with(name):
    with lock(timeout_in_sec=TIMEOUT, ttl_in_sec=TTL, key=KEY, queue_width=WIDTH):
        print("%s is running" % name)
        time.sleep(TIME_TO_SLEEP)
        print("%s is stop" % name)

@Meta.LockService.lock_decorator(timeout_in_sec=TIMEOUT, ttl_in_sec=TTL, key=KEY, queue_width=WIDTH, field_to_uniq=FIELD_TO_UNIQUE_DECORATOR)
def lock_via_decorator(name, x):
    print("%s is running" % name)
    time.sleep(TIME_TO_SLEEP)
    print("%s is stop" % name)


# Меняем target, если нужно
for i in range(1, 4):
    # t = threading.Thread(target=lock_via_with, kwargs={"name": "go" + str(i)})
    t = threading.Thread(target=lock_via_decorator, kwargs={"name": "go" + str(i), "x": 666})
    t.start()


