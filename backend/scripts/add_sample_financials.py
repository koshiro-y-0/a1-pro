"""
日経225主要銘柄にサンプル決算データを追加
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.company import Company
from app.models.financial_data import FinancialData
from datetime import datetime
import random

def generate_sample_financials(company_id: int, base_revenue: int, industry: str):
    """
    業種に応じたサンプル決算データを生成
    """
    financials = []

    # 業種ごとの利益率設定
    if industry in ['電気機器', '情報・通信業']:
        operating_margin = 0.10  # 10%
        net_margin = 0.07
    elif industry in ['医薬品', '化学']:
        operating_margin = 0.15
        net_margin = 0.10
    elif industry in ['小売業', '卸売業']:
        operating_margin = 0.05
        net_margin = 0.03
    elif industry in ['建設業', '不動産業']:
        operating_margin = 0.08
        net_margin = 0.05
    elif industry in ['輸送用機器', '機械']:
        operating_margin = 0.09
        net_margin = 0.06
    elif industry in ['銀行業', '保険業', 'その他金融業']:
        operating_margin = 0.20
        net_margin = 0.12
    else:
        operating_margin = 0.08
        net_margin = 0.05

    # 5年分のデータ生成
    for year in range(2019, 2024):
        # 年ごとに売上を増加（95-110%の範囲でランダム）
        growth = random.uniform(0.95, 1.10)
        revenue = int(base_revenue * growth * ((year - 2018) * 0.05 + 1))

        operating_profit = int(revenue * operating_margin)
        ordinary_profit = int(operating_profit * 1.05)
        net_profit = int(revenue * net_margin)

        # バランスシートデータ
        total_assets = int(revenue * 1.2)
        equity = int(total_assets * 0.40)
        total_liabilities = total_assets - equity
        current_assets = int(total_assets * 0.50)
        current_liabilities = int(total_liabilities * 0.60)

        financials.append({
            'company_id': company_id,
            'fiscal_year': year,
            'fiscal_quarter': None,
            'revenue': revenue,
            'operating_profit': operating_profit,
            'ordinary_profit': ordinary_profit,
            'net_profit': net_profit,
            'total_assets': total_assets,
            'equity': equity,
            'total_liabilities': total_liabilities,
            'current_assets': current_assets,
            'current_liabilities': current_liabilities,
            'created_at': datetime.now()
        })

    return financials

def main():
    db: Session = SessionLocal()

    try:
        # 決算データがない企業を取得（優先度順）
        companies = db.query(Company).outerjoin(FinancialData).filter(
            FinancialData.id.is_(None)
        ).limit(30).all()

        print(f"サンプル決算データ追加対象: {len(companies)}社\n")

        total_inserted = 0

        for idx, company in enumerate(companies, 1):
            print(f"[{idx}/{len(companies)}] {company.stock_code} {company.name} ({company.industry})")

            # 業種に応じた基準売上を設定
            if company.industry in ['銀行業', '保険業', 'その他金融業']:
                base_revenue = random.randint(300000000000, 1000000000000)  # 3000億-1兆
            elif company.industry in ['電気機器', '輸送用機器']:
                base_revenue = random.randint(500000000000, 3000000000000)  # 5000億-3兆
            elif company.industry in ['小売業', '卸売業']:
                base_revenue = random.randint(1000000000000, 5000000000000)  # 1兆-5兆
            elif company.industry in ['医薬品', '化学']:
                base_revenue = random.randint(200000000000, 1500000000000)  # 2000億-1.5兆
            else:
                base_revenue = random.randint(100000000000, 1000000000000)  # 1000億-1兆

            # サンプルデータ生成
            financials = generate_sample_financials(company.id, base_revenue, company.industry or 'その他')

            # データベースに登録
            for financial in financials:
                fd = FinancialData(**financial)
                db.add(fd)

            total_inserted += len(financials)
            print(f"  ✓ {len(financials)}年分のデータを追加")

            # 10社ごとにコミット
            if idx % 10 == 0:
                db.commit()
                print(f"\n中間コミット: {idx}社完了\n")

        # 最終コミット
        db.commit()

        print(f"\n完了:")
        print(f"  対象企業: {len(companies)}社")
        print(f"  登録データ数: {total_inserted}件")

    except Exception as e:
        db.rollback()
        print(f"\nエラーが発生しました: {e}")
        raise

    finally:
        db.close()

if __name__ == "__main__":
    main()
