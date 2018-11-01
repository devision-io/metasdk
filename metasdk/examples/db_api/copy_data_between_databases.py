import os
from metasdk import MetaApp
from datetime import datetime

from metasdk.utils import pretty_json

t1 = datetime.now()

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

source_db = META.db("adplatform")
destination_db = META.db("iata")

source_tbl_schema = "iata"
source_tbl_name = "prices"

destination_tbl_schema = "public"
destination_tbl_name = "prices_copy"

OUTFILE = __DIR__ + 'assets/out_' + source_tbl_name + '.tsv'


configuration = {
    "download": {
        "dbQuery": {
            "command": "SELECT * FROM " + source_tbl_schema + "." + source_tbl_name
        }
    }
}

schema_data = source_db.schema_data(configuration)
print(pretty_json(schema_data))
source_db.download_data(configuration, output_file=OUTFILE)

configuration = {
    "load": {
        "destinationTable": {
            "schema": destination_tbl_schema,
            "table": destination_tbl_name
        },
        "schema": schema_data['schema']
    }
}
upload_file = open(OUTFILE, 'rb')
destination_db.upload_data(upload_file, configuration)

t2 = datetime.now()
delta = t2 - t1
delta.total_seconds()
print("Time in sec: " + str(delta))
