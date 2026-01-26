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
from app.schemas.financial_data import FinancialDataResponse, FinancialDataWithMetrics, CombinedDataResponse
from app.services.yfinance_client import yfinance_client
from app.services.financial_calculator import financial_calculator
from app.models.financial_data import FinancialData

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


@router.get("/{stock_code}/financials", response_model=List[FinancialDataWithMetrics])
async def get_financials(
    stock_code: str,
    db: Session = Depends(get_db)
):
    """
    決算データ取得

    - 企業の過去の決算データを取得
    - 財務指標も自動計算して返却
    """
    # 企業を検索
    company = db.query(Company).filter(
        Company.stock_code == stock_code
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Company with stock code {stock_code} not found"
        )

    # 決算データ取得（通期のみ、fiscal_quarter is null）
    financial_data_list = db.query(FinancialData).filter(
        FinancialData.company_id == company.id,
        FinancialData.fiscal_quarter.is_(None)
    ).order_by(FinancialData.fiscal_year.desc()).limit(10).all()

    # 財務指標を計算して追加
    result = []
    for fd in financial_data_list:
        metrics = financial_calculator.calculate_all_metrics(
            revenue=fd.revenue,
            operating_profit=fd.operating_profit,
            net_profit=fd.net_profit,
            total_assets=fd.total_assets,
            equity=fd.equity,
            total_liabilities=fd.total_liabilities,
            current_assets=fd.current_assets,
            current_liabilities=fd.current_liabilities
        )

        result.append({
            **fd.__dict__,
            "metrics": metrics
        })

    return result


@router.get("/{stock_code}/combined", response_model=List[CombinedDataResponse])
async def get_combined_data(
    stock_code: str,
    db: Session = Depends(get_db)
):
    """
    複合データ取得

    - 決算データと株価データを組み合わせて返却
    - 売上高、経常利益、株価（期末）を年度ごとに取得
    """
    # 企業を検索
    company = db.query(Company).filter(
        Company.stock_code == stock_code
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Company with stock code {stock_code} not found"
        )

    # 決算データ取得（通期のみ）
    financial_data_list = db.query(FinancialData).filter(
        FinancialData.company_id == company.id,
        FinancialData.fiscal_quarter.is_(None)
    ).order_by(FinancialData.fiscal_year.desc()).limit(10).all()

    # 株価データ取得（過去5年分）
    stock_data = yfinance_client.get_stock_data_dict(stock_code, period="5y")

    # 年度ごとの期末株価を抽出（3月末を想定）
    stock_price_by_year = {}
    for data in stock_data:
        # 日付から年度を計算（3月末決算を想定）
        from datetime import datetime
        date = datetime.strptime(data["date"], "%Y-%m-%d")
        # 3月末付近のデータを各年度の代表値とする
        if date.month == 3:
            year = date.year
            stock_price_by_year[year] = data["close"]

    # 決算データと株価を結合
    result = []
    for fd in financial_data_list:
        # fiscal_year が YYYY-MM-DD 形式の場合、年を抽出
        fiscal_year = fd.fiscal_year
        year = int(fiscal_year[:4]) if isinstance(fiscal_year, str) else fiscal_year

        result.append({
            "fiscal_year": fd.fiscal_year,
            "revenue": fd.revenue,
            "ordinary_profit": fd.ordinary_profit,
            "stock_price": stock_price_by_year.get(year)
        })

    return result
