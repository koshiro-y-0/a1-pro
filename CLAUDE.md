# A1-PRO - 日本株分析Webアプリケーションプロジェクト仕様書

## プロジェクト概要

日本株の個別銘柄を分析するためのWebアプリケーション。銘柄コードを入力することで、ビジュアル化された決算情報、詳細な企業情報を閲覧でき、ローカルLLMを活用したRAGチャットボットによる質問応答機能を提供する。

## 目的

- 投資判断に必要な財務情報を視覚的に分かりやすく表示
- 複数資産クラスのパフォーマンス比較機能
- AI チャットボットによる柔軟な情報取得
- 個人の投資ポートフォリオ管理

---

## 技術スタック

### フロントエンド
- **フレームワーク**: Next.js (App Router)
- **言語**: TypeScript
- **スタイリング**: Tailwind CSS
- **グラフライブラリ**: Recharts または Chart.js
- **UIコンポーネント**: shadcn/ui (オプション)

### バックエンド
- **言語**: Python 3.11+
- **フレームワーク**: FastAPI
- **API構成**: RESTful API

### データベース
- **RDBMS**: MySQL 8.0+
- **ベクトルDB**: ChromaDB (RAG用)
- **ORM**: SQLAlchemy (Python側)

### AI/RAG システム
- **LLM**: Ollama (Llama 3.1 8B)
- **RAGフレームワーク**: LangChain
- **ベクトルDB**: ChromaDB
- **エンベディング**: all-MiniLM-L6-v2 (HuggingFace)

### 外部API
- **株価データ**: yfinance (Yahoo Finance非公式API)
- **決算データ**: バフェット・コードAPI (無料プラン: 月500リクエスト)
- **米国株**: yfinance
- **為替**: exchangerate-api (無料プラン)
- **暗号資産**: CoinGecko API (無料)

### インフラ・環境
- **開発環境**: ローカル (macOS - M1 Mac 8GB)
- **コンテナ**: Docker & Docker Compose
- **デプロイ**: 将来的に検討 (現時点ではローカル開発優先)

---

## システム構成

```
a1-pro/
├── frontend/          # Next.js アプリケーション
│   ├── src/
│   │   ├── app/      # App Router
│   │   ├── components/
│   │   ├── lib/
│   │   └── types/
│   └── package.json
│
├── backend/           # FastAPI アプリケーション
│   ├── app/
│   │   ├── api/      # APIエンドポイント
│   │   ├── models/   # データモデル
│   │   ├── services/ # ビジネスロジック
│   │   ├── db/       # データベース設定
│   │   └── rag/      # RAGシステム
│   ├── requirements.txt
│   └── main.py
│
├── docker-compose.yml
├── .env.example
├── CLAUDE.md
└── README.md
```

---

## 主要機能

### 1. 銘柄検索・表示機能

#### 1.1 銘柄検索
- **銘柄コード入力**: 4桁の銘柄コード (例: 7203 - トヨタ自動車)
- **銘柄名検索**: 企業名での部分一致検索
- **サジェスト機能**: 入力中に候補を表示

#### 1.2 企業情報表示
以下の情報を表示：
- 企業概要 (会社名、業種、設立年、本社所在地など)
- 事業内容
- 最新ニュース (外部API連携またはスクレイピング)
- アナリスト評価 (取得可能な場合)

### 2. ビジュアル決算機能

#### 2.1 財務指標グラフ
以下のグラフを表示（過去5〜10年分）：
- **売上高推移**: 折れ線グラフ (青系)
- **営業利益推移**: 折れ線グラフ (緑系)
- **純利益推移**: 折れ線グラフ (オレンジ系)
- **複合グラフ**: 売上高 + 経常利益 + 株価を1つのグラフに表示
  - 左軸: 売上高・経常利益 (棒グラフ)
  - 右軸: 株価 (折れ線グラフ)

#### 2.2 財務健全性指標
以下の指標を表示し、健全性を判定：
- **自己資本比率**: 40%以上で健全 (緑)、20〜40%で注意 (黄)、20%未満で危険 (赤)
- **流動比率**: 150%以上で健全
- **負債比率**: 低いほど健全
- **ROE (自己資本利益率)**: 高いほど良好
- **営業利益率**: 業種平均と比較

#### 2.3 株価チャート
- **期間選択**: 1週間、1ヶ月、3ヶ月、6ヶ月、1年、5年
- **ローソク足チャート**: 日足表示
- **移動平均線**: 25日、75日、200日 (異なる色で表示)
- **出来高**: チャート下部に表示

