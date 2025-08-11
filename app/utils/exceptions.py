from fastapi import HTTPException
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class YouTubeAPIError(Exception):
    """YouTube API関連のカスタム例外"""

    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(Exception):
    """バリデーション関連のカスタム例外"""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


def handle_youtube_api_error(error: Exception) -> HTTPException:
    """YouTube API エラーを適切なHTTPExceptionに変換"""
    error_str = str(error).lower()

    if "quota" in error_str:
        return HTTPException(
            status_code=429, detail="YouTube APIのクォータを超過しました。"
        )
    elif "forbidden" in error_str:
        return HTTPException(
            status_code=403, detail="YouTube APIへのアクセスが拒否されました。"
        )
    elif "not found" in error_str:
        return HTTPException(status_code=404, detail="動画が見つかりませんでした。")
    else:
        return HTTPException(
            status_code=500, detail="YouTube APIでエラーが発生しました。"
        )
