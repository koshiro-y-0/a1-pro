"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface OperatingProfitChartProps {
  data: FinancialData[];
}

export default function OperatingProfitChart({ data }: OperatingProfitChartProps) {
  const chartData = [...data].reverse().map((item) => ({
    year: `${item.fiscal_year}年`,
    operating_profit: item.operating_profit ? item.operating_profit / 100000000 : null,
  }));

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">営業利益推移</h3>
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
              "営業利益",
            ]}
          />
          <Line
            type="monotone"
            dataKey="operating_profit"
            stroke={chartColors.operating}
            strokeWidth={2}
            dot={{ fill: chartColors.operating, r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
