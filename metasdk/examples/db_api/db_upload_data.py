import os
from metasdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(os.path.abspath(__file__)))
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
result = db.upload_data(upload_file, configuration)
print(u"result = %s" % str(result))
