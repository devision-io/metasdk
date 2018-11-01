import time

from metasdk import MetaApp

META = MetaApp()

# Самый простой вариант без знания об общем количестве элементов
bulk_log = META.bulk_log(u'Моя пачка')
for idx in range(100):
    if bulk_log.try_log_part():
        print(u"bulk_log.get_percent_done() = %s" % str(bulk_log.get_percent_done()))
    time.sleep(1)
bulk_log.finish()


# Стандартный вариант
total = 125
bulk_log = META.bulk_log(u'Моя пачка', total, 1)

for idx in range(total):
    if bulk_log.try_log_part():
        print(u"bulk_log.get_percent_done() = %s" % str(bulk_log.get_percent_done()))
    time.sleep(1)

bulk_log.finish()

# На частых но возможно долгих процессах
bulk_log = META.bulk_log(u'Моя пачка', total, 1)

for idx in range(total):
    bulk_log.try_log_part(with_start_message=False)
