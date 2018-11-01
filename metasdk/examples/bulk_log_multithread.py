import time
from functools import partial
from multiprocessing.pool import ThreadPool

from metasdk import MetaApp

META = MetaApp()


def my_thread_fn(bulk_log, job_item):
    bulk_log.try_log_part()
    # Бизнес логика
    # работа с job_item
    time.sleep(1)


def my_main_fn():
    total = 125 * 2
    thread_cnt = 2

    bulk_log = META.bulk_log(u'Моя пачка', total, 1)
    bulk_log.try_log_part()

    all_data = range(1, total)
    pool = ThreadPool(thread_cnt)

    # Чтобы работать в многопоточном режиме с bulk_log вы
    # должны передать его как аргумент вызываемой функции таким образом
    func = partial(my_thread_fn, bulk_log)
    results = pool.map(func, all_data)

    bulk_log.finish()
    pool.close()
    pool.join()
    # print(results)


my_main_fn()
