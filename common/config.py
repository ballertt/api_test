"""配置管理：集中管理 base_url，支持多环境切换"""
import os

# 不同环境对应的接口地址
ENVIRONMENTS = {
    "dev": "https://dummyjson.com",           # 主测试环境（DummyJSON）
    "test": "https://jsonplaceholder.typicode.com",  # 备用环境
}

class Config:
    def __init__(self, env="dev"):
        self.env = env
        self.base_url = ENVIRONMENTS.get(env, ENVIRONMENTS["dev"])

# 全局配置对象（其他地方 import 这个 config 即可）
config = Config(os.getenv("TEST_ENV", "dev"))