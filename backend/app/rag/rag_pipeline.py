"""
RAG Pipeline
Retrieval-Augmented Generation pipeline for question answering
"""

from typing import Dict, Optional, List
from app.rag.llm_client import ollama_client
from app.rag.embedding import embedding_service


class RAGPipeline:
    """RAG Pipeline for question answering"""

    def __init__(self):
        self.llm = ollama_client
        self.embedding_service = embedding_service

    def _create_prompt(self, question: str, context: str) -> str:
        """
        Create prompt for LLM with context

        Args:
            question: User question
            context: Retrieved context

        Returns:
            Formatted prompt
        """
        prompt_template = """あなたは日本株の財務アナリストです。以下の情報を元に、ユーザーの質問に答えてください。

【コンテキスト情報】
{context}

【質問】
{question}

【回答ルール】
- 数値は正確に引用すること
- 情報源を明示すること
- 不明な場合は「データがありません」と答えること
- 日本語で回答すること

【回答】
"""
        return prompt_template.format(context=context, question=question)

    def answer_question(
        self,
        question: str,
        stock_code: Optional[str] = None,
        n_results: int = 5
    ) -> Dict:
        """
        Answer question using RAG

        Args:
            question: User question
            stock_code: Optional stock code to filter results
            n_results: Number of documents to retrieve

        Returns:
            Dict with answer and sources
        """
        # Search for relevant documents using embedding service
        search_results = self.embedding_service.search_similar(
            query=question,
            n_results=n_results,
            stock_code=stock_code
        )

        if not search_results:
            return {
                "answer": "関連する情報が見つかりませんでした。",
                "sources": []
            }

        # Combine documents into context
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"【情報{i}】")
            context_parts.append(result["text"])

        context = "\n\n".join(context_parts)

        # Create prompt
        prompt = self._create_prompt(question, context)

        # Generate answer
        answer = self.llm.generate(prompt)

        # Prepare sources
        sources = [
            {
                "text": result["text"],
                "metadata": result["metadata"]
            }
            for result in search_results
        ]

        return {
            "answer": answer,
            "sources": sources
        }

    async def aanswer_question(
        self,
        question: str,
        stock_code: Optional[str] = None,
        n_results: int = 5
    ) -> Dict:
        """
        Async version of answer_question

        Args:
            question: User question
            stock_code: Optional stock code to filter results
            n_results: Number of documents to retrieve

        Returns:
            Dict with answer and sources
        """
        # Search for relevant documents
        search_results = self.embedding_service.search_similar(
            query=question,
            n_results=n_results,
            stock_code=stock_code
        )

        if not search_results:
            return {
                "answer": "関連する情報が見つかりませんでした。",
                "sources": []
            }

        # Combine documents into context
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"【情報{i}】")
            context_parts.append(result["text"])

        context = "\n\n".join(context_parts)

        # Create prompt
        prompt = self._create_prompt(question, context)

        # Async generate answer
        answer = await self.llm.agenerate(prompt)

        # Prepare sources
        sources = [
            {
                "text": result["text"],
                "metadata": result["metadata"]
            }
            for result in search_results
        ]

        return {
            "answer": answer,
            "sources": sources
        }


# Singleton instance
rag_pipeline = RAGPipeline()
