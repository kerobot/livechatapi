import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY is not set in environment variables")

# 環境設定
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# レート制限設定（環境別）
if ENVIRONMENT == "production":
    DEFAULT_RATE_LIMIT = "0.3"
    DEFAULT_MAX_RETRIES = "5"
    DEFAULT_BASE_DELAY = "2.0"
    DEFAULT_LOG_LEVEL = "WARNING"
elif ENVIRONMENT == "staging":
    DEFAULT_RATE_LIMIT = "0.4"
    DEFAULT_MAX_RETRIES = "4"
    DEFAULT_BASE_DELAY = "1.5"
    DEFAULT_LOG_LEVEL = "INFO"
else:
    DEFAULT_RATE_LIMIT = "0.5"
    DEFAULT_MAX_RETRIES = "3"
    DEFAULT_BASE_DELAY = "1.0"
    DEFAULT_LOG_LEVEL = "DEBUG"

RATE_LIMIT_REQUESTS_PER_SECOND = float(
    os.getenv("RATE_LIMIT_REQUESTS_PER_SECOND", DEFAULT_RATE_LIMIT)
)
RATE_LIMIT_MAX_RETRIES = int(os.getenv("RATE_LIMIT_MAX_RETRIES", DEFAULT_MAX_RETRIES))
RATE_LIMIT_BASE_DELAY = float(os.getenv("RATE_LIMIT_BASE_DELAY", DEFAULT_BASE_DELAY))

# ログレベル設定（環境別）
LOG_LEVEL = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)

# CORS設定（環境別）
if ENVIRONMENT == "production":
    DEFAULT_CORS_ORIGINS = "https://yourdomain.com"
elif ENVIRONMENT == "staging":
    DEFAULT_CORS_ORIGINS = "https://staging.yourdomain.com,http://localhost:3000"
else:
    DEFAULT_CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"

CORS_ORIGINS_STR = os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_STR.split(",")]

# デバッグモード（環境別）
DEBUG = ENVIRONMENT in ["development", "staging"]

# API設定（環境別）
API_TITLE = f"Live Chat API ({ENVIRONMENT.capitalize()})"
API_VERSION = "1.0.0"
if ENVIRONMENT != "production":
    API_VERSION += f"-{ENVIRONMENT}"
