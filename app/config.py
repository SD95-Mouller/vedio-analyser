import os
from dotenv import load_dotenv

load_dotenv()

# 获取环境变量
COOKIES_PATH = os.getenv("COOKIES_PATH")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")