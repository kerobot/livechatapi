import time
from typing import Optional
from app.models.youtube import LiveChatMessageListResponse
from app.config import (
    YOUTUBE_API_KEY,
    RATE_LIMIT_MAX_RETRIES,
    RATE_LIMIT_BASE_DELAY,
    RATE_LIMIT_REQUESTS_PER_SECOND,
)
from app.utils.http_client import RateLimitedHTTPClient
import logging

logger = logging.getLogger(__name__)


class YouTubeService:
    def __init__(self):
        self.client = RateLimitedHTTPClient(
            max_retries=RATE_LIMIT_MAX_RETRIES,
            base_delay=RATE_LIMIT_BASE_DELAY,
        )
        self.last_request_time = 0
        self.min_interval = 1.0 / RATE_LIMIT_REQUESTS_PER_SECOND
        logger.info("🎬 YouTubeService initialized")

    def _wait_for_rate_limit(self):
        """リクエスト間隔を制御"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            logger.debug(f"⏱️ Rate limiting: waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
        self.last_request_time = time.time()

    def get_live_chat_id(self, video_id: str) -> Optional[str]:
        """ライブチャットIDを取得"""
        logger.debug(f"🔍 Fetching live chat ID for video: {video_id}")
        self._wait_for_rate_limit()

        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "liveStreamingDetails",
            "id": video_id,
            "key": YOUTUBE_API_KEY,
        }

        try:
            data = self.client.get_with_retry(url, params)
            items = data.get("items", [])

            if not items:
                logger.warning(f"🚫 No video found for ID: {video_id}")
                return None

            live_details = items[0].get("liveStreamingDetails", {})
            chat_id = live_details.get("activeLiveChatId")

            if chat_id:
                logger.info(f"✅ Live chat ID retrieved: {chat_id} (video: {video_id})")
            else:
                logger.warning(f"❌ No active live chat for video: {video_id}")

            return chat_id

        except Exception as e:
            logger.error(f"💥 Failed to get live chat ID for video {video_id}: {e}")
            raise

    def get_chat_messages(
        self, live_chat_id: str, page_token: Optional[str] = None
    ) -> LiveChatMessageListResponse:
        """ライブチャットメッセージを取得"""
        logger.debug(
            f"💬 Fetching messages for chat: {live_chat_id}, page_token: {page_token}"
        )
        self._wait_for_rate_limit()

        url = "https://www.googleapis.com/youtube/v3/liveChat/messages"
        params = {
            "liveChatId": live_chat_id,
            "part": "snippet,authorDetails",
            "key": YOUTUBE_API_KEY,
        }

        if page_token:
            params["pageToken"] = page_token

        try:
            data = self.client.get_with_retry(url, params)
            response = LiveChatMessageListResponse.model_validate(data)

            message_count = len(response.items) if hasattr(response, "items") else 0
            logger.info(
                f"📨 Retrieved {message_count} chat messages (chat: {live_chat_id})"
            )

            return response

        except Exception as e:
            logger.error(f"💥 Failed to get chat messages for {live_chat_id}: {e}")
            raise


# サービスのシングルトンインスタンス
youtube_service = YouTubeService()
