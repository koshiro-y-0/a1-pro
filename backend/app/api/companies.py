"""
Companies API Endpoints
企業関連のAPIエンドポイント
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from app.db.database import get_db
from app.models.company import Company
from app.schemas.company import (
    CompanyResponse,
    CompanySearchResult,
    CompanyCreate
)
from app.schemas.stock_price import StockPriceResponse
from app.services.yfinance_client import yfinance_client

router = APIRouter()


@router.get("/search", response_model=List[CompanySearchResult])
async def search_companies(
    q: str = Query(..., min_length=1, description="検索クエリ（銘柄コードまたは企業名）"),
    limit: int = Query(20, ge=1, le=100, description="最大取得件数"),
    db: Session = Depends(get_db)
):
    """
    銘柄検索

    - 銘柄コードまたは企業名で検索
    - 部分一致検索対応
    """
    # 銘柄コードまたは企業名で検索
    companies = db.query(Company).filter(
        or_(
            Company.stock_code.like(f"%{q}%"),
            Company.name.like(f"%{q}%")
        )
    ).limit(limit).all()

    return companies


@router.get("/{stock_code}", response_model=CompanyResponse)
async def get_company(
    stock_code: str,
    db: Session = Depends(get_db)
):
    """
    企業詳細情報取得

    - 銘柄コードで企業情報を取得
    """
    company = db.query(Company).filter(
        Company.stock_code == stock_code
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Company with stock code {stock_code} not found"
        )

    return company


@router.post("/", response_model=CompanyResponse)
async def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    """
    企業登録

    - 新規企業をデータベースに登録
    """
    # 既存チェック
    existing = db.query(Company).filter(
        Company.stock_code == company.stock_code
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Company with stock code {company.stock_code} already exists"
        )

    # 新規作成
    db_company = Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


@router.get("/{stock_code}/stock-prices", response_model=StockPriceResponse)
async def get_stock_prices(
    stock_code: str,
    period: str = Query("1mo", description="期間 (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y)")
):
    """
    株価データ取得

    - Yahoo Finance から株価データを取得
    - 期間指定可能
    """
    # 株価データ取得
    stock_data = yfinance_client.get_stock_data_dict(stock_code, period)

    if not stock_data:
        raise HTTPException(
            status_code=404,
            detail=f"Stock price data for {stock_code} not found"
        )

    return {
        "stock_code": stock_code,
        "period": period,
        "data": stock_data
    }
