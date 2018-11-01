import os
from metasdk import MetaApp

META = MetaApp()
log = META.log

MediaService = META.MediaService

resp = MediaService.info('5665d822-2edb-48b8-85a5-817043900a9a')
print(u"resp = %s" % str(resp))
# resp = {'id': '5665d822-2edb-48b8-85a5-817043900a9a', 'name': 'load_data_sample.tsv', 'extension': 'tsv', 'mime': 'text', 'url': None, 'creationTime': '2017-11-08T16:45:00Z', 'userId': 4501, 'fileSize': 256, 'info': {'test': True}, 'private': True, 'downloadUrlPart': '/api/meta/v1/media/d/5665d822-2edb-48b8-85a5-817043900a9a'}
