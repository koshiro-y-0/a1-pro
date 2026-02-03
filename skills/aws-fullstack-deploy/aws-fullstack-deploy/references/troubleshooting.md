# トラブルシューティング

## デプロイ関連

### GitHub Actions が失敗する

**SSH接続エラー**:
```
Permission denied (publickey)
```
→ `EC2_SSH_KEY` シークレットの改行が正しいか確認。.pemファイルの中身をそのままコピー。

**Host key verification failed**:
```bash
# EC2で実行
ssh-keyscan -H YOUR_EC2_IP
```
→ 出力を `known_hosts` に追加、または Actions で `StrictHostKeyChecking=no` を設定。

### docker-compose up が失敗する

**ポート競合**:
```bash
# 使用中のポートを確認
sudo lsof -i :80
sudo lsof -i :443

# 既存コンテナを停止
docker-compose down
docker stop $(docker ps -aq)
```

**ディスク容量不足**:
```bash
# Docker の不要リソースを削除
docker system prune -af
docker volume prune -f
```

## アプリケーション関連

### サイトにアクセスできない

1. **セキュリティグループ確認**:
   - 80, 443 ポートが開いているか
   - ソースが `0.0.0.0/0` か

2. **コンテナ状態確認**:
   ```bash
   docker-compose ps
   docker-compose logs nginx
   docker-compose logs backend
   docker-compose logs frontend
   ```

3. **EC2内部からの確認**:
   ```bash
   curl http://localhost
   curl http://localhost/api/health
   ```

### 502 Bad Gateway

```bash
# バックエンド/フロントエンドが起動しているか
docker-compose ps

# ログ確認
docker-compose logs backend
docker-compose logs frontend

# nginx設定の文法チェック
docker-compose exec nginx nginx -t
```

### コンテナが再起動を繰り返す

```bash
# 詳細ログを確認
docker-compose logs -f backend

# コンテナに入って調査
docker-compose exec backend sh
```

## SSL関連

### Let's Encrypt 証明書取得失敗

**ドメインが解決されない**:
```bash
# DNS確認
nslookup your-domain.com
```
→ ドメインが正しくEC2のIPを向いているか確認。

**80ポートが使用中**:
```bash
# 一時的にnginxを停止
docker stop nginx
sudo certbot certonly --standalone -d your-domain.com
```

### 証明書の更新

```bash
# 手動更新
sudo certbot renew

# 更新テスト
sudo certbot renew --dry-run
```

## パフォーマンス関連

### t2.micro のメモリ不足

```bash
# メモリ使用量確認
free -h

# スワップ追加（2GB）
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 永続化
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Docker ビルドが遅い

**マルチステージビルドの活用**:
- 本番用Dockerfileではビルドステージと実行ステージを分離

**レイヤーキャッシュの活用**:
- `package.json` や `requirements.txt` を先にコピー

## ログの確認方法

```bash
# 全コンテナのログ
docker-compose logs

# 特定コンテナのログ（リアルタイム）
docker-compose logs -f nginx

# 最新100行
docker-compose logs --tail=100 backend
```
