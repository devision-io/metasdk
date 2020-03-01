from confluent_kafka import Producer

from metasdk.examples.message_queue_service.comparison import MY_DATA, META

p = Producer({'bootstrap.servers': 's2.meta.vmc.loc:9094'})

some_data_source = [MY_DATA]

META.log.info("start")


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


for idx in range(1_000_000):
    data = MY_DATA
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    p.produce('mytopic', data)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
META.log.info("stop")