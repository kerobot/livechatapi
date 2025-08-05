import pytest
from app.utils.validators import validate_youtube_video_id, sanitize_page_token


class TestValidateYouTubeVideoId:
    """YouTube動画IDバリデーションのテスト"""

    def test_valid_video_ids(self):
        """正常な動画IDのテスト"""
        valid_ids = [
            "dQw4w9WgXcQ",  # 実際のYouTube動画ID
            "abc123_-DEF",  # 英数字とハイフン、アンダースコア
            "ABCDEFGHIJK",  # 大文字のみ
            "123456789ab",  # 数字と小文字
            "_-abcDEF123",  # アンダースコア・ハイフンから始まる
        ]

        for video_id in valid_ids:
            assert validate_youtube_video_id(video_id) is True, f"Failed for {video_id}"

    def test_invalid_video_ids(self):
        """無効な動画IDのテスト"""
        invalid_ids = [
            "",  # 空文字
            "short",  # 短すぎる
            "toolongvideoid",  # 長すぎる
            "dQw4w9WgXc@",  # 無効文字（@）
            "dQw4w9WgXc ",  # スペース含む
            "###########",  # 特殊文字のみ
            "aaaaaaaaaaa",  # 同じ文字の繰り返し
            "1111111111a",  # ほぼ同じ文字
            None,  # None
        ]

        for video_id in invalid_ids:
            assert (
                validate_youtube_video_id(video_id) is False
            ), f"Should fail for {video_id}"

    def test_edge_cases(self):
        """エッジケースのテスト"""
        # ちょうど11文字
        assert validate_youtube_video_id("12345678901") is True

        # 10文字（短い）
        assert validate_youtube_video_id("1234567890") is False

        # 12文字（長い）
        assert validate_youtube_video_id("123456789012") is False


class TestSanitizePageToken:
    """ページトークンサニタイズのテスト"""

    def test_valid_page_tokens(self):
        """正常なページトークンのテスト"""
        assert sanitize_page_token("validtoken123") == "validtoken123"
        assert sanitize_page_token("   validtoken   ") == "validtoken"
        assert sanitize_page_token(None) is None

    def test_empty_or_whitespace_tokens(self):
        """空文字や空白のテスト"""
        assert sanitize_page_token("") is None
        assert sanitize_page_token("   ") is None
        assert sanitize_page_token("\t\n") is None

    def test_dangerous_characters_removed(self):
        """危険な文字が除去されるテスト"""
        test_cases = [
            ("token<script>", "tokenscript"),
            ("token>alert", "tokenalert"),
            ('token"quote', "tokenquote"),
            ("token'quote", "tokenquote"),
            ("token&amp", "tokenamp"),
            ("token\nline", "tokenline"),
            ("token\rcarriage", "tokencarriage"),
            ("token\ttab", "tokentab"),
        ]

        for input_token, expected in test_cases:
            result = sanitize_page_token(input_token)
            assert (
                result == expected
            ), f"Expected {expected}, got {result} for input {input_token}"
