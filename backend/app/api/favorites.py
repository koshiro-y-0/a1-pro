"""
Favorites API Endpoints
お気に入り関連のAPIエンドポイント
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.favorite import Favorite
from app.models.company import Company
from app.schemas.favorite import (
    FavoriteCreate,
    FavoriteResponse,
    FavoriteWithCompany
)

router = APIRouter()


@router.get("/", response_model=List[FavoriteWithCompany])
async def get_favorites(db: Session = Depends(get_db)):
    """
    お気に入り一覧取得

    - 全お気に入り企業を取得
    - 企業情報も含めて返却
    """
    favorites = db.query(Favorite).all()

    result = []
    for favorite in favorites:
        company = db.query(Company).filter(Company.id == favorite.company_id).first()
        if company:
            result.append({
                **favorite.__dict__,
                "stock_code": company.stock_code,
                "company_name": company.name,
                "industry": company.industry
            })

    return result


@router.post("/", response_model=FavoriteResponse)
async def create_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db)
):
    """
    お気に入り追加

    - 企業をお気に入りに追加
    """
    # 企業存在確認
    company = db.query(Company).filter(Company.id == favorite.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # 既存チェック
    existing = db.query(Favorite).filter(
        Favorite.company_id == favorite.company_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")

    # 新規作成
    db_favorite = Favorite(**favorite.model_dump())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)

    return db_favorite


@router.delete("/{favorite_id}")
async def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db)
):
    """
    お気に入り削除

    - お気に入りから削除
    """
    db_favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()

    if not db_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(db_favorite)
    db.commit()

    return {"message": "Favorite deleted successfully"}


@router.delete("/by-company/{company_id}")
async def delete_favorite_by_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    企業IDでお気に入り削除

    - 企業IDを指定してお気に入りから削除
    """
    db_favorite = db.query(Favorite).filter(
        Favorite.company_id == company_id
    ).first()

    if not db_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(db_favorite)
    db.commit()

    return {"message": "Favorite deleted successfully"}
