# セットアップ手順

## 1. データベースのセットアップ

```bash
# MySQLにログイン
mysql -u root

# データベースとユーザーを作成
CREATE DATABASE IF NOT EXISTS a1pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'a1pro_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON a1pro.* TO 'a1pro_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 2. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成とアクティベート
python3 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# .envファイルの作成
cp .env.example .env
# .envファイルを編集してデータベース接続情報を設定

# テーブル作成
python << 'EOF'
from app.db.database import engine
from app.models.company import Base as CompanyBase
from app.models.financial_data import Base as FinancialBase
from app.models.stock_price import Base as StockPriceBase
from app.models.portfolio import Base as PortfolioBase
from app.models.favorite import Base as FavoriteBase

CompanyBase.metadata.create_all(bind=engine)
FinancialBase.metadata.create_all(bind=engine)
StockPriceBase.metadata.create_all(bind=engine)
PortfolioBase.metadata.create_all(bind=engine)
FavoriteBase.metadata.create_all(bind=engine)
print("Tables created!")
EOF

# サンプルデータの投入
python << 'EOF'
from app.db.database import SessionLocal
from app.models.company import Company

db = SessionLocal()
companies = [
    {"stock_code": "7203", "name": "トヨタ自動車", "industry": "輸送用機器"},
    {"stock_code": "9984", "name": "ソフトバンクグループ", "industry": "情報・通信業"},
    {"stock_code": "6758", "name": "ソニーグループ", "industry": "電気機器"},
    {"stock_code": "9433", "name": "KDDI", "industry": "情報・通信業"},
    {"stock_code": "8306", "name": "三菱UFJフィナンシャル・グループ", "industry": "銀行業"},
    {"stock_code": "6861", "name": "キーエンス", "industry": "電気機器"},
    {"stock_code": "7974", "name": "任天堂", "industry": "その他製品"},
    {"stock_code": "4063", "name": "信越化学工業", "industry": "化学"},
    {"stock_code": "6902", "name": "デンソー", "industry": "輸送用機器"},
    {"stock_code": "8035", "name": "東京エレクトロン", "industry": "電気機器"},
]
for company_data in companies:
    existing = db.query(Company).filter(Company.stock_code == company_data["stock_code"]).first()
    if not existing:
        company = Company(**company_data)
        db.add(company)
db.commit()
db.close()
print("Sample data added!")
EOF

# バックエンド起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 3. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# .env.localファイルの作成
cp .env.example .env.local
# 必要に応じて編集（デフォルトで http://localhost:8000 が設定されています）

# フロントエンド起動
npm run dev
```

## 4. アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

## トラブルシューティング

### データベース接続エラー

```bash
# データベースユーザーが存在するか確認
mysql -u a1pro_user -ppassword -e "SELECT 1;"

# テーブルが作成されているか確認
mysql -u a1pro_user -ppassword -e "USE a1pro; SHOW TABLES;"
```

### バックエンドエラー

```bash
# バックエンドのログを確認
tail -f backend.log

# 仮想環境が有効化されているか確認
which python  # venv内のpythonが表示されるはず
```

### フロントエンドエラー

```bash
# フロントエンドのログを確認
tail -f frontend.log

# .env.localファイルが存在するか確認
cat frontend/.env.local
```
