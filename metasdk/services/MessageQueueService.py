import json
from threading import Thread
import atexit
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor

"""
Классы MQS* для инкапсулирования реализации.
Библиотек для работы с кафкой много (META-2323) и
хочется иметь пространство для манева на всякий случай
"""


class MQSProducer:
    def __init__(self, producer: KafkaProducer) -> None:
        self.__producer = producer

    def send(self, topic, value, key=None):
        self.__producer.send(topic, value, key=key)


class MQSConsumer:
    def __init__(self, consumer: KafkaConsumer) -> None:
        self._consumer = consumer


class MQSAutoCommitConsumer(MQSConsumer):
    def get_messages_stream(self):
        for msg in self._consumer:
            yield MQSMessage(msg)


class MQSFrameCommitConsumer(MQSConsumer):

    def get_frames_stream(self, max_frames: int = 100000, max_messages_in_frame: int = 10000):
        for frm_idx in range(max_frames):
            frame = MQSConsumerFrame(self._consumer, max_messages_in_frame)
            yield frame
            if not frame.get_msg_processed():
                break


class MQSConsumerFrame:
    def __init__(self, consumer: KafkaConsumer, max_messages_in_frame: int) -> None:
        self.__consumer = consumer
        self.__max_messages_in_frame = max_messages_in_frame
        self.__msg_processed = 0

    def get_messages_stream(self):
        for msg in self.__consumer:
            yield MQSMessage(msg)
            self.__msg_processed += 1
            if self.__msg_processed >= self.__max_messages_in_frame:
                break
        self.__consumer.commit()

    def get_msg_processed(self):
        return self.__msg_processed


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

    def get_autocommit_consumer(self, topics: str, group_id: str, consumer_timeout_ms: float = None,
                                serializer="json") -> MQSAutoCommitConsumer:
        """
        Используется когда вам надо обрабатывать каждое собщение отдельно и фиксировать его обработку
        в фоне автоматически
        """
        consumer = self.__get_consumer(topics, group_id, consumer_timeout_ms, True, serializer)
        return MQSAutoCommitConsumer(consumer)

    def get_frame_commit_consumer(self, topics: str, group_id: str, consumer_timeout_ms: float = None,
                                  serializer="json") -> MQSFrameCommitConsumer:
        """
        Используется для групповой обработки и фиксации сообщений
        например вам надо считать 10к записей пикселя,
        отправить в ClickHouse и только после успеха зафиксировать обработку сообщений
        """
        if consumer_timeout_ms is None:
            consumer_timeout_ms = 10000
        consumer = self.__get_consumer(topics, group_id, consumer_timeout_ms, False, serializer)
        p = consumer.partitions_for_topic(topics)
        print(u"p = %s" % str(p))
        return MQSFrameCommitConsumer(consumer)

    def __get_consumer(self, topics: str, group_id: str, consumer_timeout_ms: float,
                       enable_auto_commit: bool, deserialize_type) -> KafkaConsumer:
        """
        https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
        """
        if consumer_timeout_ms is None:
            consumer_timeout_ms = float('inf')
        return KafkaConsumer(topics,
                             group_id=group_id,
                             auto_offset_reset="earliest",
                             fetch_max_wait_ms=5000,
                             partition_assignment_strategy=[RoundRobinPartitionAssignor],
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
        Вызывает блокирующую отправку сообщений в брокер.
        Будет вызвано внутренним планировщиков в отдельном потоке

        Не этот метод, но будет автоматически вызван при завершении работы скрипта
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
