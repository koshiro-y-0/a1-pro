/**
 * Company Types
 * 企業関連の型定義
 */

export interface Company {
  id: number;
  stock_code: string;
  name: string;
  industry: string | null;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface CompanySearchResult {
  id: number;
  stock_code: string;
  name: string;
  industry: string | null;
}
