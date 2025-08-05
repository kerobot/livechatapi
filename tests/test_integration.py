import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


client = TestClient(app)


class TestIntegration:
    """統合テスト"""

    def test_cors_headers(self):
        """CORSヘッダーのテスト"""
        with patch("app.api.youtube.youtube_service") as mock_service:
            mock_service.get_live_chat_id.return_value = None

            response = client.get(
                "/api/youtube/livechat?video_id=dQw4w9WgXcQ",
                headers={"Origin": "http://localhost:3000"},
            )

            assert "access-control-allow-origin" in response.headers

    def test_error_handling_chain(self):
        """エラーハンドリングの連鎖テスト"""
        # 無効なvideo_id → バリデーションエラー → HTTPException
        response = client.get("/api/youtube/livechat?video_id=")
        assert response.status_code == 400

        # 存在しないエンドポイント
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_app_startup_and_shutdown(self):
        """アプリケーションの起動・停止テスト"""
        # lifespanが正常に動作することを確認
        with TestClient(app) as test_client:
            response = test_client.get("/health")
            assert response.status_code == 200

    def test_validation_error_response_format(self):
        """バリデーションエラーのレスポンス形式テスト"""
        response = client.post(
            "/api/youtube/livechat", json={"video_id": "", "page_token": None}  # 空文字
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_request_logging_flow(self):
        """リクエストログの流れをテスト"""
        with patch("app.api.youtube.youtube_service") as mock_service:
            mock_service.get_live_chat_id.return_value = None

            # ログが出力されることを間接的に確認
            response = client.get("/api/youtube/livechat?video_id=dQw4w9WgXcQ")
            assert response.status_code == 404  # ライブチャットなしで404
