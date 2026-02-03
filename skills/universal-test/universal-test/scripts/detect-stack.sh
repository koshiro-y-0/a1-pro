#!/bin/bash
# プロジェクトの言語・フレームワークを検出するスクリプト
# 使い方: ./detect-stack.sh /path/to/project

PROJECT_DIR="${1:-.}"

echo "=== Project Stack Detection ==="
echo "Scanning: $PROJECT_DIR"
echo ""

# Python
if [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/pyproject.toml" ] || [ -f "$PROJECT_DIR/setup.py" ]; then
    echo "✅ Python detected"
    
    if grep -q "fastapi" "$PROJECT_DIR/requirements.txt" 2>/dev/null || grep -q "fastapi" "$PROJECT_DIR/pyproject.toml" 2>/dev/null; then
        echo "   Framework: FastAPI"
    elif grep -q "flask" "$PROJECT_DIR/requirements.txt" 2>/dev/null || grep -q "flask" "$PROJECT_DIR/pyproject.toml" 2>/dev/null; then
        echo "   Framework: Flask"
    elif grep -q "django" "$PROJECT_DIR/requirements.txt" 2>/dev/null || grep -q "django" "$PROJECT_DIR/pyproject.toml" 2>/dev/null; then
        echo "   Framework: Django"
    fi
    
    if grep -q "pytest" "$PROJECT_DIR/requirements.txt" 2>/dev/null; then
        echo "   Test: pytest (already installed)"
    else
        echo "   Test: pytest (recommended)"
    fi
fi

# Java
if [ -f "$PROJECT_DIR/pom.xml" ]; then
    echo "✅ Java detected (Maven)"
    echo "   Test: JUnit 5 + Mockito"
elif [ -f "$PROJECT_DIR/build.gradle" ] || [ -f "$PROJECT_DIR/build.gradle.kts" ]; then
    echo "✅ Java detected (Gradle)"
    echo "   Test: JUnit 5 + Mockito"
fi

# JavaScript/TypeScript
if [ -f "$PROJECT_DIR/package.json" ]; then
    echo "✅ JavaScript/TypeScript detected"
    
    if grep -q '"react"' "$PROJECT_DIR/package.json"; then
        echo "   Framework: React"
        echo "   Test: Jest + React Testing Library"
    elif grep -q '"next"' "$PROJECT_DIR/package.json"; then
        echo "   Framework: Next.js"
        echo "   Test: Jest + React Testing Library"
    elif grep -q '"vue"' "$PROJECT_DIR/package.json"; then
        echo "   Framework: Vue.js"
        echo "   Test: Vitest + Vue Test Utils"
    else
        echo "   Test: Jest or Vitest"
    fi
    
    if grep -q '"typescript"' "$PROJECT_DIR/package.json"; then
        echo "   Language: TypeScript"
    fi
fi

# E2E判定
if [ -f "$PROJECT_DIR/playwright.config.ts" ] || [ -f "$PROJECT_DIR/playwright.config.js" ]; then
    echo "✅ E2E: Playwright configured"
elif [ -f "$PROJECT_DIR/cypress.config.ts" ] || [ -f "$PROJECT_DIR/cypress.config.js" ]; then
    echo "✅ E2E: Cypress configured"
fi

echo ""
echo "=== Recommendations ==="
echo "Run 'テスト環境をセットアップして' to configure testing"
