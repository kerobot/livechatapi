from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from app.services.oauth2 import oauth2_service
from app.models.auth import (
    AuthUrlResponse,
    TokenRequest,
    TokenResponse,
    AuthUrlRequest,
    AuthCallbackResponse,
)
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
)


@router.get("/login", response_model=AuthUrlResponse)
def get_auth_url(
    callback_url: Optional[str] = Query(None, description="認証後のリダイレクト先URL")
):
    """
    Google OAuth2認証URLを生成するエンドポイント
    callback_urlパラメータでリダイレクト先を指定可能
    """
    try:
        auth_url, state = oauth2_service.generate_auth_url(callback_url)
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
    callback_urlが指定されている場合はリダイレクト、なければJSONレスポンス
    """
    try:
        token_info = oauth2_service.exchange_code_for_token(code, state)
        callback_url = token_info.pop("callback_url", None)

        # callback_urlがある場合はリダイレクト
        if callback_url:
            redirect_url = f"{callback_url}?access_token={token_info['access_token']}&status=success"
            logger.info(f"🔄 Redirecting to: {callback_url}")
            return RedirectResponse(url=redirect_url)

        # callback_urlがない場合はJSONレスポンス
        return TokenResponse(**token_info)

    except Exception as e:
        logger.error(f"💥 認証コールバックエラー: {e}")

        # エラー時もstateからcallback_urlを取り出してリダイレクトを試みる
        try:
            import json

            state_data = json.loads(state)
            callback_url = state_data.get("callback_url")
            if callback_url:
                error_url = f"{callback_url}?status=error&message={str(e)}"
                return RedirectResponse(url=error_url)
        except:
            pass

        raise HTTPException(status_code=400, detail=str(e))


@router.post("/token", response_model=TokenResponse)
def exchange_token(request: TokenRequest):
    """
    認証コードをアクセストークンに交換するエンドポイント（POSTバージョン）
    """
    try:
        if request.state is None:
            raise HTTPException(status_code=400, detail="stateパラメータが必要です")

        token_info = oauth2_service.exchange_code_for_token(request.code, request.state)
        # callback_urlは除外してレスポンス
        token_info.pop("callback_url", None)
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
