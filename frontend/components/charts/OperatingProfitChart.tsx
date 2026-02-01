"use client";

import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface OperatingProfitChartProps {
  data: FinancialData[];
}

export default function OperatingProfitChart({ data }: OperatingProfitChartProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  const reversedData = [...data].reverse();
  const chartData = reversedData.map((item, index) => {
    const operatingProfit = item.operating_profit ? item.operating_profit / 100000000 : null;
    const prevOperatingProfit = index > 0 && reversedData[index - 1].operating_profit
      ? reversedData[index - 1].operating_profit / 100000000
      : null;

    const yoyGrowth = operatingProfit !== null && prevOperatingProfit !== null
      ? ((operatingProfit - prevOperatingProfit) / prevOperatingProfit) * 100
      : null;

    return {
      year: `${item.fiscal_year}年`,
      operating_profit: operatingProfit,
      yoyGrowth,
    };
  });

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-gray-300 rounded-lg p-3 shadow-lg">
          <p className="font-semibold text-gray-900">{data.year}</p>
          <p className="text-sm" style={{ color: chartColors.operating }}>
            営業利益: {data.operating_profit !== null ? `${data.operating_profit.toFixed(2)} 億円` : "N/A"}
          </p>
          {data.yoyGrowth !== null && (
            <p className={`text-sm ${data.yoyGrowth >= 0 ? "text-green-600" : "text-red-600"}`}>
              前年比: {data.yoyGrowth >= 0 ? "+" : ""}{data.yoyGrowth.toFixed(2)}%
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card card-hover p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">営業利益推移</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={chartData}
          onMouseMove={(state: any) => {
            if (state.isTooltipActive) {
              setActiveIndex(state.activeTooltipIndex);
            } else {
              setActiveIndex(null);
            }
          }}
          onMouseLeave={() => setActiveIndex(null)}
        >
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
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="operating_profit"
            stroke={chartColors.operating}
            strokeWidth={2}
            dot={(props: any) => {
              const { cx, cy, index } = props;
              const isActive = index === activeIndex;
              return (
                <circle
                  cx={cx}
                  cy={cy}
                  r={isActive ? 6 : 4}
                  fill={chartColors.operating}
                  stroke="white"
                  strokeWidth={isActive ? 2 : 0}
                  style={{ cursor: "pointer" }}
                />
              );
            }}
            activeDot={{ r: 8, strokeWidth: 2, stroke: "white" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
