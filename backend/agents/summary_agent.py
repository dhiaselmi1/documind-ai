# ===============================
# backend/agents/summary_agent.py
# ===============================

from agents.base import BaseAgent
from typing import Dict, Any,List
import re


class SummaryAgent(BaseAgent):
    """Agent responsible for generating comprehensive document summaries."""

    def __init__(self, llama_service=None):
        super().__init__("Summary Agent", llama_service)

    def get_prompt_template(self) -> str:
        return """
        Create a comprehensive summary of the following document. Include:

        1. **Main Purpose**: What is this document about?
        2. **Key Points**: 3-5 most important points
        3. **Stakeholders**: Who are the main parties involved?
        4. **Context**: When and why was this created?
        5. **Outcomes**: What are the expected results or next steps?

        Keep the summary clear, concise, and professional.

        Document text:
        {text}

        Summary:
        """

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Generate a comprehensive summary of the document."""
        self.set_status("analyzing")

        try:
            prompt = self.get_prompt_template().format(text=text[:4000])

            if self.llama_service:
                summary = await self.generate_response(prompt)
            else:
                summary = self._generate_fallback_summary(text)

            # Extract key statistics
            stats = self._extract_document_stats(text)

            self.set_status("completed")

            return {
                "agent": self.name,
                "summary": summary,
                "statistics": stats,
                "key_topics": self._extract_key_topics(text)
            }

        except Exception as e:
            self.set_status("error")
            return {
                "agent": self.name,
                "summary": f"Error generating summary: {str(e)}",
                "statistics": {},
                "key_topics": []
            }

    def _generate_fallback_summary(self, text: str) -> str:
        """Generate summary using simple heuristics."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s) > 20]

        # Take first sentence, some middle sentences, and last sentence
        if len(sentences) <= 3:
            summary = ". ".join(sentences) + "."
        else:
            summary_sentences = [sentences[0]]

            # Add some middle sentences
            middle_start = len(sentences) // 3
            middle_end = 2 * len(sentences) // 3
            summary_sentences.extend(sentences[middle_start:middle_start + 2])

            # Add last sentence
            summary_sentences.append(sentences[-1])

            summary = ". ".join(summary_sentences) + "."

        return f"**Document Summary**: {summary}"

    def _extract_document_stats(self, text: str) -> Dict[str, Any]:
        """Extract basic statistics from the document."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        paragraphs = text.split('\n\n')

        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "paragraph_count": len([p for p in paragraphs if p.strip()]),
            "character_count": len(text),
            "avg_words_per_sentence": len(words) / max(len(sentences), 1)
        }

    def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics using simple keyword frequency."""
        # Remove common words
        stop_words = set(
            ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are',
             'was', 'were', 'be', 'been', 'have', 'has', 'had', 'will', 'would', 'could', 'should'])

        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        word_freq = {}

        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top 5 most frequent words as topics
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        return [word.title() for word, freq in top_words]

