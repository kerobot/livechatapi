import requests
from typing import Optional
from app.models.youtube import LiveChatMessageListResponse
from app.config import YOUTUBE_API_KEY


def get_live_chat_id(video_id: str) -> Optional[str]:
    url = f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={video_id}&key={YOUTUBE_API_KEY}"
    res = requests.get(url)
    items = res.json().get("items", [])
    if not items:
        return None
    return items[0]["liveStreamingDetails"].get("activeLiveChatId")


def get_chat_messages(
    live_chat_id: str, page_token: Optional[str] = None
) -> LiveChatMessageListResponse:
    url = f"https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId={live_chat_id}&part=snippet,authorDetails&key={YOUTUBE_API_KEY}"
    if page_token:
        url += f"&pageToken={page_token}"
    res = requests.get(url)
    data = res.json()
    return LiveChatMessageListResponse.parse_obj(data)
