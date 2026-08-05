from common.http_client import HttpClient

client = HttpClient()
resp = client.get("/users/1")
print("状态码:", resp.status_code)
print("返回:", resp.json())