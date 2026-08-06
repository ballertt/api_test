"""商品搜索接口测试"""
import pytest
from api.product_api import ProductApi


@pytest.mark.parametrize("keyword", ["beauty", "mascara", "cream"])
def test_search_products(keyword):
    """搜索商品，返回列表"""
    resp = ProductApi().search(keyword)
    assert resp.status_code == 200
    data = resp.json()
    assert "products" in data
    assert isinstance(data["products"], list)