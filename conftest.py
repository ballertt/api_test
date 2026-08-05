"""全局 fixture：公共的请求客户端"""
import pytest
from common.http_client import HttpClient
from api.login_api import LoginApi


@pytest.fixture(scope="session")
def api_client():
    """公共请求客户端（未登录）"""
    client = HttpClient()
    yield client
    client.session.close()


@pytest.fixture(scope="session")
def login_client():
    """已登录、带 token 的请求客户端"""
    client = HttpClient()
    login_api = LoginApi(client)
    login_api.login_and_save_token()
    yield client
    client.session.close()