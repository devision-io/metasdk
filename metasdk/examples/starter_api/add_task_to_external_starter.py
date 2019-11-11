from metasdk import MetaApp, StarterService

META = MetaApp()

starter = StarterService(META, META.db("garpun_main"), "http://code.harpoon.lan:28341")
res = starter.submit("Notice.DeactivateOldNotices", {
    "foo": "bar"
})
print(u"res = %s" % str(res))