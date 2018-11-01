from metasdk import MetaApp

META = MetaApp(meta_url="http://localhost:8080")

FeedSrv = META.FeedService
# deprecated
# data_result = FeedSrv.datasource_fetch("c99e4390-99fa-4bc5-b1d0-4d6fed06893d")

# for row in data_result['rows']:
#     print(u"name = %s" % str(row['name']))

# Result
# name = Юрий Гагарин
# name = Дмитрий Менделеев
# name = Дмитрий Медведев
# name = Владимир Путин

data_result = FeedSrv.datasource_process("c99e4390-99fa-4bc5-b1d0-4d6fed06893d")

print(u"data_result = %s" % str(data_result))