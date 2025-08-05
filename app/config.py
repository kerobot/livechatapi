import os
from dotenv import load_dotenv

load_dotenv()  # .envファイル読み込み

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
