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

    def _format_symbol(self, symbol: str, asset_type: str = "jp_stock") -> str:
        """
        資産タイプに応じてシンボルをフォーマット

        Args:
            symbol: 銘柄コード/シンボル
            asset_type: 資産クラス (jp_stock, us_stock, crypto, fx)

        Returns:
            フォーマット済みシンボル
        """
        if asset_type == "jp_stock":
            # 日本株: .T を追加
            return f"{symbol}.T" if not symbol.endswith(".T") else symbol
        elif asset_type == "us_stock":
            # 米国株: そのまま (例: AAPL, TSLA)
            return symbol
        elif asset_type == "crypto":
            # 暗号資産: -USD を追加 (例: BTC-USD, ETH-USD)
            return f"{symbol}-USD" if not symbol.endswith("-USD") else symbol
        elif asset_type == "fx":
            # 為替: JPY=X 形式 (例: USDJPY=X, EURJPY=X)
            if not symbol.endswith("=X"):
                return f"{symbol}=X"
            return symbol
        else:
            return symbol

    def get_stock_data(
        self,
        stock_code: str,
        period: str = "1mo",
        interval: str = "1d",
        asset_type: str = "jp_stock"
    ) -> Optional[pd.DataFrame]:
        """
        株価データ取得（複数資産対応）

        Args:
            stock_code: 銘柄コード (例: "7203" for トヨタ, "AAPL" for Apple)
            period: 期間 ("1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "max")
            interval: 間隔 ("1m", "5m", "1h", "1d", "1wk", "1mo")
            asset_type: 資産クラス (jp_stock, us_stock, crypto, fx)

        Returns:
            株価データのDataFrame
        """
        try:
            symbol = self._format_symbol(stock_code, asset_type)

            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)

            if data.empty:
                return None

            return data
        except Exception as e:
            print(f"yfinance error: {e}")
            return None

    def get_current_price(
        self,
        symbol: str,
        asset_type: str = "jp_stock"
    ) -> Optional[float]:
        """
        現在価格を取得

        Args:
            symbol: 銘柄コード/シンボル
            asset_type: 資産クラス

        Returns:
            現在価格
        """
        try:
            formatted_symbol = self._format_symbol(symbol, asset_type)
            ticker = yf.Ticker(formatted_symbol)

            # 最新データを取得
            hist = ticker.history(period="1d")
            if hist.empty:
                return None

            return float(hist['Close'].iloc[-1])
        except Exception as e:
            print(f"Error getting current price for {symbol}: {e}")
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
