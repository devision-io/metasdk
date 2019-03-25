# Более подробное описание в документации по ошибкам что в каком случае использовать


class SDKError(Exception):
    """
    Корневая ошибка для SDK
    """
    pass


class BadRequestError(SDKError):
    """
    Запрос принципиально неправильный (неверная версия api, не передан обязательный параметр и пр.) (HTTP 400)
    """
    pass


class AuthError(SDKError):
    """
    Невозможно авторизоваться (HTTP 401)
    """
    pass


class ForbiddenError(SDKError):
    """
    Нет прав для соверщения операции (HTTP 403)
    """
    pass


class ServerError(SDKError):
    """
    Сервер ответил ошибкой (HTTP >500)
    """
    pass


class NoContentError(SDKError):
    """
    Нет содержимого (HTTP 204)
    """
    pass


class RequestError(SDKError):
    """
    Ошибка исполнения запроса(HTTP >400)
    """
    pass


class UnexpectedError(SDKError):
    """
    Непредвиденная ошибка (HTTP other)
    """
    pass


class DbQueryError(SDKError):
    """
    Ошибка работы с базой данных
    """
    pass


class RetryHttpRequestError(SDKError):
    """
    Невозможность повторного запроса (HTTP 502, 503, 504)
    """
    pass


class ApiProxyError(SDKError):
    """
    Ошибка работы с прокси
    """
    pass


class EndOfTriesError(SDKError):
    """
    Достигнут лимит количества повторов запроса
    """
    pass


class LockServiceError(SDKError):
    """
    Ошибка при работе с сервисом блокировки очереди (LockService)
    """
    pass


class BadParametersError(SDKError):
    """
    Ошибка неправильной настройки параметров для запроса апи или фидов
    """
    pass


class RateLimitError(SDKError):
    """
    Достигнут лимит обращений к сервису за секунду.
    Параметр waiting_time - обязательно передавать при вызове ошибки. Пример: raise RateLimitError(waiting_time=5)
    """

    def __init__(self, *args, waiting_time):
        self.waiting_time = waiting_time


class QuotaLimitError(SDKError):
    """
    Ошибка неправильной настройки параметров для запроса апи или фидов
    """
    pass
