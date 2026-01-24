"""
Company Model
企業マスタテーブル
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    stock_code = Column(String(10), unique=True, index=True, nullable=False, comment="銘柄コード")
    name = Column(String(255), nullable=False, comment="企業名")
    industry = Column(String(100), comment="業種")
    description = Column(Text, comment="事業内容")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="作成日時")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新日時")

    def __repr__(self):
        return f"<Company(stock_code='{self.stock_code}', name='{self.name}')>"
