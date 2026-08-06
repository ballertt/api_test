"""使用 Mock 技术模拟接口返回"""
import responses
from api.product_api import ProductApi
from api.login_api import LoginApi
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
def test_mock_login_api():
    """Mock：模拟第三方认证服务 503 不可用"""
    responses.add(
        responses.POST,
        "https://auth.example.com/login",
        json={"error": "Service Unavailable", "message": "Authentication service is temporarily unavailable"},
        status=503,
    )

    # 业务代码调用登录接口（实际会被 responses 拦截）
    login_data={"username": "testuser", "password": "testpass123"}
    resp = LoginApi().client.post("https://auth.example.com/login", json=login_data)

    # 断言业务代码能正确处理503错误
    assert resp.status_code == 503
    assert resp.json()["error"] == "Service Unavailable"
    assert "temporarily unavailable" in resp.json()["message"]
