"use client";

import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";
import { useEffect, useState } from "react";

interface FinancialHealthIndicatorProps {
  data: FinancialData[];
}

type HealthStatus = "healthy" | "warning" | "danger";

interface HealthAssessment {
  status: HealthStatus;
  label: string;
  color: string;
}

export default function FinancialHealthIndicator({
  data,
}: FinancialHealthIndicatorProps) {
  // カウントアップアニメーション用のstate（Hooksは常に最初に呼ぶ）
  const [displayScore, setDisplayScore] = useState(0);

  // 早期リターンの前にHooksを呼ぶ
  if (data.length === 0) return null;

  const latestData = data[0];
  const metrics = latestData.metrics;

  const assessEquityRatio = (ratio: number | null): HealthAssessment => {
    if (ratio === null)
      return { status: "warning", label: "データなし", color: chartColors.warning };
    if (ratio >= 40)
      return { status: "healthy", label: "健全", color: chartColors.healthy };
    if (ratio >= 20)
      return { status: "warning", label: "注意", color: chartColors.warning };
    return { status: "danger", label: "危険", color: chartColors.danger };
  };

  const assessCurrentRatio = (ratio: number | null): HealthAssessment => {
    if (ratio === null)
      return { status: "warning", label: "データなし", color: chartColors.warning };
    if (ratio >= 200)
      return { status: "healthy", label: "健全", color: chartColors.healthy };
    if (ratio >= 100)
      return { status: "warning", label: "注意", color: chartColors.warning };
    return { status: "danger", label: "危険", color: chartColors.danger };
  };

  const assessROE = (roe: number | null): HealthAssessment => {
    if (roe === null)
      return { status: "warning", label: "データなし", color: chartColors.warning };
    if (roe >= 10)
      return { status: "healthy", label: "健全", color: chartColors.healthy };
    if (roe >= 5)
      return { status: "warning", label: "注意", color: chartColors.warning };
    return { status: "danger", label: "危険", color: chartColors.danger };
  };

  const assessOperatingMargin = (margin: number | null): HealthAssessment => {
    if (margin === null)
      return { status: "warning", label: "データなし", color: chartColors.warning };
    if (margin >= 10)
      return { status: "healthy", label: "健全", color: chartColors.healthy };
    if (margin >= 5)
      return { status: "warning", label: "注意", color: chartColors.warning };
    return { status: "danger", label: "危険", color: chartColors.danger };
  };

  const assessments = {
    equityRatio: assessEquityRatio(metrics.equity_ratio),
    currentRatio: assessCurrentRatio(metrics.current_ratio),
    roe: assessROE(metrics.roe),
    operatingMargin: assessOperatingMargin(metrics.operating_margin),
  };

  const scoreMap = {
    healthy: 2,
    warning: 1,
    danger: 0,
  };

  const totalScore =
    scoreMap[assessments.equityRatio.status] +
    scoreMap[assessments.currentRatio.status] +
    scoreMap[assessments.roe.status] +
    scoreMap[assessments.operatingMargin.status];

  const maxScore = 8;
  const scorePercentage = (totalScore / maxScore) * 100;

  let overallStatus: HealthAssessment;
  if (scorePercentage >= 75) {
    overallStatus = { status: "healthy", label: "健全", color: chartColors.healthy };
  } else if (scorePercentage >= 50) {
    overallStatus = { status: "warning", label: "注意", color: chartColors.warning };
  } else {
    overallStatus = { status: "danger", label: "危険", color: chartColors.danger };
  }

  // eslint-disable-next-line react-hooks/rules-of-hooks
  useEffect(() => {
    let currentScore = 0;
    const increment = totalScore / 30; // 30フレームで完了
    const timer = setInterval(() => {
      currentScore += increment;
      if (currentScore >= totalScore) {
        setDisplayScore(totalScore);
        clearInterval(timer);
      } else {
        setDisplayScore(Math.floor(currentScore));
      }
    }, 20);

    return () => clearInterval(timer);
  }, [totalScore]);

  // ゲージの角度を計算 (180度 = 半円)
  const gaugeAngle = (scorePercentage / 100) * 180;

  return (
    <div className="card card-hover p-6 bg-gradient-to-br from-white to-gray-50">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">財務健全性コックピット</h3>

      {/* Gauge Meter */}
      <div className="mb-8 flex flex-col items-center">
        <div className="relative w-64 h-32 mb-4">
          {/* Background Arc (Gray) */}
          <svg className="w-full h-full" viewBox="0 0 200 100">
            {/* Danger Zone (Red) */}
            <path
              d="M 20 80 A 80 80 0 0 1 60 15"
              fill="none"
              stroke="#ef4444"
              strokeWidth="12"
              opacity="0.2"
            />
            {/* Warning Zone (Yellow) */}
            <path
              d="M 60 15 A 80 80 0 0 1 140 15"
              fill="none"
              stroke="#f59e0b"
              strokeWidth="12"
              opacity="0.2"
            />
            {/* Healthy Zone (Green) */}
            <path
              d="M 140 15 A 80 80 0 0 1 180 80"
              fill="none"
              stroke="#10b981"
              strokeWidth="12"
              opacity="0.2"
            />

            {/* Active Arc */}
            <path
              d="M 20 80 A 80 80 0 0 1 180 80"
              fill="none"
              stroke={overallStatus.color}
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray={`${(gaugeAngle / 180) * 251} 251`}
              className="transition-all duration-1000 ease-out"
            />

            {/* Needle */}
            <g
              transform={`rotate(${gaugeAngle - 90} 100 80)`}
              className="transition-transform duration-1000 ease-out"
            >
              <line
                x1="100"
                y1="80"
                x2="100"
                y2="20"
                stroke="#374151"
                strokeWidth="2"
                strokeLinecap="round"
              />
              <circle cx="100" cy="80" r="4" fill="#374151" />
            </g>
          </svg>

          {/* Score Display */}
          <div className="absolute inset-0 flex flex-col items-center justify-end pb-2">
            <p className="text-4xl font-bold" style={{ color: overallStatus.color }}>
              {displayScore} / {maxScore}
            </p>
            <p className="text-sm text-gray-600 mt-1">{overallStatus.label}</p>
          </div>
        </div>

        {/* Legend */}
        <div className="flex gap-4 text-xs">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-gray-600">危険</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-gray-600">注意</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-gray-600">健全</span>
          </div>
        </div>
      </div>

      {/* Individual Assessments - Rich Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Equity Ratio Card */}
        <MetricCard
          title="自己資本比率"
          value={metrics.equity_ratio}
          unit="%"
          assessment={assessments.equityRatio}
          sparklineData={data.slice(0, 5).reverse().map(d => d.metrics.equity_ratio || 0)}
          change={calculateChange(data, 'equity_ratio')}
        />

        {/* Current Ratio Card */}
        <MetricCard
          title="流動比率"
          value={metrics.current_ratio}
          unit="%"
          assessment={assessments.currentRatio}
          sparklineData={data.slice(0, 5).reverse().map(d => d.metrics.current_ratio || 0)}
          change={calculateChange(data, 'current_ratio')}
        />

        {/* ROE Card */}
        <MetricCard
          title="ROE"
          value={metrics.roe}
          unit="%"
          assessment={assessments.roe}
          sparklineData={data.slice(0, 5).reverse().map(d => d.metrics.roe || 0)}
          change={calculateChange(data, 'roe')}
        />

        {/* Operating Margin Card */}
        <MetricCard
          title="営業利益率"
          value={metrics.operating_margin}
          unit="%"
          assessment={assessments.operatingMargin}
          sparklineData={data.slice(0, 5).reverse().map(d => d.metrics.operating_margin || 0)}
          change={calculateChange(data, 'operating_margin')}
        />
      </div>
    </div>
  );
}

