# ===============================
# backend/agents/base.py
# ===============================

from abc import ABC, abstractmethod
from typing import Any, Dict
import asyncio


class BaseAgent(ABC):
    """Abstract base class for all document analysis agents."""

    def __init__(self, name: str, llama_service=None, model_name: str = "llama3"):
        self.name = name
        self.llama_service = llama_service
        self.model_name = model_name
        self.status = "ready"

    @abstractmethod
    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze the given text and return results."""
        pass

    def get_prompt_template(self) -> str:
        """Get the prompt template for this agent."""
        return ""

    async def generate_response(self, prompt: str) -> str:
        """Generate response using Llama3 (or fallback if unavailable)."""
        if self.llama_service:
            return await self.llama_service.generate(prompt, model=self.model_name)
        else:
            # Fallback to simple rule-based analysis for demo
            return self._fallback_analysis(prompt)

    def _fallback_analysis(self, text: str) -> str:
        """Fallback analysis when Llama3 is not available."""
        return f"[{self.model_name}] Analysis from {self.name}: Processing {len(text)} characters of text."

    def set_status(self, status: str):
        """Update agent status."""
        self.status = status

    def get_status(self) -> Dict[str, str]:
        """Get current agent status."""
        return {
            "name": self.name,
            "status": self.status,
            "model": self.model_name
        }
