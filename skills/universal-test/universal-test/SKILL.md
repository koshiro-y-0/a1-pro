---
name: universal-test
description: 多言語対応のテスト自動化スキル。Python(pytest)、Java(JUnit)、JavaScript/TypeScript(Jest/Vitest)、React(Testing Library)、E2E(Playwright)に対応。「テストして」「テストを書いて」「テストコードを生成」「TDDで開発」「CIにテスト追加」などのリクエストで使用。プロジェクトの言語を自動検出し、適切なテストフレームワークでテストコード生成・実行・CI設定を行う。
---

# Universal Test Skill

プロジェクトの言語を自動検出し、適切なテストを生成・実行する。

## ワークフロー

```
「テストして」
    ↓
言語自動検出（※1）
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

※1 言語検出の優先順位:
1. `requirements.txt` / `pyproject.toml` → Python
2. `pom.xml` / `build.gradle` → Java
3. `package.json` → JS/TS（中身で React/Node 判定）

## コマンド対応表

| ユーザーの指示 | 実行アクション |
|--------------|---------------|
| 「テストして」 | 既存テスト実行 |
| 「テストを書いて」 | 対象コードのテスト生成 |
| 「テスト環境をセットアップ」 | 設定ファイル生成 |
| 「カバレッジを見せて」 | カバレッジ計測実行 |
| 「CIにテスト追加」 | GitHub Actions設定 |
| 「TDDで開発したい」 | TDDワークフロー開始 |

## Phase 1: テスト環境セットアップ

言語に応じて `assets/` 内の設定ファイルをコピー:

| 言語 | 設定ファイル |
|-----|-------------|
| Python | `assets/python/pytest.ini`, `conftest.py` |
| Java | `assets/java/build.gradle.test` |
| JS/TS | `assets/javascript/jest.config.js` |
| React | `assets/react/jest.config.js`, `setupTests.ts` |
| E2E | `assets/e2e/playwright.config.ts` |

## Phase 2: テストコード生成

### 生成ルール

1. **対象ファイルを特定**: ユーザー指定 or 変更されたファイル
2. **テストパターン適用**: `references/test-patterns.md` 参照
3. **命名規則**:
   - Python: `test_<module>.py`
   - Java: `<Class>Test.java`
   - JS/TS: `<file>.test.ts` or `<file>.spec.ts`

### テストの種類

| 種類 | 目的 | 生成タイミング |
|-----|------|--------------|
| Unit | 関数・メソッド単体 | 基本（常に生成） |
| Integration | 複数モジュール連携 | API・DB接続時 |
| E2E | ユーザーフロー | UI完成後 |

## Phase 3: テスト実行

```bash
# Python
pytest -v --cov=src --cov-report=html

# Java
./gradlew test jacocoTestReport

# JavaScript/TypeScript
npm test -- --coverage

# E2E
npx playwright test
```

## Phase 4: CI設定（GitHub Actions）

`assets/github-actions/test.yml` をプロジェクトにコピー。

言語に応じて適切なワークフローを選択:
- `test-python.yml`
- `test-java.yml`
- `test-javascript.yml`
- `test-e2e.yml`

## TDDワークフロー

「TDDで開発」と言われたら `references/tdd-workflow.md` に従う:

```
1. Red: 失敗するテストを書く
2. Green: テストが通る最小限のコードを書く
3. Refactor: コードを整理
4. 繰り返し
```

## テスト生成のベストプラクティス

詳細は `references/test-patterns.md` 参照。

基本方針:
- 正常系 + 異常系（境界値、エラー）を網羅
- モック/スタブは外部依存のみに使用
- テスト名は「何をテストしているか」を明確に
- 1テスト1アサーション（原則）
