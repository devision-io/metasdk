from metasdk import MetaApp

META = MetaApp()

ret = META.DevService.fetch_db_credentials()
print(u"ret = %s" % str(ret))


ret = META.DevService.issue_access_token(6, ['meta.role.dev'])
print(u"ret = %s" % str(ret))

ret = META.DevService.clear_cache()
print(u"ret = %s" % str(ret))
