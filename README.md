# 🎬 YouTube Live Chat API

YouTube ライブ配信のチャットメッセージをリアルタイムで取得する高性能なFastAPI Webアプリケーション

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com/)
[![Poetry](https://img.shields.io/badge/Poetry-managed-blue.svg)](https://python-poetry.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 特徴

- 🚀 **高速**: FastAPIベースの非同期処理
- 🛡️ **安全**: 入力バリデーション、レート制限、エラーハンドリング
- 📊 **監視**: 構造化ログ、パフォーマンス計測
- 🌐 **CORS対応**: フロントエンドとの連携
- 🧪 **テスト完備**: 単体・統合テスト
- 📈 **スケーラブル**: 環境別設定、プロダクション対応

## 🎯 主な機能

- YouTube Live Chat メッセージのリアルタイム取得
- ページネーション対応（nextPageToken）
- レート制限とリトライ機能
- 詳細なユーザー情報（アバター、バッジなど）
- 自動ドキュメント生成（Swagger UI）

## 🚀 クイックスタート

### 必要要件

- Python 3.13+
- Poetry 2.1+
- YouTube Data API v3 キー

### インストール

```powershell
# リポジトリをクローン
git clone https://github.com/kerobot/livechatapi.git
cd livechatapi

# Poetryで依存関係をインストール
poetry install

# 仮想環境を有効化
poetry shell
```

### 環境設定

`.env` ファイルを作成してAPIキーを設定：

```env
# YouTube Data API v3 キー（必須）
YOUTUBE_API_KEY=your_youtube_api_key_here

# 環境設定（オプション）
ENVIRONMENT=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# レート制限設定（オプション）
RATE_LIMIT_REQUESTS_PER_SECOND=0.5
RATE_LIMIT_MAX_RETRIES=3
RATE_LIMIT_BASE_DELAY=1.0
```

### 実行

```powershell
# 開発サーバー起動
poetry run uvicorn app.main:app --reload

# または
python -m uvicorn app.main:app --reload
```

サーバーが起動したら以下のURLにアクセス：

- **API**: http://127.0.0.1:8000
- **ドキュメント**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📚 API使用方法

### ライブチャット取得

```bash
# GETリクエスト
curl "http://127.0.0.1:8000/api/youtube/livechat?video_id=dQw4w9WgXcQ"

# ページネーション
curl "http://127.0.0.1:8000/api/youtube/livechat?video_id=dQw4w9WgXcQ&page_token=NEXT_PAGE_TOKEN"
```

```javascript
// JavaScript例
const response = await fetch('http://127.0.0.1:8000/api/youtube/livechat?video_id=dQw4w9WgXcQ');
const data = await response.json();
console.log(data);
```

### レスポンス例

```json
{
  "kind": "youtube#liveChatMessageListResponse",
  "nextPageToken": "GhE9zH...",
  "pollingIntervalMillis": 5000,
  "items": [
    {
      "id": "message_id",
      "snippet": {
        "publishedAt": "2025-08-08T10:30:00Z",
        "displayMessage": "素晴らしい配信ですね！",
        "authorDetails": {
          "channelId": "UCxxxxx",
          "displayName": "ユーザー名",
          "profileImageUrl": "https://yt3.ggpht.com/...",
          "isVerified": false,
          "isChatOwner": false,
          "isChatSponsor": false,
          "isChatModerator": false
        }
      }
    }
  ]
}
```

## 🧪 テスト

```powershell
# 全テスト実行
poetry run pytest

# カバレッジ付き
poetry run pytest --cov=app

# 特定のテストファイル
poetry run pytest tests/test_api_youtube.py

# 詳細出力
poetry run pytest -v -s
```

## 🏗️ プロジェクト構造

```
livechatapi/
├── app/                    # メインアプリケーション
│   ├── __init__.py
│   ├── main.py            # FastAPIアプリケーション
│   ├── config.py          # 設定管理
│   ├── api/               # APIルーター
│   │   ├── __init__.py
│   │   └── youtube.py     # YouTube API エンドポイント
│   ├── models/            # Pydanticモデル
│   │   ├── __init__.py
│   │   ├── request.py     # リクエストモデル
│   │   └── youtube.py     # YouTubeレスポンスモデル
│   ├── services/          # ビジネスロジック
│   │   ├── __init__.py
│   │   └── youtube.py     # YouTube Data API クライアント
│   └── utils/             # ユーティリティ
│       ├── __init__.py
│       ├── exceptions.py  # カスタム例外
│       ├── http_client.py # HTTPクライアント
│       ├── logger.py      # ログ設定
│       └── validators.py  # バリデーション
├── tests/                 # テストコード
│   ├── __init__.py
│   ├── conftest.py       # pytest設定
│   ├── test_*.py         # 各種テスト
│   └── run_tests.py      # テスト実行スクリプト
├── logs/                 # ログファイル
├── pyproject.toml        # Poetry設定
├── poetry.lock          # 依存関係ロック
├── .env                 # 環境変数（要作成）
└── README.md           # このファイル
```

## ⚙️ 設定オプション

### 環境変数

| 変数名 | デフォルト | 説明 |
|--------|-----------|------|
| `YOUTUBE_API_KEY` | **必須** | YouTube Data API v3 キー |
| `ENVIRONMENT` | `development` | 実行環境 (`development`, `staging`, `production`) |
| `LOG_LEVEL` | `DEBUG` | ログレベル |
| `CORS_ORIGINS` | `http://localhost:3000,http://127.0.0.1:3000` | CORS許可オリジン |
| `RATE_LIMIT_REQUESTS_PER_SECOND` | `0.5` | レート制限（秒間リクエスト数） |
| `RATE_LIMIT_MAX_RETRIES` | `3` | 最大リトライ回数 |
| `RATE_LIMIT_BASE_DELAY` | `1.0` | リトライ基本遅延（秒） |

### 環境別デフォルト設定

#### Development
- レート制限: 0.5 req/s
- ログレベル: DEBUG
- CORS: localhost許可

#### Staging
- レート制限: 0.4 req/s
- ログレベル: INFO
- CORS: staging.yourdomain.com許可

#### Production
- レート制限: 0.3 req/s
- ログレベル: WARNING
- CORS: yourdomain.com許可

## 🎯 フロントエンド連携

このAPIは以下のフロントエンドフレームワークと連携可能：

- React / Next.js
- Vue.js / Nuxt.js
- Angular
- Vanilla JavaScript

### React連携例

```typescript
// YouTube Live Chat Viewer Component
const [messages, setMessages] = useState([]);

const fetchMessages = async (videoId: string, pageToken?: string) => {
  const url = new URL('http://localhost:8000/api/youtube/livechat');
  url.searchParams.set('video_id', videoId);
  if (pageToken) url.searchParams.set('page_token', pageToken);
  
  const response = await fetch(url.toString());
  const data = await response.json();
  
  setMessages(prev => [...prev, ...data.items]);
  return data.nextPageToken;
};
```

## 📈 パフォーマンス

- **レスポンス時間**: 通常 100-300ms
- **レート制限**: YouTube API クォータに準拠
- **同時接続**: FastAPIの非同期処理により高いスループット
- **メモリ使用量**: 軽量（約50MB）

## 🛡️ セキュリティ

- 入力値の厳密なバリデーション
- SQLインジェクション対策（不要だがベストプラクティス）
- レート制限によるDoS攻撃対策
- CORS設定による跨サイトリクエスト制御
- 詳細なログ記録

## 🐛 トラブルシューティング

### よくある問題

1. **YouTube API エラー**
   ```
   YouTube API Error: The request cannot be completed because you have exceeded your quota.
   ```
   → API キーのクォータを確認してください

2. **CORS エラー**
   ```
   Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
   ```
   → `.env` の `CORS_ORIGINS` を確認してください

3. **ライブチャット未発見**
   ```
   ライブ配信が見つからないか、ライブチャットが無効です
   ```
   → 動画IDが正しく、ライブ配信中であることを確認してください

### デバッグ

```powershell
# デバッグモードで起動
ENVIRONMENT=development LOG_LEVEL=DEBUG uvicorn app.main:app --reload

# ログファイル確認
cat logs/livechatapi-development.log
```

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照

## 👥 作者

- **kerobot** - 初期開発・メンテナンス

## 🙏 謝辞

- [FastAPI](https://fastapi.tiangolo.com/) - 素晴らしいWebフレームワーク
- [YouTube Data API](https://developers.google.com/youtube/v3) - ライブチャットデータの提供
- [Poetry](https://python-poetry.org/) - 依存関係管理

---

⭐ このプロジェクトが気に入ったらスターをお願いします！
