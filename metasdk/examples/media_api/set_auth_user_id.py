import base64

from metasdk import MetaApp
from metasdk.utils import pretty_json

META = MetaApp(meta_url="http://localhost:8080")
log = META.log

#
# Вы можете установить ID пользователя, от лица которого будут работать запросы
# Это полезно, когда вам надо сгенерировать приватный файл в фоновом режиме.
# Это user_id вы можете передать и прочитать из поля data в task
#
META.auth_user_id = 3503

YOUR_FILE_CONTENT_BASE64 = base64.b64encode(b'Custom user file').decode("utf-8")
# Получаете инстанс сервиса и делаете запрос к нему
result = META.MediaService.persist_one(
    file_base64_content=YOUR_FILE_CONTENT_BASE64,
    filename="req.txt",
    extension="txt",
    mime="plain/text"
)
print(u"result = %s" % result)
# Формат ответа стандартный для меты
first = result['rows'][0]
print(u"result['rows'][0]['url'] = %s" % first['url'])
print(u"first = %s" % first)
print(u"result = %s" % pretty_json(result))
