"""
Exchange Rate Client
為替レート取得クライアント
"""

import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import os


class ExchangeRateClient:
    """為替レートAPIクライアント"""

    def __init__(self):
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY", "")
        self.base_url = "https://v6.exchangerate-api.com/v6"

    def get_exchange_rate(
        self,
        base_currency: str = "USD",
        target_currency: str = "JPY"
    ) -> Optional[float]:
        """
        為替レート取得

        Args:
            base_currency: 基準通貨 (例: USD, EUR)
            target_currency: 対象通貨 (例: JPY)

        Returns:
            為替レート
        """
        try:
            if not self.api_key:
                # APIキーがない場合はyfinanceを使用
                return self._get_rate_from_yfinance(base_currency, target_currency)

            url = f"{self.base_url}/{self.api_key}/pair/{base_currency}/{target_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get("result") == "success":
                return float(data.get("conversion_rate", 0))

            return None
        except Exception as e:
            print(f"Exchange rate API error: {e}")
            # フォールバック: yfinanceを使用
            return self._get_rate_from_yfinance(base_currency, target_currency)

    def _get_rate_from_yfinance(
        self,
        base_currency: str,
        target_currency: str
    ) -> Optional[float]:
        """
        yfinanceから為替レートを取得（フォールバック）

        Args:
            base_currency: 基準通貨
            target_currency: 対象通貨

        Returns:
            為替レート
        """
        try:
            import yfinance as yf

            # 通貨ペアのシンボル作成 (例: USDJPY=X)
            symbol = f"{base_currency}{target_currency}=X"
            ticker = yf.Ticker(symbol)

            hist = ticker.history(period="1d")
            if hist.empty:
                return None

            return float(hist['Close'].iloc[-1])
        except Exception as e:
            print(f"yfinance exchange rate error: {e}")
            return None

    def get_multiple_rates(
        self,
        base_currency: str = "USD",
        target_currencies: List[str] = None
    ) -> Dict[str, float]:
        """
        複数通貨の為替レート取得

        Args:
            base_currency: 基準通貨
            target_currencies: 対象通貨リスト

        Returns:
            通貨ペアと為替レートの辞書
        """
        if target_currencies is None:
            target_currencies = ["JPY", "EUR", "GBP", "CNY"]

        rates = {}
        for currency in target_currencies:
            rate = self.get_exchange_rate(base_currency, currency)
            if rate:
                rates[f"{base_currency}/{currency}"] = rate

        return rates

    def get_historical_rates(
        self,
        base_currency: str,
        target_currency: str,
        days: int = 30
    ) -> List[Dict]:
        """
        過去の為替レート取得（yfinance使用）

        Args:
            base_currency: 基準通貨
            target_currency: 対象通貨
            days: 取得日数

        Returns:
            為替レートの履歴
        """
        try:
            import yfinance as yf

            symbol = f"{base_currency}{target_currency}=X"
            ticker = yf.Ticker(symbol)

            # 期間指定でデータ取得
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            hist = ticker.history(start=start_date, end=end_date)

            if hist.empty:
                return []

            result = []
            for index, row in hist.iterrows():
                result.append({
                    "date": index.strftime("%Y-%m-%d"),
                    "rate": float(row["Close"])
                })

            return result
        except Exception as e:
            print(f"Historical rates error: {e}")
            return []


# Singleton instance
exchange_rate_client = ExchangeRateClient()
