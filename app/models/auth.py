from pydantic import BaseModel, Field
from typing import Optional


class AuthUrlRequest(BaseModel):
    """OAuth2認証URL生成リクエスト"""

    callback_url: Optional[str] = Field(None, description="認証後のリダイレクト先URL")


class AuthUrlResponse(BaseModel):
    """OAuth2認証URL生成レスポンス"""

    auth_url: str = Field(..., description="Google OAuth2認証URL")
    state: str = Field(..., description="CSRF攻撃防止用のstateパラメータ")


class TokenRequest(BaseModel):
    """OAuth2トークン取得リクエスト"""

    code: str = Field(..., description="認証コード")
    state: Optional[str] = Field(
        None, description="stateパラメータ（callback_url含む）"
    )


class TokenResponse(BaseModel):
    """OAuth2トークンレスポンス"""

    access_token: str = Field(..., description="アクセストークン")
    refresh_token: Optional[str] = Field(None, description="リフレッシュトークン")
    expires_in: int = Field(..., description="トークンの有効期限（秒）")
    token_type: str = Field(default="Bearer", description="トークンタイプ")


class AuthCallbackResponse(BaseModel):
    """OAuth2認証コールバックレスポンス"""

    status: str = Field(..., description="認証ステータス（success/error）")
    message: str = Field(..., description="レスポンスメッセージ")
    access_token: Optional[str] = Field(None, description="アクセストークン（成功時）")
    redirect_url: Optional[str] = Field(None, description="リダイレクト先URL")


class PostChatMessageRequest(BaseModel):
    """ライブチャット投稿リクエスト"""

    video_id: str = Field(
        ..., description="YouTube動画ID（11文字）", min_length=11, max_length=11
    )
    message_text: str = Field(
        ..., min_length=1, max_length=200, description="投稿するメッセージ"
    )
    access_token: str = Field(..., description="OAuth2アクセストークン")


class PostChatMessageResponse(BaseModel):
    """ライブチャット投稿レスポンス"""

    message_id: str = Field(..., description="投稿されたメッセージのID")
    message_text: str = Field(..., description="投稿されたメッセージテキスト")
    author_name: str = Field(..., description="投稿者名")
    published_at: str = Field(..., description="投稿日時")
    success: bool = Field(default=True, description="投稿成功フラグ")
