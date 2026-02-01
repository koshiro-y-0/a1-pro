"""
Performance Calculator
資産パフォーマンス計算サービス
"""

import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd


class PerformanceCalculator:
    """パフォーマンス計算"""

    @staticmethod
    def normalize_prices(prices: List[float], base_value: float = 100.0) -> List[float]:
        """
        価格を正規化（基準日=100）

        Args:
            prices: 価格リスト
            base_value: 基準値

        Returns:
            正規化された価格リスト
        """
        if not prices or prices[0] == 0:
            return [base_value] * len(prices)

        base_price = prices[0]
        return [(price / base_price) * base_value for price in prices]

    @staticmethod
    def calculate_total_return(prices: List[float]) -> float:
        """
        総リターン計算

        Args:
            prices: 価格リスト

        Returns:
            総リターン（%）
        """
        if not prices or len(prices) < 2 or prices[0] == 0:
            return 0.0

        return ((prices[-1] - prices[0]) / prices[0]) * 100

    @staticmethod
    def calculate_volatility(prices: List[float]) -> Optional[float]:
        """
        ボラティリティ計算（年率換算）

        Args:
            prices: 価格リスト

        Returns:
            年率ボラティリティ（%）
        """
        if not prices or len(prices) < 2:
            return None

        # 日次リターン計算
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] != 0:
                daily_return = (prices[i] - prices[i-1]) / prices[i-1]
                returns.append(daily_return)

        if not returns:
            return None

        # 標準偏差を計算し、年率換算（√252）
        std_dev = np.std(returns)
        annual_volatility = std_dev * np.sqrt(252) * 100

        return float(annual_volatility)

    @staticmethod
    def calculate_max_drawdown(prices: List[float]) -> Optional[float]:
        """
        最大ドローダウン計算

        Args:
            prices: 価格リスト

        Returns:
            最大ドローダウン（%）
        """
        if not prices or len(prices) < 2:
            return None

        max_price = prices[0]
        max_dd = 0.0

        for price in prices:
            if price > max_price:
                max_price = price

            drawdown = ((price - max_price) / max_price) * 100
            if drawdown < max_dd:
                max_dd = drawdown

        return float(max_dd)

    @staticmethod
    def calculate_sharpe_ratio(
        prices: List[float],
        risk_free_rate: float = 0.0
    ) -> Optional[float]:
        """
        シャープレシオ計算

        Args:
            prices: 価格リスト
            risk_free_rate: リスクフリーレート（年率%）

        Returns:
            シャープレシオ
        """
        if not prices or len(prices) < 2:
            return None

        # 日次リターン計算
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] != 0:
                daily_return = (prices[i] - prices[i-1]) / prices[i-1]
                returns.append(daily_return)

        if not returns:
            return None

        # 平均リターンと標準偏差
        mean_return = np.mean(returns)
        std_return = np.std(returns)

        if std_return == 0:
            return None

        # 年率換算
        annual_return = mean_return * 252
        annual_std = std_return * np.sqrt(252)

        # リスクフリーレートを日割り換算
        daily_rf = risk_free_rate / 100 / 252

        # シャープレシオ
        sharpe = (annual_return - daily_rf * 252) / annual_std

        return float(sharpe)

    @classmethod
    def calculate_metrics(cls, prices: List[float]) -> Dict:
        """
        全てのメトリクスを計算

        Args:
            prices: 価格リスト

        Returns:
            メトリクス辞書
        """
        return {
            "total_return": cls.calculate_total_return(prices),
            "volatility": cls.calculate_volatility(prices),
            "max_drawdown": cls.calculate_max_drawdown(prices),
            "sharpe_ratio": cls.calculate_sharpe_ratio(prices)
        }

    @staticmethod
    def create_ranking(assets_performance: List[Dict]) -> List[Dict]:
        """
        パフォーマンスランキング作成

        Args:
            assets_performance: 資産パフォーマンスリスト

        Returns:
            ランキング
        """
        # 総リターンでソート
        sorted_assets = sorted(
            assets_performance,
            key=lambda x: x.get("total_return", 0),
            reverse=True
        )

        ranking = []
        for idx, asset in enumerate(sorted_assets, 1):
            ranking.append({
                "rank": idx,
                "symbol": asset.get("symbol"),
                "name": asset.get("name"),
                "asset_type": asset.get("asset_type"),
                "total_return": asset.get("total_return"),
                "volatility": asset.get("volatility"),
                "max_drawdown": asset.get("max_drawdown")
            })

        return ranking


# Singleton instance
performance_calculator = PerformanceCalculator()
