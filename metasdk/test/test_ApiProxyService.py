import pytest

from metasdk import ApiProxyService, MetaApp
from metasdk.exceptions import ForbiddenError


api_proxy_service = ApiProxyService(MetaApp())


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


forbidden_error_response = MockResponse({"error": {"type": "ForbiddenError", "text": "azaza"}}, 200)


def mock_post(*_, **__):
    return forbidden_error_response


def test_raise_business_api_proxy_business_errors_on_call_proxy(mocker):
    mocker.patch('requests.post', new=mock_post)
    with pytest.raises(ForbiddenError):
        api_proxy_service.call_proxy("engine", {}, "native_call", True, None, False, True)


def test_raise_business_api_proxy_business_errors_on_call_proxy_with_paging(mocker):
    mocker.patch('requests.post', new=mock_post)
    with pytest.raises(ForbiddenError):
        api_proxy_service.call_proxy_with_paging("engine", {}, "native_call", True, None, 2, True).__next__()


def test_raise_business_api_proxy_business_errors_on_check_err():
    with pytest.raises(ForbiddenError):
        api_proxy_service.check_err(forbidden_error_response, True, None, True)
