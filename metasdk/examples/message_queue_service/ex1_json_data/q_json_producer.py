import time
from metasdk import MetaApp

META = MetaApp()
producer = META.MessageQueueService.get_producer()
producer.send()

for i in range(10000):
    q.send_message("foo8", {"a": i})
    # q.flush_all()
    # time.sleep(0.5)

print("end")
