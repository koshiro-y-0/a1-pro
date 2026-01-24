"""
Financial Data Model
決算データテーブル
"""

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True, comment="企業ID")
    fiscal_year = Column(Integer, nullable=False, index=True, comment="会計年度")
    fiscal_quarter = Column(Integer, comment="四半期 (1-4, nullで通期)")
    revenue = Column(BigInteger, comment="売上高")
    operating_profit = Column(BigInteger, comment="営業利益")
    ordinary_profit = Column(BigInteger, comment="経常利益")
    net_profit = Column(BigInteger, comment="純利益")
    total_assets = Column(BigInteger, comment="総資産")
    equity = Column(BigInteger, comment="自己資本")
    total_liabilities = Column(BigInteger, comment="総負債")
    current_assets = Column(BigInteger, comment="流動資産")
    current_liabilities = Column(BigInteger, comment="流動負債")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="作成日時")

    # Relationship
    company = relationship("Company", backref="financial_data")

    def __repr__(self):
        return f"<FinancialData(company_id={self.company_id}, fiscal_year={self.fiscal_year})>"
