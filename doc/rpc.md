# RPC Meta Services

Это API внутренних функций Меты, все эти функции доступны вам через редактор в Web-интерфейсе

## Примеры

[Список примеров](https://github.com/devision-io/metasdk/tree/master/metasdk/examples/settings_api)


## CacheService

```python
from metasdk import MetaApp

META = MetaApp()
log = META.log

META.auth_user_id = 11790
# Пример прогрева кеша
result = META.CacheService.warm_page_cache(
    '88',
    '4993',
    None,
    None,
    {
        "stateParams": {
            "firstLoading": True
        }
    }
)
print(u"export_res = %s" % str(result))
```


## MediaService

```python
import os
from metasdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd() + "/"

upload_file = open(__DIR__ + '../assets/load_data_sample.tsv', 'rb')

MediaService = META.MediaService
result = MediaService.upload(upload_file, {
    "isPrivate": True, # Файл будет доступен только для пользователя, работающего с апи
    "ttlInSec": 9999, # Обязательно для временных файлов. Кол-во секунд через которые мета автоматически удалит файл
    "entityId": 2770,
    "objectId": "114aecf5-04f1-44fa-8ad1-842b7f31a2df",
    "info": {"test": True} # Метаданные файла
})
print(u"result = %s" % str(result))
# result = {'id': 'ae2ef57a-c948-4ba4-8b68-6598352a2eb8', 'name': 'load_data_sample.tsv', 'extension': 'tsv', 'mime': 'text', 'url': None, 'creationTime': '2017-11-08T16:57:46Z', 'userId': 4501, 'fileSize': 256, 'info': {'test': True}, 'private': True, 'downloadUrlPart': '/api/meta/v1/media/d/ae2ef57a-c948-4ba4-8b68-6598352a2eb8'}

# Скачать файл
result = MediaService.download('ae2ef57a-c948-4ba4-8b68-6598352a2eb8',as_stream=False)
print(u"result.content = %s" % str(result.content))

# Информация по файлу
resp = MediaService.info('5665d822-2edb-48b8-85a5-817043900a9a')
print(u"resp = %s" % str(resp))
# resp = {'id': '5665d822-2edb-48b8-85a5-817043900a9a', 'name': 'load_data_sample.tsv', 'extension': 'tsv', 'mime': 'text', 'url': None, 'creationTime': '2017-11-08T16:45:00Z', 'userId': 4501, 'fileSize': 256, 'info': {'test': True}, 'private': True, 'downloadUrlPart': '/api/meta/v1/media/d/5665d822-2edb-48b8-85a5-817043900a9a'}
```


Это выведет вам что-то вроде такого:

```python
# 16:48:19:INFO: Читаем настройки разработчика из локального файла {'path': '/Users/arturgspb/.rwmeta/developer_settings.json'}
# 16:48:19:INFO: Инициализация службы {'debug': True}
# Empty stdin...
# result['rows'][0]['url'] = http://localhost:8080/media/d/c6509ac7-b410-4f77-8f0b-7c1dfd6a871b
# first = {u'url': u'http://localhost:8080/media/d/c6509ac7-b410-4f77-8f0b-7c1dfd6a871b', u'id': u'c6509ac7-b410-4f77-8f0b-7c1dfd6a871b', u'full_path': u'/mnt/static/public/74/reqtxt-2016-09-02_16-48-19-(4501).txt'}
# result = {
#     "boxed": false,
#     "columns": [
#         {
#             "displayName": "Id",
#             "fullDisplayName": "Id",
#             "isPrimary": true,
#             "isStyled": false,
#             "name": "id",
#             "role": "dimension",
#             "type": "TEXT"
#         },
#         {
#             "displayName": "url",
#             "fullDisplayName": "url",
#             "isStyled": true,
#             "name": "url",
#             "role": "dimension",
#             "type": "TEXT"
#         },
#         {
#             "displayName": "downloadUrlPart",
#             "fullDisplayName": "downloadUrlPart",
#             "isStyled": true,
#             "name": "downloadUrlPart",
#             "role": "dimension",
#             "type": "TEXT"
#         },
#         {
#             "displayName": "fullPath",
#             "fullDisplayName": "fullPath",
#             "isStyled": true,
#             "name": "fullPath",
#             "role": "dimension",
#             "type": "TEXT"
#         }
#     ],
#     "containsLego": false,
#     "empty": false,
#     "exportable": true,
#     "frame": false,
#     "hasTemplate": false,
#     "legoProperties": null,
#     "metaData": {
#         "filtersAvailable": true,
#         "orderByAvailable": false,
#         "pagerAvailable": false,
#         "searchTextAvailable": false
#     },
#     "name": "",
#     "pager": {
#         "limit": 20,
#         "maxPageLimit": 1000,
#         "offset": 0,
#         "total": null
#     },
#     "rows": [
#         {
#             "full_path": "/mnt/static/public/74/reqtxt-2016-09-02_16-48-19-(4501).txt",
#             "id": "c6509ac7-b410-4f77-8f0b-7c1dfd6a871b",
#             "url": "http://localhost:8080/media/d/c6509ac7-b410-4f77-8f0b-7c1dfd6a871b"
#         }
#     ],
#     "template": null
# }
```


## DbQueryService

Делайте запросы к БД к вашим подключениям

```python
# Важно значть, что эти методы:
# - НЕ парсят и НЕ меняют запросы к БД (кроме подстановки prepared statements)
# - НЕ являются каким-то отдельным обобщенным SQL-диалектом. Т.е. запросы в этом виже будут переданы напрямую в БД
# - Обовщяют получение данных и их типлв

db_adplatform = META.db("adplatform")

# Методы query, all, one ОБЯЗАТЕЛЬНО должны возвращать ResultSet (может быть и пустой)
# Т.е. нельзя делать UPDATE, INSET, DELETE, TRUNCATE, исключение - если в PostgreSQL вы делаете RETURNING

# Вернет стандартный метовский data_result, где есть rows, columns, meta_data и пр
data_result = db_adplatform.query("SELECT * FROM users LIMIT 10")

# Вернет rows из data result
users = db_adplatform.all("SELECT * FROM users LIMIT 10")

# Вернет первый элемент из rows или None, если нет первого элемента
users = db_adplatform.one("SELECT * FROM users WHERE id=4501 LIMIT 1")


# Метод update используется для запросов, которые НЕ ВОЗВРАЩАЮТ результат в виде ResultSet (в БД)
db_meta_samples = META.db("meta_samples")
dr = db_meta_samples.update("""
    UPDATE counters SET inc = inc + 1 WHERE name = :name
""", {"name": "md_source_update"})
print(u"dr = %s" % pretty_json(dr))

# Для случаев, когда вам надо сделать массовую вставку группы строк
# Эта запись НЕ вызывает цикл вставки по одной записи, это реально групповая удобная вставка
# Является хорошей альтернативой к генерации списка VALUES или INSERT FROM SELECT с размапливанием json в таблицу
dr = db_meta_samples.batch_update("""
    INSERT INTO test_batch_update VALUES (:id, :mytime::timestamp)
    ON CONFLICT(id) DO UPDATE SET mod_time=NOW()
""", [
    {"id": "py_1", "mytime": "2014-01-01"},
    {"id": "py_2", "mytime": "2014-01-01"},
])
print(u"dr = %s" % pretty_json(dr))
```


Отдельно стоит упомянуть про LoadData Api

Этот API позваоляет как в BigQuery создавать таблицу у казанной БД и потоково загружать в нее данные из файла формата TSV

Это позволяет ускорять вставку данных в таблицу от 2 до 4-5 раз.

ВАЖНО! Данные всегда добавляются в указанную таблицу и никакой очистки старых данных нет - вы должны почистить таблицу сами, если вам это нужно

```python
import os
from metasdk import MetaApp

META = MetaApp()

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

upload_file = open(__DIR__ + 'assets/load_data_sample.tsv', 'rb')


configuration = {
    "load": {
        "destinationTable": {
            "schema": "public",
            "table": "xxx_ya_stat"
        },
        "schema": {
            "fields": [
                {"name": "Date", "type": "DATE"},
                {"name": "Clicks", "type": "LONG"},
                {"name": "Cost", "type": "DECIMAL"},
                {"name": "AdNetworkType", "type": "TEXT"},
            ]
        }
    }
}

db = META.db("meta_samples")
db.upload_data(upload_file, configuration)
```


## SettingsService

Рассчитан на чтение параметров из мета конфигурации

Это удобно когда вы хотите хранить ссылки/токены для вшешних api, какие-то глобальные или частные настройки.

При этом вы хотите дать некоторым пользователям вохможность это редактировать через интерфейс

```python
settings = META.SettingsService

# Вернуть только данные
rwapp_conf = settings.data_get("rwapp")

# Полная информация о данных + данные
full_rwapp_conf = settings.data_get("rwapp", data_only=False)

onec_url = settings.config_param("rwapp", "app.onec.url")
```


## IssueService

Управляйте тикетами через стандартные методы

```python
from metasdk import MetaApp

META = MetaApp()

IssueService = META.IssueService

test_issue_id = 12067
IssueService.add_issue_msg(test_issue_id, "robo test")
IssueService.done_issue(test_issue_id)
```


## UserManagementService

Управляйте пользователями

```python
from metasdk import MetaApp

META = MetaApp()

UserManagementService = META.UserManagementService
resp = UserManagementService.send_recovery_notice("arturgspb", "meta")
print(u"resp = %s" % str(resp))
# resp = {'error': None, 'error_details': None, 'success_details': 'Вам отправлено уведомление о сбросе пароля на email art@realweb.ru. Следуйте инструкциям из письма.'}

resp = UserManagementService.send_recovery_notice("unknown_login_123123123", "meta")
print(u"resp = %s" % str(resp))
# resp = {'error': 'user_not_found', 'error_details': 'Пользователь с таким логином не найден', 'success_details': None}
```



## StarterService

Для работы с апи запускатора


## MailService

Для работы с почтовым клиентом

```python
from metasdk import MetaApp

META = MetaApp()

# Рекомендуется выдумывать unique_id для КАЖДОГО письма, чтобы избежать спама при ошибках или повторных запусках ваших скриптов
gen_id = "HJljkasdlkjasd"
META.MailService.submit_mail("meta@realweb.ru", "art@realweb.ru", "TTT", "ttt pong", unique_id="my_mail_category__" + gen_id)

# Без уникализации письма. Не рекомендуется, так как если ваш ког будет багать и бесконечно добавлять письма - то, вы можете заспамить адресатов
META.MailService.submit_mail("meta@realweb.ru", "art@realweb.ru", "TTT", "ttt pong")
```