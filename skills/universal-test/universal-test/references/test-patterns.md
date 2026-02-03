# テストパターン・ベストプラクティス

## 共通原則

### AAA パターン（全言語共通）

```
Arrange: 準備（データ、モック設定）
Act:     実行（テスト対象を呼び出し）
Assert:  検証（結果を確認）
```

### テストケース設計

| カテゴリ | テスト内容 |
|---------|-----------|
| 正常系 | 期待通りの入力で期待通りの出力 |
| 境界値 | 最小値、最大値、空、null |
| 異常系 | 不正入力、例外発生 |
| エッジケース | 特殊文字、大量データ |

---

## Python (pytest)

### 基本構造

```python
import pytest
from src.calculator import Calculator

class TestCalculator:
    """Calculator クラスのテスト"""
    
    def setup_method(self):
        """各テスト前の準備"""
        self.calc = Calculator()
    
    def test_add_正の数(self):
        """正の数の加算"""
        assert self.calc.add(2, 3) == 5
    
    def test_add_負の数(self):
        """負の数の加算"""
        assert self.calc.add(-1, -1) == -2
    
    def test_divide_ゼロ除算でエラー(self):
        """ゼロ除算で例外発生"""
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(10, 0)
```

### パラメータ化テスト

```python
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_パラメータ化(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected
```

### モック

```python
from unittest.mock import Mock, patch

def test_api呼び出し(self):
    with patch('src.service.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"data": "test"}
        result = self.service.fetch_data()
        assert result == {"data": "test"}
```

### フィクスチャ

```python
# conftest.py
import pytest

@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Test User"}

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()
```

---

## Java (JUnit 5)

### 基本構造

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    
    private Calculator calc;
    
    @BeforeEach
    void setUp() {
        calc = new Calculator();
    }
    
    @Test
    @DisplayName("正の数の加算")
    void testAdd_正の数() {
        assertEquals(5, calc.add(2, 3));
    }
    
    @Test
    @DisplayName("ゼロ除算で例外")
    void testDivide_ゼロ除算() {
        assertThrows(ArithmeticException.class, () -> {
            calc.divide(10, 0);
        });
    }
}
```

### パラメータ化テスト

```java
@ParameterizedTest
@CsvSource({
    "1, 2, 3",
    "0, 0, 0",
    "-1, 1, 0"
})
void testAdd_パラメータ化(int a, int b, int expected) {
    assertEquals(expected, calc.add(a, b));
}
```

### Mockito

```java
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ServiceTest {
    
    @Mock
    private Repository repository;
    
    @InjectMocks
    private Service service;
    
    @Test
    void testFindById() {
        when(repository.findById(1L)).thenReturn(Optional.of(new Entity()));
        
        var result = service.findById(1L);
        
        assertTrue(result.isPresent());
        verify(repository).findById(1L);
    }
}
```

---

## JavaScript/TypeScript (Jest)

### 基本構造

```typescript
import { Calculator } from './calculator';

describe('Calculator', () => {
  let calc: Calculator;
  
  beforeEach(() => {
    calc = new Calculator();
  });
  
  describe('add', () => {
    it('正の数を加算できる', () => {
      expect(calc.add(2, 3)).toBe(5);
    });
    
    it('負の数を加算できる', () => {
      expect(calc.add(-1, -1)).toBe(-2);
    });
  });
  
  describe('divide', () => {
    it('ゼロ除算でエラー', () => {
      expect(() => calc.divide(10, 0)).toThrow();
    });
  });
});
```

### 非同期テスト

```typescript
describe('API', () => {
  it('データを取得できる', async () => {
    const result = await api.fetchData();
    expect(result).toEqual({ data: 'test' });
  });
});
```

### モック

```typescript
jest.mock('./api');

import { api } from './api';

const mockApi = api as jest.Mocked<typeof api>;

beforeEach(() => {
  mockApi.fetchData.mockResolvedValue({ data: 'test' });
});
```

---

## React (Testing Library)

### コンポーネントテスト

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('ラベルが表示される', () => {
    render(<Button label="Click me" />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  it('クリックでハンドラが呼ばれる', () => {
    const handleClick = jest.fn();
    render(<Button label="Click" onClick={handleClick} />);
    
    fireEvent.click(screen.getByText('Click'));
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### フォームテスト

```typescript
it('入力値が更新される', async () => {
  render(<LoginForm />);
  
  const input = screen.getByLabelText('Email');
  await userEvent.type(input, 'test@example.com');
  
  expect(input).toHaveValue('test@example.com');
});
```

---

## E2E (Playwright)

### 基本構造

```typescript
import { test, expect } from '@playwright/test';

test.describe('ログイン機能', () => {
  test('正常にログインできる', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });
  
  test('不正なパスワードでエラー', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'wrong');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('.error')).toBeVisible();
  });
});
```

---

## カバレッジ目標

| レベル | カバレッジ | 用途 |
|-------|-----------|------|
| 最低限 | 60% | 個人プロジェクト |
| 推奨 | 80% | チーム開発 |
| 厳格 | 90%+ | 重要システム |

重要なのはカバレッジの数字より**クリティカルパスのテスト**。
