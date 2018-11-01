from metasdk import MetaApp

META = MetaApp()
log = META.log

configuration = {
    "database": {
        # укажите meta alias для БД
        "alias": "adplatform",

        # или укажите все подключение
        # "name": "XXXXXXXX",
        # "host": "XXXXXXXX",
        # "port": 777,
        # "username": "XXXXXXXX",
        # "password": "XXXXXXXX",
        # "type": "MySQL"
    },
    "download": {
        "sourceFormat": "JSON_NEWLINE",
        "dbQuery": {
            "command": """ SELECT * FROM users LIMIT 10 """
        }
    }
}

DbService = META.DbService
result = DbService.persist_query(configuration)
print(u"result = %s" % str(result))
print(u"result['downloadUrlPart'] = %s" % str(result['downloadUrlPart']))