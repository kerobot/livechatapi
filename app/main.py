import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from datetime import datetime
from app.api import youtube_router
from app.api.auth import router as auth_router
from app.models.request import HealthCheckResponse
from app.utils.logger import setup_logger
from app.utils.exceptions import YouTubeAPIError, ValidationError
from app.config import CORS_ORIGINS, ENVIRONMENT, DEBUG, API_TITLE, API_VERSION
import logging

# ログ設定を最初に実行
setup_logger()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"🚀 Live Chat API starting up in {ENVIRONMENT} mode...")
    logger.info(f"🌐 CORS origins: {CORS_ORIGINS}")
    logger.info(f"🐛 Debug mode: {DEBUG}")
    yield
    # Shutdown
    logger.info("👋 Live Chat API shutting down...")


app = FastAPI(
    title=API_TITLE,  # 環境名が入る
    description="YouTubeライブチャット取得API",
    version=API_VERSION,  # 環境別バージョン
    debug=DEBUG,  # 環境別デバッグモード
    lifespan=lifespan,
)


# 例外ハンドラー（環境別でレスポンス内容変更）
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"🚫 Validation error: {exc.errors()}")

    # 本番環境では詳細なエラー情報を隠す
    if ENVIRONMENT == "production":
        return JSONResponse(
            status_code=422, content={"detail": "入力値にエラーがあります。"}
        )
    else:
        return JSONResponse(
            status_code=422,
            content={"detail": "入力値にエラーがあります。", "errors": exc.errors()},
        )


@app.exception_handler(YouTubeAPIError)
async def youtube_api_exception_handler(request: Request, exc: YouTubeAPIError):
    logger.error(f"📺 YouTube API error: {exc.message}")
    return JSONResponse(status_code=500, content={"detail": exc.message})


@app.exception_handler(ValidationError)
async def custom_validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning(f"⚠️ Custom validation error: {exc.field} - {exc.message}")
    return JSONResponse(
        status_code=400, content={"detail": f"{exc.field}: {exc.message}"}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(youtube_router)
app.include_router(auth_router)


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    logger.debug("Health check requested")
    return HealthCheckResponse(
        status="healthy",
        message=f"Live Chat API is running in {ENVIRONMENT} mode!",  # 環境名表示！
        timestamp=datetime.now().isoformat(),
    )


# 開発環境限定のエンドポイント
if DEBUG:

    @app.get("/debug/config")
    async def debug_config():
        """デバッグ用設定確認エンドポイント（開発・ステージング限定）"""
        return {
            "environment": ENVIRONMENT,
            "debug": DEBUG,
            "cors_origins": CORS_ORIGINS,
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
        }
