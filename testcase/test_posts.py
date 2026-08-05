"""JSONPlaceholder 帖子接口自动化测试用例"""
import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


# ============ 1. 正向用例 ============

def test_get_posts_list():
    """查询帖子列表，应返回 200 和数组"""
    resp = requests.get(f"{BASE_URL}/posts")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) > 0


def test_get_post_by_id():
    """查询单篇帖子，应返回对应 id"""
    resp = requests.get(f"{BASE_URL}/posts/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert "title" in data
    assert "body" in data


def test_create_post():
    """新增帖子，应返回 201 和带新 id 的对象"""
    payload = {"title": "foo", "body": "bar", "userId": 1}
    resp = requests.post(f"{BASE_URL}/posts", json=payload)
    assert resp.status_code == 201
    assert resp.json()["title"] == "foo"


def test_update_post():
    """整体更新帖子，title 应被修改"""
    payload = {"id": 1, "title": "updated", "body": "updated body", "userId": 1}
    resp = requests.put(f"{BASE_URL}/posts/1", json=payload)
    assert resp.status_code == 200
    assert resp.json()["title"] == "updated"


def test_patch_post():
    """部分更新帖子，只改 title"""
    resp = requests.patch(f"{BASE_URL}/posts/1", json={"title": "patched"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "patched"


def test_delete_post():
    """删除帖子，应返回 200 或 204"""
    resp = requests.delete(f"{BASE_URL}/posts/1")
    assert resp.status_code in (200, 204)


# ============ 2. 逆向 / 异常用例 ============

def test_get_post_not_found():
    """查询不存在的帖子，应返回 404"""
    resp = requests.get(f"{BASE_URL}/posts/999999")
    assert resp.status_code == 404


def test_get_user_not_found():
    """查询不存在的用户，应返回 404"""
    resp = requests.get(f"{BASE_URL}/users/999999")
    assert resp.status_code == 404


# ============ 3. 参数化（数据驱动） ============

@pytest.mark.parametrize("post_id, expected_status", [
    (1, 200),
    (100, 200),
    (999999, 404),
])
def test_get_post_status_codes(post_id, expected_status):
    """参数化：不同 id 返回不同状态码"""
    resp = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert resp.status_code == expected_status


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_posts_exist(post_id):
    """参数化：多个 id 都应存在"""
    resp = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == post_id


# ============ 4. 边界用例 ============

def test_pagination_limit():
    """分页边界：_limit=1 只应返回 1 条"""
    resp = requests.get(f"{BASE_URL}/posts", params={"_page": 1, "_limit": 1})
    assert resp.status_code == 200
    assert len(resp.json()) == 1


# ============ 5. 使用 fixture（共享 Session） ============

def test_get_post_with_session(api_session):
    """使用共享 Session 发送请求"""
    resp = api_session.get(f"{BASE_URL}/posts/1")
    assert resp.status_code == 200