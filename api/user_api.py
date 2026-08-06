"""用户接口对象"""
from common.http_client import HttpClient


class UserApi:
    def __init__(self, client=None):
        self.client = client or HttpClient()

    def get_user(self, user_id):
        """查询用户"""
        return self.client.get(f"/users/{user_id}")