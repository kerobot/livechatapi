import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.config import LOG_LEVEL, ENVIRONMENT


def setup_logger():
    """アプリケーション全体のログ設定"""

    # ログディレクトリを作成
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # ルートロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    # 既存のハンドラーをクリア
    root_logger.handlers.clear()

    # フォーマッター設定（環境別）
    if ENVIRONMENT == "production":
        # 本番環境では絵文字なし、構造化ログ
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        # 開発環境では絵文字あり
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # コンソールハンドラー
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 環境別ログレベル
    if ENVIRONMENT == "production":
        console_handler.setLevel(logging.WARNING)
    else:
        console_handler.setLevel(logging.INFO)

    root_logger.addHandler(console_handler)

    # ファイルログ（全環境対応）
    file_handler = RotatingFileHandler(
        log_dir / f"livechatapi-{ENVIRONMENT}.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    # 環境別ファイルログレベル
    if ENVIRONMENT == "production":
        file_handler.setLevel(logging.INFO)  # 本番でもファイルには詳細ログ
    else:
        file_handler.setLevel(logging.DEBUG)

    root_logger.addHandler(file_handler)

    # エラー専用ログ（本番環境では必須）
    if ENVIRONMENT == "production":
        error_handler = RotatingFileHandler(
            log_dir / "error.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=10,
            encoding="utf-8",
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_handler)

    logging.info(f"Logger setup completed for {ENVIRONMENT} environment!")
