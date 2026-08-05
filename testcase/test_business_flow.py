"""业务流测试：登录 → 查商品 → 加购物车 → 验证购物车"""
from common.http_client import HttpClient
from api.login_api import LoginApi
from api.product_api import ProductApi
from api.cart_api import CartApi

USERNAME = "emilys"
PASSWORD = "emilyspass"


def test_business_flow_explicit():
    """显式版：手动登录、手动提取 id、手动传参（看懂每一步）"""
    # ===== 第 1 步：登录，拿到 token 和 userId =====
    login_api = LoginApi()
    login_resp = login_api.login(USERNAME, PASSWORD)
    assert login_resp.status_code == 200
    token = login_resp.json()["accessToken"]
    user_id = login_resp.json()["id"]          # ← 接口依赖①：userId 从登录响应提取
    assert user_id

    # ===== 第 2 步：把 token 注入客户端 =====
    client = HttpClient()
    client.set_token(token)                    # ← 之后所有请求自动带 Authorization

    # ===== 第 3 步：查商品，拿到 product_id =====
    product_api = ProductApi(client)
    product_resp = product_api.get_product(1)
    assert product_resp.status_code == 200
    product_id = product_resp.json()["id"]     # ← 接口依赖②：product_id 从商品响应提取
    assert product_id == 1

    # ===== 第 4 步：加购物车（userId 和 productId 都来自前面接口）=====
    cart_api = CartApi(client)
    add_resp = cart_api.add_to_cart(user_id, product_id)
    assert add_resp.status_code in (200, 201)
    assert add_resp.json()["totalProducts"] == 1

    # ===== 第 5 步：验证购物车里确实有商品 =====
    carts_resp = cart_api.get_user_carts(user_id)
    assert carts_resp.status_code == 200
    assert len(carts_resp.json()["carts"]) > 0

def test_business_flow_with_fixture(login_client):
    """fixture 版：login_client 自带 token，不用手动登录"""
    # 1. 从 /auth/me 拿 userId（带 token 访问认证接口）
    me = login_client.get("/auth/me")
    assert me.status_code == 200
    user_id = me.json()["id"]

    # 2. 查商品拿 productId
    product_api = ProductApi(login_client)
    product_id = product_api.get_product(2).json()["id"]

    # 3. 加购物车
    cart_api = CartApi(login_client)
    add_resp = cart_api.add_to_cart(user_id, product_id)
    assert add_resp.status_code in (200, 201)

    # 4. 验证
    carts = cart_api.get_user_carts(user_id)
    assert carts.status_code == 200
    assert len(carts.json()["carts"]) > 0

def test_me_without_token_unauthorized():
    """逆向：不带 token 访问 /auth/me 应返回 401"""
    client = HttpClient()               # 新建客户端，没有 set_token
    resp = client.get("/auth/me")
    assert resp.status_code == 401


def test_me_with_wrong_token_unauthorized():
    """逆向：token 错误也应返回 401"""
    client = HttpClient()
    client.set_token("this-is-a-fake-token")
    resp = client.get("/auth/me")
    assert resp.status_code == 401