**グラフの色分けルール**:
- 各指標ごとに明確に色を分ける
- 売上高: 青 (#3B82F6)
- 営業利益: 緑 (#10B981)
- 純利益: オレンジ (#F59E0B)
- 経常利益: 紫 (#8B5CF6)
- 株価: 濃い青 (#1E40AF)
- プラス値: 緑系、マイナス値: 赤系

### 3. RAG チャットボット機能

#### 3.1 RAGシステム
- **データソース**:
  - 取得した決算データ
  - 企業情報
  - ニュース記事
  - 財務諸表 (PDF等をパース)
- **ベクトル化**: 企業情報・決算データをベクトルDBに保存
- **検索**: ユーザーの質問に関連する情報を検索
- **回答生成**: Ollama (Llama 3.1 8B) で自然言語回答を生成

#### 3.2 対応する質問例
- 「この企業の直近の売上高は？」
- 「営業利益率の推移を教えて」
- 「財務状況は健全？」
- 「競合他社と比較してどう？」
- 「最新のニュースは？」

#### 3.3 チャット UI
- チャット形式のインターフェース
- 質問履歴の保存
- ソース情報の表示 (どのデータから回答したか)

### 4. ポートフォリオ管理機能

#### 4.1 保有銘柄登録
以下の情報を入力・保存：
- 銘柄コード
- 購入日
- 購入価格
- 購入数量
- 資産クラス (日本株、米国株、為替、暗号資産など)

#### 4.2 パフォーマンス計算
- **個別銘柄のパフォーマンス**:
  - 購入価格からの騰落率 (%)
  - 損益金額
  - 現在の評価額
- **ポートフォリオ全体**:
  - 総投資額
  - 現在の総評価額
  - 総損益 (金額・%)

#### 4.3 お気に入り機能
- 銘柄をお気に入りに追加
- お気に入りリストから素早くアクセス
- お気に入り銘柄の一覧表示

### 5. 複数資産パフォーマンス比較機能

#### 5.1 対応資産クラス
- **日本株**: 個別銘柄、日経平均、TOPIX
- **米国株**: 個別銘柄、S&P500、NASDAQ
- **為替**: USD/JPY, EUR/JPY など
- **暗号資産**: BTC, ETH など
- **商品**: 将来的に検討 (無料APIが見つかれば)
- **不動産**: 将来的に検討 (データソース次第)

#### 5.2 比較機能
- **基準日設定**: 任意の日付を起点に設定
- **複数資産選択**: 最大10銘柄まで同時比較
- **正規化グラフ**: 基準日を100として相対パフォーマンスを表示
- **色分け**: 各資産ごとに異なる色でライン表示

#### 5.3 表示情報
- パフォーマンスランキング
- 騰落率 (%)
- 最大ドローダウン
- ボラティリティ

---

## データ取得・更新戦略

### 株価データ (15分遅延)
- **取得方法**: yfinance (Yahoo Finance非公式API)
- **更新頻度**: ユーザーがページを開いた際にリアルタイム取得
- **キャッシュ**: 15分間キャッシュして、API負荷を軽減

### 決算データ (定期自動取得)
- **取得方法**: バフェット・コードAPI (月500リクエスト制限)
- **更新頻度**: 1日1回、深夜3時に自動実行 (cron or APScheduler)
- **対象**: お気に入り登録銘柄 + 直近閲覧された銘柄 (優先順位付け)

### 企業情報・ニュース
- **取得方法**:
  - バフェット・コードAPI
  - スクレイピング (robots.txt遵守)
- **更新頻度**: 週1回程度

### 為替・暗号資産データ
- **取得方法**:
  - 為替: exchangerate-api
  - 暗号資産: CoinGecko API
- **更新頻度**: 1時間に1回程度

---

## データベース設計 (主要テーブル)

### 1. companies (企業マスタ)
| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT (PK) | 企業ID |
| stock_code | VARCHAR(10) (UNIQUE) | 銘柄コード |
| name | VARCHAR(255) | 企業名 |
| industry | VARCHAR(100) | 業種 |
| description | TEXT | 事業内容 |
| created_at | DATETIME | 作成日時 |
| updated_at | DATETIME | 更新日時 |

### 2. financial_data (決算データ)
| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT (PK) | ID |
| company_id | INT (FK) | 企業ID |
| fiscal_year | INT | 会計年度 |
| fiscal_quarter | INT | 四半期 (1-4, nullで通期) |
| revenue | BIGINT | 売上高 |
| operating_profit | BIGINT | 営業利益 |
| ordinary_profit | BIGINT | 経常利益 |
| net_profit | BIGINT | 純利益 |
| total_assets | BIGINT | 総資産 |
| equity | BIGINT | 自己資本 |
| created_at | DATETIME | 作成日時 |

### 3. stock_prices (株価データ)
| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT (PK) | ID |
| company_id | INT (FK) | 企業ID |
| date | DATE | 日付 |
| open | DECIMAL(10,2) | 始値 |
| high | DECIMAL(10,2) | 高値 |
| low | DECIMAL(10,2) | 安値 |
| close | DECIMAL(10,2) | 終値 |
| volume | BIGINT | 出来高 |

### 4. portfolio (ポートフォリオ)
| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT (PK) | ID |
| asset_type | VARCHAR(50) | 資産クラス (jp_stock, us_stock, crypto, fx) |
| symbol | VARCHAR(20) | 銘柄コード/シンボル |
| purchase_date | DATE | 購入日 |
| purchase_price | DECIMAL(15,2) | 購入価格 |
| quantity | DECIMAL(15,4) | 数量 |
| created_at | DATETIME | 作成日時 |

### 5. favorites (お気に入り)
| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT (PK) | ID |
| company_id | INT (FK) | 企業ID |
| created_at | DATETIME | 作成日時 |

---

## API エンドポイント設計

### 企業・銘柄関連
- `GET /api/companies/search?q={query}` - 銘柄検索
- `GET /api/companies/{stock_code}` - 企業詳細取得
- `GET /api/companies/{stock_code}/financials` - 決算データ取得
- `GET /api/companies/{stock_code}/stock-prices?period={period}` - 株価データ取得

### ポートフォリオ関連
- `GET /api/portfolio` - ポートフォリオ一覧
- `POST /api/portfolio` - 保有銘柄追加
- `PUT /api/portfolio/{id}` - 保有銘柄更新
- `DELETE /api/portfolio/{id}` - 保有銘柄削除
- `GET /api/portfolio/performance` - パフォーマンス計算

### お気に入り関連
- `GET /api/favorites` - お気に入り一覧
- `POST /api/favorites` - お気に入り追加
- `DELETE /api/favorites/{id}` - お気に入り削除

### 比較機能関連
- `POST /api/compare` - 複数資産のパフォーマンス比較
  - Request Body: `{ symbols: ["7203", "AAPL", "BTC-USD"], start_date: "2023-01-01" }`

### RAG チャットボット関連
- `POST /api/chat` - チャット質問送信
  - Request Body: `{ question: "トヨタの売上高は?", context: "7203" }`
- `GET /api/chat/history` - チャット履歴取得

### データ更新関連
- `POST /api/admin/update-financials` - 決算データ手動更新
- `POST /api/admin/update-stock-prices` - 株価データ手動更新

---

## RAGシステム詳細設計

### アーキテクチャ
```
ユーザー質問
    ↓
LangChain (質問をベクトル化)
    ↓
ChromaDB (類似ベクトル検索)
    ↓
関連データ取得 (決算データ、企業情報など)
    ↓
Ollama Llama 3.1 (プロンプト + コンテキスト)
    ↓
回答生成
```

### データのベクトル化
以下のデータをChromaDBに保存：
- 企業概要テキスト
- 決算短信のテキスト (パース後)
- ニュース記事
- 財務指標とその説明

### プロンプト設計
```
あなたは日本株の財務アナリストです。以下の情報を元に、ユーザーの質問に答えてください。

【企業情報】
{company_info}

【財務データ】
{financial_data}

【質問】
{user_question}

【回答ルール】
- 数値は正確に引用すること
- 情報源を明示すること
- 不明な場合は「データがありません」と答えること
```

### Ollama セットアップ
- モデル: `llama3.1:8b`
- メモリ: 4-6GB使用想定
- 推論速度: M1 Mac 8GBで実用的な速度

---

## UI/UXデザイン方針

### デザインコンセプト
- **シンプル & ビジネスライク**: 情報が見やすく、プロフェッショナルな印象
- **明るい色調**: 白ベース + 青系のアクセントカラー
- **データ視覚化重視**: グラフが主役、テキストは補助的に

### カラーパレット
- **ベース**: 白 (#FFFFFF), ライトグレー (#F3F4F6)
- **プライマリ**: 青 (#3B82F6)
- **アクセント**:
  - 成功/上昇: 緑 (#10B981)
  - 警告: 黄 (#F59E0B)
  - 危険/下落: 赤 (#EF4444)
- **グラフカラー**:
  - 売上高: #3B82F6 (青)
  - 営業利益: #10B981 (緑)
  - 純利益: #F59E0B (オレンジ)
  - 経常利益: #8B5CF6 (紫)
  - 株価: #1E40AF (濃い青)

### レイアウト
- **ヘッダー**: ロゴ + 検索バー + ナビゲーション
- **サイドバー**: お気に入りリスト、ポートフォリオ概要
- **メインエリア**:
  - 企業情報カード
  - 財務グラフエリア (2-3カラムレイアウト)
  - チャットボット (右下固定 or モーダル)
- **レスポンシブ対応**: モバイルでも利用可能

### フォント
- **見出し**: Inter, sans-serif (Bold)
- **本文**: Inter, sans-serif (Regular)
- **数値**: Roboto Mono, monospace

---

## 開発フェーズ

### Phase 1: 環境構築・基盤開発 (Week 1-2)
- [ ] プロジェクト構成作成
- [ ] Docker環境構築 (MySQL, ChromaDB)
- [ ] Next.js + FastAPI の初期セットアップ
- [ ] データベース設計・マイグレーション
- [ ] Ollama + LangChain セットアップ

### Phase 2: コア機能開発 (Week 3-5)
- [ ] 銘柄検索機能
- [ ] 企業情報表示
- [ ] 株価データ取得・表示
- [ ] 決算データ取得・表示
- [ ] 基本的なグラフ表示 (売上高、利益、株価)

### Phase 3: ビジュアル決算機能 (Week 6-7)
- [ ] 財務指標グラフの実装
- [ ] 複合グラフ (売上高+経常利益+株価)
- [ ] 財務健全性判定ロジック
- [ ] グラフの色分け・インタラクティブ機能

### Phase 4: RAGチャットボット (Week 8-9)
- [ ] ChromaDBへのデータ投入
- [ ] LangChain RAGパイプライン構築
- [ ] Ollama統合
- [ ] チャットUI実装
- [ ] 質問-回答フローのテスト

### Phase 5: ポートフォリオ機能 (Week 10-11)
- [ ] 保有銘柄登録機能
- [ ] パフォーマンス計算ロジック
- [ ] お気に入り機能
- [ ] ポートフォリオダッシュボード

### Phase 6: 複数資産比較機能 (Week 12-13)
- [ ] 米国株データ取得
- [ ] 為替データ取得
- [ ] 暗号資産データ取得
- [ ] 複数資産比較グラフ
- [ ] パフォーマンス計算・ランキング

### Phase 7: 自動更新・最適化 (Week 14-15)
- [ ] 決算データ自動取得 (スケジューラー)
- [ ] キャッシュ機構
- [ ] パフォーマンス最適化
- [ ] エラーハンドリング強化

### Phase 8: UI/UX改善・テスト (Week 16)
- [ ] デザイン調整
- [ ] レスポンシブ対応
- [ ] E2Eテスト
- [ ] ドキュメント整備

---

## 将来的な拡張機能 (Phase 9以降)

### ユーザー認証・管理
- [ ] ログイン・ログアウト機能
- [ ] ユーザーごとのポートフォリオ管理
- [ ] マルチユーザー対応

### 高度な分析機能
- [ ] テクニカル指標 (RSI, MACD, ボリンジャーバンドなど)
- [ ] スクリーニング機能 (条件検索)
- [ ] アラート機能 (株価通知など)

### レポート機能
- [ ] PDF レポート出力
- [ ] Excelエクスポート
- [ ] 月次レポート自動生成

### デプロイ・公開
- [ ] クラウドデプロイ (AWS, GCP, またはVercel + Railway)
- [ ] CI/CDパイプライン
- [ ] モニタリング・ログ収集

### データソース拡充
- [ ] 商品データ (金、原油など) - 無料API調査
- [ ] 不動産データ - データソース調査
- [ ] より詳細な決算情報 (EDINET完全対応)

---

## 技術的な注意事項

### M1 Mac 8GB での最適化
- **Ollamaメモリ設定**: `OLLAMA_NUM_GPU=1`, `OLLAMA_MAX_LOADED_MODELS=1`
- **ChromaDB**: ディスク永続化モード (メモリ節約)
- **MySQLメモリ設定**: innodb_buffer_pool_size を 256MB程度に制限

### API レート制限対策
- **バフェット・コード**: 月500リクエスト → 1日約16銘柄まで更新可能
- **yfinance**: 非公式のため、過度なアクセスを避ける (キャッシュ活用)
- **CoinGecko**: 無料プランは50リクエスト/分

### データ整合性
- トランザクション管理を徹底
- 外部API障害時のフォールバック処理
- データ取得失敗時のリトライロジック

### セキュリティ
- APIキーは `.env` で管理 (Git管理外)
- SQLインジェクション対策 (ORMの適切な使用)
- CORS設定

---

## 開発環境セットアップ手順

### 1. 必要なツールのインストール
```bash
# Homebrewでインストール
brew install node
brew install python@3.11
brew install mysql
brew install ollama

# Ollama Llama 3.1 のダウンロード
ollama pull llama3.1:8b
```

### 2. プロジェクトのクローン
```bash
git clone https://github.com/koshiro-y-0/a1-pro.git
cd a1-pro
```

### 3. フロントエンドのセットアップ
```bash
cd frontend
npm install
cp .env.example .env.local
# .env.local に必要な環境変数を設定
npm run dev
```

### 4. バックエンドのセットアップ
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env に必要な環境変数を設定
uvicorn main:app --reload
```

### 5. データベースのセットアップ
```bash
# MySQLを起動
brew services start mysql

# データベース作成
mysql -u root -p
CREATE DATABASE a1pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'a1pro_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON a1pro.* TO 'a1pro_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# マイグレーション実行
cd backend
alembic upgrade head
```

### 6. Docker Compose (推奨)
```bash
# プロジェクトルートで実行
docker-compose up -d
```

---

## 環境変数一覧

### フロントエンド (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### バックエンド (.env)
```
# Database
DATABASE_URL=mysql+pymysql://a1pro_user:your_password@localhost:3306/a1pro

# External APIs
BUFFETT_CODE_API_KEY=your_buffett_code_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./data/chromadb

# Scheduler
UPDATE_SCHEDULE_HOUR=3
UPDATE_SCHEDULE_MINUTE=0
```

---

## テスト戦略

### フロントエンド
- **Unit Test**: Jest + React Testing Library
- **E2E Test**: Playwright

### バックエンド
- **Unit Test**: pytest
- **API Test**: pytest + httpx
- **RAG Test**: LangChain評価フレームワーク

---

## パフォーマンス目標

- **ページ読み込み**: 3秒以内
- **グラフ描画**: 1秒以内
- **チャットボット応答**: 5秒以内 (Ollama推論時間含む)
- **API応答時間**: 500ms以内 (キャッシュ有効時)

---

## ドキュメント管理

- **CLAUDE.md**: 本仕様書 (プロジェクト全体の設計)
- **README.md**: プロジェクト概要、セットアップ手順
- **API.md**: API仕様書 (エンドポイント詳細)
- **CONTRIBUTING.md**: 開発ガイドライン (将来的に)

---

## リスク管理

### 技術的リスク
| リスク | 対策 |
|-------|------|
| Ollamaのメモリ不足 | 軽量モデル使用、不要時にアンロード |
| API制限超過 | キャッシュ強化、優先度付けロジック |
| データ取得エラー | リトライ機構、フォールバック処理 |
| M1互換性問題 | Docker利用、ARM対応ライブラリ選定 |

### データリスク
| リスク | 対策 |
|-------|------|
| API仕様変更 | アダプターパターンで抽象化 |
| データ品質問題 | バリデーション強化、異常値検出 |
| ストレージ不足 | 古いデータの定期削除、圧縮 |

---

## 成功指標 (KPI)

- [ ] 100銘柄以上のデータ取得・表示
- [ ] チャットボット回答精度 80%以上
- [ ] グラフ表示の正確性 100%
- [ ] システムアップタイム 95%以上 (ローカル稼働時)
- [ ] ページ読み込み時間 3秒以内

---

## 参考資料・リンク

### API ドキュメント
- [バフェット・コードAPI](https://www.buffett-code.com/api)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [exchangerate-api](https://www.exchangerate-api.com/)

### 技術ドキュメント
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)

### デザイン参考
- [Yahoo! Finance](https://finance.yahoo.co.jp/)
- [Bloomberg](https://www.bloomberg.co.jp/)
- [TradingView](https://www.tradingview.com/)

---

## バージョン履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0.0 | 2026-01-24 | 初版作成 |

---

## ライセンス

TBD (プロジェクト公開時に決定)

---

## お問い合わせ

GitHub Issues: https://github.com/koshiro-y-0/a1-pro/issues

---

**Document END**
