from metasdk import MetaApp

META = MetaApp()

q = META.MessageQueueService

incr = 0
for m in q.receive_messages("foo8", "foo_group8", consumer_timeout_ms=10000):
    incr += 1
    print("m = %s" % str(m))
    print("m.value = %s" % str(m.value))
    print("m.value = %s" % str(type(m.value)))
print(u"incr = %s" % str(incr))