from metasdk import MetaApp

META = MetaApp()
q = META.MessageQueueService

messages = q.receive_messages("imgs", "g1", serializer="bytes")
for m in messages:
    print("m = %s" % str(m))
    print("m.value = %s" % str(m.value))
    print("m.value = %s" % str(type(m.value)))
