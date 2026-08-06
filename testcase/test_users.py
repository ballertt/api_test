"""用户接口测试"""
import pytest
from api.user_api import UserApi


def test_get_user_success():
    """正向：查询用户"""
    resp = UserApi().get_user(1)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["firstName"]


def test_get_user_not_found():
    """逆向：用户不存在"""
    resp = UserApi().get_user(999999)
    assert resp.status_code == 404


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_users_exist(user_id):
    """参数化：多个用户都存在"""
    resp = UserApi().get_user(user_id)
    assert resp.status_code == 200
    assert resp.json()["id"] == user_id