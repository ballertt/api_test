"""登录接口数据驱动测试用例"""
import pytest
from common.data_loader import load_json
from api.login_api import LoginApi
from jsonschema import validate

LOGIN_DATA = load_json("login_data.json")


@pytest.mark.parametrize("case", LOGIN_DATA,
                         ids=lambda c: f"login-{c['username']}-{c['password'] or 'empty'}")
def test_login_cases(case):
    """数据驱动：多条登录场景共用一条脚本"""
    resp = LoginApi().login(case["username"], case["password"])
    assert resp.status_code == case["expected_status"]
    if resp.status_code == 200:
        assert resp.json().get("accessToken")

LOGIN_SCHEMA = {
    "type": "object",
    "required": ["id", "username", "accessToken", "refreshToken"],
    "properties": {
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "accessToken": {"type": "string"},
        "refreshToken": {"type": "string"},
    },
}


def test_login_response_schema():
    """校验登录响应结构"""
    resp = LoginApi().login("emilys", "emilyspass")
    assert resp.status_code == 200
    validate(instance=resp.json(), schema=LOGIN_SCHEMA)