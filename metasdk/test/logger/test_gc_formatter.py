import logging

from metasdk.logger.logger import Logger
from metasdk.logger import GCloudFormatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)
h = logging.NullHandler()
gc_formatter = GCloudFormatter()
h.setFormatter(gc_formatter)
logger.addHandler(h)

log = Logger()


def test_request_log_for_error_level_with_error_http_response_code(caplog):
    with caplog.at_level(logging.INFO):
        log.log_request("method", "url", "user_agent")
        log.error('info_message_0', {"info_context_key_1": "info_context_value_0"})
        formatted_log_message = gc_formatter.format(caplog.records[0])
        assert formatted_log_message["context"]["httpRequest"] == {'method': 'method',
                                                                   'url': 'url',
                                                                   'userAgent': 'user_agent',
                                                                   'referrer': '-',
                                                                   'responseStatusCode': 0,
                                                                   'remoteIp': '-'}


def test_request_log_for_info_level(caplog):
    with caplog.at_level(logging.INFO):
        log.log_request("method", "url", "user_agent")
        log.info('info_message_0', {"info_context_key_1": "info_context_value_0"})
        formatted_log_message = gc_formatter.format(caplog.records[0])
        assert formatted_log_message["context"].get("httpRequest") is None