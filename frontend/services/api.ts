/**
 * API Client
 * バックエンドAPIとの通信クライアント
 */

import axios from "axios";
import { Company, CompanySearchResult } from "@/types/company";
import { FinancialData } from "@/types/financial";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Companies API
export const companiesApi = {
  search: async (query: string, limit: number = 20): Promise<CompanySearchResult[]> => {
    const response = await apiClient.get("/api/companies/search", {
      params: { q: query, limit },
    });
    return response.data;
  },

  get: async (stockCode: string): Promise<Company> => {
    const response = await apiClient.get(`/api/companies/${stockCode}`);
    return response.data;
  },

  getFinancials: async (stockCode: string): Promise<FinancialData[]> => {
    const response = await apiClient.get(`/api/companies/${stockCode}/financials`);
    return response.data;
  },
};

export default apiClient;
