# A1-PRO - 日本株分析Webアプリケーション

日本株の個別銘柄を分析するためのWebアプリケーション。ビジュアル化された決算情報、RAGチャットボット、ポートフォリオ管理機能を提供します。

## 📋 主要機能

- **銘柄検索・分析**: 銘柄コードまたは企業名で検索
- **ビジュアル決算**: 売上高、利益、財務指標のグラフ表示
- **RAGチャットボット**: Ollama (Llama 3.1) を使った質問応答
- **ポートフォリオ管理**: 保有銘柄の損益管理
- **複数資産比較**: 日本株、米国株、為替、暗号資産のパフォーマンス比較

## 🛠 技術スタック

### フロントエンド
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Recharts

### バックエンド
- Python 3.11+
- FastAPI
- SQLAlchemy
- MySQL 8.0

### AI/RAG
- Ollama (Llama 3.1 8B)
- LangChain
- ChromaDB

### 外部API
- バフェット・コードAPI
- Yahoo Finance (yfinance)
- CoinGecko API
- exchangerate-api

## 🚀 セットアップ

### 前提条件

以下がインストールされている必要があります：

- Node.js 20+
- Python 3.11+
- MySQL 8.0+
- Docker & Docker Compose
- Ollama

### 1. リポジトリのクローン

```bash
git clone https://github.com/koshiro-y-0/a1-pro.git
cd a1-pro
```

### 2. Ollamaのセットアップ

```bash
# Ollamaのインストール（macOS）
brew install ollama

# Llama 3.1 8Bモデルのダウンロード
ollama pull llama3.1:8b

# Ollamaサービスの起動
ollama serve
```

### 3. Docker Composeで環境構築

```bash
# 環境変数ファイルのコピー
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 環境変数の編集（必要に応じて）
# backend/.env と frontend/.env.local を編集

# Dockerコンテナの起動
docker-compose up -d
```

### 4. データベースのマイグレーション

```bash
# バックエンドコンテナに入る
docker-compose exec backend bash

# マイグレーション実行
alembic upgrade head

# コンテナから出る
exit
```

### 5. アプリケーションへのアクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

## 📝 開発環境セットアップ（ローカル）

### フロントエンド

```bash
cd frontend
npm install
npm run dev
```

### バックエンド

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🗂 プロジェクト構成

```
a1-pro/
├── frontend/          # Next.jsアプリケーション
│   ├── src/
│   │   ├── app/      # App Router
│   │   ├── components/
│   │   ├── lib/
│   │   └── types/
│   └── package.json
│
├── backend/           # FastAPIアプリケーション
│   ├── app/
│   │   ├── api/      # APIエンドポイント
│   │   ├── models/   # データモデル
│   │   ├── services/ # ビジネスロジック
│   │   ├── db/       # データベース設定
│   │   └── rag/      # RAGシステム
│   ├── requirements.txt
│   └── main.py
│
├── docker/            # Docker関連ファイル
├── docs/              # ドキュメント
├── docker-compose.yml
├── CLAUDE.md          # プロジェクト仕様書
├── TODO.md            # 実行計画・TODOリスト
└── README.md
```

## 🔑 環境変数

### バックエンド (.env)

```bash
# Database
DATABASE_URL=mysql+pymysql://a1pro_user:password@localhost:3306/a1pro

# External APIs
BUFFETT_CODE_API_KEY=your_api_key_here
EXCHANGE_RATE_API_KEY=your_api_key_here

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./data/chromadb
```

### フロントエンド (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📖 ドキュメント

- [プロジェクト仕様書](./CLAUDE.md) - 完全な技術仕様
- [実行計画・TODOリスト](./TODO.md) - 開発フェーズとタスク

## 🎨 UIの特徴

### デザインシステム
- **カラーパレット**: プライマリ（青）、成功（緑）、警告（オレンジ）、危険（赤）、アクセント（紫）
- **アニメーション**: ページ遷移、フェードイン、スライドイン、ホバーエフェクト
- **レスポンシブ**: モバイル、タブレット、デスクトップ対応
- **コンポーネント**: カード、ボタン、入力フィールドの統一スタイル

### 主要ページ
- **ホーム**: 銘柄検索、企業情報、財務グラフ、チャットボット
- **ポートフォリオ**: 保有銘柄一覧、パフォーマンスサマリー
- **比較**: 複数資産のパフォーマンス比較グラフ

## 🧪 テスト

### フロントエンド

```bash
cd frontend
npm test
npm run test:e2e  # Playwrightテスト
```

### バックエンド

```bash
cd backend
pytest
```

## 🛣 ロードマップ

- [x] Phase 1: 環境構築・基盤開発
- [x] Phase 2: コア機能開発
- [x] Phase 3: ビジュアル決算機能
- [x] Phase 4: RAGチャットボット
- [x] Phase 5: ポートフォリオ機能
- [x] Phase 6: 複数資産比較機能
- [x] Phase 7: 自動更新・最適化
- [x] Phase 8: UI/UX改善・テスト
  - [x] デザイン統一とアニメーション
  - [x] レスポンシブ対応
  - [ ] E2Eテスト（今後実装予定）
  - [x] ドキュメント整備

詳細は[TODO.md](./TODO.md)を参照してください。

## 🤝 コントリビューション

現在、このプロジェクトは個人開発中です。将来的にコントリビューションを受け付ける予定です。

## 📄 ライセンス

TBD

## 📞 お問い合わせ

GitHub Issues: https://github.com/koshiro-y-0/a1-pro/issues

---

**開発開始日**: 2026-01-24
