"""
Portfolio Calculator Service
ポートフォリオのパフォーマンス計算サービス
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.company import Company
from app.services.yfinance_client import yfinance_client


class PortfolioCalculator:
    """ポートフォリオ計算クラス"""

    @staticmethod
    def calculate_individual_performance(
        purchase_price: float,
        purchase_quantity: float,
        current_price: Optional[float]
    ) -> Dict:
        """
        個別銘柄のパフォーマンス計算

        Args:
            purchase_price: 購入価格
            purchase_quantity: 購入数量
            current_price: 現在価格

        Returns:
            パフォーマンス情報
        """
        purchase_value = purchase_price * purchase_quantity

        if current_price is None:
            return {
                "purchase_value": purchase_value,
                "current_value": None,
                "profit_loss": None,
                "profit_loss_percentage": None
            }

        current_value = current_price * purchase_quantity
        profit_loss = current_value - purchase_value
        profit_loss_percentage = (profit_loss / purchase_value) * 100 if purchase_value > 0 else 0

        return {
            "purchase_value": purchase_value,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_percentage
        }

    @staticmethod
    def get_current_price(asset_type: str, symbol: str) -> Optional[float]:
        """
        現在価格を取得

        Args:
            asset_type: 資産クラス
            symbol: シンボル/銘柄コード

        Returns:
            現在価格
        """
        if asset_type in ["jp_stock", "us_stock"]:
            stock_data = yfinance_client.get_stock_data_dict(symbol, period="1d")
            if stock_data and len(stock_data) > 0:
                return stock_data[-1]["close"]

        # 他の資産クラス（暗号資産、為替など）は将来実装
        return None

    @classmethod
    def calculate_portfolio_summary(
        cls,
        db: Session
    ) -> Dict:
        """
        ポートフォリオ全体のサマリー計算

        Args:
            db: データベースセッション

        Returns:
            サマリー情報
        """
        portfolio_items = db.query(Portfolio).all()

        total_purchase_value = 0
        total_current_value = 0
        asset_allocation = {}

        for item in portfolio_items:
            purchase_value = item.purchase_price * item.quantity
            total_purchase_value += purchase_value

            # 現在価格取得
            current_price = cls.get_current_price(item.asset_type, item.symbol)

            if current_price:
                current_value = current_price * item.quantity
                total_current_value += current_value

            # 資産クラス別集計
            if item.asset_type not in asset_allocation:
                asset_allocation[item.asset_type] = {
                    "purchase_value": 0,
                    "current_value": 0,
                    "count": 0
                }

            asset_allocation[item.asset_type]["purchase_value"] += purchase_value
            if current_price:
                asset_allocation[item.asset_type]["current_value"] += current_price * item.quantity
            asset_allocation[item.asset_type]["count"] += 1

        # 総損益計算
        total_profit_loss = total_current_value - total_purchase_value if total_current_value > 0 else 0
        total_profit_loss_percentage = (
            (total_profit_loss / total_purchase_value) * 100
            if total_purchase_value > 0 else 0
        )

        # 資産クラス別比率計算
        for asset_type, data in asset_allocation.items():
            data["allocation_percentage"] = (
                (data["purchase_value"] / total_purchase_value) * 100
                if total_purchase_value > 0 else 0
            )

        return {
            "total_purchase_value": total_purchase_value,
            "total_current_value": total_current_value,
            "total_profit_loss": total_profit_loss,
            "total_profit_loss_percentage": total_profit_loss_percentage,
            "asset_allocation": asset_allocation,
            "total_items": len(portfolio_items)
        }


# グローバルインスタンス
portfolio_calculator = PortfolioCalculator()
