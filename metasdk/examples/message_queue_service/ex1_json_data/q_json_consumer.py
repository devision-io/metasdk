from metasdk import MetaApp

META = MetaApp()

q = META.MessageQueueService

incr = 0
consumer = q.get_consumer("foo8", "foo_group8", consumer_timeout_ms=10000)
for m in consumer.get_messages_stream():
    incr += 1
    print("m = %s" % str(m))
    print("m.value = %s" % str(m.value))
    print("m.value = %s" % str(type(m.value)))
print(u"incr = %s" % str(incr))