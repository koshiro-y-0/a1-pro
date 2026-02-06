"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface OperatingMarginChartProps {
  data: FinancialData[];
}

export default function OperatingMarginChart({ data }: OperatingMarginChartProps) {
  const chartData = [...data].reverse().map((item) => ({
    year: `${item.fiscal_year}年`,
    operating_margin: item.metrics?.operating_margin || null,
  }));

  const getHealthColor = (value: number | null) => {
    if (value === null) return chartColors.grid;
    if (value >= 10) return chartColors.healthy;
    if (value >= 5) return chartColors.warning;
    return chartColors.danger;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">営業利益率推移</h3>
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
                <span key="value" style={{ color: healthColor }}>
                  {value !== null ? `${Number(value).toFixed(2)} %` : "N/A"}
                </span>,
                "営業利益率",
              ];
            }}
          />
          <Line
            type="monotone"
            dataKey="operating_margin"
            stroke={chartColors.healthy}
            strokeWidth={2}
            dot={(props: any) => {
              const { cx, cy, index, payload } = props;
              const color = getHealthColor(payload.operating_margin);
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
