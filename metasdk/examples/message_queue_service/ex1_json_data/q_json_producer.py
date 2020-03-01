import time
from metasdk import MetaApp
from metasdk.examples.message_queue_service.ex1_json_data import topic

META = MetaApp()
producer = META.MessageQueueService.get_producer()

stop = 1_000_000_000
stop = 1_000_000
for i in range(stop):
    producer.send(topic, {"a": i})
    # time.sleep(0.5)

print("end")
