"""
Financial Health Assessment Service
財務健全性判定サービス
"""

from typing import Optional
from enum import Enum


class HealthStatus(str, Enum):
    """健全性ステータス"""
    HEALTHY = "healthy"  # 健全
    WARNING = "warning"  # 注意
    DANGER = "danger"    # 危険


class FinancialHealthAssessment:
    """財務健全性評価"""

    @staticmethod
    def assess_equity_ratio(equity_ratio: Optional[float]) -> HealthStatus:
        """
        自己資本比率による健全性判定

        - 40%以上: 健全
        - 20-40%: 注意
        - 20%未満: 危険
        """
        if equity_ratio is None:
            return HealthStatus.WARNING

        if equity_ratio >= 40:
            return HealthStatus.HEALTHY
        elif equity_ratio >= 20:
            return HealthStatus.WARNING
        else:
            return HealthStatus.DANGER

    @staticmethod
    def assess_current_ratio(current_ratio: Optional[float]) -> HealthStatus:
        """
        流動比率による健全性判定

        - 200%以上: 健全
        - 100-200%: 注意
        - 100%未満: 危険
        """
        if current_ratio is None:
            return HealthStatus.WARNING

        if current_ratio >= 200:
            return HealthStatus.HEALTHY
        elif current_ratio >= 100:
            return HealthStatus.WARNING
        else:
            return HealthStatus.DANGER

    @staticmethod
    def assess_roe(roe: Optional[float]) -> HealthStatus:
        """
        ROEによる健全性判定

        - 10%以上: 健全
        - 5-10%: 注意
        - 5%未満: 危険
        """
        if roe is None:
            return HealthStatus.WARNING

        if roe >= 10:
            return HealthStatus.HEALTHY
        elif roe >= 5:
            return HealthStatus.WARNING
        else:
            return HealthStatus.DANGER

    @staticmethod
    def assess_operating_margin(operating_margin: Optional[float]) -> HealthStatus:
        """
        営業利益率による健全性判定

        - 10%以上: 健全
        - 5-10%: 注意
        - 5%未満: 危険
        """
        if operating_margin is None:
            return HealthStatus.WARNING

        if operating_margin >= 10:
            return HealthStatus.HEALTHY
        elif operating_margin >= 5:
            return HealthStatus.WARNING
        else:
            return HealthStatus.DANGER

    @classmethod
    def assess_overall_health(
        cls,
        equity_ratio: Optional[float],
        current_ratio: Optional[float],
        roe: Optional[float],
        operating_margin: Optional[float]
    ) -> dict:
        """
        総合的な財務健全性判定

        各指標を評価し、総合スコアを算出
        """
        assessments = {
            "equity_ratio": cls.assess_equity_ratio(equity_ratio),
            "current_ratio": cls.assess_current_ratio(current_ratio),
            "roe": cls.assess_roe(roe),
            "operating_margin": cls.assess_operating_margin(operating_margin)
        }

        # スコア計算（健全=2点、注意=1点、危険=0点）
        score_map = {
            HealthStatus.HEALTHY: 2,
            HealthStatus.WARNING: 1,
            HealthStatus.DANGER: 0
        }

        total_score = sum(score_map[status] for status in assessments.values())
        max_score = 8  # 4指標 × 2点

        # 総合判定
        score_percentage = (total_score / max_score) * 100

        if score_percentage >= 75:
            overall_status = HealthStatus.HEALTHY
        elif score_percentage >= 50:
            overall_status = HealthStatus.WARNING
        else:
            overall_status = HealthStatus.DANGER

        return {
            "overall_status": overall_status,
            "score": total_score,
            "max_score": max_score,
            "score_percentage": round(score_percentage, 2),
            "assessments": assessments
        }


# グローバルインスタンス
financial_health_assessor = FinancialHealthAssessment()
