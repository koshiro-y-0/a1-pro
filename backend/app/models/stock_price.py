"""
Stock Price Model
株価データテーブル
"""

from sqlalchemy import Column, Integer, Date, Numeric, BigInteger, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.database import Base


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True, comment="企業ID")
    date = Column(Date, nullable=False, index=True, comment="日付")
    open = Column(Numeric(10, 2), comment="始値")
    high = Column(Numeric(10, 2), comment="高値")
    low = Column(Numeric(10, 2), comment="安値")
    close = Column(Numeric(10, 2), comment="終値")
    volume = Column(BigInteger, comment="出来高")

    # Relationship
    company = relationship("Company", backref="stock_prices")

    # Composite index for efficient querying
    __table_args__ = (
        Index('idx_company_date', 'company_id', 'date'),
    )

    def __repr__(self):
        return f"<StockPrice(company_id={self.company_id}, date={self.date}, close={self.close})>"
