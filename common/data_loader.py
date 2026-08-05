"""读取测试数据文件的工具"""
import json
import os


def load_json(file_name):
    """从 testdata 目录读取 JSON 文件，返回解析后的数据"""
    file_path = os.path.join("testdata", file_name)
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)