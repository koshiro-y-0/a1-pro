"use client";

import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import CompanyInfo from "@/components/CompanyInfo";
import FinancialTable from "@/components/FinancialTable";
import RevenueChart from "@/components/charts/RevenueChart";
import OperatingProfitChart from "@/components/charts/OperatingProfitChart";
import NetProfitChart from "@/components/charts/NetProfitChart";
import EquityRatioChart from "@/components/charts/EquityRatioChart";
import CurrentRatioChart from "@/components/charts/CurrentRatioChart";
import ROEChart from "@/components/charts/ROEChart";
import OperatingMarginChart from "@/components/charts/OperatingMarginChart";
import CombinedChart from "@/components/charts/CombinedChart";
import FinancialHealthIndicator from "@/components/FinancialHealthIndicator";
import { CompanySearchResult, Company } from "@/types/company";
import { FinancialData, CombinedData } from "@/types/financial";
import { companiesApi } from "@/services/api";

export default function Home() {
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [financialData, setFinancialData] = useState<FinancialData[]>([]);
  const [combinedData, setCombinedData] = useState<CombinedData[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSelectCompany = async (searchResult: CompanySearchResult) => {
    setIsLoading(true);
    try {
      const [company, financials, combined] = await Promise.all([
        companiesApi.get(searchResult.stock_code),
        companiesApi.getFinancials(searchResult.stock_code),
        companiesApi.getCombinedData(searchResult.stock_code),
      ]);
      setSelectedCompany(company);
      setFinancialData(financials);
      setCombinedData(combined);
    } catch (error) {
      console.error("Failed to fetch company data:", error);
      setFinancialData([]);
      setCombinedData([]);
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

        {/* Company Data */}
        {!isLoading && selectedCompany && (
          <div className="max-w-7xl mx-auto space-y-6">
            {/* Company Info */}
            <CompanyInfo company={selectedCompany} />

            {/* Financial Health Indicator */}
            {financialData.length > 0 && (
              <FinancialHealthIndicator data={financialData} />
            )}

            {/* Charts */}
            {financialData.length > 0 && (
              <>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <RevenueChart data={financialData} />
                  <OperatingProfitChart data={financialData} />
                  <NetProfitChart data={financialData} />
                </div>

                {/* Financial Indicator Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <EquityRatioChart data={financialData} />
                  <CurrentRatioChart data={financialData} />
                  <ROEChart data={financialData} />
                  <OperatingMarginChart data={financialData} />
                </div>

                {/* Combined Chart */}
                {combinedData.length > 0 && (
                  <CombinedChart data={combinedData} />
                )}

                {/* Financial Table */}
                <FinancialTable data={financialData} />
              </>
            )}

            {financialData.length === 0 && (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <p className="text-gray-500">決算データが登録されていません</p>
              </div>
            )}
          </div>
        )}

        {/* Welcome Message */}
        {!isLoading && !selectedCompany && (
          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-8 text-center">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              ようこそ
            </h2>
            <p className="text-gray-700 mb-4">
              銘柄コードまたは企業名を入力して、企業情報や決算データを検索できます。
            </p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-800">
                <strong>Phase 2 完全実装:</strong> 銘柄検索、企業情報表示、決算データ、グラフ表示
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
