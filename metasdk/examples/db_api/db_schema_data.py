import os
from metasdk import MetaApp

META = MetaApp(meta_url="http://localhost:8080")
log = META.log

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd() + "/"

configuration = {
    "download": {
        "dbQuery": {
            "command": "SELECT * FROM products WHERE productname ilike '%Gula%' LIMIT 1000"
        }
    }
}

db = META.db("nw")
schema_data = db.schema_data(configuration)
print(u"schema_data = %s" % str(schema_data))

