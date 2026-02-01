"""
Crypto Client
暗号資産データ取得クライアント
"""

import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import time


class CryptoClient:
    """CoinGecko API クライアント"""

    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.last_request_time = 0
        self.rate_limit_delay = 1.2  # 50 requests/minute = 1.2 seconds between requests

    def _rate_limit(self):
        """レート制限対応"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_request)

        self.last_request_time = time.time()

    def get_crypto_price(
        self,
        crypto_id: str,
        vs_currency: str = "usd"
    ) -> Optional[float]:
        """
        暗号資産の現在価格取得

        Args:
            crypto_id: 暗号資産ID (例: bitcoin, ethereum)
            vs_currency: 基準通貨 (usd, jpy)

        Returns:
            現在価格
        """
        try:
            self._rate_limit()

            url = f"{self.base_url}/simple/price"
            params = {
                "ids": crypto_id,
                "vs_currencies": vs_currency
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if crypto_id in data and vs_currency in data[crypto_id]:
                return float(data[crypto_id][vs_currency])

            return None
        except Exception as e:
            print(f"CoinGecko price error: {e}")
            # フォールバック: yfinanceを使用
            return self._get_price_from_yfinance(crypto_id)

    def _get_price_from_yfinance(self, crypto_id: str) -> Optional[float]:
        """
        yfinanceから暗号資産価格を取得（フォールバック）

        Args:
            crypto_id: 暗号資産ID

        Returns:
            現在価格
        """
        try:
            import yfinance as yf

            # ID to symbol mapping
            symbol_map = {
                "bitcoin": "BTC-USD",
                "ethereum": "ETH-USD",
                "ripple": "XRP-USD",
                "cardano": "ADA-USD",
                "solana": "SOL-USD"
            }

            symbol = symbol_map.get(crypto_id.lower())
            if not symbol:
                return None

            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")

            if hist.empty:
                return None

            return float(hist['Close'].iloc[-1])
        except Exception as e:
            print(f"yfinance crypto error: {e}")
            return None

    def get_crypto_market_data(
        self,
        crypto_id: str,
        vs_currency: str = "usd"
    ) -> Optional[Dict]:
        """
        暗号資産の市場データ取得

        Args:
            crypto_id: 暗号資産ID
            vs_currency: 基準通貨

        Returns:
            市場データ
        """
        try:
            self._rate_limit()

            url = f"{self.base_url}/coins/{crypto_id}"
            params = {
                "localization": "false",
                "tickers": "false",
                "community_data": "false",
                "developer_data": "false"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            market_data = data.get("market_data", {})
            current_price = market_data.get("current_price", {}).get(vs_currency)
            market_cap = market_data.get("market_cap", {}).get(vs_currency)
            total_volume = market_data.get("total_volume", {}).get(vs_currency)

            return {
                "id": crypto_id,
                "name": data.get("name"),
                "symbol": data.get("symbol", "").upper(),
                "current_price": current_price,
                "market_cap": market_cap,
                "total_volume": total_volume,
                "price_change_24h": market_data.get("price_change_percentage_24h"),
                "price_change_7d": market_data.get("price_change_percentage_7d"),
                "price_change_30d": market_data.get("price_change_percentage_30d")
            }
        except Exception as e:
            print(f"CoinGecko market data error: {e}")
            return None

    def get_historical_data(
        self,
        crypto_id: str,
        vs_currency: str = "usd",
        days: int = 30
    ) -> List[Dict]:
        """
        暗号資産の履歴データ取得

        Args:
            crypto_id: 暗号資産ID
            vs_currency: 基準通貨
            days: 取得日数

        Returns:
            価格履歴
        """
        try:
            self._rate_limit()

            url = f"{self.base_url}/coins/{crypto_id}/market_chart"
            params = {
                "vs_currency": vs_currency,
                "days": days,
                "interval": "daily"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            prices = data.get("prices", [])

            result = []
            for price_data in prices:
                timestamp = price_data[0] / 1000  # milliseconds to seconds
                date = datetime.fromtimestamp(timestamp)
                result.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "price": float(price_data[1])
                })

            return result
        except Exception as e:
            print(f"CoinGecko historical data error: {e}")
            return []

    def search_crypto(self, query: str) -> List[Dict]:
        """
        暗号資産検索

        Args:
            query: 検索クエリ

        Returns:
            検索結果
        """
        try:
            self._rate_limit()

            url = f"{self.base_url}/search"
            params = {"query": query}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            coins = data.get("coins", [])

            return [
                {
                    "id": coin.get("id"),
                    "name": coin.get("name"),
                    "symbol": coin.get("symbol", "").upper(),
                    "market_cap_rank": coin.get("market_cap_rank")
                }
                for coin in coins[:10]  # 上位10件
            ]
        except Exception as e:
            print(f"CoinGecko search error: {e}")
            return []

    @staticmethod
    def get_popular_cryptos() -> List[str]:
        """人気の暗号資産IDリスト"""
        return [
            "bitcoin",
            "ethereum",
            "ripple",
            "cardano",
            "solana",
            "polkadot",
            "dogecoin",
            "avalanche-2",
            "polygon",
            "chainlink"
        ]


# Singleton instance
crypto_client = CryptoClient()
