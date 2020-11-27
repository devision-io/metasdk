# Логирование

Тут мы рассмотрим обычный логгер и Bulk-логгер, который нужен, чтобы не спамить большим кол-вом логов, при обработке больших массиов данных с неизвестным временем на обработку одного элемента

## Logger

```python
log = META.log

# Объявите глобальный контекст, чтобы не писать это каждый раз
log.set_entity('campaign_id', -1)
# По сути это просто хранилище глобавльных переменных контекста
log.set_entity('test', True)
log.warning('Do warning log', {"count": 1, "mycontextParam": [1, 3, 4]})
log.info('Info log')

logging.info('Default logging')

# удалите глобальный контекст, когда он вам больше не нужен
log.remove_entity('test')
log.info('Info log2')
```

Это выведет вам что-то вроде такого:

```python
#  00:03:11:WARNING: Do warning log {'count': 1, 'mycontextParam': [1, 3, 4], 'test': True, 'campaign_id': -1}
#  00:03:11:INFO: Info log {'test': True, 'campaign_id': -1}
#  00:03:11:INFO: Default logging {'test': True, 'campaign_id': -1}
#  00:03:11:INFO: Info log2 {'campaign_id': -1}
```


## Bulk Logger

Используется для логирования пачек из обрабатываемого списка.

Делает запись в лог только если прошло определенное кол-во времени

```python
total = 125
# Получаете инстанс bulk-логгера через объект приложения
# Список параметров вам подскажет IDE
bulk_log = META.bulk_log(u'Моя пачка', total, 1)

for idx in xrange(total):
    # Первый вызов всегда try_log_part, чтобы ознаменовать начало выполнения цикла
    bulk_log.try_log_part()

    # На ЧАСТЫХ, но возможно БЫСТРЫХ процессах можете использовать параметр with_start_message=False
    # Это исключит запись надписи о начале работы над пачкой и, если пачка сделается до
    # мин. время логирования, то записи не произойдет вообще
    # bulk_log.try_log_part(with_start_message=False)

    # далее ваша бизнес-логика
    time.sleep(1)

# finish вызывать необязательно, но часто нужно,
# чтобы точно сказать, что обработка выполнена
bulk_log.finish()
```

Это выведет вам что-то вроде такого:

```python
# 23:55:31:INFO: Начали цикл: Моя пачка {}
# 23:56:31:INFO: Моя пачка {'counter': 61, 'percentDone': 48, 'maxCount': 125}
# 23:57:31:INFO: Моя пачка {'counter': 121, 'percentDone': 96, 'maxCount': 125}
# 23:57:36:INFO: Закончили цикл: Моя пачка {}
```


## Bulk Logger Thread Pool

Используется для логирования пачек из обрабатываемого списка.
Делает запись в лог только если прошло определенное кол-во времени

```python
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
    #print(results)

my_main_fn()
```


Это выведет вам что-то вроде такого:

```python
# 16:25:08:INFO: Начали цикл: Моя пачка {}
# 16:26:08:INFO: Моя пачка {'counter': 122, 'percentDone': 48, 'maxCount': 250}
# 16:27:09:INFO: Моя пачка {'counter': 242, 'percentDone': 96, 'maxCount': 250}
# 16:27:17:INFO: Закончили цикл: Моя пачка {}
```


