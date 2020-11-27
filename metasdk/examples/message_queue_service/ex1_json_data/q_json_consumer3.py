from metasdk import MetaApp
from metasdk.examples.message_queue_service.ex1_json_data import topic

META = MetaApp()

mqs = META.MessageQueueService

META.log.info("start")
incr = 0
consumer = mqs.get_frame_commit_consumer(topic, "g1")
for f in consumer.get_frames_stream():
    for m in f.get_messages_stream():
        incr += 1
    print(u"1111  = %s" % str(incr))

META.log.info("stop")

print(u"22222  = %s" % str(incr))
