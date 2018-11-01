from metasdk import MetaApp

META = MetaApp(meta_url="http://localhost:8080")
log = META.log

export = META.ExportService
# res = export.export_page(58, 3203, ["res"], export_format="html")
# print(u"res = %s" % str(res))

res_ds = export.export_data_source('e4082545-7388-4e2c-893f-3c0124fc5d26')
print(u"res_ds = %s" % str(len(res_ds['rows'])))
