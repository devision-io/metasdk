from metasdk import MetaApp

META = MetaApp()
q = META.MessageQueueService

q.send_message("imgs", b'123', serializer="bytes")
