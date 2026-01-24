"""
Favorite Model
お気に入りテーブル
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True, comment="企業ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="作成日時")

    # Relationship
    company = relationship("Company", backref="favorites")

    def __repr__(self):
        return f"<Favorite(company_id={self.company_id})>"
