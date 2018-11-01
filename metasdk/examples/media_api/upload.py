import os
from metasdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd() + "/"

upload_file = open(__DIR__ + '../assets/load_data_sample.tsv', 'rb')

MediaService = META.MediaService
result = MediaService.upload(upload_file, {
    "entityId": 2770,
    "objectId": "114aecf5-04f1-44fa-8ad1-842b7f31a2df",
    "info": {"test": True}
})
print(u"result = %s" % str(result))
# result = {'id': 'ae2ef57a-c948-4ba4-8b68-6598352a2eb8', 'name': 'load_data_sample.tsv', 'extension': 'tsv', 'mime': 'text', 'url': None, 'creationTime': '2017-11-08T16:57:46Z', 'userId': 4501, 'fileSize': 256, 'info': {'test': True}, 'private': True, 'downloadUrlPart': '/api/meta/v1/media/d/ae2ef57a-c948-4ba4-8b68-6598352a2eb8'}


