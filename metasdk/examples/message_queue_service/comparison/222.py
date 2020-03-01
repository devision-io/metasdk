from kafka import KafkaAdminClient
from kafka.admin import NewPartitions

client = KafkaAdminClient(bootstrap_servers='s2.meta.vmc.loc:9094')

# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaAdminClient.html
client.create_partitions({
    "foo99": NewPartitions(6)
})


"""
единое место хранение всех раскатываемых репозиториев (api и workers)
автоподписка на хуки стеша на коммиты в репы
билд при коммите в любой зарегистрированный репозиторий
сборка через запускатор
парсинг xunit xml и сбор результатов тестов в cloud storage (отметка, что тестов нет, если их нет вообще)
? сбор метрик и отправка в кафу для логирования
отправка в докер регистри
сохранение метаданных билда, чтобы можно было откатить

? UI ко всему этому - возможно как раз локальная мета пойдет для отображения списков сервисов

Нужна кнопка "выкатить в окружение {XXX}" для немастер веток


"""