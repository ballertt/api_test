"""请求客户端封装：统一 headers、超时、日志、token 注入"""
import requests
from common.config import config
from common.logger import logger


class HttpClient:
    def __init__(self, base_url=None):
        # 不传就用全局配置的 base_url
        self.base_url = base_url or config.base_url
        self.session = requests.Session()
        # 统一请求头：改这里，所有接口都生效
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = 10

    def set_token(self, token):
        """登录成功后，把 token 注入后续所有请求"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, url, **kwargs):
        return self._request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self._request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request("DELETE", url, **kwargs)

    def _request(self, method, url, **kwargs):
        # 相对地址自动拼 base_url；绝对地址直接用
        if not url.startswith("http"):
            url = f"{self.base_url}{url}"
        kwargs.setdefault("timeout", self.timeout)

        # 日志：记录请求
        logger.info(f"[REQ] {method} {url} json={kwargs.get('json')}")

        # 发请求
        resp = self.session.request(method, url, **kwargs)

        # 日志：记录响应（限制长度，防止刷屏）
        logger.info(f"[RESP] status={resp.status_code} body={resp.text[:300]}")

        return resp
