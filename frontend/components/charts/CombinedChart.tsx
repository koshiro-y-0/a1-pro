"use client";

import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { CombinedData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

interface CombinedChartProps {
  data: CombinedData[];
}

export default function CombinedChart({ data }: CombinedChartProps) {
  const chartData = [...data].reverse().map((item) => ({
    year: `${item.fiscal_year}年`,
    revenue: item.revenue ? item.revenue / 100000000 : null,
    ordinary_profit: item.ordinary_profit ? item.ordinary_profit / 100000000 : null,
    stock_price: item.stock_price || null,
  }));

  return (
    <div className="card card-hover p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        売上高・経常利益・株価推移
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={chartColors.grid} />
          <XAxis
            dataKey="year"
            tick={{ fill: chartColors.text }}
            style={{ fontSize: "12px" }}
          />
          <YAxis
            yAxisId="left"
            tick={{ fill: chartColors.text }}
            style={{ fontSize: "12px" }}
            label={{ value: "億円", angle: -90, position: "insideLeft" }}
          />
          <YAxis
            yAxisId="right"
            orientation="right"
            tick={{ fill: chartColors.text }}
            style={{ fontSize: "12px" }}
            label={{ value: "円", angle: 90, position: "insideRight" }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "white",
              border: "1px solid #E5E7EB",
              borderRadius: "8px",
            }}
            formatter={(value: any, name: string) => {
              if (name === "revenue") {
                return [`${Number(value).toFixed(2)} 億円`, "売上高"];
              } else if (name === "ordinary_profit") {
                return [`${Number(value).toFixed(2)} 億円`, "経常利益"];
              } else if (name === "stock_price") {
                return [`${Number(value).toFixed(2)} 円`, "株価"];
              }
              return [value, name];
            }}
          />
          <Legend
            wrapperStyle={{ fontSize: "14px" }}
            formatter={(value) => {
              if (value === "revenue") return "売上高";
              if (value === "ordinary_profit") return "経常利益";
              if (value === "stock_price") return "株価";
              return value;
            }}
          />
          <Bar
            yAxisId="left"
            dataKey="revenue"
            fill={chartColors.revenue}
            name="revenue"
          />
          <Bar
            yAxisId="left"
            dataKey="ordinary_profit"
            fill={chartColors.ordinary}
            name="ordinary_profit"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="stock_price"
            stroke={chartColors.stock}
            strokeWidth={2}
            dot={{ fill: chartColors.stock, r: 4 }}
            activeDot={{ r: 6 }}
            name="stock_price"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
