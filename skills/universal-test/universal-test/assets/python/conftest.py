"""pytest 共通設定・フィクスチャ"""
import pytest
from unittest.mock import Mock

# ============================================
# 基本フィクスチャ
# ============================================

@pytest.fixture
def sample_data():
    """サンプルデータ"""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }

@pytest.fixture
def mock_response():
    """モックHTTPレスポンス"""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"success": True}
    return mock

# ============================================
# DB関連フィクスチャ（必要に応じてコメント解除）
# ============================================

# @pytest.fixture
# def db_session():
#     """テスト用DBセッション"""
#     from src.database import SessionLocal
#     session = SessionLocal()
#     yield session
#     session.rollback()
#     session.close()

# ============================================
# 非同期フィクスチャ
# ============================================

@pytest.fixture
def event_loop():
    """非同期テスト用イベントループ"""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# ============================================
# テスト用ヘルパー
# ============================================

@pytest.fixture
def assert_called_once_with_partial():
    """部分一致でモック呼び出しを検証"""
    def _assert(mock, **expected_kwargs):
        mock.assert_called_once()
        _, kwargs = mock.call_args
        for key, value in expected_kwargs.items():
            assert kwargs.get(key) == value, f"{key}: {kwargs.get(key)} != {value}"
    return _assert
