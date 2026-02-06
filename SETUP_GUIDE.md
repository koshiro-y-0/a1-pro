# A1-PRO EC2セットアップガイド

## 📋 あなたのEC2情報

- **パブリックIP**: `15.134.206.23`
- **アクセスURL**: http://15.134.206.23

## 🚀 セットアップ手順

### Step 1: SSH接続の準備

#### 1.1 キーペアの確認

EC2インスタンス作成時にダウンロードしたキーペア（.pemファイル）を準備してください。

**キーペアの場所を確認:**
```bash
# キーペアファイルを見つける（例: Downloads フォルダ）
ls ~/Downloads/*.pem
```

**キーペアのパーミッション設定:**
```bash
# キーペアファイルのパーミッションを変更
chmod 400 ~/Downloads/your-key.pem
```

#### 1.2 EC2に接続

**Amazon Linux 2023の場合:**
```bash
ssh -i ~/Downloads/your-key.pem ec2-user@15.134.206.23
```

**Ubuntu 22.04の場合:**
```bash
ssh -i ~/Downloads/your-key.pem ubuntu@15.134.206.23
```

⚠️ **接続できない場合:**
- セキュリティグループでポート22（SSH）が開いているか確認
- キーペアファイルのパスが正しいか確認
- EC2インスタンスが起動中か確認

---

### Step 2: EC2上でセットアップスクリプトを実行

EC2に接続できたら、以下のコマンドを実行:

```bash
# リポジトリのクローン
git clone https://github.com/koshiro-y-0/a1-pro.git
cd a1-pro

# セットアップスクリプトを実行
chmod +x scripts/ec2-setup.sh
./scripts/ec2-setup.sh
```

**スクリプトが実行すること:**
1. Docker & Docker Composeのインストール
2. Gitのインストール
3. リポジトリのクローン
4. .envファイルのテンプレート作成
5. Ollama のインストール（オプション）

**Ollama のインストール:**
- RAGチャットボット機能を使う場合: `y` を入力
- 使わない場合: `n` を入力

---

### Step 3: 環境変数の設定

`.env`ファイルを編集してAPIキーやパスワードを設定:

```bash
cd ~/a1-pro
nano .env
```

**編集内容:**
```env
# Database Configuration
MYSQL_ROOT_PASSWORD=your_secure_root_password_here
MYSQL_PASSWORD=your_secure_password_here

# API Keys
BUFFETT_CODE_API_KEY=your_buffett_code_api_key_here
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key_here

# Ollama Configuration (変更不要)
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1:8b

# Frontend Configuration (変更不要)
NEXT_PUBLIC_API_URL=http://localhost/api
```

**保存方法（nano エディタ）:**
- 編集が終わったら: `Ctrl + O` → `Enter` (保存)
- 終了: `Ctrl + X`

---

### Step 4: アプリケーションの起動

```bash
cd ~/a1-pro

# Docker Composeでビルド・起動
docker-compose up -d --build

# 起動確認
docker-compose ps
```

**成功すると以下のコンテナが起動します:**
- a1pro-mysql (MySQL データベース)
- a1pro-chromadb (ベクトルDB)
- a1pro-backend (FastAPI バックエンド)
- a1pro-frontend (Next.js フロントエンド)
- a1pro-nginx (リバースプロキシ)

---

### Step 5: データベースの初期化

```bash
# データベースマイグレーションを実行
docker-compose exec backend alembic upgrade head

# サンプルデータの投入（オプション）
docker-compose exec backend python scripts/add_sample_financials.py
```

---

### Step 6: 動作確認

#### 6.1 ログ確認

```bash
# 全体のログを確認
docker-compose logs -f

# 特定のサービスのログ
docker-compose logs -f backend
docker-compose logs -f frontend
```

#### 6.2 ヘルスチェック

```bash
# ヘルスチェック
curl http://localhost/health

# または
curl http://15.134.206.23/health
```

`healthy` と表示されればOK！

#### 6.3 ブラウザでアクセス

ブラウザで以下のURLを開く:
```
http://15.134.206.23
```

A1-PROアプリケーションが表示されれば成功！🎉

---

