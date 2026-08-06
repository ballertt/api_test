"""购物车接口数据驱动测试"""
import pytest
from common.data_loader import load_json
from api.cart_api import CartApi

CART_DATA = load_json("cart_data.json")


@pytest.mark.parametrize("case", CART_DATA,
                         ids=lambda c: f"cart-p{c['product_id']}")
def test_add_to_cart(case):
    """数据驱动：加购物车"""
    api = CartApi()
    resp = api.add_to_cart(case["user_id"], case["product_id"], case["quantity"])
    assert resp.status_code == case["expected_status"]
    if resp.status_code == 201:
        data = resp.json()
        assert data["totalProducts"] == 1
        assert data["totalQuantity"] == case["quantity"]


def test_get_user_carts():
    """正向：查询用户的购物车"""
    api = CartApi()
    resp = api.get_user_carts(1)
    assert resp.status_code == 200
    data = resp.json()
    assert "carts" in data
    assert isinstance(data["carts"], list)


def test_get_user_carts_not_found():
    """边界：查询不存在的用户购物车（返回需实测）"""
    api = CartApi()
    resp = api.get_user_carts(999999)
    assert resp.status_code in (200, 404)