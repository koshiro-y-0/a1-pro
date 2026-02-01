"""
Cache Service
In-memoryキャッシュサービス
"""

from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import threading


class CacheEntry:
    """キャッシュエントリ"""

    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.expires_at = datetime.now() + timedelta(seconds=ttl_seconds)

    def is_expired(self) -> bool:
        """有効期限切れかチェック"""
        return datetime.now() > self.expires_at


class CacheService:
    """In-memoryキャッシュサービス"""

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """
        キャッシュから値を取得

        Args:
            key: キャッシュキー

        Returns:
            キャッシュされた値、存在しないまたは期限切れの場合はNone
        """
        with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]

            if entry.is_expired():
                del self._cache[key]
                return None

            return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int = 900):
        """
        キャッシュに値を設定

        Args:
            key: キャッシュキー
            value: キャッシュする値
            ttl_seconds: 有効期限（秒）、デフォルト15分
        """
        with self._lock:
            self._cache[key] = CacheEntry(value, ttl_seconds)

    def delete(self, key: str):
        """
        キャッシュから値を削除

        Args:
            key: キャッシュキー
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self):
        """全キャッシュをクリア"""
        with self._lock:
            self._cache.clear()

    def clear_pattern(self, pattern: str):
        """
        パターンに一致するキャッシュをクリア

        Args:
            pattern: パターン文字列（部分一致）
        """
        with self._lock:
            keys_to_delete = [
                key for key in self._cache.keys() if pattern in key
            ]
            for key in keys_to_delete:
                del self._cache[key]

    def get_stats(self) -> Dict[str, int]:
        """
        キャッシュ統計情報を取得

        Returns:
            統計情報
        """
        with self._lock:
            total_entries = len(self._cache)
            expired_entries = sum(
                1 for entry in self._cache.values() if entry.is_expired()
            )
            active_entries = total_entries - expired_entries

            return {
                "total_entries": total_entries,
                "active_entries": active_entries,
                "expired_entries": expired_entries
            }

    def cleanup_expired(self):
        """期限切れキャッシュを削除"""
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items() if entry.is_expired()
            ]
            for key in expired_keys:
                del self._cache[key]


# Singleton instance
cache_service = CacheService()


# キャッシュTTL定数
CACHE_TTL_STOCK_PRICE = 900  # 15分 (株価データ)
CACHE_TTL_FINANCIAL = 86400  # 1日 (決算データ)
CACHE_TTL_COMPANY_INFO = 3600  # 1時間 (企業情報)
CACHE_TTL_EXCHANGE_RATE = 1800  # 30分 (為替)
CACHE_TTL_CRYPTO = 300  # 5分 (暗号資産)
