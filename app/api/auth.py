from fastapi import APIRouter, HTTPException, Query
from app.services.oauth2 import oauth2_service
from app.models.auth import AuthUrlResponse, TokenRequest, TokenResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
)


@router.get("/url", response_model=AuthUrlResponse)
def get_auth_url():
    """
    Google OAuth2認証URLを生成するエンドポイント
    """
    try:
        auth_url, state = oauth2_service.generate_auth_url()
        return AuthUrlResponse(auth_url=auth_url, state=state)
    except Exception as e:
        logger.error(f"💥 認証URL生成エラー: {e}")
        raise HTTPException(status_code=500, detail="認証URL生成に失敗しました")


@router.get("/callback")
def auth_callback(
    code: str = Query(..., description="Google認証サーバーからの認証コード"),
    state: str = Query(..., description="CSRF攻撃防止用のstateパラメータ"),
):
    """
    Google OAuth2認証コールバックエンドポイント
    """
    try:
        token_info = oauth2_service.exchange_code_for_token(code, state)
        return TokenResponse(**token_info)
    except Exception as e:
        logger.error(f"💥 認証コールバックエラー: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/token", response_model=TokenResponse)
def exchange_token(request: TokenRequest):
    """
    認証コードをアクセストークンに交換するエンドポイント（POSTバージョン）
    """
    try:
        token_info = oauth2_service.exchange_code_for_token(request.code, request.state)
        return TokenResponse(**token_info)
    except Exception as e:
        logger.error(f"💥 トークン交換エラー: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh")
def refresh_token(refresh_token: str):
    """
    リフレッシュトークンを使用してアクセストークンを更新
    """
    try:
        token_info = oauth2_service.refresh_access_token(refresh_token)
        return TokenResponse(**token_info)
    except Exception as e:
        logger.error(f"💥 トークン更新エラー: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/validate")
def validate_token(
    access_token: str = Query(..., description="検証するアクセストークン")
):
    """
    アクセストークンの有効性を検証
    """
    try:
        is_valid = oauth2_service.validate_token(access_token)
        return {
            "valid": is_valid,
            "message": "トークン有効" if is_valid else "トークン無効",
        }
    except Exception as e:
        logger.error(f"💥 トークン検証エラー: {e}")
        raise HTTPException(status_code=500, detail="トークン検証に失敗しました")
