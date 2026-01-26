"use client";

import { FinancialData } from "@/types/financial";
import chartColors from "@/lib/chartColors";

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

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">財務健全性判定</h3>

      {/* Overall Status */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 mb-1">総合評価</p>
            <p className="text-2xl font-bold" style={{ color: overallStatus.color }}>
              {overallStatus.label}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600 mb-1">スコア</p>
            <p className="text-2xl font-bold text-gray-900">
              {totalScore} / {maxScore}
            </p>
            <p className="text-xs text-gray-500">{scorePercentage.toFixed(0)}%</p>
          </div>
        </div>
      </div>

      {/* Individual Assessments */}
      <div className="space-y-3">
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <p className="text-sm font-medium text-gray-700">自己資本比率</p>
            <p className="text-xs text-gray-500">
              {metrics.equity_ratio !== null
                ? `${metrics.equity_ratio.toFixed(2)}%`
                : "N/A"}
            </p>
          </div>
          <span
            className="px-3 py-1 rounded-full text-sm font-semibold"
            style={{
              backgroundColor: assessments.equityRatio.color + "20",
              color: assessments.equityRatio.color,
            }}
          >
            {assessments.equityRatio.label}
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <p className="text-sm font-medium text-gray-700">流動比率</p>
            <p className="text-xs text-gray-500">
              {metrics.current_ratio !== null
                ? `${metrics.current_ratio.toFixed(2)}%`
                : "N/A"}
            </p>
          </div>
          <span
            className="px-3 py-1 rounded-full text-sm font-semibold"
            style={{
              backgroundColor: assessments.currentRatio.color + "20",
              color: assessments.currentRatio.color,
            }}
          >
            {assessments.currentRatio.label}
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <p className="text-sm font-medium text-gray-700">ROE</p>
            <p className="text-xs text-gray-500">
              {metrics.roe !== null ? `${metrics.roe.toFixed(2)}%` : "N/A"}
            </p>
          </div>
          <span
            className="px-3 py-1 rounded-full text-sm font-semibold"
            style={{
              backgroundColor: assessments.roe.color + "20",
              color: assessments.roe.color,
            }}
          >
            {assessments.roe.label}
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <p className="text-sm font-medium text-gray-700">営業利益率</p>
            <p className="text-xs text-gray-500">
              {metrics.operating_margin !== null
                ? `${metrics.operating_margin.toFixed(2)}%`
                : "N/A"}
            </p>
          </div>
          <span
            className="px-3 py-1 rounded-full text-sm font-semibold"
            style={{
              backgroundColor: assessments.operatingMargin.color + "20",
              color: assessments.operatingMargin.color,
            }}
          >
            {assessments.operatingMargin.label}
          </span>
        </div>
      </div>
    </div>
  );
}
