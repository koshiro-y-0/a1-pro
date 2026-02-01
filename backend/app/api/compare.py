"""
Compare API
複数資産比較APIエンドポイント
"""

from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timedelta

from app.schemas.compare import (
    CompareRequest,
    CompareResponse,
    AssetPerformance,
    DataPoint
)
from app.services.yfinance_client import yfinance_client
from app.services.crypto_client import crypto_client
from app.services.exchange_rate_client import exchange_rate_client
from app.services.performance_calculator import performance_calculator


router = APIRouter()


@router.post("/compare", response_model=CompareResponse)
async def compare_assets(request: CompareRequest):
    """
    複数資産のパフォーマンス比較

    Args:
        request: 比較リクエスト

    Returns:
        比較結果
    """
    if len(request.assets) < 1:
        raise HTTPException(status_code=400, detail="At least one asset is required")

    if len(request.assets) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 assets allowed")

    # 期間設定
    period = request.period or "1y"

    # データ取得
    assets_data = []

    for asset in request.assets:
        try:
            data = await _get_asset_data(
                symbol=asset.symbol,
                asset_type=asset.asset_type,
                period=period
            )

            if not data:
                continue

            # 価格リスト作成
            prices = [point["price"] for point in data]
            dates = [point["date"] for point in data]

            if not prices:
                continue

            # 正規化
            normalized_prices = performance_calculator.normalize_prices(prices)

            # メトリクス計算
            metrics = performance_calculator.calculate_metrics(prices)

            # データポイント作成
            data_points = []
            for i, (date, price, norm_price) in enumerate(zip(dates, prices, normalized_prices)):
                data_points.append(DataPoint(
                    date=date,
                    value=price,
                    normalized_value=norm_price
                ))

            # 表示名を設定
            display_name = asset.name or asset.symbol

            assets_data.append(AssetPerformance(
                symbol=asset.symbol,
                asset_type=asset.asset_type,
                name=display_name,
                data=data_points,
                total_return=metrics["total_return"],
                volatility=metrics["volatility"],
                max_drawdown=metrics["max_drawdown"]
            ))

        except Exception as e:
            print(f"Error processing {asset.symbol}: {e}")
            continue

    if not assets_data:
        raise HTTPException(status_code=404, detail="No data found for any assets")

    # 期間情報
    all_dates = [point.date for asset in assets_data for point in asset.data]
    start_date = min(all_dates) if all_dates else datetime.now().strftime("%Y-%m-%d")
    end_date = max(all_dates) if all_dates else datetime.now().strftime("%Y-%m-%d")

    # ランキング作成
    ranking_data = [
        {
            "symbol": asset.symbol,
            "name": asset.name,
            "asset_type": asset.asset_type,
            "total_return": asset.total_return,
            "volatility": asset.volatility,
            "max_drawdown": asset.max_drawdown
        }
        for asset in assets_data
    ]
    ranking = performance_calculator.create_ranking(ranking_data)

    return CompareResponse(
        assets=assets_data,
        start_date=start_date,
        end_date=end_date,
        ranking=ranking
    )


async def _get_asset_data(symbol: str, asset_type: str, period: str) -> List[dict]:
    """
    資産データ取得

    Args:
        symbol: シンボル
        asset_type: 資産クラス
        period: 期間

    Returns:
        価格データ
    """
    if asset_type == "crypto":
        # 暗号資産の場合、期間を日数に変換
        days_map = {
            "1mo": 30,
            "3mo": 90,
            "6mo": 180,
            "1y": 365,
            "5y": 1825
        }
        days = days_map.get(period, 365)

        # CoinGecko ID取得（簡易マッピング）
        crypto_id_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "XRP": "ripple",
            "ADA": "cardano",
            "SOL": "solana"
        }
        crypto_id = crypto_id_map.get(symbol.upper(), symbol.lower())

        historical_data = crypto_client.get_historical_data(
            crypto_id=crypto_id,
            vs_currency="usd",
            days=days
        )

        return [{"date": item["date"], "price": item["price"]} for item in historical_data]

    elif asset_type == "fx":
        # 為替の場合
        # シンボルからbase/targetを抽出 (例: USD/JPY -> USD, JPY)
        if "/" in symbol:
            base, target = symbol.split("/")
        else:
            # USDJPY形式の場合
            base = symbol[:3]
            target = symbol[3:]

        days_map = {
            "1mo": 30,
            "3mo": 90,
            "6mo": 180,
            "1y": 365,
            "5y": 1825
        }
        days = days_map.get(period, 365)

        historical_data = exchange_rate_client.get_historical_rates(
            base_currency=base,
            target_currency=target,
            days=days
        )

        return [{"date": item["date"], "price": item["rate"]} for item in historical_data]

    else:
        # 株式（日本株・米国株）の場合
        df = yfinance_client.get_stock_data(
            stock_code=symbol,
            period=period,
            interval="1d",
            asset_type=asset_type
        )

        if df is None or df.empty:
            return []

        result = []
        for index, row in df.iterrows():
            result.append({
                "date": index.strftime("%Y-%m-%d"),
                "price": float(row["Close"])
            })

        return result
