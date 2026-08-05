"""购物车接口对象"""
from common.http_client import HttpClient


class CartApi:
    def __init__(self, client=None):
        self.client = client or HttpClient()

    def add_to_cart(self, user_id, product_id, quantity=1):
        """加购物车：把某个商品加入某个用户的购物车"""
        payload = {
            "userId": user_id,
            "products": [{"id": product_id, "quantity": quantity}],
        }
        return self.client.post("/carts/add", json=payload)

    def get_user_carts(self, user_id):
        """查询某用户的购物车"""
        return self.client.get(f"/carts/user/{user_id}")