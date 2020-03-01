from metasdk import MetaApp

META = MetaApp()

q = META.MessageQueueService

incr = 0
consumer = q.get_autocommit_consumer("foo8", None)
for m in consumer.get_messages_stream():
    incr += 1
    print(u"22222 m = %s" % str(m))
print(u"22222  = %s" % str(incr))