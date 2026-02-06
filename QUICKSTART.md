# A1-PRO クイックスタートガイド 🚀

**EC2 IP**: `15.134.206.23`

## 📝 必要な情報

以下の情報を準備してください:

- [ ] EC2のSSHキーペア（.pemファイル）
- [ ] MySQLパスワード（自分で決める）
- [ ] バフェット・コードAPIキー（https://www.buffett-code.com/api）
- [ ] 為替APIキー（https://www.exchangerate-api.com/）

---

## ⚡ 5ステップでデプロイ

### 1️⃣ EC2に接続

```bash
# キーペアのパーミッション設定
chmod 400 ~/Downloads/your-key.pem

# EC2に接続（Amazon Linuxの場合）
ssh -i ~/Downloads/your-key.pem ec2-user@15.134.206.23

# Ubuntuの場合
ssh -i ~/Downloads/your-key.pem ubuntu@15.134.206.23
```

---

### 2️⃣ セットアップスクリプトを実行

```bash
git clone https://github.com/koshiro-y-0/a1-pro.git
cd a1-pro
chmod +x scripts/ec2-setup.sh
./scripts/ec2-setup.sh
```

**質問が出たら:**
- Ollama をインストール？ → `y`（RAGチャットボット使う）または `n`（使わない）

---

### 3️⃣ 環境変数を設定

```bash
cd ~/a1-pro
nano .env
```

**以下を編集:**
```env
MYSQL_ROOT_PASSWORD=YourSecurePassword123
MYSQL_PASSWORD=YourSecurePassword456
BUFFETT_CODE_API_KEY=your_actual_api_key
EXCHANGE_RATE_API_KEY=your_actual_api_key
```

**保存:** `Ctrl+O` → `Enter` → `Ctrl+X`

---

### 4️⃣ アプリを起動

```bash
cd ~/a1-pro

# ビルド＆起動
docker-compose up -d --build

# マイグレーション
docker-compose exec backend alembic upgrade head

# 状態確認
docker-compose ps
```

---

### 5️⃣ 動作確認

```bash
# ヘルスチェック
curl http://localhost/health

# ブラウザで開く
# http://15.134.206.23
```

---

## 🔧 GitHub Secrets設定（自動デプロイ用）

https://github.com/koshiro-y-0/a1-pro/settings/secrets/actions

**追加するSecrets:**

```
EC2_HOST = 15.134.206.23
EC2_USER = ec2-user  (または ubuntu)
EC2_SSH_KEY = (cat ~/Downloads/your-key.pem の内容全体)
MYSQL_ROOT_PASSWORD = (Step 3で設定した値)
MYSQL_PASSWORD = (Step 3で設定した値)
BUFFETT_CODE_API_KEY = (Step 3で設定した値)
EXCHANGE_RATE_API_KEY = (Step 3で設定した値)
```

---

## 🎉 完了！

✅ **アクセスURL**: http://15.134.206.23

✅ **今後の更新**: `git push origin main` で自動デプロイ

---

## 🆘 問題が発生したら

```bash
# ログ確認
docker-compose logs -f

# 再起動
docker-compose restart

# 完全リセット
docker-compose down
docker-compose up -d --build
```

詳細は `SETUP_GUIDE.md` を参照してください。
