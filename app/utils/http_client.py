import time
import random
import requests
from typing import Optional, Dict, Any
from app.config import ENVIRONMENT  # ← 追加
import logging

logger = logging.getLogger(__name__)


class RateLimitedHTTPClient:
    """レート制限対応のHTTPクライアント"""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.session = requests.Session()

        # 環境別User-Agent設定
        user_agent = f"LiveChatAPI/1.0 ({ENVIRONMENT})"
        if ENVIRONMENT == "production":
            user_agent += " (Production)"

        self.session.headers.update({"User-Agent": user_agent})

    def get_with_retry(self, url: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        """指数バックオフとジッターを使ったリトライ機能付きGET"""
        for attempt in range(self.max_retries + 1):
            try:
                # 環境別タイムアウト設定
                timeout = 30 if ENVIRONMENT == "production" else 10
                response = self.session.get(url, params=params, timeout=timeout)

                # レート制限チェック
                if response.status_code == 429:
                    if attempt == self.max_retries:
                        raise Exception("Rate limit exceeded after all retries")

                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        delay = int(retry_after)
                    else:
                        delay = self.base_delay * (2**attempt) + random.uniform(0, 1)

                    logger.warning(
                        f"Rate limited. Retrying in {delay:.2f} seconds... (attempt {attempt + 1})"
                    )
                    time.sleep(delay)
                    continue

                response.raise_for_status()
                data = response.json()

                # YouTube APIエラーチェック
                if "error" in data:
                    error = data["error"]
                    if (
                        error.get("code") == 403
                        and "quota" in error.get("message", "").lower()
                    ):
                        raise Exception("YouTube API quota exceeded")
                    raise Exception(f"YouTube API Error: {error.get('message')}")

                logger.debug(f"Request successful: {url}")
                return data

            except requests.RequestException as e:
                if attempt == self.max_retries:
                    raise Exception(
                        f"Request failed after {self.max_retries} retries: {e}"
                    )

                delay = self.base_delay * (2**attempt) + random.uniform(0, 1)
                logger.warning(
                    f"Request failed (attempt {attempt + 1}). Retrying in {delay:.2f} seconds..."
                )
                time.sleep(delay)

        raise Exception("Unexpected error in retry logic")

    def close(self):
        """セッションを閉じる"""
        self.session.close()
