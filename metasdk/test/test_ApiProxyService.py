import unittest
from unittest.mock import patch

from metasdk import ApiProxyService, MetaApp
from metasdk.exceptions import ForbiddenError


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


forbidden_error_response = MockResponse({"error": {"type": "ForbiddenError", "text": "azaza"}}, 200)


def mock_post(*_, **__):
    return forbidden_error_response


class TestApiProxyService(unittest.TestCase):
    @patch("requests.post", new=mock_post)
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

    @patch("requests.post", new=mock_post)
    def test_raise_business_api_proxy_business_errors_on_call_proxy_with_paging(self):
        g = ApiProxyService(MetaApp()).call_proxy_with_paging("engine", {}, "native_call", True, None, 2, True)
        self.assertRaises(ForbiddenError, g.__next__)

    def test_raise_business_api_proxy_business_errors_on_check_err(self):
        self.assertRaises(ForbiddenError,
                          ApiProxyService(MetaApp()).check_err,
                          forbidden_error_response,
                          True,
                          None,
                          True)


if __name__ == "__main__":
    unittest.main()
