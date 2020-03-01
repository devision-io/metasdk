import time
from metasdk import MetaApp

META = MetaApp()
producer = META.MessageQueueService.get_producer()

for i in range(10000):
    producer.send("foo8", {"a": i})
    # q.flush_all()
    # time.sleep(0.5)

print("end")
