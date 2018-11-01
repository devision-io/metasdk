import json


class DbService:
    def __init__(self, app, default_headers):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
        self.__default_headers = default_headers
        self.__options = {}

    def upload(self, file_descriptor, settings):
        """
        Загружает файл в облако
        :param file_descriptor: открытый дескриптор
        :param settings: настройки загрузки
        :rtype: requests.Response
        """
        multipart_form_data = {
            'file': file_descriptor
        }
        params = {"settings": json.dumps(settings)}
        dr = self.__app.native_api_call('media', 'upload', params, self.__options, True, multipart_form_data, False, http_path="/api/meta/v1/", http_method='POST',
                                        connect_timeout_sec=60 * 10)
        return json.loads(dr.text)

    def persist_query(self, configuration):
        params = {}
        params.update(configuration)
        dr = self.__app.native_api_call('db', 'persist-query', params, self.__options)
        return json.loads(dr.text)
