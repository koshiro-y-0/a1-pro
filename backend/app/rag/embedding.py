"""
Embedding Service for RAG
テキストのベクトル化とChromaDBへの保存
"""

from typing import List, Dict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os


class EmbeddingService:
    """エンベディングサービス"""

    def __init__(self):
        """初期化"""
        # Sentence Transformerモデルのロード
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # ChromaDB設定
        persist_directory = os.getenv(
            "CHROMA_PERSIST_DIRECTORY",
            "./data/chromadb"
        )

        # ChromaDBクライアント作成
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))

        # コレクション取得または作成
        self.collection_name = "financial_data"
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "日本株の企業情報・決算データ"}
            )

    def embed_text(self, text: str) -> List[float]:
        """
        テキストをベクトル化

        Args:
            text: 入力テキスト

        Returns:
            エンベディングベクトル
        """
        embedding = self.model.encode(text)
        return embedding.tolist()

    def add_documents(
        self,
        chunks: List[Dict[str, str]],
        stock_code: str
    ) -> None:
        """
        ドキュメントをChromaDBに追加

        Args:
            chunks: チャンクリスト（text, metadataを含む）
            stock_code: 銘柄コード
        """
        if not chunks:
            return

        documents = []
        embeddings = []
        ids = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            text = chunk["text"]
            metadata = chunk["metadata"]

            # エンベディング生成
            embedding = self.embed_text(text)

            # ID生成
            chunk_id = f"{stock_code}_{metadata['type']}_{i}"

            documents.append(text)
            embeddings.append(embedding)
            ids.append(chunk_id)
            metadatas.append(metadata)

        # ChromaDBに追加
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

    def search_similar(
        self,
        query: str,
        n_results: int = 5,
        stock_code: str = None
    ) -> List[Dict]:
        """
        類似ドキュメントを検索

        Args:
            query: 検索クエリ
            n_results: 取得件数
            stock_code: 銘柄コードでフィルタ（オプション）

        Returns:
            検索結果リスト
        """
        # クエリをベクトル化
        query_embedding = self.embed_text(query)

        # 検索条件
        where = None
        if stock_code:
            where = {"stock_code": stock_code}

        # ChromaDBで検索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )

        # 結果を整形
        formatted_results = []
        if results["documents"] and len(results["documents"]) > 0:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                })

        return formatted_results

    def delete_company_data(self, stock_code: str) -> None:
        """
        特定企業のデータを削除

        Args:
            stock_code: 銘柄コード
        """
        # 該当する銘柄コードのドキュメントを削除
        self.collection.delete(
            where={"stock_code": stock_code}
        )

    def get_collection_count(self) -> int:
        """
        コレクション内のドキュメント数を取得

        Returns:
            ドキュメント数
        """
        return self.collection.count()


# グローバルインスタンス
embedding_service = EmbeddingService()
