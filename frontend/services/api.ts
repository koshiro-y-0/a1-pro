/**
 * API Client
 * バックエンドAPIとの通信クライアント
 */

import axios from "axios";
import { Company, CompanySearchResult } from "@/types/company";
import { FinancialData, CombinedData } from "@/types/financial";
import { ChatRequest, ChatResponse } from "@/types/chat";

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

  getCombinedData: async (stockCode: string): Promise<CombinedData[]> => {
    const response = await apiClient.get(`/api/companies/${stockCode}/combined`);
    return response.data;
  },
};

// Chat API
export const chatApi = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await apiClient.post("/api/chat", request);
    return response.data;
  },

  createIndex: async (stockCode: string): Promise<{ message: string; chunks_count: number }> => {
    const response = await apiClient.post("/api/chat/index", { stock_code: stockCode });
    return response.data;
  },

  getStats: async (): Promise<{ total_documents: number; collection_name: string }> => {
    const response = await apiClient.get("/api/chat/stats");
    return response.data;
  },
};

export default apiClient;
