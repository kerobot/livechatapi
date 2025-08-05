from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional


class LiveChatRequest(BaseModel):
    """ライブチャットリクエストのバリデーションモデル"""

    video_id: str = Field(
        ...,
        description="YouTubeの動画ID（11文字）",
        examples=["dQw4w9WgXcQ"],
        min_length=11,
        max_length=11,
    )

    page_token: Optional[str] = Field(
        None, description="ページネーション用トークン", max_length=200
    )

    @field_validator("video_id")
    @classmethod
    def validate_video_id(cls, v):
        if not v:
            raise ValueError("video_idは必須だよ〜")

        pattern = r"^[a-zA-Z0-9_-]{11}$"
        if not re.match(pattern, v):
            raise ValueError(
                "video_idの形式が間違ってるよ〜！11文字の英数字・ハイフン・アンダースコアのみOK"
            )

        return v

    @field_validator("page_token")
    @classmethod
    def validate_page_token(cls, v):
        if v is None:
            return v

        if v.strip() == "":
            return None

        dangerous_chars = ["<", ">", '"', "'", "&", "\n", "\r", "\t"]
        if any(char in v for char in dangerous_chars):
            raise ValueError("page_tokenに危険な文字が含まれてるよ〜")

        return v.strip()


class HealthCheckResponse(BaseModel):
    """ヘルスチェックのレスポンスモデル"""

    status: str = Field(..., examples=["healthy"])
    message: str = Field(..., examples=["Live Chat API is running!"])
    timestamp: str = Field(..., examples=["2025-08-05T18:33:52+09:00"])
