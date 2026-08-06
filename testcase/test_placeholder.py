"""JSONPlaceholder 补充用例（用绝对地址）"""
from common.http_client import HttpClient

PLACEHOLDER = "https://jsonplaceholder.typicode.com"


def test_get_comments_by_post():
    """正向：查询某帖子的评论"""
    client = HttpClient()
    resp = client.get(f"{PLACEHOLDER}/comments", params={"postId": 1})
    assert resp.status_code == 200
    assert len(resp.json()) > 0


def test_get_todos_list():
    """正向：查询待办列表"""
    client = HttpClient()
    resp = client.get(f"{PLACEHOLDER}/todos")
    assert resp.status_code == 200
    assert len(resp.json()) > 0