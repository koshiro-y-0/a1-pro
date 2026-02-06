# A1-PRO Deployment Guide

A1-PRO財務分析アプリケーションをAWS EC2にデプロイするためのガイドです。

## 📋 前提条件

- AWSアカウント
- GitHubアカウント
- 基本的なLinuxコマンドの知識

## 🚀 デプロイ手順

### Phase 1: AWS EC2インスタンス作成

#### 1.1 EC2インスタンスの立ち上げ

1. AWSマネジメントコンソールにログイン
2. EC2ダッシュボードに移動
3. **「インスタンスを起動」**をクリック

#### 1.2 インスタンス設定

**AMI選択:**
- Amazon Linux 2023 (推奨) または Ubuntu 22.04 LTS

**インスタンスタイプ:**
- `t3.medium` (2 vCPU, 4 GiB RAM) - 推奨
- `t3.small` (2 vCPU, 2 GiB RAM) - 最小構成

**ストレージ:**
- 30 GB gp3 (推奨)

**キーペア:**
- 新しいキーペアを作成し、`.pem`ファイルをダウンロード
- ファイル名: `a1pro-key.pem` (例)

**セキュリティグループ:**
新しいセキュリティグループを作成:

| タイプ | プロトコル | ポート範囲 | ソース | 説明 |
|--------|-----------|-----------|--------|------|
| SSH | TCP | 22 | 0.0.0.0/0 | SSH接続 |
| HTTP | TCP | 80 | 0.0.0.0/0 | Webアクセス |
| HTTPS | TCP | 443 | 0.0.0.0/0 | 暗号化Webアクセス |

⚠️ **セキュリティ注意**: 本番環境では、SSHアクセスを特定のIPアドレスに制限してください。

### Phase 2: EC2インスタンスへの接続

#### 2.1 SSH接続

```bash
# キーペアのパーミッション変更
chmod 400 a1pro-key.pem

# EC2に接続
ssh -i a1pro-key.pem ec2-user@<EC2のパブリックIP>
# Ubuntu の場合: ssh -i a1pro-key.pem ubuntu@<EC2のパブリックIP>
```

### Phase 3: EC2セットアップ

#### 3.1 セットアップスクリプトの実行

```bash
# リポジトリのクローン
git clone https://github.com/koshiro-y-0/a1-pro.git
cd a1-pro

# セットアップスクリプトの実行
chmod +x scripts/ec2-setup.sh
./scripts/ec2-setup.sh
```

このスクリプトは以下を自動的に実行します:
- Dockerのインストール
- Docker Composeのインストール
- Gitのインストール
- リポジトリのクローン
- Ollama のインストール (オプション)

#### 3.2 環境変数の設定

`.env`ファイルを編集:

```bash
nano ~/.a1-pro/.env
```

以下の値を設定:

```env
# Database Configuration
MYSQL_ROOT_PASSWORD=your_secure_root_password
MYSQL_PASSWORD=your_secure_password

# API Keys
BUFFETT_CODE_API_KEY=your_buffett_code_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key

# Ollama Configuration
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1:8b

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost/api
```

### Phase 4: アプリケーションの起動

#### 4.1 Docker Composeでビルド・起動

```bash
cd ~/a1-pro

# コンテナのビルド
docker-compose build

# コンテナの起動
docker-compose up -d

# 起動確認
docker-compose ps
```

#### 4.2 データベースマイグレーション

```bash
# マイグレーション実行
docker-compose exec backend alembic upgrade head
```

#### 4.3 動作確認

```bash
# ログ確認
docker-compose logs -f

# ヘルスチェック
curl http://localhost/health
```

ブラウザでアクセス:
```
http://<EC2のパブリックIP>
```

### Phase 5: GitHub Actions CI/CD設定

#### 5.1 GitHub Secretsの登録

GitHubリポジトリの **Settings** → **Secrets and variables** → **Actions** に移動し、以下を追加:

