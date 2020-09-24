import json
import orjson
from requests import Response


class DataResult:
    """
    Класс данных, полученных из Meta API
    Позволяет потоково получать данные по мере их поступления из api
    Служит для обработки больших массивов данных
    """

    def __init__(self, resp: Response):
        self.__resp = resp

        self.__rows_iter = self.__resp.iter_lines()
        self.columns = self.__line_unserialize(next(self.__rows_iter))

    def __iter__(self):
        for line in self.__rows_iter:
            yield self.__line_unserialize(line)
        self.__resp.close()

    def __line_unserialize(self, line_str):
        # стандартный json.loads даже близко не дает схожей производительности
        # orjson в несколько раз быстрее
        return orjson.loads(line_str.decode("utf-8"))


class DbService:
    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
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

    def stream_query(self, configuration):
        """
        Не сохраняет ничего и ни куда.
        Мета передает данные в output,
        а python client должен их быстро вычитывать и закрывать коннект.
        Также позволяет получать список колонок
        :param configuration: dict
        :return: DataResult
        """
        params = {}
        params.update(configuration)
        dr = self.__app.native_api_call('db', 'stream-query', params, self.__options, stream=True)
        return DataResult(dr)
