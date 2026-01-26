"""
A1-PRO FastAPI Application
Main entry point for the backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="A1-PRO API",
    description="日本株分析Webアプリケーション バックエンドAPI",
    version="0.1.0",
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
from app.api import companies, chat, portfolio, favorites

app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["favorites"])
