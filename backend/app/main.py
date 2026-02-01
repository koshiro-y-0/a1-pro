"""
A1-PRO FastAPI Application
Main entry point for the backend API
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

# スケジューラーのインポート
from app.services.scheduler import scheduler_service
from app.exceptions import A1ProException

# ロガー設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時: スケジューラー開始
    scheduler_service.start()
    yield
    # 終了時: スケジューラー停止
    scheduler_service.stop()


app = FastAPI(
    title="A1-PRO API",
    description="日本株分析Webアプリケーション バックエンドAPI",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "A1-PRO API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "service": "a1-pro-backend"
    }


# ルーター登録
from app.api import companies, chat, portfolio, favorites, compare

app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["favorites"])
app.include_router(compare.router, prefix="/api", tags=["compare"])


# グローバルエラーハンドラー
@app.exception_handler(A1ProException)
async def a1pro_exception_handler(request: Request, exc: A1ProException):
    """A1-PRO カスタム例外ハンドラー"""
    logger.error(f"A1ProException: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "type": exc.__class__.__name__}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """グローバル例外ハンドラー"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "type": "InternalServerError"}
    )
