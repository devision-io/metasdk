import os

from metasdk import MetaApp

META = MetaApp()
q = META.MessageQueueService

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd()

consumer = q.get_consumer("imgs", "g1", serializer="bytes")
for m in consumer.get_messages_stream():
    print("m = %s" % str(m))
    print("m.value = %s" % str(m.value))
    print("m.value = %s" % str(type(m.value)))
    with open(__DIR__ + "/copy_metacrm_logo_" + str(m.timestamp) + ".jpg", 'wb') as f:
        f.write(m.value)
