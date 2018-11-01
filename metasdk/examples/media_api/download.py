from metasdk import MetaApp

META = MetaApp()
log = META.log

META.auth_user_id = 10191
result = META.MediaService.download("93ed70c9-2aa9-4fc6-971e-b41619c46f30")
print(u"result.content = %s" % str(result.content))
