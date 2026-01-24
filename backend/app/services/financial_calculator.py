"""
Financial Calculator
財務指標計算サービス
"""

from typing import Optional, Dict
from app.schemas.financial_data import FinancialMetrics


class FinancialCalculator:
    """財務指標計算クラス"""

    @staticmethod
    def calculate_equity_ratio(
        equity: Optional[int],
        total_assets: Optional[int]
    ) -> Optional[float]:
        """
        自己資本比率を計算

        Args:
            equity: 自己資本
            total_assets: 総資産

        Returns:
            自己資本比率 (%)
        """
        if equity is None or total_assets is None or total_assets == 0:
            return None
        return round((equity / total_assets) * 100, 2)

    @staticmethod
    def calculate_current_ratio(
        current_assets: Optional[int],
        current_liabilities: Optional[int]
    ) -> Optional[float]:
        """
        流動比率を計算

        Args:
            current_assets: 流動資産
            current_liabilities: 流動負債

        Returns:
            流動比率 (%)
        """
        if current_assets is None or current_liabilities is None or current_liabilities == 0:
            return None
        return round((current_assets / current_liabilities) * 100, 2)

    @staticmethod
    def calculate_debt_ratio(
        total_liabilities: Optional[int],
        total_assets: Optional[int]
    ) -> Optional[float]:
        """
        負債比率を計算

        Args:
            total_liabilities: 総負債
            total_assets: 総資産

        Returns:
            負債比率 (%)
        """
        if total_liabilities is None or total_assets is None or total_assets == 0:
            return None
        return round((total_liabilities / total_assets) * 100, 2)

    @staticmethod
    def calculate_roe(
        net_profit: Optional[int],
        equity: Optional[int]
    ) -> Optional[float]:
        """
        ROE (自己資本利益率) を計算

        Args:
            net_profit: 純利益
            equity: 自己資本

        Returns:
            ROE (%)
        """
        if net_profit is None or equity is None or equity == 0:
            return None
        return round((net_profit / equity) * 100, 2)

    @staticmethod
    def calculate_operating_margin(
        operating_profit: Optional[int],
        revenue: Optional[int]
    ) -> Optional[float]:
        """
        営業利益率を計算

        Args:
            operating_profit: 営業利益
            revenue: 売上高

        Returns:
            営業利益率 (%)
        """
        if operating_profit is None or revenue is None or revenue == 0:
            return None
        return round((operating_profit / revenue) * 100, 2)

    @classmethod
    def calculate_all_metrics(
        cls,
        revenue: Optional[int],
        operating_profit: Optional[int],
        net_profit: Optional[int],
        total_assets: Optional[int],
        equity: Optional[int],
        total_liabilities: Optional[int],
        current_assets: Optional[int],
        current_liabilities: Optional[int]
    ) -> FinancialMetrics:
        """
        全ての財務指標を計算

        Returns:
            財務指標
        """
        return FinancialMetrics(
            equity_ratio=cls.calculate_equity_ratio(equity, total_assets),
            current_ratio=cls.calculate_current_ratio(current_assets, current_liabilities),
            debt_ratio=cls.calculate_debt_ratio(total_liabilities, total_assets),
            roe=cls.calculate_roe(net_profit, equity),
            operating_margin=cls.calculate_operating_margin(operating_profit, revenue)
        )


# Singleton instance
financial_calculator = FinancialCalculator()
