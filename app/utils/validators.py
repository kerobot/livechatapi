import re
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def validate_youtube_video_id(video_id: str) -> bool:
    """YouTube動画IDの詳細バリデーション"""
    if not video_id or len(video_id) != 11:
        logger.warning(
            f"🚫 Invalid video_id length: {len(video_id) if video_id else 0}"
        )
        return False

    pattern = r"^[a-zA-Z0-9_-]{11}$"
    if not re.match(pattern, video_id):
        logger.warning(f"🚫 Invalid video_id pattern: {video_id}")
        return False

    # 全部同じ文字はおかしい
    if len(set(video_id)) <= 2:
        logger.warning(f"🚫 Suspicious video_id: {video_id}")
        return False

    return True


def sanitize_page_token(page_token: Optional[str]) -> Optional[str]:
    """ページトークンの清浄化"""
    if not page_token:
        return None

    cleaned = page_token.strip()
    if not cleaned:
        return None

    # 危険な文字を除去
    dangerous_patterns = [
        r'[<>"\'\&\n\r\t]',
        r"[\x00-\x1f\x7f-\x9f]",
    ]

    for pattern in dangerous_patterns:
        cleaned = re.sub(pattern, "", cleaned)

    return cleaned if cleaned else None
