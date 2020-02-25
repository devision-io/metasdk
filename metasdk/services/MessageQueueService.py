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
        self.__value_serializer = {
            "json": lambda m: json.dumps(m).encode('ascii'),
            "bytes": None
        }
        self.__value_deserializer = {
            "json": lambda m: json.loads(m.decode('ascii')),
            "bytes": None
        }

    def send_message(self, topic: str, value: dict, serializer="json"):
        producer = self.__get_producer(serializer)
        producer.send(topic, value)
        self.__incr += 1

    def receive_messages(self, topics: str, group_id: str, consumer_timeout_ms: float = None, serializer="json"):
        if consumer_timeout_ms is None:
            consumer_timeout_ms = float('inf')
        consumer = self.__get_consumer(topics, group_id, consumer_timeout_ms, serializer)
        for msg in consumer:
            yield msg

    def __get_consumer(self, topics: str, group_id: str, consumer_timeout_ms: float, deserialize_type) -> KafkaConsumer:
        # TODO: enable_auto_commit
        return KafkaConsumer(topics,
                             group_id=group_id,
                             consumer_timeout_ms=consumer_timeout_ms,
                             value_deserializer=self.__value_deserializer[deserialize_type],
                             bootstrap_servers=self.__app.kafka_url)

    def __get_producer(self, serialize_type) -> KafkaProducer:
        if serialize_type not in self.__producers_by_serialize_type:
            p = KafkaProducer(bootstrap_servers=self.__app.kafka_url,
                              value_serializer=self.__value_serializer[serialize_type],
                              retries=5,
                              compression_type='gzip')

            def exit_handler():
                p.close(60)

            # Регистрировать надо именно после создания продьюсера, так как если делать ДО, то
            # внутренний кафковый exit_handler запускается с timeout=0 и ничего не отправляется
            atexit.register(exit_handler)

            self.__producers_by_serialize_type[serialize_type] = p

        return self.__producers_by_serialize_type[serialize_type]

    def flush_all(self):
        """
        Вызывает блокирующую отправку сообщений в брокер
        """
        if not self.__producers_by_serialize_type:
            return

        p: KafkaProducer
        for p in self.__producers_by_serialize_type.values():
            p.flush()

    def __send_scheduler(self):
        def send_timer():
            import time
            while True:
                try:
                    self.flush_all()
                except Exception as e:
                    self.__app.log.error("Unable to flush message queue", {"e": e})
                time.sleep(5)

        w = Thread(target=send_timer)
        w.setDaemon(True)
        w.start()
