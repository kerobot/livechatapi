from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.youtube import youtube_service
from app.models.youtube import LiveChatMessageListResponse
from app.models.request import LiveChatRequest
from app.utils.validators import validate_youtube_video_id, sanitize_page_token
from app.utils.exceptions import handle_youtube_api_error
import logging
import time

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/youtube",
    tags=["youtube"],
)


@router.post("/livechat", response_model=LiveChatMessageListResponse)
def youtube_livechat_post(request: LiveChatRequest):
    """POSTメソッドでのライブチャット取得（バリデーション強化版）"""
    return _get_livechat(request.video_id, request.page_token)


@router.get("/livechat", response_model=LiveChatMessageListResponse)
def youtube_livechat_get(video_id: str, page_token: Optional[str] = None):
    """GETメソッドでのライブチャット取得（後方互換性のため）"""
    if not validate_youtube_video_id(video_id):
        logger.warning(f"🚫 Invalid video_id: {video_id}")
        raise HTTPException(
            status_code=400,
            detail="無効な動画IDです。11文字の英数字・ハイフン・アンダースコアのみ使用してください。",
        )

    cleaned_page_token = sanitize_page_token(page_token)
    return _get_livechat(video_id, cleaned_page_token)


def _get_livechat(
    video_id: str, page_token: Optional[str]
) -> LiveChatMessageListResponse:
    """ライブチャット取得の共通処理"""
    start_time = time.time()
    logger.info(f"📹 Livechat request - video_id: {video_id}")

    try:
        live_chat_id = youtube_service.get_live_chat_id(video_id)
        if not live_chat_id:
            logger.warning(f"❌ Live chat not found for video: {video_id}")
            raise HTTPException(
                status_code=404,
                detail="ライブ配信が見つからないか、ライブチャットが無効です。",
            )

        data = youtube_service.get_chat_messages(live_chat_id, page_token)

        elapsed = time.time() - start_time
        message_count = len(data.items) if hasattr(data, "items") else 0
        logger.info(
            f"✅ Success - video_id: {video_id}, messages: {message_count}, time: {elapsed:.2f}s"
        )

        return data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error - video_id: {video_id}, error: {str(e)}")
        raise handle_youtube_api_error(e)
