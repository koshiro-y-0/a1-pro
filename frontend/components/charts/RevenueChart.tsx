"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface RevenueChartProps {
  data: FinancialData[];
}

export default function RevenueChart({ data }: RevenueChartProps) {
  // データを逆順にして古い年度から表示
  const chartData = [...data].reverse().map((item) => ({
    year: `${item.fiscal_year}年`,
    revenue: item.revenue ? item.revenue / 100000000 : null, // 億円に変換
  }));

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">売上高推移</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={chartColors.grid} />
          <XAxis
            dataKey="year"
            tick={{ fill: chartColors.text }}
            style={{ fontSize: "12px" }}
          />
          <YAxis
            tick={{ fill: chartColors.text }}
            style={{ fontSize: "12px" }}
            label={{ value: "億円", angle: -90, position: "insideLeft" }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "white",
              border: "1px solid #E5E7EB",
              borderRadius: "8px",
            }}
            formatter={(value: any) => [
              `${Number(value).toFixed(2)} 億円`,
              "売上高",
            ]}
          />
          <Line
            type="monotone"
            dataKey="revenue"
            stroke={chartColors.revenue}
            strokeWidth={2}
            dot={{ fill: chartColors.revenue, r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
