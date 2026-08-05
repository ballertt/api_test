import pytest
import requests


@pytest.fixture(scope="session")
def api_session():
    """整个测试会话共用一个 Session，自动带 Accept 请求头"""
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()