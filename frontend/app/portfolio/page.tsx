"use client";

import { useState, useEffect } from "react";
import { portfolioApi } from "@/services/api";
import {
  PortfolioWithPerformance,
  PortfolioPerformance,
} from "@/types/portfolio";
import Link from "next/link";
import Loading from "@/components/Loading";
import PageTransition from "@/components/PageTransition";
import MobileMenu from "@/components/MobileMenu";

export default function PortfolioPage() {
  const [portfolio, setPortfolio] = useState<PortfolioWithPerformance[]>([]);
  const [performance, setPerformance] = useState<PortfolioPerformance | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [portfolioData, performanceData] = await Promise.all([
        portfolioApi.getAll(),
        portfolioApi.getPerformance(),
      ]);
      setPortfolio(portfolioData);
      setPerformance(performanceData);
    } catch (error) {
      console.error("Failed to fetch portfolio data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("この銘柄を削除してもよろしいですか？")) return;

    try {
      await portfolioApi.delete(id);
      fetchData();
    } catch (error) {
      console.error("Failed to delete portfolio item:", error);
    }
  };

  const formatCurrency = (value: number | null) => {
    if (value === null) return "N/A";
    return value.toLocaleString("ja-JP", {
      style: "currency",
      currency: "JPY",
    });
  };

  const formatPercentage = (value: number | null) => {
    if (value === null) return "N/A";
    const sign = value >= 0 ? "+" : "";
    return `${sign}${value.toFixed(2)}%`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <MobileMenu />
      <div className="container mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8 animate-fadeInDown">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">ポートフォリオ</h1>
            <p className="text-gray-600 mt-1">保有銘柄とパフォーマンス</p>
          </div>
          <Link
            href="/"
            className="btn btn-primary"
          >
            ホームに戻る
          </Link>
        </div>

        {isLoading ? (
          <Loading text="読み込み中..." />
        ) : (
          <PageTransition>
            {/* Performance Summary */}
            {performance && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div className="card card-hover p-6">
                  <p className="text-sm text-gray-600 mb-1">総投資額</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatCurrency(performance.total_purchase_value)}
                  </p>
                </div>
                <div className="card card-hover p-6">
                  <p className="text-sm text-gray-600 mb-1">現在評価額</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatCurrency(performance.total_current_value)}
                  </p>
                </div>
                <div className="card card-hover p-6">
                  <p className="text-sm text-gray-600 mb-1">損益</p>
                  <p
                    className={`text-2xl font-bold ${
                      performance.total_profit_loss >= 0
                        ? "text-green-600"
                        : "text-red-600"
                    }`}
                  >
                    {formatCurrency(performance.total_profit_loss)}
                  </p>
                </div>
                <div className="card card-hover p-6">
                  <p className="text-sm text-gray-600 mb-1">損益率</p>
                  <p
                    className={`text-2xl font-bold ${
                      performance.total_profit_loss_percentage >= 0
                        ? "text-green-600"
                        : "text-red-600"
                    }`}
                  >
                    {formatPercentage(performance.total_profit_loss_percentage)}
                  </p>
                </div>
              </div>
            )}

            {/* Portfolio Table */}
            <div className="card overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">
                  保有銘柄一覧
                </h2>
              </div>

              {portfolio.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  保有銘柄がありません
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          銘柄
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                          購入日
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          数量
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          購入価格
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          現在価格
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          評価額
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          損益
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                          損益率
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                          操作
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {portfolio.map((item) => (
                        <tr key={item.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4">
                            <div>
                              <p className="font-medium text-gray-900">
                                {item.symbol}
                              </p>
                              {item.company_name && (
                                <p className="text-sm text-gray-500">
                                  {item.company_name}
                                </p>
                              )}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-900">
                            {item.purchase_date}
                          </td>
                          <td className="px-6 py-4 text-right text-sm text-gray-900">
                            {item.quantity.toLocaleString()}
                          </td>
                          <td className="px-6 py-4 text-right text-sm text-gray-900">
                            {formatCurrency(item.purchase_price)}
                          </td>
                          <td className="px-6 py-4 text-right text-sm text-gray-900">
                            {formatCurrency(item.current_price)}
                          </td>
                          <td className="px-6 py-4 text-right text-sm text-gray-900">
                            {formatCurrency(item.current_value)}
                          </td>
                          <td
                            className={`px-6 py-4 text-right text-sm font-medium ${
                              item.profit_loss && item.profit_loss >= 0
                                ? "text-green-600"
                                : "text-red-600"
                            }`}
                          >
                            {formatCurrency(item.profit_loss)}
                          </td>
                          <td
                            className={`px-6 py-4 text-right text-sm font-medium ${
                              item.profit_loss_percentage &&
                              item.profit_loss_percentage >= 0
                                ? "text-green-600"
                                : "text-red-600"
                            }`}
                          >
                            {formatPercentage(item.profit_loss_percentage)}
                          </td>
                          <td className="px-6 py-4 text-center">
                            <button
                              onClick={() => handleDelete(item.id)}
                              className="btn btn-danger text-sm"
                            >
                              削除
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </PageTransition>
        )}
      </div>
    </div>
  );
}
