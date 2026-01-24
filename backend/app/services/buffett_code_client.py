"""
Buffett Code API Client
バフェット・コードAPIとの通信クライアント
"""

import os
import httpx
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class BuffettCodeClient:
    """バフェット・コードAPIクライアント"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Buffett Code API client

        Args:
            api_key: API key (default: from environment variable)
        """
        self.api_key = api_key or os.getenv("BUFFETT_CODE_API_KEY")
        self.base_url = "https://api.buffett-code.com/api/v3"
        self.headers = {
            "x-api-key": self.api_key
        } if self.api_key else {}

    async def get_company_info(self, stock_code: str) -> Optional[Dict]:
        """
        企業情報を取得

        Args:
            stock_code: 銘柄コード

        Returns:
            企業情報のDict、エラー時はNone
        """
        if not self.api_key:
            return None

        url = f"{self.base_url}/company"
        params = {"ticker": stock_code}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data
            except httpx.HTTPError as e:
                print(f"Buffett Code API error: {e}")
                return None

    async def get_financial_data(
        self,
        stock_code: str,
        fiscal_year: Optional[int] = None
    ) -> Optional[Dict]:
        """
        決算データを取得

        Args:
            stock_code: 銘柄コード
            fiscal_year: 会計年度（オプション）

        Returns:
            決算データのDict、エラー時はNone
        """
        if not self.api_key:
            return None

        url = f"{self.base_url}/quarter"
        params = {"ticker": stock_code}
        if fiscal_year:
            params["fy"] = fiscal_year

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data
            except httpx.HTTPError as e:
                print(f"Buffett Code API error: {e}")
                return None

    async def search_companies(self, query: str) -> List[Dict]:
        """
        企業検索（簡易版 - API制限を考慮）

        Args:
            query: 検索クエリ

        Returns:
            検索結果のリスト
        """
        # Note: バフェット・コードAPIには直接的な検索エンドポイントがないため、
        # ここでは基本的なロジックのみ実装
        # 実際の実装では、ローカルDBから検索するか、別のAPIを使用
        return []


# Singleton instance
buffett_code_client = BuffettCodeClient()
