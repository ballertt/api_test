"""日志模块：控制台 + 文件双重输出"""
import logging
import os

# 确保 logs 目录存在
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 创建 logger
logger = logging.getLogger("api_test")
logger.setLevel(logging.INFO)

# 日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# 1. 输出到控制台（Run 窗口可见）
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 2. 输出到文件 logs/test.log
file_handler = logging.FileHandler(f"{LOG_DIR}/test.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)