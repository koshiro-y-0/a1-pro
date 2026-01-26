"""
Portfolio API Endpoints
ポートフォリオ関連のAPIエンドポイント
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.portfolio import Portfolio
from app.models.company import Company
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioResponse,
    PortfolioWithPerformance
)
from app.services.yfinance_client import yfinance_client
from app.services.portfolio_calculator import portfolio_calculator

router = APIRouter()


@router.get("/", response_model=List[PortfolioWithPerformance])
async def get_portfolio(db: Session = Depends(get_db)):
    """
    ポートフォリオ一覧取得

    - 全保有銘柄を取得
    - 現在価格とパフォーマンスを計算
    """
    portfolio_items = db.query(Portfolio).all()

    result = []
    for item in portfolio_items:
        # 現在価格を取得
        current_price = None
        company_name = None

        if item.asset_type == "jp_stock":
            # 日本株の場合
            stock_data = yfinance_client.get_stock_data_dict(item.symbol, period="1d")
            if stock_data:
                current_price = stock_data[-1]["close"]

            # 企業名取得
            company = db.query(Company).filter(Company.stock_code == item.symbol).first()
            if company:
                company_name = company.name

        elif item.asset_type == "us_stock":
            # 米国株の場合
            stock_data = yfinance_client.get_stock_data_dict(item.symbol, period="1d")
            if stock_data:
                current_price = stock_data[-1]["close"]
            company_name = item.symbol

        # パフォーマンス計算
        current_value = None
        profit_loss = None
        profit_loss_percentage = None

        if current_price:
            current_value = current_price * item.quantity
            purchase_value = item.purchase_price * item.quantity
            profit_loss = current_value - purchase_value
            profit_loss_percentage = (profit_loss / purchase_value) * 100

        result.append({
            **item.__dict__,
            "current_price": current_price,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_percentage,
            "company_name": company_name
        })

    return result


@router.post("/", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db)
):
    """
    保有銘柄追加

    - 新しい保有銘柄を登録
    """
    # 新規作成
    db_portfolio = Portfolio(**portfolio.model_dump())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)

    return db_portfolio


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
async def update_portfolio(
    portfolio_id: int,
    portfolio: PortfolioUpdate,
    db: Session = Depends(get_db)
):
    """
    保有銘柄更新

    - 既存の保有銘柄情報を更新
    """
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio item not found")

    # 更新
    update_data = portfolio.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_portfolio, key, value)

    db.commit()
    db.refresh(db_portfolio)

    return db_portfolio


@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    保有銘柄削除

    - 既存の保有銘柄を削除
    """
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio item not found")

    db.delete(db_portfolio)
    db.commit()

    return {"message": "Portfolio item deleted successfully"}


@router.get("/performance")
async def get_portfolio_performance(db: Session = Depends(get_db)):
    """
    ポートフォリオ全体のパフォーマンス取得

    - 総投資額、総評価額、総損益を計算
    - 資産クラス別アロケーション情報を返却
    """
    summary = portfolio_calculator.calculate_portfolio_summary(db)

    return summary
