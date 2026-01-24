"""
Vector Store using ChromaDB
Handles vector database operations for RAG
"""

import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


class VectorStore:
    """ChromaDB Vector Store for RAG"""

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: str = "a1pro_documents"
    ):
        """
        Initialize ChromaDB vector store

        Args:
            persist_directory: Directory to persist data (default: from env)
            collection_name: Name of the collection
        """
        self.persist_directory = persist_directory or os.getenv(
            "CHROMA_PERSIST_DIRECTORY",
            "./data/chromadb"
        )

        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "A1-PRO financial documents"}
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ):
        """
        Add documents to vector store

        Args:
            documents: List of document texts
            metadatas: Optional list of metadata dicts
            ids: Optional list of document IDs
        """
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()

        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict:
        """
        Search for similar documents

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            Search results with documents and metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(self.collection.name)

    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        return self.collection.count()


# Singleton instance
vector_store = VectorStore()
