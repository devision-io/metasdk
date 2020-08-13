import logging
from typing import TypeVar

from metasdk.logger import LOGGER_ENTITY, REQUEST_LOG


def preprocessing(func):
    def wrapper(self, msg, context=None):
        """ Этот декоратор занимается предобработкой входных параметров:
            1. Проверяет context на None.
            2. Добавляет к msg имя класса объекта ошибки. Например: msg + ModuleNotFoundError
         """
        if context is None:
            context = {}

        error_obj = context.get('e')
        if isinstance(error_obj, Exception):
            try:
                msg = msg + ' ' + str(error_obj.__class__.__name__)
            except Exception:
                pass

        return func(self, msg, context)
    return wrapper


async def error_log_middleware(request, handler):
    Logger.log_request(**{"method": request.method,
                          "url": str(request.url),
                          "uesrAgent": request.headers["User-Agent"],
                          "referrer": request.headers["Referrer"], #TODO check how it work
                          "responseStatusCode": 0,
                          "remoteIp": request.remote})
    response = await handler(request)
    Logger.set_log_request_response_status_code(response.status)
    return response

# Нужно для работы в aiohttp (см. реализацию декоратор middleware в aiohttp)
error_log_middleware.__middleware_version__ = 1


class Logger:
    """
    Прослойка для упрощения апи логгера
    """

    def set_entity(self, key, value):
        if value is None:
            self.remove_entity(key)
        else:
            LOGGER_ENTITY[key] = value


    @staticmethod
    def log_request(method: str, url: str, user_agent: str,
                    referrer: str="-", remote_ip:str="-"):
        REQUEST_LOG.update({"method": method,
                            "url": url,
                            "userAgent": user_agent,
                            "referrer": referrer,
                            "remoteIp": remote_ip})


    @staticmethod
    def set_log_request_response_status_code(response_status_code: int):
        REQUEST_LOG["responseStatusCode"] = response_status_code


    def remove_entity(self, key):
        LOGGER_ENTITY.pop(key, None)

    def info(self, msg, context=None):
        if context is None:
            context = {}
        logging.info(msg, extra={'context': context})

    @preprocessing
    def warning(self, msg, context):
        logging.warning(msg, extra={'context': context})

    @preprocessing
    def error(self, msg, context):
        logging.error(msg, extra={'context': context})

    @preprocessing
    def critical(self, msg, context):
        logging.critical(msg, extra={'context': context})

    @preprocessing
    def exception(self, msg, context):
        logging.exception(msg, extra={'context': context})
