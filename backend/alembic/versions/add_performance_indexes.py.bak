"""add performance indexes

Revision ID: add_performance_indexes
Revises:
Create Date: 2026-02-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_performance_indexes'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """パフォーマンス最適化のためのインデックス追加"""

    # companies テーブル
    op.create_index('idx_companies_stock_code', 'companies', ['stock_code'])
    op.create_index('idx_companies_name', 'companies', ['name'])

    # financial_data テーブル
    op.create_index('idx_financial_data_company_id', 'financial_data', ['company_id'])
    op.create_index('idx_financial_data_fiscal_year', 'financial_data', ['fiscal_year'])
    op.create_index('idx_financial_data_company_year', 'financial_data', ['company_id', 'fiscal_year'])

    # stock_prices テーブル
    op.create_index('idx_stock_prices_company_id', 'stock_prices', ['company_id'])
    op.create_index('idx_stock_prices_date', 'stock_prices', ['date'])
    op.create_index('idx_stock_prices_company_date', 'stock_prices', ['company_id', 'date'])

    # portfolio テーブル
    op.create_index('idx_portfolio_asset_type', 'portfolio', ['asset_type'])
    op.create_index('idx_portfolio_symbol', 'portfolio', ['symbol'])

    # favorites テーブル
    op.create_index('idx_favorites_company_id', 'favorites', ['company_id'])


def downgrade():
    """インデックス削除"""

    # companies テーブル
    op.drop_index('idx_companies_stock_code', table_name='companies')
    op.drop_index('idx_companies_name', table_name='companies')

    # financial_data テーブル
    op.drop_index('idx_financial_data_company_id', table_name='financial_data')
    op.drop_index('idx_financial_data_fiscal_year', table_name='financial_data')
    op.drop_index('idx_financial_data_company_year', table_name='financial_data')

    # stock_prices テーブル
    op.drop_index('idx_stock_prices_company_id', table_name='stock_prices')
    op.drop_index('idx_stock_prices_date', table_name='stock_prices')
    op.drop_index('idx_stock_prices_company_date', table_name='stock_prices')

    # portfolio テーブル
    op.drop_index('idx_portfolio_asset_type', table_name='portfolio')
    op.drop_index('idx_portfolio_symbol', table_name='portfolio')

    # favorites テーブル
    op.drop_index('idx_favorites_company_id', table_name='favorites')
