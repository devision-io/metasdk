import json
from threading import Thread
import atexit
from kafka import KafkaProducer, KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

"""
Классы MQS* для инкапсулирования реализации.
Библиотек для работы с кафкой много (META-2323) и
хочется иметь пространство для манева на всякий случай
"""


class MQSProducer:
    def __init__(self, producer: KafkaProducer) -> None:
        self.__producer = producer

    def send(self, topic, value):
        self.__producer.send(topic, value)


class MQSConsumer:
    def __init__(self, consumer: KafkaConsumer) -> None:
        self.__consumer = consumer

    def get_messages_stream(self):
        for msg in self.__consumer:
            yield MQSMessage(msg)


class MQSMessage:
    def __init__(self, record: ConsumerRecord) -> None:
        self.__record = record

    @property
    def topic(self):
        return self.__record.topic

    @property
    def partition(self):
        return self.__record.partition

    @property
    def key(self):
        return self.__record.key

    @property
    def value(self):
        return self.__record.value

    @property
    def timestamp(self):
        return self.__record.timestamp

    def __str__(self) -> str:
        return str(self.__dict__)


class MessageQueueService:

    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
        self.__producers_by_serialize_type = {}
        self.__scheduler_sec_timeout = 0.5
        self.__send_scheduler()

        # Important! msgpack не дает скорости по сравнению с json+gzip,
        # но зависимость при этом добавляет. Поэтому пока его не поддерживаем
        self.__value_serializer = {
            "json": lambda m: json.dumps(m).encode('ascii'),
            "bytes": None
        }
        self.__value_deserializer = {
            "json": lambda m: json.loads(m.decode('ascii')),
            "bytes": None
        }

    def scheduler_sec_timeout(self, sec: float):
        """Уже установлено по умолчанию"""
        self.__scheduler_sec_timeout = sec

    def get_producer(self, serializer="json") -> MQSProducer:
        producer = self.__get_producer(serializer)
        return MQSProducer(producer)

    def get_consumer(self, topics: str, group_id: str, consumer_timeout_ms: float = None,
                     enable_auto_commit: bool = True, serializer="json") -> MQSConsumer:
        if consumer_timeout_ms is None:
            consumer_timeout_ms = float('inf')
        consumer = self.__get_consumer(topics, group_id, consumer_timeout_ms, enable_auto_commit, serializer)
        return MQSConsumer(consumer)

    def __get_consumer(self, topics: str, group_id: str, consumer_timeout_ms: float,
                       enable_auto_commit: bool, deserialize_type) -> KafkaConsumer:
        return KafkaConsumer(topics,
                             group_id=group_id,
                             consumer_timeout_ms=consumer_timeout_ms,
                             enable_auto_commit=enable_auto_commit,
                             value_deserializer=self.__value_deserializer[deserialize_type],
                             bootstrap_servers=self.__app.kafka_url)

    def __get_producer(self, serialize_type) -> KafkaProducer:
        if serialize_type not in self.__producers_by_serialize_type:
            p = KafkaProducer(bootstrap_servers=self.__app.kafka_url,
                              value_serializer=self.__value_serializer[serialize_type],
                              retries=5,
                              compression_type='gzip')

            def exit_handler():
                # даем время на отправку всех неотправленных сообщений в брокер
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
        """
        Таймер для безусловной отправки сообщений раз в __scheduler_sec_timeout сек.
        """

        def send_timer():
            import time
            while True:
                try:
                    self.flush_all()
                except Exception as e:
                    self.__app.log.error("Unable to flush message queue", {"e": e})
                time.sleep(self.__scheduler_sec_timeout)

        w = Thread(target=send_timer)
        w.setDaemon(True)
        w.start()
