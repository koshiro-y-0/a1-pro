/**
 * Compare Types
 * 複数資産比較用の型定義
 */

export interface AssetSymbol {
  symbol: string;
  asset_type: "jp_stock" | "us_stock" | "crypto" | "fx";
  name?: string;
}

export interface CompareRequest {
  assets: AssetSymbol[];
  start_date?: string;
  period?: "1mo" | "3mo" | "6mo" | "1y" | "5y";
}

export interface DataPoint {
  date: string;
  value: number;
  normalized_value: number;
}

export interface AssetPerformance {
  symbol: string;
  asset_type: string;
  name: string;
  data: DataPoint[];
  total_return: number;
  volatility: number | null;
  max_drawdown: number | null;
}

export interface RankingItem {
  rank: number;
  symbol: string;
  name: string;
  asset_type: string;
  total_return: number;
  volatility: number | null;
  max_drawdown: number | null;
}

export interface CompareResponse {
  assets: AssetPerformance[];
  start_date: string;
  end_date: string;
  ranking: RankingItem[];
}
