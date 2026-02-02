"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface CurrentRatioChartProps {
  data: FinancialData[];
}

export default function CurrentRatioChart({ data }: CurrentRatioChartProps) {
  const chartData = [...data].reverse().map((item) => ({
    year: `${item.fiscal_year}年`,
    current_ratio: item.metrics?.current_ratio || null,
  }));

  const getHealthColor = (value: number | null) => {
    if (value === null) return chartColors.grid;
    if (value >= 200) return chartColors.healthy;
    if (value >= 100) return chartColors.warning;
    return chartColors.danger;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">流動比率推移</h3>
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
            label={{ value: "%", angle: -90, position: "insideLeft" }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "white",
              border: "1px solid #E5E7EB",
              borderRadius: "8px",
            }}
            formatter={(value: any) => {
              const healthColor = getHealthColor(value);
              return [
                <span style={{ color: healthColor }}>
                  {value !== null ? `${Number(value).toFixed(2)} %` : "N/A"}
                </span>,
                "流動比率",
              ];
            }}
          />
          <Line
            type="monotone"
            dataKey="current_ratio"
            stroke={chartColors.healthy}
            strokeWidth={2}
            dot={(props: any) => {
              const { cx, cy, index, payload } = props;
              const color = getHealthColor(payload.current_ratio);
              return (
                <circle
                  key={`dot-${payload.year}-${index}`}
                  cx={cx}
                  cy={cy}
                  r={4}
                  fill={color}
                  stroke={color}
                />
              );
            }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
