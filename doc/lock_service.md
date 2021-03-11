# LockService

Используется для ограничения одновременно запущенных участков кода. 
Это бывает необходимо в ситуациях когда есть жесткие лимиты от внешнего апи на количество одновременных обращений,
или в ситуациях когда мы работаем с объектом для которого чувствительны одновременные изменения, например бюджет аккаунта.

## Описание параметров
key: Ключ, который определяет уникальность выполняемого участка кода.

ttl_in_sec: Сколько времени ключ будет жить в Redis'e. По истечении времени ключ удалится и начнется выполнение следующего участка кода. Необходимо указать время за которое участок кода должен успеть выполниться.

timeout_in_sec: Сколько времени функция lock будет пытаться поставить участок кода на выполнение. По истечении времени вызовется исключение. Слишком большое значение может привести к зависанию кода.

queue_width: Максимально возможное количество одновременно запущенных участков кода


```python
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

```

