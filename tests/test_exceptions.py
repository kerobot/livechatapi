import pytest
from fastapi import HTTPException
from app.utils.exceptions import (
    YouTubeAPIError,
    ValidationError,
    handle_youtube_api_error,
)


class TestYouTubeAPIError:
    """YouTubeAPIErrorのテスト"""

    def test_youtube_api_error_creation(self):
        """YouTubeAPIError作成のテスト"""
        error = YouTubeAPIError("Test message", "TEST_CODE")
        assert error.message == "Test message"
        assert error.error_code == "TEST_CODE"
        assert str(error) == "Test message"

    def test_youtube_api_error_without_code(self):
        """エラーコードなしのYouTubeAPIError"""
        error = YouTubeAPIError("Test message")
        assert error.message == "Test message"
        assert error.error_code is None


class TestValidationError:
    """ValidationErrorのテスト"""

    def test_validation_error_creation(self):
        """ValidationError作成のテスト"""
        error = ValidationError("video_id", "Invalid format")
        assert error.field == "video_id"
        assert error.message == "Invalid format"
        assert str(error) == "video_id: Invalid format"


class TestHandleYouTubeApiError:
    """YouTube APIエラーハンドリングのテスト"""

    def test_quota_exceeded_error(self):
        """クォータ超過エラーのテスト"""
        error = Exception("quota exceeded for this project")
        result = handle_youtube_api_error(error)

        assert isinstance(result, HTTPException)
        assert result.status_code == 429
        assert "クォータを超過しました。" in result.detail

    def test_forbidden_error(self):
        """アクセス拒否エラーのテスト"""
        error = Exception("forbidden access to this resource")
        result = handle_youtube_api_error(error)

        assert isinstance(result, HTTPException)
        assert result.status_code == 403
        assert "アクセスが拒否されました。" in result.detail

    def test_not_found_error(self):
        """リソースが見つからないエラーのテスト"""
        error = Exception("video not found")
        result = handle_youtube_api_error(error)

        assert isinstance(result, HTTPException)
        assert result.status_code == 404
        assert "見つかりませんでした。" in result.detail

    def test_generic_error(self):
        """一般的なエラーのテスト"""
        error = Exception("some unknown error")
        result = handle_youtube_api_error(error)

        assert isinstance(result, HTTPException)
        assert result.status_code == 500
        assert "エラーが発生しました。" in result.detail
