from time import sleep

from metasdk.queue_locker import QueueLock


@QueueLock(timeout_in_sec=30, field_to_uniq=['x'])
def foo(func, *args, **kwargs):
    return func(*args, **kwargs)

def feo(y):
    print('start', y)
    sleep(7)
    print('end')
    return y

foo(feo,8)