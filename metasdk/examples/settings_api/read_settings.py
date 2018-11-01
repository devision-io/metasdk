import os
from metasdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

ss = META.SettingsService

# # Вернуть только данные
rwapp_conf = ss.data_get("rwapp")
print(u"rwapp_conf = %s" % str(rwapp_conf))

# Полная информация о данных + данные
full_rwapp_conf = ss.data_get("rwapp", data_only=False)
print(u"full_rwapp_conf = %s" % str(full_rwapp_conf))

# Сбросить локальный кеш
ss.clear_cache()

onec_url = ss.config_param("rwapp", "app.onec.url")
print(u"onec_url = %s" % str(onec_url))

### ОШИБКИ

# Пример 404 для конфига
try:
    unknown_data = ss.data_get("unknown_data")
except Exception as e:
    print("ОШИБКА!!!! = %s" % str(e))

try:
    unknown_param = ss.config_param("rwapp", "app.unknown_param")
except Exception as e:
    print("ОШИБКА!!!! = %s" % str(e))
