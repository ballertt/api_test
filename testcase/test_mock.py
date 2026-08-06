"""使用 Mock 技术模拟接口返回"""
import responses
from api.product_api import ProductApi
from api.login_api import LoginApi
from api.user_api import UserApi
@responses.activate
def test_mock_product_detail():
    """Mock：模拟一个还没开发好的商品接口"""
    # 预设：当收到 GET https://dummyjson.com/products/999 时，返回下面这段
    responses.add(
        responses.GET,
        "https://dummyjson.com/products/999",
        json={"id": 999, "title": "Mocked Product", "price": 99.99},
        status=200,
    )

    # 业务代码照常调用（实际不会发到网上，会被 responses 拦截）
    resp = ProductApi().get_product(999)

    assert resp.status_code == 200
    assert resp.json()["title"] == "Mocked Product"


@responses.activate
def test_mock_third_party_api():
    """Mock：模拟第三方支付回调接口"""
    responses.add(
        responses.GET,
        "https://api.payment.example.com/status/order123",
        json={"order_id": "order123", "status": "paid"},
        status=200,
    )

    # 假装业务代码调用了第三方接口
    resp = ProductApi().client.get("https://api.payment.example.com/status/order123")

    assert resp.status_code == 200
    assert resp.json()["status"] == "paid"

@responses.activate
def test_mock_login_service_down():
    """Mock：模拟登录服务不可用（503）"""
    responses.add(
        responses.POST,
        "https://dummyjson.com/auth/login",
        json={"message": "service down"},
        status=503,
    )
    resp = LoginApi().login("emilys", "emilyspass")
    assert resp.status_code == 503


@responses.activate
def test_mock_user_api_error():
    """Mock：模拟用户接口 500"""
    responses.add(
        responses.GET,
        "https://dummyjson.com/users/1",
        json={"message": "internal error"},
        status=500,
    )
    resp = UserApi().get_user(1)
    assert resp.status_code == 500
