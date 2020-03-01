import os

from metasdk import MetaApp

META = MetaApp()
q = META.MessageQueueService

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd()

consumer = q.get_frame_commit_consumer("collect", "g1", consumer_timeout_ms=5000,
                                       serializer="bytes")

incr = 0
for frame in consumer.get_frames_stream(max_messages_in_frame=5000, max_frames=5):
    print(u"frame = %s" % str(frame))

    for m in frame.get_messages_stream():
        print(u"m = %s" % str(m))

    # print("m.value = %s" % str(m.value))
    # print("m.value = %s" % str(type(m.value)))
    # incr += 1

# print("incr = %s" % str(incr))
