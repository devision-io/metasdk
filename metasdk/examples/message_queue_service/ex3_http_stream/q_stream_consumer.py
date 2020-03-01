import os

from metasdk import MetaApp

META = MetaApp()
q = META.MessageQueueService

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd()

consumer = q.get_consumer("collect", "g1", consumer_timeout_ms=1000000,
                          serializer="bytes")

incr = 0
for m in consumer.get_messages_stream():
    print("m = %s" % str(m))
    # print("m.value = %s" % str(m.value))
    # print("m.value = %s" % str(type(m.value)))
    # incr += 1

# print("incr = %s" % str(incr))
