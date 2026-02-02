"use client";

import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface NetProfitChartProps {
  data: FinancialData[];
}

export default function NetProfitChart({ data }: NetProfitChartProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  const reversedData = [...data].reverse();
  const chartData = reversedData.map((item, index) => {
    const netProfit = item.net_profit ? item.net_profit / 100000000 : null;
    const prevNetProfit = index > 0 && reversedData[index - 1].net_profit
      ? reversedData[index - 1].net_profit / 100000000
      : null;

    const yoyGrowth = netProfit !== null && prevNetProfit !== null
      ? ((netProfit - prevNetProfit) / prevNetProfit) * 100
      : null;

    return {
      year: `${item.fiscal_year}年`,
      net_profit: netProfit,
      yoyGrowth,
    };
  });

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-gray-300 rounded-lg p-3 shadow-lg">
          <p className="font-semibold text-gray-900">{data.year}</p>
          <p className="text-sm" style={{ color: chartColors.net }}>
            純利益: {data.net_profit !== null ? `${data.net_profit.toFixed(2)} 億円` : "N/A"}
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
      <h3 className="text-lg font-semibold text-gray-900 mb-4">純利益推移</h3>
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
            dataKey="net_profit"
            stroke={chartColors.net}
            strokeWidth={2}
            dot={(props: any) => {
              const { cx, cy, index, payload } = props;
              const isActive = index === activeIndex;
              return (
                <circle
                  key={`dot-${payload.year}-${index}`}
                  cx={cx}
                  cy={cy}
                  r={isActive ? 6 : 4}
                  fill={chartColors.net}
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
