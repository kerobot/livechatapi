import pytest
import os
from unittest.mock import patch


@pytest.fixture(autouse=True)
def setup_test_environment():
    """テスト用環境変数の設定"""
    test_env = {
        "ENVIRONMENT": "test",
        "YOUTUBE_API_KEY": "test_api_key_1234567890",
        "LOG_LEVEL": "DEBUG",
        "CORS_ORIGINS": "http://localhost:3000,http://localhost:8000",
        "RATE_LIMIT_REQUESTS_PER_SECOND": "2.0",  # テスト用に高めに設定
        "RATE_LIMIT_MAX_RETRIES": "2",
        "RATE_LIMIT_BASE_DELAY": "0.5",
    }

    with patch.dict(os.environ, test_env, clear=False):
        yield


@pytest.fixture
def mock_youtube_api_response():
    """YouTube APIのモックレスポンス"""
    return {
        "kind": "youtube#liveChatMessageListResponse",
        "etag": "test_etag_12345",
        "nextPageToken": "CAoQAA",
        "pollingIntervalMillis": 5000,
        "items": [
            {
                "kind": "youtube#liveChatMessage",
                "etag": "message_etag_67890",
                "id": "LCC.message_id_12345",
                "snippet": {
                    "type": "textMessageEvent",
                    "liveChatId": "chat_id_123",
                    "authorChannelId": "UC_author_id_12345",
                    "publishedAt": "2024-01-01T12:00:00.000Z",
                    "hasDisplayContent": True,
                    "displayMessage": "こんにちは〜！テストメッセージだよ💖",
                },
                "authorDetails": {
                    "channelId": "UC_author_id_12345",
                    "channelUrl": "https://www.youtube.com/channel/UC_author_id_12345",
                    "displayName": "テストユーザー",
                    "profileImageUrl": "https://yt3.ggpht.com/test_avatar.jpg",
                    "isVerified": False,
                    "isChatOwner": False,
                    "isChatSponsor": False,
                    "isChatModerator": False,
                },
            }
        ],
    }


@pytest.fixture
def mock_video_response():
    """YouTube動画情報のモックレスポンス"""
    return {
        "items": [{"liveStreamingDetails": {"activeLiveChatId": "test_chat_id_123"}}]
    }


@pytest.fixture
def mock_empty_response():
    """空のレスポンス"""
    return {
        "kind": "youtube#liveChatMessageListResponse",
        "etag": "empty_etag",
        "nextPageToken": None,
        "pollingIntervalMillis": 5000,
        "items": [],
    }
