"use client";

import { useState } from "react";
import { compareApi } from "@/services/api";
import {
  AssetSymbol,
  CompareResponse,
  RankingItem,
} from "@/types/compare";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import Loading from "@/components/Loading";
import PageTransition from "@/components/PageTransition";
import MobileMenu from "@/components/MobileMenu";

const ASSET_TYPE_LABELS: Record<string, string> = {
  jp_stock: "日本株",
  us_stock: "米国株",
  crypto: "暗号資産",
  fx: "為替",
};

const PERIOD_OPTIONS = [
  { value: "1mo", label: "1ヶ月" },
  { value: "3mo", label: "3ヶ月" },
  { value: "6mo", label: "6ヶ月" },
  { value: "1y", label: "1年" },
  { value: "5y", label: "5年" },
];

const CHART_COLORS = [
  "#3B82F6", // 青
  "#10B981", // 緑
  "#F59E0B", // オレンジ
  "#8B5CF6", // 紫
  "#EF4444", // 赤
  "#06B6D4", // シアン
  "#F97316", // ディープオレンジ
  "#EC4899", // ピンク
  "#84CC16", // ライム
  "#6366F1", // インディゴ
];

export default function ComparePage() {
  const [assets, setAssets] = useState<AssetSymbol[]>([]);
  const [newAsset, setNewAsset] = useState<AssetSymbol>({
    symbol: "",
    asset_type: "jp_stock",
    name: "",
  });
  const [period, setPeriod] = useState<"1mo" | "3mo" | "6mo" | "1y" | "5y">("1y");
  const [compareResult, setCompareResult] = useState<CompareResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAddAsset = () => {
    if (!newAsset.symbol) {
      alert("シンボルを入力してください");
      return;
    }

    if (assets.length >= 10) {
      alert("最大10銘柄まで追加できます");
      return;
    }

    setAssets([...assets, { ...newAsset }]);
    setNewAsset({ symbol: "", asset_type: "jp_stock", name: "" });
  };

  const handleRemoveAsset = (index: number) => {
    setAssets(assets.filter((_, i) => i !== index));
  };

  const handleCompare = async () => {
    if (assets.length < 1) {
      alert("少なくとも1つの資産を追加してください");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await compareApi.compare({
        assets,
        period,
      });
      setCompareResult(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || "比較データの取得に失敗しました");
      console.error("Compare error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // チャート用データ変換
  const chartData = compareResult
    ? (() => {
        const dateMap = new Map<string, any>();

        compareResult.assets.forEach((asset) => {
          asset.data.forEach((point) => {
            if (!dateMap.has(point.date)) {
              dateMap.set(point.date, { date: point.date });
            }
            dateMap.get(point.date)![asset.symbol] = point.normalized_value;
          });
        });

        return Array.from(dateMap.values()).sort((a, b) =>
          a.date.localeCompare(b.date)
        );
      })()
    : [];

  return (
    <div className="min-h-screen bg-gray-50">
      <MobileMenu />
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold mb-8 animate-fadeInDown">資産パフォーマンス比較</h1>

        {/* 資産追加フォーム */}
        <div className="card p-6 mb-6 animate-fadeIn">
          <h2 className="text-xl font-semibold mb-4">資産を追加</h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                シンボル/銘柄コード
              </label>
              <input
                type="text"
                value={newAsset.symbol}
                onChange={(e) =>
                  setNewAsset({ ...newAsset, symbol: e.target.value })
                }
                placeholder="例: 7203, AAPL, BTC"
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                資産クラス
              </label>
              <select
                value={newAsset.asset_type}
                onChange={(e) =>
                  setNewAsset({
                    ...newAsset,
                    asset_type: e.target.value as any,
                  })
                }
                className="input"
              >
                <option value="jp_stock">日本株</option>
                <option value="us_stock">米国株</option>
                <option value="crypto">暗号資産</option>
                <option value="fx">為替</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                表示名（オプション）
              </label>
              <input
                type="text"
                value={newAsset.name || ""}
                onChange={(e) =>
                  setNewAsset({ ...newAsset, name: e.target.value })
                }
                placeholder="例: トヨタ"
                className="input"
              />
            </div>

            <div className="flex items-end">
              <button
                onClick={handleAddAsset}
                className="btn btn-primary w-full"
              >
                追加
              </button>
            </div>
          </div>

          {/* 追加された資産リスト */}
          {assets.length > 0 && (
            <div className="mt-4">
              <h3 className="text-sm font-medium text-gray-700 mb-2">
                追加済み資産 ({assets.length}/10)
              </h3>
              <div className="flex flex-wrap gap-2">
                {assets.map((asset, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-800 rounded-full"
                  >
                    <span className="text-sm">
                      {asset.name || asset.symbol} ({ASSET_TYPE_LABELS[asset.asset_type]})
                    </span>
                    <button
                      onClick={() => handleRemoveAsset(index)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* 期間選択と比較実行 */}
        <div className="card p-6 mb-6 animate-fadeIn">
          <div className="flex items-end gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                比較期間
              </label>
              <select
                value={period}
                onChange={(e) => setPeriod(e.target.value as any)}
                className="input"
              >
                {PERIOD_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={handleCompare}
              disabled={isLoading || assets.length === 0}
              className="btn btn-success px-6"
            >
              {isLoading ? "比較中..." : "比較実行"}
            </button>
          </div>
        </div>

        {/* エラー表示 */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
            {error}
          </div>
        )}

        {/* 比較結果 */}
        {compareResult && (
          <PageTransition>
            {/* パフォーマンスグラフ */}
            <div className="card p-6 mb-6">
              <h2 className="text-xl font-semibold mb-4">
                正規化パフォーマンス推移（基準日=100）
              </h2>
              <p className="text-sm text-gray-600 mb-4">
                期間: {compareResult.start_date} 〜 {compareResult.end_date}
              </p>

              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="date"
                    tick={{ fontSize: 12 }}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  {compareResult.assets.map((asset, index) => (
                    <Line
                      key={asset.symbol}
                      type="monotone"
                      dataKey={asset.symbol}
                      name={asset.name}
                      stroke={CHART_COLORS[index % CHART_COLORS.length]}
                      strokeWidth={2}
                      dot={false}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* パフォーマンスランキング */}
            <div className="card p-6 animate-fadeIn">
              <h2 className="text-xl font-semibold mb-4">パフォーマンスランキング</h2>

              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        順位
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        資産名
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        種別
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                        総リターン
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                        ボラティリティ
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                        最大DD
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {compareResult.ranking.map((item: RankingItem) => (
                      <tr key={item.symbol}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {item.rank}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {item.name} ({item.symbol})
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {ASSET_TYPE_LABELS[item.asset_type]}
                        </td>
                        <td
                          className={`px-6 py-4 whitespace-nowrap text-sm text-right font-semibold ${
                            item.total_return >= 0
                              ? "text-green-600"
                              : "text-red-600"
                          }`}
                        >
                          {item.total_return >= 0 ? "+" : ""}
                          {item.total_return.toFixed(2)}%
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                          {item.volatility !== null
                            ? `${item.volatility.toFixed(2)}%`
                            : "-"}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-red-600">
                          {item.max_drawdown !== null
                            ? `${item.max_drawdown.toFixed(2)}%`
                            : "-"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </PageTransition>
        )}
      </div>
    </div>
  );
}
