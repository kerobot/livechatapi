"""
API エンドポイント関連のモジュール
各サービスのAPIルーターをここで管理
"""

from .youtube import router as youtube_router

__all__ = ["youtube_router"]
