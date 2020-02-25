from metasdk import MetaApp

META = MetaApp()

q = META.MessageQueueService

incr = 0
for m in q.receive_messages("foo5", "foo_group5", consumer_timeout_ms=5000):
    incr += 1
    # print(u"m = %s" % str(m))
print(u"incr = %s" % str(incr))