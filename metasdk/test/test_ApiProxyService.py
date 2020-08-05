import unittest
from unittest.mock import patch

from metasdk import ApiProxyService, MetaApp
from metasdk.exceptions import ApiProxyError, ForbiddenError


def raise_ApiProxyError(*_, **__):
    raise ApiProxyError('azazaza ForbiddenError qwerty')


class TestApiProxyService(unittest.TestCase):
    @patch('requests.post', new=raise_ApiProxyError)
    def test_raise_business_api_proxy_business_errors_on_call_proxy(self):
        self.assertRaises(ForbiddenError,
                          ApiProxyService(MetaApp()).call_proxy,
                          "engine",
                          {},
                          "native_call",
                          True,
                          None,
                          False,
                          True)

    @patch('requests.post', new=raise_ApiProxyError)
    def test_raise_business_api_proxy_business_errors_on_call_proxy_with_paging(self):
        g = ApiProxyService(MetaApp()).call_proxy_with_paging("engine", {}, "native_call", True, None, 2, True)
        self.assertRaises(ForbiddenError, g.__next__,)


if __name__ == '__main__':
    unittest.main()
