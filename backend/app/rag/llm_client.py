"""
LLM Client for Ollama
Handles connection and interaction with Ollama (Llama 3.1)
"""

import os
from typing import Optional
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()


class OllamaClient:
    """Ollama LLM Client"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize Ollama client

        Args:
            base_url: Ollama server URL (default: from env or localhost:11434)
            model: Model name (default: from env or llama3.1:8b)
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")

        self.llm = Ollama(
            base_url=self.base_url,
            model=self.model,
            temperature=0.7,
        )

    def generate(self, prompt: str) -> str:
        """
        Generate response from Ollama

        Args:
            prompt: Input prompt

        Returns:
            Generated response
        """
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            raise Exception(f"Ollama generation failed: {str(e)}")

    async def agenerate(self, prompt: str) -> str:
        """
        Async generate response from Ollama

        Args:
            prompt: Input prompt

        Returns:
            Generated response
        """
        try:
            response = await self.llm.ainvoke(prompt)
            return response
        except Exception as e:
            raise Exception(f"Ollama async generation failed: {str(e)}")


# Singleton instance
ollama_client = OllamaClient()
