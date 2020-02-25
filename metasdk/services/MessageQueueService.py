import json
from threading import Thread
import atexit
from kafka import KafkaProducer, KafkaConsumer


class MessageQueueService:

    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
        self.__producers_by_serialize_type = {}
        self.__send_scheduler()
        self.__incr = 0

    def send_message(self, topic: str, value: dict):
        producer = self.__get_producer('json')
        producer.send(topic, value)
        self.__incr += 1

    def receive_messages(self, topics: str, group_id: str, consumer_timeout_ms=None):
        if consumer_timeout_ms is None:
            consumer_timeout_ms = float('inf')
        return self.__get_consumer(topics, group_id, consumer_timeout_ms, "json")

    def __get_consumer(self, topics: str, group_id: str, consumer_timeout_ms: float, deserialize_type) -> KafkaConsumer:
        return KafkaConsumer(topics,
                             group_id=group_id,
                             consumer_timeout_ms=consumer_timeout_ms,
                             value_deserializer=self.__get_value_deserializer(deserialize_type),
                             bootstrap_servers=self.__app.kafka_url)

    def __get_producer(self, serialize_type) -> KafkaProducer:
        if serialize_type not in self.__producers_by_serialize_type:
            p = KafkaProducer(bootstrap_servers=self.__app.kafka_url,
                              value_serializer=self.__get_value_serializer(serialize_type),
                              retries=5,
                              compression_type='gzip')

            def exit_handler():
                p.close(60)

            # Регистрировать надо именно после создания продьюсера, так как если делать ДО, то
            # внутренний кафковый exit_handler запускается с timeout=0 и ничего не отправляется
            atexit.register(exit_handler)

            self.__producers_by_serialize_type[serialize_type] = p

        return self.__producers_by_serialize_type[serialize_type]

    def __get_value_serializer(self, serialize_type):
        value_serializer = {
            "json": lambda m: json.dumps(m).encode('ascii')
        }[serialize_type]
        return value_serializer

    def __get_value_deserializer(self, serialize_type):
        value_serializer = {
            "json": lambda m: json.loads(m.decode('ascii'))
        }[serialize_type]
        return value_serializer

    def flush_all(self):
        if not self.__producers_by_serialize_type:
            return

        print(u"flush_all")
        print(u"self.__incr = %s" % str(self.__incr))
        print(u"self.__producers_by_serialize_type = %s" % str(self.__producers_by_serialize_type))

        p: KafkaProducer
        for p in self.__producers_by_serialize_type.values():
            p.flush()

    def __send_scheduler(self):
        def send_timer():
            import time
            while True:
                try:
                    self.flush_all()
                except:
                    # TODO:
                    self.__app.log.error("Unable to flush message queue")
                    pass
                time.sleep(5)

        w = Thread(target=send_timer)
        w.setDaemon(True)
        w.start()
