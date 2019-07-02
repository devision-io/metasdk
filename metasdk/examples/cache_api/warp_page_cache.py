from metasdk import MetaApp
from datetime import datetime

t1 = datetime.now()

META = MetaApp()
log = META.log

META.auth_user_id = 11790
# Пример прогрева кеша
result = META.CacheService.warm_page_cache(
    '88',
    '4993',
    None,
    None,
    {
        "stateParams": {
            "firstLoading": True
        }
    }
)
print(u"export_res = %s" % str(result))