### Step 7: GitHub Actions の設定

自動デプロイを有効にするため、GitHub Secretsを設定します。

#### 7.1 GitHubリポジトリにアクセス

https://github.com/koshiro-y-0/a1-pro

#### 7.2 Secrets の設定

**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

以下のSecretsを追加:

| Secret名 | 値 | 説明 |
|---------|-----|------|
| `EC2_HOST` | `15.134.206.23` | EC2のパブリックIP |
| `EC2_USER` | `ec2-user` または `ubuntu` | SSH接続ユーザー名 |
| `EC2_SSH_KEY` | `.pem`ファイルの内容 | EC2の秘密鍵（全文） |
| `MYSQL_ROOT_PASSWORD` | Step 3で設定した値 | MySQLルートパスワード |
| `MYSQL_PASSWORD` | Step 3で設定した値 | MySQLユーザーパスワード |
| `BUFFETT_CODE_API_KEY` | Step 3で設定した値 | バフェット・コードAPIキー |
| `EXCHANGE_RATE_API_KEY` | Step 3で設定した値 | 為替APIキー |

**`EC2_SSH_KEY` の取得方法:**
```bash
# ローカルマシンで実行
cat ~/Downloads/your-key.pem
```

表示された内容全体（`-----BEGIN RSA PRIVATE KEY-----` から `-----END RSA PRIVATE KEY-----` まで）をコピーして貼り付け。

---

### Step 8: 自動デプロイのテスト

GitHub Secretsを設定したら、自動デプロイをテスト:

```bash
# ローカルマシンで実行
cd /path/to/local/a1-pro

# ダミーの変更をコミット
git commit --allow-empty -m "Test auto-deploy"
git push origin main
```

**GitHub Actionsで確認:**
1. https://github.com/koshiro-y-0/a1-pro/actions にアクセス
2. 「Deploy to EC2」ワークフローが実行されているか確認
3. 緑のチェックマークが表示されれば成功！

---

## 🎯 完了チェックリスト

- [ ] EC2にSSH接続できる
- [ ] セットアップスクリプトを実行した
- [ ] `.env`ファイルを編集した
- [ ] Docker Composeでコンテナを起動した
- [ ] データベースマイグレーションを実行した
- [ ] http://15.134.206.23 でアプリにアクセスできる
- [ ] GitHub Secretsを設定した
- [ ] 自動デプロイが動作する

---

## 🛠️ 管理コマンド

### コンテナの管理

```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# 再起動
docker-compose restart

# ログ確認
docker-compose logs -f [service_name]

# コンテナの状態確認
docker-compose ps
```

### アプリケーションの更新

```bash
# 最新コードを取得
cd ~/a1-pro
git pull origin main

# コンテナを再ビルド・再起動
docker-compose up -d --build

# マイグレーション実行
docker-compose exec backend alembic upgrade head
```

### データベース管理

```bash
# MySQLに接続
docker-compose exec mysql mysql -u a1pro_user -p a1pro

# バックアップ
docker-compose exec mysql mysqldump -u root -p a1pro > backup_$(date +%Y%m%d).sql

# リストア
docker-compose exec -T mysql mysql -u root -p a1pro < backup_YYYYMMDD.sql
```

---

## 🐛 トラブルシューティング

### コンテナが起動しない

```bash
# エラーログを確認
docker-compose logs

# 個別にビルド
docker-compose build backend
docker-compose up backend
```

### データベース接続エラー

```bash
# MySQLの状態確認
docker-compose exec mysql mysqladmin ping -h localhost

# MySQLのログ確認
docker-compose logs mysql
```

### ポートが使用中

```bash
# ポートを使用しているプロセスを確認
sudo lsof -i :80
sudo lsof -i :3000
sudo lsof -i :8000

# プロセスを停止
sudo kill -9 <PID>
```

### メモリ不足

```bash
# スワップを追加
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 永続化
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 📞 サポート

問題が発生した場合:
- **GitHub Issues**: https://github.com/koshiro-y-0/a1-pro/issues
- **ログを確認**: `docker-compose logs -f`

---

**最終更新**: 2026-02-06
**EC2 IP**: 15.134.206.23
