import os

from metasdk import MetaApp

META = MetaApp()
q = META.MessageQueueService.get_producer(serializer="bytes")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd()

with open(__DIR__ + "/metacrm_logo.jpg", 'rb') as f:
    content = f.read()
    print("content = %s" % str(content))
    print("content = %s" % str(len(content)))
    print("content = %s" % str(type(content)))
    q.send("imgs", content)
