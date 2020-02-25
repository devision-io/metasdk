import time
from metasdk import MetaApp

META = MetaApp()
q = META.MessageQueueService

for i in range(10000):
    q.send_message("foo5", {"a": i})
    # q.flush_all()
    # time.sleep(0.5)

print("end")
