# AWS EC2 初期設定ガイド

## 1. EC2インスタンスの作成

### AWSコンソールでの操作

1. **EC2ダッシュボード** → 「インスタンスを起動」

2. **AMI選択**:
   - Amazon Linux 2023（推奨）または Ubuntu 22.04 LTS
   - 64-bit (x86)

3. **インスタンスタイプ**:
   - `t2.micro`（無料枠対象、1vCPU, 1GB RAM）
   - `t3.micro`（無料枠対象、2vCPU, 1GB RAM）※より高性能

4. **キーペア**:
   - 新規作成: RSA, .pem形式
   - ダウンロードして安全に保管（GitHub Secretsにも使用）

5. **ネットワーク設定**:
   - VPC: デフォルト
   - サブネット: 任意のAZ
   - パブリックIP自動割り当て: 有効

6. **セキュリティグループ**:
   ```
   タイプ        ポート   ソース
   SSH          22       自分のIP（または 0.0.0.0/0）
   HTTP         80       0.0.0.0/0
   HTTPS        443      0.0.0.0/0
   ```

7. **ストレージ**:
   - 8GB gp3（無料枠内）
   - 必要に応じて増量（30GBまで無料）

## 2. Elastic IP（固定IP）の設定

IPアドレスを固定したい場合:

1. EC2 → Elastic IP → 「Elastic IPアドレスを割り当てる」
2. 作成したIPを選択 → 「アクション」→「Elastic IPアドレスの関連付け」
3. 対象インスタンスを選択

**注意**: 未使用のElastic IPは課金されるため、インスタンス削除時は解放する。

## 3. SSH接続

```bash
# 権限設定
chmod 400 your-key.pem

# 接続（Amazon Linux）
ssh -i your-key.pem ec2-user@YOUR_PUBLIC_IP

# 接続（Ubuntu）
ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP
```

## 4. 無料枠の注意点

| リソース | 無料枠 | 超過時 |
|---------|--------|--------|
| EC2 t2.micro | 750時間/月 | 約$0.012/時間 |
| EBS | 30GB | 約$0.10/GB/月 |
| データ転送（OUT） | 100GB/月 | 約$0.09/GB |
| Elastic IP | インスタンス関連付け時無料 | $0.005/時間 |

## 5. コスト管理

1. **Budgets設定**: AWS Budgets → 月額上限アラート設定
2. **請求アラート**: CloudWatch → 請求アラーム作成
3. **使用状況確認**: Cost Explorer で定期確認
