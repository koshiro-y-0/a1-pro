"""
RAG Pipeline
Retrieval-Augmented Generation pipeline for question answering
"""

from typing import Dict, Optional
from app.rag.llm_client import ollama_client
from app.rag.vector_store import vector_store


class RAGPipeline:
    """RAG Pipeline for question answering"""

    def __init__(self):
        self.llm = ollama_client
        self.vector_store = vector_store

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
        company_context: Optional[str] = None,
        n_results: int = 5
    ) -> Dict:
        """
        Answer question using RAG

        Args:
            question: User question
            company_context: Optional company context (stock code, name)
            n_results: Number of documents to retrieve

        Returns:
            Dict with answer and sources
        """
        # Search for relevant documents
        search_results = self.vector_store.search(
            query=question,
            n_results=n_results
        )

        # Extract documents
        documents = search_results.get('documents', [[]])[0]
        metadatas = search_results.get('metadatas', [[]])[0]

        if not documents:
            return {
                "answer": "関連する情報が見つかりませんでした。",
                "sources": []
            }

        # Combine documents into context
        context = "\n\n".join(documents)

        # Add company context if provided
        if company_context:
            context = f"【企業情報】\n{company_context}\n\n{context}"

        # Create prompt
        prompt = self._create_prompt(question, context)

        # Generate answer
        answer = self.llm.generate(prompt)

        # Prepare sources
        sources = [
            {
                "text": doc,
                "metadata": meta
            }
            for doc, meta in zip(documents, metadatas)
        ]

        return {
            "answer": answer,
            "sources": sources
        }

    async def aanswer_question(
        self,
        question: str,
        company_context: Optional[str] = None,
        n_results: int = 5
    ) -> Dict:
        """
        Async version of answer_question

        Args:
            question: User question
            company_context: Optional company context
            n_results: Number of documents to retrieve

        Returns:
            Dict with answer and sources
        """
        # Search for relevant documents
        search_results = self.vector_store.search(
            query=question,
            n_results=n_results
        )

        documents = search_results.get('documents', [[]])[0]
        metadatas = search_results.get('metadatas', [[]])[0]

        if not documents:
            return {
                "answer": "関連する情報が見つかりませんでした。",
                "sources": []
            }

        context = "\n\n".join(documents)

        if company_context:
            context = f"【企業情報】\n{company_context}\n\n{context}"

        prompt = self._create_prompt(question, context)

        # Async generate answer
        answer = await self.llm.agenerate(prompt)

        sources = [
            {
                "text": doc,
                "metadata": meta
            }
            for doc, meta in zip(documents, metadatas)
        ]

        return {
            "answer": answer,
            "sources": sources
        }


# Singleton instance
rag_pipeline = RAGPipeline()
