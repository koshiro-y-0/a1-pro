"""
yfinance Client
Yahoo Finance からの株価データ取得クライアント
"""

import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd


class YFinanceClient:
    """Yahoo Finance クライアント"""

    def __init__(self):
        pass

    def get_stock_data(
        self,
        stock_code: str,
        period: str = "1mo",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        株価データ取得

        Args:
            stock_code: 銘柄コード (例: "7203.T" for トヨタ)
            period: 期間 ("1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "max")
            interval: 間隔 ("1m", "5m", "1h", "1d", "1wk", "1mo")

        Returns:
            株価データのDataFrame
        """
        try:
            # 日本株の場合、.T を追加
            symbol = f"{stock_code}.T" if not stock_code.endswith(".T") else stock_code

            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)

            if data.empty:
                return None

            return data
        except Exception as e:
            print(f"yfinance error: {e}")
            return None

    def get_stock_info(self, stock_code: str) -> Optional[Dict]:
        """
        企業情報取得

        Args:
            stock_code: 銘柄コード

        Returns:
            企業情報のDict
        """
        try:
            symbol = f"{stock_code}.T" if not stock_code.endswith(".T") else stock_code
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info
        except Exception as e:
            print(f"yfinance info error: {e}")
            return None

    def get_stock_data_dict(
        self,
        stock_code: str,
        period: str = "1mo"
    ) -> List[Dict]:
        """
        株価データを辞書形式で取得

        Args:
            stock_code: 銘柄コード
            period: 期間

        Returns:
            株価データのリスト
        """
        df = self.get_stock_data(stock_code, period)

        if df is None or df.empty:
            return []

        # DataFrameを辞書のリストに変換
        result = []
        for index, row in df.iterrows():
            result.append({
                "date": index.strftime("%Y-%m-%d"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"])
            })

        return result


# Singleton instance
yfinance_client = YFinanceClient()