| Secret名 | 値 | 説明 |
|---------|-----|------|
| `EC2_HOST` | `54.123.45.67` | EC2のパブリックIP |
| `EC2_USER` | `ec2-user` | SSH接続ユーザー名 |
| `EC2_SSH_KEY` | `.pem`ファイルの内容 | EC2の秘密鍵全体 |
| `MYSQL_ROOT_PASSWORD` | `your_password` | MySQLルートパスワード |
| `MYSQL_PASSWORD` | `your_password` | MySQLユーザーパスワード |
| `BUFFETT_CODE_API_KEY` | `your_key` | バフェット・コードAPIキー |
| `EXCHANGE_RATE_API_KEY` | `your_key` | 為替APIキー |

#### 5.2 自動デプロイの確認

`main`ブランチにプッシュすると自動的にデプロイされます:

```bash
git add .
git commit -m "Update application"
git push origin main
```

GitHub Actionsの **Actions** タブで進行状況を確認できます。

### Phase 6 (オプション): HTTPS設定

#### 6.1 ドメイン設定

**無料オプション:**
- `http://<EC2のIP>.nip.io` - 設定不要のDNS

**有料オプション (推奨):**
- Route 53でドメインを購入 (年間$12〜)
- Aレコードを設定

#### 6.2 Let's Encrypt SSL証明書

ドメインがある場合:

```bash
cd ~/a1-pro

# SSL設定スクリプトの実行
sudo ./scripts/ssl-setup.sh your-domain.com
```

## 🔧 管理コマンド

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

# コンテナに入る
docker-compose exec [service_name] bash
```

### データベース管理

```bash
# MySQLに接続
docker-compose exec mysql mysql -u a1pro_user -p a1pro

# バックアップ
docker-compose exec mysql mysqldump -u root -p a1pro > backup.sql

# リストア
docker-compose exec -T mysql mysql -u root -p a1pro < backup.sql
```

### アプリケーション更新

```bash
# コードをプル
git pull origin main

# コンテナ再ビルド
docker-compose up -d --build

# マイグレーション実行
docker-compose exec backend alembic upgrade head
```

## 📊 モニタリング

### リソース使用状況

```bash
# システムリソース
docker stats

# ディスク使用量
docker system df

# コンテナステータス
docker-compose ps
```

### ログの確認

```bash
# 全サービスのログ
docker-compose logs -f

# 特定サービスのログ
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql

# エラーのみ
docker-compose logs | grep -i error
```

## 🛡️ セキュリティ

### 推奨設定

1. **SSHパスワード認証を無効化**
```bash
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no
sudo systemctl restart sshd
```

2. **ファイアウォール設定**
```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

3. **自動アップデート有効化**
```bash
# Amazon Linux
sudo yum install -y yum-cron
sudo systemctl enable yum-cron
sudo systemctl start yum-cron

# Ubuntu
sudo apt-get install unattended-upgrades
```

## 🐛 トラブルシューティング

### コンテナが起動しない

```bash
# ログ確認
docker-compose logs

# 個別にビルド
docker-compose build [service_name]
docker-compose up [service_name]
```

### データベース接続エラー

```bash
# MySQLの状態確認
docker-compose exec mysql mysqladmin ping

# 環境変数確認
docker-compose config
```

### メモリ不足

```bash
# スワップ追加
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 💰 コスト見積もり

### AWS料金 (東京リージョン)

**t3.medium (推奨):**
- EC2インスタンス: 約$30/月
- EBS (30GB): 約$3/月
- データ転送: 〜$5/月
- **合計: 約$38/月**

**t3.small (最小):**
- EC2インスタンス: 約$15/月
- EBS (30GB): 約$3/月
- **合計: 約$18/月**

**無料利用枠 (初年度):**
- t2.micro: 750時間/月 無料
- EBS 30GB: 無料

## 📚 参考資料

- [AWS EC2ドキュメント](https://docs.aws.amazon.com/ec2/)
- [Docker Composeドキュメント](https://docs.docker.com/compose/)
- [Let's Encryptドキュメント](https://letsencrypt.org/docs/)
- [GitHub Actionsドキュメント](https://docs.github.com/actions)

## ❓ サポート

問題が発生した場合:
- GitHub Issues: https://github.com/koshiro-y-0/a1-pro/issues
- プロジェクトREADME: https://github.com/koshiro-y-0/a1-pro

---

**最終更新**: 2026-02-06
