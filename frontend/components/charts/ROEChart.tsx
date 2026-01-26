"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface ROEChartProps {
  data: FinancialData[];
}

export default function ROEChart({ data }: ROEChartProps) {
  const chartData = [...data].reverse().map((item) => ({
    year: `${item.fiscal_year}年`,
    roe: item.metrics?.roe || null,
  }));

  const getHealthColor = (value: number | null) => {
    if (value === null) return chartColors.grid;
    if (value >= 10) return chartColors.healthy;
    if (value >= 5) return chartColors.warning;
    return chartColors.danger;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">ROE推移</h3>
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
                "ROE",
              ];
            }}
          />
          <Line
            type="monotone"
            dataKey="roe"
            stroke={chartColors.healthy}
            strokeWidth={2}
            dot={(props: any) => {
              const { cx, cy, payload } = props;
              const color = getHealthColor(payload.roe);
              return (
                <circle
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
