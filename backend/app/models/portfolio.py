"""
Portfolio Model
ポートフォリオテーブル
"""

from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True)
    asset_type = Column(String(50), nullable=False, comment="資産クラス (jp_stock, us_stock, crypto, fx)")
    symbol = Column(String(20), nullable=False, comment="銘柄コード/シンボル")
    purchase_date = Column(Date, nullable=False, comment="購入日")
    purchase_price = Column(Numeric(15, 2), nullable=False, comment="購入価格")
    quantity = Column(Numeric(15, 4), nullable=False, comment="数量")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="作成日時")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新日時")

    def __repr__(self):
        return f"<Portfolio(asset_type='{self.asset_type}', symbol='{self.symbol}')>"
