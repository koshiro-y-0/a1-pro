---
name: aws-fullstack-deploy
description: AWS EC2へのフルスタックWebアプリデプロイスキル。Docker Compose、GitHub Actions CI/CD、HTTPS対応、Route 53ドメイン設定をサポート。バックエンドはPython(FastAPI/Flask)またはJava(Spring Boot)、フロントエンドはReact/Next.js/HTML+CSS+JSに対応。「AWSにデプロイ」「EC2にデプロイ」「本番環境を構築」「CI/CDを設定」などのリクエストで使用。
---

# AWS Fullstack Deploy Skill

EC2 + Docker Compose構成でフルスタックWebアプリを安全にデプロイする。

## アーキテクチャ概要

```
GitHub → GitHub Actions → EC2 (Docker Compose)
                            ├─ Nginx (リバースプロキシ + SSL)
                            ├─ Frontend (React/Next.js)
                            └─ Backend (Python/Java)
```

## デプロイ手順

### Phase 1: AWS初期設定

1. AWSアカウント作成（未作成の場合）
2. EC2インスタンス作成: `references/aws-setup.md` 参照
3. セキュリティグループ設定: 22(SSH), 80(HTTP), 443(HTTPS)のみ開放

### Phase 2: プロジェクト構成

ユーザーの技術スタックに応じてテンプレートを選択:

| バックエンド | フロントエンド | 使用テンプレート |
|-------------|---------------|-----------------|
| Python (FastAPI) | React/Next.js | `assets/python-react/` |
| Python (Flask) | HTML/CSS/JS | `assets/python-static/` |
| Java (Spring Boot) | React/Next.js | `assets/java-react/` |

### Phase 3: ファイル配置

プロジェクトルートに以下を配置:

```
project/
├── docker-compose.yml      # assets/から選択
├── nginx/
│   └── nginx.conf          # assets/nginx/nginx.conf
├── .github/
│   └── workflows/
│       └── deploy.yml      # assets/github-actions/deploy.yml
├── frontend/               # ユーザーのフロントエンド
└── backend/                # ユーザーのバックエンド
```

### Phase 4: EC2セットアップ

EC2にSSH接続後、`scripts/ec2-setup.sh` を実行:

```bash
chmod +x ec2-setup.sh && ./ec2-setup.sh
```

### Phase 5: GitHub Actions設定

1. GitHubリポジトリの Settings → Secrets and variables → Actions に追加:
   - `EC2_HOST`: EC2のパブリックIP or ドメイン
   - `EC2_USER`: `ec2-user`(Amazon Linux) または `ubuntu`(Ubuntu)
   - `EC2_SSH_KEY`: EC2の秘密鍵（.pemファイルの中身）

2. `assets/github-actions/deploy.yml` を `.github/workflows/` にコピー

### Phase 6: HTTPS設定（Let's Encrypt）

ドメインがある場合、EC2上で実行:

```bash
chmod +x ssl-setup.sh && sudo ./ssl-setup.sh your-domain.com
```

### Phase 7: ドメイン設定

**Route 53（有料 年間$12〜）**: `references/route53-setup.md` 参照

**無料代替案**:
- IPアドレス直接: `http://YOUR_EC2_IP`
- nip.io: `http://YOUR_EC2_IP.nip.io`（設定不要の無料DNS）

## セキュリティチェックリスト

- [ ] SSHパスワード認証を無効化
- [ ] セキュリティグループで必要ポートのみ開放
- [ ] 環境変数でシークレット管理（.envはgitignore）
- [ ] HTTPS強制（HTTP→HTTPSリダイレクト）

## トラブルシューティング

`references/troubleshooting.md` 参照
