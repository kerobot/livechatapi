import secrets
import json
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import logging
from app.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    OAUTH_REDIRECT_URI,
    YOUTUBE_OAUTH_SCOPES,
)

logger = logging.getLogger(__name__)


class OAuth2Service:
    """Google OAuth2認証サービス"""

    def __init__(self):
        self._client_config = {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [OAUTH_REDIRECT_URI],
            }
        }
        self._active_states: Dict[str, bool] = {}  # セキュリティのためstateを管理

    def generate_auth_url(self) -> tuple[str, str]:
        """
        OAuth2認証URLを生成
        Returns:
            tuple: (認証URL, stateパラメータ)
        """
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
            raise ValueError(
                "❌ OAuth2設定が不完全です。GOOGLE_CLIENT_ID と GOOGLE_CLIENT_SECRET を設定してください。"
            )

        try:
            flow = Flow.from_client_config(
                self._client_config,
                scopes=YOUTUBE_OAUTH_SCOPES,
                redirect_uri=OAUTH_REDIRECT_URI,
            )

            # CSRF攻撃防止用のstateパラメータ生成
            state = secrets.token_urlsafe(32)
            self._active_states[state] = True

            auth_url, _ = flow.authorization_url(
                access_type="offline", include_granted_scopes="true", state=state
            )

            logger.info(f"🔐 OAuth2認証URL生成完了: state={state}")
            return auth_url, state

        except Exception as e:
            logger.error(f"💥 OAuth2認証URL生成エラー: {e}")
            raise Exception(f"認証URL生成に失敗しました: {str(e)}")

    def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """
        認証コードをアクセストークンに交換
        Args:
            code: Google認証サーバーから返された認証コード
            state: CSRF攻撃防止用のstateパラメータ
        Returns:
            dict: トークン情報
        """
        # stateパラメータ検証
        if state not in self._active_states:
            logger.warning(f"🚫 不正なstateパラメータ: {state}")
            raise ValueError("不正なstateパラメータです。")

        # 使用済みstateを削除
        del self._active_states[state]

        try:
            flow = Flow.from_client_config(
                self._client_config,
                scopes=YOUTUBE_OAUTH_SCOPES,
                redirect_uri=OAUTH_REDIRECT_URI,
            )

            flow.fetch_token(code=code)
            credentials = flow.credentials

            token_info = {
                "access_token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "expires_in": 3600,  # Googleは通常1時間
                "token_type": "Bearer",
            }

            logger.info("✅ OAuth2トークン取得成功")
            return token_info

        except Exception as e:
            logger.error(f"💥 OAuth2トークン取得エラー: {e}")
            raise Exception(f"トークン取得に失敗しました: {str(e)}")

    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        リフレッシュトークンを使用してアクセストークンを更新
        Args:
            refresh_token: リフレッシュトークン
        Returns:
            dict: 新しいトークン情報
        """
        try:
            credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
                token_uri="https://oauth2.googleapis.com/token",
            )

            request = Request()
            credentials.refresh(request)

            token_info = {
                "access_token": credentials.token,
                "refresh_token": credentials.refresh_token or refresh_token,
                "expires_in": 3600,
                "token_type": "Bearer",
            }

            logger.info("🔄 OAuth2トークン更新成功")
            return token_info

        except Exception as e:
            logger.error(f"💥 OAuth2トークン更新エラー: {e}")
            raise Exception(f"トークン更新に失敗しました: {str(e)}")

    def validate_token(self, access_token: str) -> bool:
        """
        アクセストークンの有効性を検証
        Args:
            access_token: 検証するアクセストークン
        Returns:
            bool: トークンが有効かどうか
        """
        try:
            import requests

            response = requests.get(
                f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
            )

            if response.status_code == 200:
                token_info = response.json()
                # スコープ確認
                scopes = token_info.get("scope", "").split()
                required_scope = "https://www.googleapis.com/auth/youtube.force-ssl"

                if required_scope in scopes:
                    logger.info("✅ アクセストークン有効")
                    return True
                else:
                    logger.warning("⚠️ 必要なスコープが不足")
                    return False
            else:
                logger.warning("⚠️ アクセストークン無効")
                return False

        except Exception as e:
            logger.error(f"💥 トークン検証エラー: {e}")
            return False


# シングルトンインスタンス
oauth2_service = OAuth2Service()
