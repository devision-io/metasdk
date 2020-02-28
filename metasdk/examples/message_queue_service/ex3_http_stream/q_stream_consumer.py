import os

from metasdk import MetaApp

META = MetaApp()
q = META.MessageQueueService

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd()

messages = q.receive_messages("collect", "g1", serializer="bytes", consumer_timeout_ms=10000)

incr = 0
for m in messages:
    print("m = %s" % str(m))
    # print("m.value = %s" % str(m.value))
    # print("m.value = %s" % str(type(m.value)))
    incr += 1

print("incr = %s" % str(incr))
