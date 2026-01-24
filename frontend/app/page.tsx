"use client";

import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import CompanyInfo from "@/components/CompanyInfo";
import { CompanySearchResult, Company } from "@/types/company";
import { companiesApi } from "@/services/api";

export default function Home() {
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSelectCompany = async (searchResult: CompanySearchResult) => {
    setIsLoading(true);
    try {
      const company = await companiesApi.get(searchResult.stock_code);
      setSelectedCompany(company);
    } catch (error) {
      console.error("Failed to fetch company:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">A1-PRO</h1>
          <p className="text-lg text-gray-600">日本株分析Webアプリケーション</p>
        </div>

        {/* Search Bar */}
        <div className="flex justify-center mb-8">
          <SearchBar onSelectCompany={handleSelectCompany} />
        </div>

        {/* Loading */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full"></div>
            <p className="mt-4 text-gray-600">読み込み中...</p>
          </div>
        )}

        {/* Company Info */}
        {!isLoading && selectedCompany && (
          <div className="max-w-4xl mx-auto">
            <CompanyInfo company={selectedCompany} />
          </div>
        )}

        {/* Welcome Message */}
        {!isLoading && !selectedCompany && (
          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-8 text-center">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              ようこそ
            </h2>
            <p className="text-gray-700 mb-4">
              銘柄コードまたは企業名を入力して、企業情報を検索できます。
            </p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-800">
                <strong>Phase 2 実装完了:</strong> 銘柄検索機能、企業情報表示
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
