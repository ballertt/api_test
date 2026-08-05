import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# GET 查列表（带查询参数：第 1 页，每页 2 条）
resp = requests.get(f"{BASE_URL}/posts", params={"_page": 1, "_limit": 2})
print("GET 数量:", len(resp.json()))          # 应该输出 2

# POST 新增（用 json= 传请求体）
payload = {"title": "foo", "body": "bar", "userId": 1}
resp = requests.post(f"{BASE_URL}/posts", json=payload)
print("POST 状态码:", resp.status_code)        # 201
print("POST 返回的新对象:", resp.json())        # 带 id: 101

# PUT 整体更新
payload = {"id": 1, "title": "updated", "body": "updated body", "userId": 1}
resp = requests.put(f"{BASE_URL}/posts/1", json=payload)
print("PUT title:", resp.json()["title"])      # updated

# DELETE 删除
resp = requests.delete(f"{BASE_URL}/posts/1")
print("DELETE 状态码:", resp.status_code)      # 200