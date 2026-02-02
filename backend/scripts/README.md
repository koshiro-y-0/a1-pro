# Scripts - データ取得・管理スクリプト

このディレクトリには、A1-PROプロジェクトで使用するデータ取得・管理スクリプトが含まれています。

## スクリプト一覧

### 1. 銘柄データ管理

#### `import_csv_companies.py`
CSVファイルから銘柄データをインポートします。

```bash
# 使用方法
cd backend
source venv/bin/activate
python scripts/import_csv_companies.py
```

**入力**: `scripts/prime_companies.csv`
**出力**: データベースに銘柄を登録

#### `prime_companies.csv`
東証プライム市場の主要銘柄リスト（175社）

カラム:
- `stock_code`: 銘柄コード（4桁）
- `name`: 企業名
- `industry`: 業種

---

### 2. 決算データ取得

#### `fetch_financials_buffett.py`
バフェット・コードAPIを使用して決算データを自動取得します。

**API制限**: 月500リクエスト

```bash
# 使用方法
cd backend
source venv/bin/activate

# APIキーを環境変数に設定
export BUFFETT_CODE_API_KEY='your_api_key_here'

# スクリプト実行
python scripts/fetch_financials_buffett.py
```

**機能**:
- 決算データがない企業を自動検出
- バフェット・コードAPIから通期決算データを取得
- データベースに自動登録
- API制限対策（1秒/リクエスト）

**取得データ**:
- 売上高 (revenue)
- 営業利益 (operating_profit)
- 経常利益 (ordinary_profit)
- 純利益 (net_profit)
- 総資産 (total_assets)
- 自己資本 (equity)
- 総負債 (total_liabilities)
- 流動資産 (current_assets)
- 流動負債 (current_liabilities)

---

### 3. 銘柄リスト自動取得（開発中）

#### `fetch_prime_companies.py`
JPX（日本取引所グループ）から銘柄リストを自動取得します。

**現在の状態**: SSL証明書エラーのため使用不可
**代替手段**: `import_csv_companies.py` を使用

```bash
# 使用方法（将来用）
cd backend
source venv/bin/activate
python scripts/fetch_prime_companies.py
```

---

## セットアップ

### 必要な環境変数

```bash
# バフェット・コードAPIキー（決算データ取得用）
export BUFFETT_CODE_API_KEY='your_api_key_here'
```

### APIキーの取得方法

1. **バフェット・コードAPI**
   - URL: https://www.buffett-code.com/api
   - 無料プラン: 月500リクエスト
   - 登録: メールアドレスのみ

---

## 実行例

### 1. 銘柄データをインポート

```bash
cd backend
source venv/bin/activate
python scripts/import_csv_companies.py
```

**出力例**:
```
東証プライム銘柄のインポートを開始します...

CSVファイルを読み込み中: /path/to/prime_companies.csv
読み込んだ銘柄数: 175
100件登録完了...

登録完了:
  新規登録: 164件
  スキップ: 11件
  合計: 175件

完了しました！
```

### 2. 決算データを取得

```bash
cd backend
source venv/bin/activate
export BUFFETT_CODE_API_KEY='your_key'
python scripts/fetch_financials_buffett.py
```

**出力例**:
```
決算データ取得対象: 100社
API制限: 月500リクエスト

[1/100] 7203 トヨタ自動車
  ✓ 5年分のデータを登録
[2/100] 9984 ソフトバンクグループ
  ✓ 5年分のデータを登録
...

完了:
  成功: 95社
  失敗: 5社
  登録データ数: 475件
```

---

## トラブルシューティング

### SSL証明書エラー

```
[SSL: CERTIFICATE_VERIFY_FAILED]
```

**対処法**: CSVインポート方式を使用してください

### API制限エラー

```
Error 429: Too Many Requests
```

**対処法**: 月500リクエストの制限に達しています。翌月まで待つか、複数のAPIキーを使用してください。

### データベース接続エラー

```
sqlalchemy.exc.OperationalError
```

**対処法**:
1. MySQLが起動しているか確認: `mysql.server status`
2. データベースが存在するか確認: `mysql -u root -e "SHOW DATABASES;"`
3. 環境変数を確認: `.env` ファイルの `DATABASE_URL`

---

## 今後の拡張予定

- [ ] 東証スタンダード市場の銘柄追加
- [ ] 東証グロース市場の銘柄追加
- [ ] 株価データの自動取得（yfinance）
- [ ] スケジューラーによる定期実行
- [ ] 複数データソースの統合

---

## 参考リンク

- [バフェット・コードAPI](https://www.buffett-code.com/api)
- [JPX 日本取引所グループ](https://www.jpx.co.jp/)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
