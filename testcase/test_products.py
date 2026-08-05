"""商品接口数据驱动测试用例"""
import pytest
import allure
from common.data_loader import load_json
from api.product_api import ProductApi
from jsonschema import validate

# 模块加载时读取一次数据文件
PRODUCTS_DATA = load_json("products_data.json")


@pytest.mark.parametrize("case", PRODUCTS_DATA,
                         ids=lambda c: f"product-{c['product_id']}")
def test_product_detail(case):
    """数据驱动：一条脚本跑多组商品数据"""
    with allure.step("发起商品查询请求"):
        resp = ProductApi().get_product(case["product_id"])

    # 根据数据里的期望状态码分支断言
    if case["expected_status"] == 404:
        with allure.step("断言响应"):
            assert resp.status_code == case["expected_status"]
    else:
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == case["product_id"]
        assert data["title"] == case["expected_title"]
        assert data["price"] == case["expected_price"]

# 商品详情的响应结构蓝图
PRODUCT_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "price", "description", "category"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "description": {"type": "string"},
        "category": {"type": "string"},
    },
}


def test_product_response_schema():
    """校验商品响应结构：必需字段和类型都符合蓝图"""
    resp = ProductApi().get_product(1)
    assert resp.status_code == 200
    validate(instance=resp.json(), schema=PRODUCT_SCHEMA)