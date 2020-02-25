from metasdk import MetaApp

META = MetaApp()

q = META.MessageQueueService

incr = 0
for m in q.receive_messages("foo5", None):
    incr += 1
    print(u"22222 m = %s" % str(m))
print(u"22222  = %s" % str(incr))