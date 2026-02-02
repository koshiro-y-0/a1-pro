"""
東証プライム銘柄の取得スクリプト
yfinance と jpx (日本取引所グループ) のデータを使用して銘柄リストを取得
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import requests
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.company import Company
from datetime import datetime

def fetch_jpx_listed_companies():
    """
    JPX (日本取引所グループ) から上場企業リストを取得
    """
    # JPXの上場企業リストCSV
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001dwl-att/data_j.xls"

    try:
        print("JPXから銘柄リストをダウンロード中...")
        df = pd.read_excel(url)

        # カラム名を確認して適切に処理
        print(f"取得したカラム: {df.columns.tolist()}")

        # プライム市場のみフィルター
        if '市場・商品区分' in df.columns:
            df_prime = df[df['市場・商品区分'].str.contains('プライム', na=False)]
        else:
            df_prime = df  # カラムがない場合は全て取得

        print(f"プライム市場の銘柄数: {len(df_prime)}")

        return df_prime

    except Exception as e:
        print(f"JPXからの取得に失敗: {e}")
        return None

def insert_companies_to_db(df: pd.DataFrame):
    """
    データベースに銘柄を登録
    """
    db: Session = SessionLocal()

    try:
        inserted_count = 0
        skipped_count = 0

        # DataFrameを処理
        for index, row in df.iterrows():
            # カラム名を柔軟に処理
            stock_code = None
            name = None
            industry = None

            # 銘柄コード取得
            if 'コード' in row:
                stock_code = str(row['コード']).strip()
            elif 'code' in row:
                stock_code = str(row['code']).strip()
            elif 'Code' in row:
                stock_code = str(row['Code']).strip()

            # 企業名取得
            if '銘柄名' in row:
                name = str(row['銘柄名']).strip()
            elif 'name' in row:
                name = str(row['name']).strip()
            elif 'Name' in row:
                name = str(row['Name']).strip()

            # 業種取得
            if '33業種区分' in row:
                industry = str(row['33業種区分']).strip()
            elif 'sector' in row:
                industry = str(row['sector']).strip()
            elif 'Sector' in row:
                industry = str(row['Sector']).strip()

            # 必須項目のチェック
            if not stock_code or not name:
                continue

            # 4桁の銘柄コードに正規化
            try:
                stock_code = str(int(float(stock_code))).zfill(4)
            except:
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
                industry=industry if industry and industry != 'nan' else None,
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

    except Exception as e:
        db.rollback()
        print(f"エラーが発生しました: {e}")
        raise

    finally:
        db.close()

def main():
    print("東証プライム銘柄の取得を開始します...\n")

    # JPXから取得を試みる
    df = fetch_jpx_listed_companies()

    if df is None or len(df) == 0:
        print("銘柄リストの取得に失敗しました")
        return

    # データベースに登録
    print("\nデータベースへの登録を開始します...")
    insert_companies_to_db(df)

    print("\n完了しました！")

if __name__ == "__main__":
    main()
