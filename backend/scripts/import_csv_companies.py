"""
CSVファイルから銘柄をインポート
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.company import Company
from datetime import datetime

def import_companies_from_csv(csv_path: str):
    """
    CSVファイルから銘柄を登録
    """
    db: Session = SessionLocal()

    try:
        # CSVを読み込み
        print(f"CSVファイルを読み込み中: {csv_path}")
        df = pd.read_csv(csv_path)

        print(f"読み込んだ銘柄数: {len(df)}")

        inserted_count = 0
        skipped_count = 0

        # DataFrameを処理
        for index, row in df.iterrows():
            stock_code = str(row['stock_code']).strip()
            name = str(row['name']).strip()
            industry = str(row['industry']).strip() if pd.notna(row['industry']) else None

            # 4桁の銘柄コードに正規化
            try:
                stock_code = str(int(float(stock_code))).zfill(4)
            except:
                print(f"警告: 無効な銘柄コード: {stock_code}")
                continue

            # 既存チェック
            existing = db.query(Company).filter(
                Company.stock_code == stock_code
            ).first()

            if existing:
                skipped_count += 1
                continue

            # 新規登録
            company = Company(
                stock_code=stock_code,
                name=name,
                industry=industry,
                description=None,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            db.add(company)
            inserted_count += 1

            # 100件ごとにコミット
            if inserted_count % 100 == 0:
                db.commit()
                print(f"{inserted_count}件登録完了...")

        # 最終コミット
        db.commit()

        print(f"\n登録完了:")
        print(f"  新規登録: {inserted_count}件")
        print(f"  スキップ: {skipped_count}件")
        print(f"  合計: {inserted_count + skipped_count}件")

    except Exception as e:
        db.rollback()
        print(f"エラーが発生しました: {e}")
        raise

    finally:
        db.close()

def main():
    csv_path = os.path.join(os.path.dirname(__file__), 'prime_companies.csv')

    print("東証プライム銘柄のインポートを開始します...\n")
    import_companies_from_csv(csv_path)
    print("\n完了しました！")

if __name__ == "__main__":
    main()
