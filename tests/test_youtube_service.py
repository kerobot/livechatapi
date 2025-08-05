import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app
from app.models.youtube import LiveChatMessageListResponse


client = TestClient(app)


@pytest.fixture
def mock_youtube_api_response():
    """ダミーのレスポンスデータを返すfixture"""
    return {
        "kind": "youtube#liveChatMessageListResponse",
        "etag": "dummy_etag",
        "nextPageToken": "CAoQAA",
        "pollingIntervalMillis": 5000,
        "items": [],
        "pageInfo": {"totalResults": 0, "resultsPerPage": 0},
    }


class TestYouTubeAPI:
    """YouTube API エンドポイントのテスト"""

    @patch("app.api.youtube.youtube_service")
    def test_get_livechat_success(self, mock_service, mock_youtube_api_response):
        """GET /api/youtube/livechat 成功のテスト"""
        # モックレスポンスを作成
        mock_response = LiveChatMessageListResponse.model_validate(
            mock_youtube_api_response
        )

        # モックの設定
        mock_service.get_live_chat_id.return_value = "chat_id_123"
        mock_service.get_chat_messages.return_value = mock_response

        response = client.get("/api/youtube/livechat?video_id=dQw4w9WgXcQ")

        assert response.status_code == 200
        data = response.json()
        assert data["nextPageToken"] == "CAoQAA"
        assert data["pollingIntervalMillis"] == 5000

        # モックが正しく呼ばれたかチェック
        mock_service.get_live_chat_id.assert_called_once_with("dQw4w9WgXcQ")
        mock_service.get_chat_messages.assert_called_once_with("chat_id_123", None)

    def test_get_livechat_invalid_video_id(self):
        """無効な動画IDのテスト"""
        response = client.get("/api/youtube/livechat?video_id=short")
        assert response.status_code == 400
        data = response.json()
        assert "無効な動画ID" in data["detail"]

    @patch("app.api.youtube.youtube_service")
    def test_get_livechat_no_live_chat(self, mock_service):
        """ライブチャットが存在しない場合のテスト"""
        mock_service.get_live_chat_id.return_value = None

        response = client.get("/api/youtube/livechat?video_id=dQw4w9WgXcQ")

        assert response.status_code == 404
        data = response.json()
        assert "ライブ配信が見つからない" in data["detail"]

    @patch("app.api.youtube.youtube_service")
    def test_post_livechat_success(self, mock_service, mock_youtube_api_response):
        """POST /api/youtube/livechat 成功のテスト"""
        mock_response = LiveChatMessageListResponse.model_validate(
            mock_youtube_api_response
        )

        mock_service.get_live_chat_id.return_value = "chat_id_123"
        mock_service.get_chat_messages.return_value = mock_response

        payload = {"video_id": "dQw4w9WgXcQ", "page_token": "valid_token"}

        response = client.post("/api/youtube/livechat", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["nextPageToken"] == "CAoQAA"

        # モックが正しく呼ばれたかチェック
        mock_service.get_live_chat_id.assert_called_once_with("dQw4w9WgXcQ")
        mock_service.get_chat_messages.assert_called_once_with(
            "chat_id_123", "valid_token"
        )

    def test_post_livechat_invalid_payload(self):
        """無効なペイロードのテスト"""
        payload = {"video_id": "short", "page_token": "valid_token"}

        response = client.post("/api/youtube/livechat", json=payload)

        assert response.status_code == 422

    def test_health_check(self):
        """ヘルスチェックのテスト"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "message" in data

    def test_missing_video_id(self):
        """video_idが欠けている場合のテスト"""
        response = client.get("/api/youtube/livechat")
        assert response.status_code == 422

    def test_empty_video_id(self):
        """空のvideo_idのテスト"""
        response = client.get("/api/youtube/livechat?video_id=")
        assert response.status_code == 400

    @patch("app.api.youtube.youtube_service")
    def test_youtube_api_error(self, mock_service):
        """YouTube APIエラーのテスト"""
        from app.utils.exceptions import YouTubeAPIError

        mock_service.get_live_chat_id.side_effect = YouTubeAPIError(
            "API quota exceeded"
        )

        response = client.get("/api/youtube/livechat?video_id=dQw4w9WgXcQ")

        # エラーハンドリングによってステータスコードが決まる
        assert response.status_code in [429, 500]  # クォータエラーは429か500

    @patch("app.api.youtube.youtube_service")
    def test_with_page_token(self, mock_service, mock_youtube_api_response):
        """ページトークン付きのテスト"""
        mock_response = LiveChatMessageListResponse.model_validate(
            mock_youtube_api_response
        )

        mock_service.get_live_chat_id.return_value = "chat_id_123"
        mock_service.get_chat_messages.return_value = mock_response

        response = client.get(
            "/api/youtube/livechat?video_id=dQw4w9WgXcQ&page_token=testtoken"
        )

        assert response.status_code == 200
        # ページトークンが正しく渡されたかチェック
        mock_service.get_chat_messages.assert_called_once_with(
            "chat_id_123", "testtoken"
        )

    @patch("app.api.youtube.youtube_service")
    def test_cors_headers(self, mock_service):
        """CORSヘッダーのテスト"""
        # モックを設定してエラーを避ける
        mock_service.get_live_chat_id.return_value = None

        response = client.get(
            "/api/youtube/livechat?video_id=dQw4w9WgXcQ",
            headers={"Origin": "http://localhost:3000"},
        )

        # CORSヘッダーが設定されてることを確認
        assert "access-control-allow-origin" in response.headers

    @patch("app.api.youtube.youtube_service")
    def test_sanitize_page_token(self, mock_service, mock_youtube_api_response):
        """ページトークンのサニタイズテスト"""
        mock_response = LiveChatMessageListResponse.model_validate(
            mock_youtube_api_response
        )

        mock_service.get_live_chat_id.return_value = "chat_id_123"
        mock_service.get_chat_messages.return_value = mock_response

        # 危険な文字を含むページトークンをテスト
        response = client.get(
            "/api/youtube/livechat?video_id=dQw4w9WgXcQ&page_token=token<script>"
        )

        # サニタイズされて処理される
        assert response.status_code == 200
        # サニタイズされたトークンが渡されることを確認
        mock_service.get_chat_messages.assert_called_once_with(
            "chat_id_123", "tokenscript"  # 危険な文字が除去される
        )

    @patch("app.api.youtube.youtube_service")
    def test_long_video_id(self, mock_service):
        """長すぎる動画IDのテスト"""
        long_video_id = "a" * 15  # 15文字（11文字を超える）

        response = client.get(f"/api/youtube/livechat?video_id={long_video_id}")

        assert response.status_code == 400
        data = response.json()
        assert "無効な動画ID" in data["detail"]

    def test_options_request(self):
        """OPTIONSリクエストのテスト（CORS preflight）"""
        response = client.options(
            "/api/youtube/livechat",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )

        # OPTIONSリクエストが適切に処理される
        assert response.status_code in [200, 204]
