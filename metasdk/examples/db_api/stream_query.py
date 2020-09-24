from metasdk import MetaApp

META = MetaApp()

shard_key = "{GOOGLE_CLOUD_PROJECT_ID}#{EX_ACCESS_ID}"
QUERY = """
SELECT * FROM `{YOUR_TABLE}`
"""

configuration = {
    "database": {
        # укажите meta alias для БД
        "alias": "bigquery",

        # или укажите все подключение
        # в этом случае shard_key должен быть None
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
            "maxRows": 10_000_000,
            "command": QUERY,
            "shardKey": shard_key
        }
    },
    "timeZone": "UTC",
}
META.log.info("start")
result = META.DbService.stream_query(configuration)

columns = result.columns
print("columns = %s" % str(columns))

idx = 0
blog = META.bulk_log("rows", None, part_log_time_minutes=1)
for r in result:
    blog.try_log_part()
    idx += 1
    if idx % 5000 == 0:
        print("idx = %s" % str(idx))
print("idx = %s" % str(idx))
META.log.info("stop")
