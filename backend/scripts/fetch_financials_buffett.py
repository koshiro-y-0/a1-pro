"""
バフェット・コードAPIを使用して決算データを取得
API制限: 月500リクエスト
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import time
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.company import Company
from app.models.financial_data import FinancialData
from datetime import datetime

# 環境変数からAPIキーを取得
BUFFETT_CODE_API_KEY = os.getenv('BUFFETT_CODE_API_KEY', '')
BASE_URL = "https://api.buffett-code.com/api/v3"

def fetch_company_financials(stock_code: str, api_key: str):
    """
    バフェット・コードAPIから決算データを取得
    """
    if not api_key:
        print("警告: BUFFETT_CODE_API_KEY が設定されていません")
        return None

    url = f"{BASE_URL}/quarter"
    headers = {"x-api-key": api_key}
    params = {"ticker": stock_code}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 404:
            print(f"  銘柄 {stock_code}: データなし")
            return None
        else:
            print(f"  エラー {response.status_code}: {stock_code}")
            return None

    except Exception as e:
        print(f"  例外発生 {stock_code}: {e}")
        return None

def insert_financial_data(db: Session, company: Company, financial_json: dict):
    """
    取得したデータをDBに登録
    """
    if not financial_json or 'data' not in financial_json:
        return 0

    inserted_count = 0

    for item in financial_json['data']:
        fiscal_year = item.get('fiscal_year')
        fiscal_quarter = item.get('fiscal_quarter')

        # 通期のみ対象（fiscal_quarter = 0）
        if fiscal_quarter != 0:
            continue

        # 既存チェック
        existing = db.query(FinancialData).filter(
            FinancialData.company_id == company.id,
            FinancialData.fiscal_year == fiscal_year,
            FinancialData.fiscal_quarter.is_(None)
        ).first()

        if existing:
            continue

        # データ作成
        financial_data = FinancialData(
            company_id=company.id,
            fiscal_year=fiscal_year,
            fiscal_quarter=None,  # 通期
            revenue=item.get('sales') or item.get('net_sales'),
            operating_profit=item.get('operating_income'),
            ordinary_profit=item.get('ordinary_income'),
            net_profit=item.get('net_income'),
            total_assets=item.get('total_assets'),
            equity=item.get('equity'),
            total_liabilities=item.get('total_liabilities'),
            current_assets=item.get('current_assets'),
            current_liabilities=item.get('current_liabilities'),
            created_at=datetime.now()
        )

        db.add(financial_data)
        inserted_count += 1

    return inserted_count

def main():
    """
    メイン処理
    """
    db: Session = SessionLocal()

    try:
        # APIキーチェック
        if not BUFFETT_CODE_API_KEY:
            print("エラー: 環境変数 BUFFETT_CODE_API_KEY が設定されていません")
            print("\n使用方法:")
            print("export BUFFETT_CODE_API_KEY='your_api_key_here'")
            print("python scripts/fetch_financials_buffett.py")
            return

        # 決算データがない企業を取得
        companies = db.query(Company).outerjoin(FinancialData).filter(
            FinancialData.id.is_(None)
        ).limit(100).all()  # 一度に100社まで

        print(f"決算データ取得対象: {len(companies)}社")
        print(f"API制限: 月500リクエスト\n")

        total_inserted = 0
        success_count = 0
        fail_count = 0

        for index, company in enumerate(companies, 1):
            print(f"[{index}/{len(companies)}] {company.stock_code} {company.name}")

            # APIリクエスト
            financial_json = fetch_company_financials(company.stock_code, BUFFETT_CODE_API_KEY)

            if financial_json:
                # データ登録
                inserted = insert_financial_data(db, company, financial_json)
                if inserted > 0:
                    db.commit()
                    total_inserted += inserted
                    success_count += 1
                    print(f"  ✓ {inserted}年分のデータを登録")
                else:
                    print(f"  - データなし")
            else:
                fail_count += 1

            # API制限対策: 1秒待機
            if index < len(companies):
                time.sleep(1)

        print(f"\n完了:")
        print(f"  成功: {success_count}社")
        print(f"  失敗: {fail_count}社")
        print(f"  登録データ数: {total_inserted}件")

    except Exception as e:
        db.rollback()
        print(f"\nエラーが発生しました: {e}")
        raise

    finally:
        db.close()

if __name__ == "__main__":
    main()
