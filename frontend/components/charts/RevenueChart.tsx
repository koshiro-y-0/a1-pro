"use client";

import { useState } from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface RevenueChartProps {
  data: FinancialData[];
}

export default function RevenueChart({ data }: RevenueChartProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  const reversedData = [...data].reverse();
  const chartData = reversedData.map((item, index) => {
    const revenue = item.revenue ? item.revenue / 100000000 : null;
    const prevRevenue = index > 0 && reversedData[index - 1].revenue
      ? reversedData[index - 1].revenue / 100000000
      : null;

    const yoyGrowth = revenue !== null && prevRevenue !== null
      ? ((revenue - prevRevenue) / prevRevenue) * 100
      : null;

    return {
      year: `${item.fiscal_year}年`,
      revenue,
      yoyGrowth,
    };
  });

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-gray-300 rounded-lg p-3 shadow-lg">
          <p className="font-semibold text-gray-900">{data.year}</p>
          <p className="text-sm" style={{ color: chartColors.revenue }}>
            売上高: {data.revenue !== null ? `${data.revenue.toFixed(2)} 億円` : "N/A"}
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
      <h3 className="text-lg font-semibold text-gray-900 mb-4">売上高推移</h3>
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
            <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={chartColors.revenue} stopOpacity={0.8}/>
              <stop offset="95%" stopColor={chartColors.revenue} stopOpacity={0.1}/>
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
            dataKey="revenue"
            stroke={chartColors.revenue}
            strokeWidth={3}
            fill="url(#revenueGradient)"
            dot={(props: any) => {
              const { cx, cy, index, payload } = props;
              const isActive = index === activeIndex;
              return (
                <circle
                  key={`dot-${payload.fiscal_year}-${index}`}
                  cx={cx}
                  cy={cy}
                  r={isActive ? 6 : 4}
                  fill={chartColors.revenue}
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
