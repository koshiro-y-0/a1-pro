"""
Chat API Endpoints
チャットボット関連のAPIエンドポイント
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.db.database import get_db
from app.models.company import Company
from app.rag.rag_pipeline import rag_pipeline
from app.rag.data_processor import data_processor
from app.rag.embedding import embedding_service

router = APIRouter()


class ChatRequest(BaseModel):
    """チャットリクエスト"""
    question: str
    stock_code: Optional[str] = None


class ChatResponse(BaseModel):
    """チャットレスポンス"""
    answer: str
    sources: list


class IndexRequest(BaseModel):
    """インデックス作成リクエスト"""
    stock_code: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    チャット質問に回答

    - RAGシステムを使用して質問に答える
    - 銘柄コード指定でフィルタ可能
    """
    try:
        # RAGパイプラインで回答生成
        result = await rag_pipeline.aanswer_question(
            question=request.question,
            stock_code=request.stock_code,
            n_results=5
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"チャット処理エラー: {str(e)}"
        )


@router.post("/chat/index")
async def create_index(
    request: IndexRequest,
    db: Session = Depends(get_db)
):
    """
    企業データをインデックス化

    - 企業情報と決算データをChromaDBに投入
    - 既存データは削除して再投入
    """
    try:
        # 企業を検索
        company = db.query(Company).filter(
            Company.stock_code == request.stock_code
        ).first()

        if not company:
            raise HTTPException(
                status_code=404,
                detail=f"銘柄コード {request.stock_code} の企業が見つかりません"
            )

        # 既存データを削除
        embedding_service.delete_company_data(request.stock_code)

        # ドキュメントチャンク作成
        chunks = data_processor.create_document_chunks(db, company)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="インデックス化するデータがありません"
            )

        # ChromaDBに追加
        embedding_service.add_documents(chunks, request.stock_code)

        return {
            "message": f"{company.name}（{request.stock_code}）のデータをインデックス化しました",
            "chunks_count": len(chunks)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"インデックス作成エラー: {str(e)}"
        )


@router.get("/chat/stats")
async def get_stats():
    """
    インデックス統計情報取得

    - ChromaDB内のドキュメント数を返す
    """
    try:
        count = embedding_service.get_collection_count()

        return {
            "total_documents": count,
            "collection_name": embedding_service.collection_name
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"統計取得エラー: {str(e)}"
        )
