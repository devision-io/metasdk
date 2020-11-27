from kafka import KafkaAdminClient
from kafka.admin import NewPartitions
from metasdk.examples.message_queue_service.ex1_json_data import topic

client = KafkaAdminClient(bootstrap_servers='s2.meta.vmc.loc:9094')


client.create_partitions({
    topic: NewPartitions(3)
})

