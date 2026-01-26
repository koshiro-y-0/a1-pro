/**
 * Financial Data Types
 * 決算データ関連の型定義
 */

export interface FinancialMetrics {
  equity_ratio: number | null;
  current_ratio: number | null;
  debt_ratio: number | null;
  roe: number | null;
  operating_margin: number | null;
}

export interface FinancialData {
  id: number;
  company_id: number;
  fiscal_year: number;
  fiscal_quarter: number | null;
  revenue: number | null;
  operating_profit: number | null;
  ordinary_profit: number | null;
  net_profit: number | null;
  total_assets: number | null;
  equity: number | null;
  total_liabilities: number | null;
  current_assets: number | null;
  current_liabilities: number | null;
  created_at: string;
  metrics: FinancialMetrics;
}

export interface CombinedData {
  fiscal_year: number;
  revenue: number | null;
  ordinary_profit: number | null;
  stock_price: number | null;
}
