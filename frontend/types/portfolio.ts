/**
 * Portfolio Types
 * ポートフォリオ関連の型定義
 */

export interface Portfolio {
  id: number;
  asset_type: string;
  symbol: string;
  purchase_date: string;
  purchase_price: number;
  quantity: number;
  created_at: string;
}

export interface PortfolioWithPerformance extends Portfolio {
  current_price: number | null;
  current_value: number | null;
  profit_loss: number | null;
  profit_loss_percentage: number | null;
  company_name: string | null;
}

export interface PortfolioCreate {
  asset_type: string;
  symbol: string;
  purchase_date: string;
  purchase_price: number;
  quantity: number;
}

export interface PortfolioUpdate {
  purchase_date?: string;
  purchase_price?: number;
  quantity?: number;
}

export interface PortfolioPerformance {
  total_purchase_value: number;
  total_current_value: number;
  total_profit_loss: number;
  total_profit_loss_percentage: number;
  asset_allocation: {
    [key: string]: {
      purchase_value: number;
      current_value: number;
      count: number;
      allocation_percentage: number;
    };
  };
  total_items: number;
}

export interface Favorite {
  id: number;
  company_id: number;
  created_at: string;
}

export interface FavoriteWithCompany extends Favorite {
  stock_code: string;
  company_name: string;
  industry: string | null;
}

export interface FavoriteCreate {
  company_id: number;
}
