/**
 * Chat Types
 * チャット関連の型定義
 */

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  sources?: ChatSource[];
}

export interface ChatSource {
  text: string;
  metadata: {
    stock_code?: string;
    company_name?: string;
    type?: string;
    fiscal_year?: number;
  };
}

export interface ChatRequest {
  question: string;
  stock_code?: string;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}
