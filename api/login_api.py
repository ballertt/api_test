"""登录接口对象"""
from common.http_client import HttpClient


class LoginApi:
    def __init__(self, client=None):
        # 复用传入的客户端，或新建一个
        self.client = client or HttpClient()

    def login(self, username, password):
        """POST /auth/login 登录，返回响应对象"""
        payload = {"username": username, "password": password}
        resp = self.client.post("/auth/login", json=payload)
        return resp

    def login_and_save_token(self, username="emilys",
                             password="emilyspass"):
        """登录成功并把 token 注入客户端，方便后续接口直接用"""
        resp = self.login(username, password)
        if resp.status_code == 200:
            # DummyJSON 返回 accessToken（也可能叫 token），取其中一个
            token = resp.json().get("accessToken") or resp.json().get("token")
            self.client.set_token(token)
            return token
        return None