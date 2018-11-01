from metasdk import MetaApp

META = MetaApp(starter_api_url="http://s2.meta.vmc.loc:28341")

ret = META.StarterService.submit("adptools.clear_logs", {})
print(u"ret = %s" % str(ret))
