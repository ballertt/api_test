"""登录接口测试用例"""
from api.login_api import LoginApi

# 主测试账号（DummyJSON 官方文档账号，你已用 Postman 验证可登录）
USERNAME = "emilys"
PASSWORD = "emilyspass"


def test_login_success():
    """正向：正确账号密码登录，返回 200 和 token"""
    login_api = LoginApi()
    resp = login_api.login(USERNAME, PASSWORD)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("accessToken") or data.get("token")


def test_login_missing_password():
    """逆向：缺少密码应返回 400"""
    login_api = LoginApi()
    resp = login_api.login(USERNAME, "")
    assert resp.status_code == 400


def test_login_wrong_password():
    """逆向：密码错误应返回 400"""
    login_api = LoginApi()
    resp = login_api.login(USERNAME, "wrong-password")
    assert resp.status_code == 400


def test_get_me_after_login(login_client):
    """使用带 token 的客户端请求认证接口 /auth/me"""
    resp = login_client.get("/auth/me")
    assert resp.status_code == 200
    assert resp.json()["username"] == USERNAME