// Helper function to calculate year-over-year change
function calculateChange(data: FinancialData[], metric: keyof FinancialData['metrics']): number | null {
  if (data.length < 2) return null;
  const latest = data[0].metrics[metric];
  const previous = data[1].metrics[metric];
  if (latest === null || previous === null || previous === 0) return null;
  return ((latest - previous) / previous) * 100;
}

// Metric Card Component with Sparkline
interface MetricCardProps {
  title: string;
  value: number | null;
  unit: string;
  assessment: HealthAssessment;
  sparklineData: number[];
  change: number | null;
}

function MetricCard({ title, value, unit, assessment, sparklineData, change }: MetricCardProps) {
  const hasIncrease = change !== null && change > 0;
  const hasDecrease = change !== null && change < 0;

  return (
    <div className="relative p-4 bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-lg transition-all duration-300">
      {/* Background Sparkline (subtle) */}
      <div className="absolute inset-0 opacity-10">
        <Sparkline data={sparklineData} color={assessment.color} />
      </div>

      {/* Content */}
      <div className="relative">
        <div className="flex items-start justify-between mb-2">
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <div className="flex items-baseline gap-2 mt-1">
              <p className="text-2xl font-bold text-gray-900">
                {value !== null ? value.toFixed(2) : "N/A"}
                <span className="text-sm font-normal text-gray-500">{unit}</span>
              </p>
              {change !== null && (
                <span
                  className={`text-xs font-semibold flex items-center ${
                    hasIncrease ? "text-green-600" : hasDecrease ? "text-red-600" : "text-gray-500"
                  }`}
                >
                  {hasIncrease ? "↗" : hasDecrease ? "↘" : "→"} {Math.abs(change).toFixed(1)}%
                </span>
              )}
            </div>
          </div>
          <span
            className="px-2 py-1 rounded-full text-xs font-semibold"
            style={{
              backgroundColor: assessment.color + "20",
              color: assessment.color,
            }}
          >
            {assessment.label}
          </span>
        </div>

        {/* Mini Sparkline */}
        <div className="h-8 mt-2">
          <Sparkline data={sparklineData} color={assessment.color} />
        </div>
      </div>
    </div>
  );
}

// Simple Sparkline Component
interface SparklineProps {
  data: number[];
  color: string;
}

function Sparkline({ data, color }: SparklineProps) {
  if (data.length === 0) return null;

  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;

  const points = data
    .map((value, index) => {
      const x = (index / (data.length - 1)) * 100;
      const y = 100 - ((value - min) / range) * 100;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
