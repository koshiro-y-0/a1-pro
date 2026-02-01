"""
Custom Exceptions
カスタム例外クラス
"""

from fastapi import HTTPException, status


class A1ProException(Exception):
    """A1-PRO基本例外クラス"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class CompanyNotFoundException(A1ProException):
    """企業が見つからない例外"""

    def __init__(self, stock_code: str):
        message = f"Company with stock code {stock_code} not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class DataNotAvailableException(A1ProException):
    """データ取得不可例外"""

    def __init__(self, data_type: str, identifier: str):
        message = f"{data_type} data for {identifier} is not available"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ExternalAPIException(A1ProException):
    """外部API呼び出しエラー"""

    def __init__(self, api_name: str, detail: str):
        message = f"External API error ({api_name}): {detail}"
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE)


class ValidationException(A1ProException):
    """バリデーションエラー"""

    def __init__(self, field: str, detail: str):
        message = f"Validation error for {field}: {detail}"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class DatabaseException(A1ProException):
    """データベースエラー"""

    def __init__(self, detail: str):
        message = f"Database error: {detail}"
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CacheException(A1ProException):
    """キャッシュエラー"""

    def __init__(self, detail: str):
        message = f"Cache error: {detail}"
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)
