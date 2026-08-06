"""商品接口对象"""
from common.http_client import HttpClient


class ProductApi:
    def __init__(self, client=None):
        self.client = client or HttpClient()

    def get_product(self, product_id):
        """查询单个商品"""
        return self.client.get(f"/products/{product_id}")

    def list_products(self, limit=10):
        """查询商品列表"""
        return self.client.get("/products", params={"limit": limit})

    def search(self, keyword):
        """搜索商品"""
        return self.client.get("/products/search", params={"q": keyword})