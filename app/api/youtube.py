from fastapi import APIRouter, Query
from typing import Optional
from app.services.youtube import get_live_chat_id, get_chat_messages
from app.models.youtube import LiveChatMessageListResponse

router = APIRouter(
    prefix="/api/youtube",
    tags=["youtube"],
)


@router.get("/livechat", response_model=LiveChatMessageListResponse)
def youtube_livechat(
    video_id: str = Query(...), page_token: Optional[str] = Query(None)
):
    live_chat_id = get_live_chat_id(video_id)
    if not live_chat_id:
        return {"error": "ライブ配信が見つからないか、ライブチャットが無効です"}
    data = get_chat_messages(live_chat_id, page_token)
    return data
