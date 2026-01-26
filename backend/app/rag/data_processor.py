"""
Data Processor for RAG
企業情報・決算データをテキスト化してRAGシステムに投入するための前処理
"""

from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.company import Company
from app.models.financial_data import FinancialData


class DataProcessor:
    """データ前処理クラス"""

    @staticmethod
    def process_company_info(company: Company) -> str:
        """
        企業情報をテキスト化

        Args:
            company: 企業モデル

        Returns:
            テキスト化された企業情報
        """
        text = f"""
企業名: {company.name}
銘柄コード: {company.stock_code}
業種: {company.industry or "不明"}
事業内容: {company.description or "情報なし"}
"""
        return text.strip()

    @staticmethod
    def process_financial_data(
        company: Company,
        financial_data_list: List[FinancialData]
    ) -> str:
        """
        決算データをテキスト化

        Args:
            company: 企業モデル
            financial_data_list: 決算データリスト

        Returns:
            テキスト化された決算データ
        """
        if not financial_data_list:
            return f"{company.name}の決算データはありません。"

        text_parts = [f"{company.name}（{company.stock_code}）の決算データ:\n"]

        for fd in financial_data_list:
            year_text = f"\n【{fd.fiscal_year}年度】"
            if fd.fiscal_quarter:
                year_text += f" 第{fd.fiscal_quarter}四半期"

            financial_info = []

            if fd.revenue is not None:
                revenue_oku = fd.revenue / 100000000
                financial_info.append(f"売上高: {revenue_oku:.2f}億円")

            if fd.operating_profit is not None:
                op_oku = fd.operating_profit / 100000000
                financial_info.append(f"営業利益: {op_oku:.2f}億円")

            if fd.ordinary_profit is not None:
                ord_oku = fd.ordinary_profit / 100000000
                financial_info.append(f"経常利益: {ord_oku:.2f}億円")

            if fd.net_profit is not None:
                net_oku = fd.net_profit / 100000000
                financial_info.append(f"純利益: {net_oku:.2f}億円")

            if fd.total_assets is not None:
                assets_oku = fd.total_assets / 100000000
                financial_info.append(f"総資産: {assets_oku:.2f}億円")

            if fd.equity is not None:
                equity_oku = fd.equity / 100000000
                financial_info.append(f"自己資本: {equity_oku:.2f}億円")

            text_parts.append(year_text)
            text_parts.append(", ".join(financial_info))

        return "\n".join(text_parts)

    @staticmethod
    def process_financial_metrics(
        company: Company,
        financial_data: FinancialData
    ) -> str:
        """
        財務指標をテキスト化

        Args:
            company: 企業モデル
            financial_data: 決算データ

        Returns:
            テキスト化された財務指標
        """
        from app.services.financial_calculator import financial_calculator

        metrics = financial_calculator.calculate_all_metrics(
            revenue=financial_data.revenue,
            operating_profit=financial_data.operating_profit,
            net_profit=financial_data.net_profit,
            total_assets=financial_data.total_assets,
            equity=financial_data.equity,
            total_liabilities=financial_data.total_liabilities,
            current_assets=financial_data.current_assets,
            current_liabilities=financial_data.current_liabilities
        )

        text_parts = [
            f"{company.name}（{company.stock_code}）の{financial_data.fiscal_year}年度の財務指標:"
        ]

        if metrics.equity_ratio is not None:
            text_parts.append(f"自己資本比率: {metrics.equity_ratio:.2f}%")

        if metrics.current_ratio is not None:
            text_parts.append(f"流動比率: {metrics.current_ratio:.2f}%")

        if metrics.debt_ratio is not None:
            text_parts.append(f"負債比率: {metrics.debt_ratio:.2f}%")

        if metrics.roe is not None:
            text_parts.append(f"ROE（自己資本利益率）: {metrics.roe:.2f}%")

        if metrics.operating_margin is not None:
            text_parts.append(f"営業利益率: {metrics.operating_margin:.2f}%")

        return "\n".join(text_parts)

    @classmethod
    def create_document_chunks(
        cls,
        db: Session,
        company: Company
    ) -> List[Dict[str, str]]:
        """
        企業データを複数のチャンクに分割してドキュメント作成

        Args:
            db: データベースセッション
            company: 企業モデル

        Returns:
            チャンクのリスト（各チャンクは {"text": str, "metadata": dict}）
        """
        chunks = []

        # チャンク1: 企業情報
        company_text = cls.process_company_info(company)
        chunks.append({
            "text": company_text,
            "metadata": {
                "stock_code": company.stock_code,
                "company_name": company.name,
                "type": "company_info"
            }
        })

        # チャンク2: 決算データ（全体）
        financial_data_list = db.query(FinancialData).filter(
            FinancialData.company_id == company.id,
            FinancialData.fiscal_quarter.is_(None)
        ).order_by(FinancialData.fiscal_year.desc()).limit(10).all()

        if financial_data_list:
            financial_text = cls.process_financial_data(company, financial_data_list)
            chunks.append({
                "text": financial_text,
                "metadata": {
                    "stock_code": company.stock_code,
                    "company_name": company.name,
                    "type": "financial_data"
                }
            })

        # チャンク3-N: 各年度の財務指標
        for fd in financial_data_list[:5]:  # 直近5年分
            metrics_text = cls.process_financial_metrics(company, fd)
            chunks.append({
                "text": metrics_text,
                "metadata": {
                    "stock_code": company.stock_code,
                    "company_name": company.name,
                    "fiscal_year": fd.fiscal_year,
                    "type": "financial_metrics"
                }
            })

        return chunks


# グローバルインスタンス
data_processor = DataProcessor()
