"use client";

import { FinancialData } from "@/types/financial";

interface FinancialTableProps {
  data: FinancialData[];
}

export default function FinancialTable({ data }: FinancialTableProps) {
  const formatNumber = (num: number | null) => {
    if (num === null) return "-";
    return (num / 100000000).toFixed(2) + "億円";
  };

  const formatPercent = (num: number | null) => {
    if (num === null) return "-";
    return num.toFixed(2) + "%";
  };

  const getHealthColor = (ratio: number | null, thresholds: { good: number; warning: number }) => {
    if (ratio === null) return "text-gray-500";
    if (ratio >= thresholds.good) return "text-success font-semibold";
    if (ratio >= thresholds.warning) return "text-warning font-semibold";
    return "text-danger font-semibold";
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-4">決算データ</h3>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                年度
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                売上高
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                営業利益
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                純利益
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                自己資本比率
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                ROE
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                営業利益率
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                  {item.fiscal_year}年
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700">
                  {formatNumber(item.revenue)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700">
                  {formatNumber(item.operating_profit)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700">
                  {formatNumber(item.net_profit)}
                </td>
                <td className={`px-4 py-3 whitespace-nowrap text-sm text-right ${getHealthColor(item.metrics.equity_ratio, { good: 40, warning: 20 })}`}>
                  {formatPercent(item.metrics.equity_ratio)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700">
                  {formatPercent(item.metrics.roe)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700">
                  {formatPercent(item.metrics.operating_margin)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {data.length === 0 && (
        <p className="text-center text-gray-500 py-8">決算データがありません</p>
      )}
    </div>
  );
}
