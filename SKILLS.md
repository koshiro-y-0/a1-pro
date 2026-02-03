# A1-PRO Claude Skills

このプロジェクトで使用可能なClaudeスキルの一覧です。

## 利用可能なスキル

### 1. universal-test
**ファイル**: `skills/universal-test.skill`

多言語対応のテスト自動化スキル。

#### 対応言語・フレームワーク
- **Python**: pytest
- **Java**: JUnit 5 + Mockito
- **JavaScript/TypeScript**: Jest/Vitest
- **React**: React Testing Library
- **E2E**: Playwright

#### 使用方法
以下のようなリクエストで自動的に起動：
- 「テストして」
- 「テストを書いて」
- 「テストコードを生成」
- 「TDDで開発」
- 「CIにテスト追加」

#### 機能
1. **言語自動検出**: プロジェクトの構成ファイル（`requirements.txt`, `pom.xml`, `package.json`など）から自動判定
2. **テスト環境セットアップ**: 適切な設定ファイルを自動生成
3. **テストコード生成**: Unit/Integration/E2Eテストを自動生成
4. **テスト実行**: カバレッジレポート付きでテスト実行
5. **CI/CD設定**: GitHub Actionsのワークフロー生成
6. **TDDワークフロー**: Red-Green-Refactorサイクルをサポート

#### ワークフロー
```
「テストして」
    ↓
言語自動検出
    ↓
┌─────────────────────────────────────┐
│ Python → pytest                      │
│ Java → JUnit 5 + Mockito            │
│ JavaScript/TypeScript → Jest/Vitest │
│ React → React Testing Library       │
│ E2E → Playwright                    │
└─────────────────────────────────────┘
    ↓
テスト生成 or 実行
```

---

### 2. aws-fullstack-deploy
**ファイル**: `skills/aws-fullstack-deploy.skill`

AWS EC2へのフルスタックWebアプリデプロイスキル。

#### 対応スタック
**バックエンド**:
- Python (FastAPI/Flask)
- Java (Spring Boot)

**フロントエンド**:
- React
- Next.js
- HTML + CSS + JavaScript

#### 使用方法
以下のようなリクエストで自動的に起動：
- 「AWSにデプロイ」
- 「EC2にデプロイ」
- 「本番環境を構築」
- 「CI/CDを設定」

#### 機能
1. **AWS初期設定**: EC2インスタンス作成・セキュリティグループ設定
2. **Docker構成**: Docker Composeでマルチコンテナ構成
3. **Nginx設定**: リバースプロキシ + SSL対応
4. **GitHub Actions**: 自動デプロイCI/CDパイプライン
5. **HTTPS対応**: Let's Encrypt無料SSL証明書
6. **ドメイン設定**: Route 53設定サポート

#### アーキテクチャ
```
GitHub → GitHub Actions → EC2 (Docker Compose)
                            ├─ Nginx (リバースプロキシ + SSL)
                            ├─ Frontend (React/Next.js)
                            └─ Backend (Python/Java)
```

#### デプロイ手順
1. **Phase 1**: AWS初期設定（EC2インスタンス作成）
2. **Phase 2**: プロジェクト構成選択（技術スタックに応じたテンプレート）
3. **Phase 3**: 設定ファイル配置（docker-compose.yml, nginx.conf等）
4. **Phase 4**: EC2セットアップ（Dockerインストール等）
5. **Phase 5**: GitHub Actions設定（Secretsの登録）
6. **Phase 6**: HTTPS設定（Let's Encrypt）
7. **Phase 7**: ドメイン設定（Route 53 or 無料代替）

#### セキュリティ
- SSHパスワード認証無効化
- 必要ポートのみ開放（22, 80, 443）
- 環境変数でシークレット管理
- HTTPS強制リダイレクト

---

## スキルの追加方法

```bash
# universal-testスキルを追加
claude skill add /Users/yamadakoshiro/Desktop/a1-pro/skills/universal-test.skill

# aws-fullstack-deployスキルを追加
claude skill add /Users/yamadakoshiro/Desktop/a1-pro/skills/aws-fullstack-deploy.skill
```

## スキル一覧確認

```bash
claude skill list
```

## スキルの削除

```bash
# スキル名で削除
claude skill remove universal-test
claude skill remove aws-fullstack-deploy
```

---

## 参考資料

### universal-test
- `skills/universal-test/universal-test/SKILL.md` - スキルの詳細仕様
- `skills/universal-test/universal-test/references/test-patterns.md` - テストパターン集
- `skills/universal-test/universal-test/references/tdd-workflow.md` - TDDワークフロー
- `skills/universal-test/universal-test/scripts/detect-stack.sh` - 言語検出スクリプト

### aws-fullstack-deploy
- `skills/aws-fullstack-deploy/aws-fullstack-deploy/SKILL.md` - スキルの詳細仕様
- `skills/aws-fullstack-deploy/aws-fullstack-deploy/references/aws-setup.md` - AWS初期設定
- `skills/aws-fullstack-deploy/aws-fullstack-deploy/references/troubleshooting.md` - トラブルシューティング
- `skills/aws-fullstack-deploy/aws-fullstack-deploy/references/route53-setup.md` - Route 53設定
- `skills/aws-fullstack-deploy/aws-fullstack-deploy/scripts/ec2-setup.sh` - EC2セットアップスクリプト
- `skills/aws-fullstack-deploy/aws-fullstack-deploy/scripts/ssl-setup.sh` - SSL設定スクリプト

---

**最終更新日**: 2026-02-03
