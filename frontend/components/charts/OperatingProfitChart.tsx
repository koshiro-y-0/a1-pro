"use client";

import { useState } from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
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
    <div className="card card-hover p-6 bg-white shadow-lg">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">営業利益推移</h3>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart
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
          <defs>
            <linearGradient id="operatingGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={chartColors.operating} stopOpacity={0.8}/>
              <stop offset="95%" stopColor={chartColors.operating} stopOpacity={0.1}/>
            </linearGradient>
          </defs>
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
          <Area
            type="monotone"
            dataKey="operating_profit"
            stroke={chartColors.operating}
            strokeWidth={3}
            fill="url(#operatingGradient)"
            dot={(props: any) => {
              const { cx, cy, index, payload } = props;
              const isActive = index === activeIndex;
              return (
                <circle
                  key={`dot-${payload.year}-${index}`}
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
            animationDuration={1500}
            animationEasing="ease-out"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
