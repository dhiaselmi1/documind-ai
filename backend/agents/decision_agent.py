
# ===============================
# backend/agents/decision_agent.py
# ===============================

from agents.base import BaseAgent
from typing import Dict, Any, List
import re


class DecisionAgent(BaseAgent):
    """Agent responsible for extracting decisions, action items, and next steps."""

    def __init__(self, llama_service=None):
        super().__init__("Decision Extractor", llama_service)
        self.decision_indicators = [
            "decided", "resolved", "agreed", "approved", "authorized",
            "action item", "next step", "follow up", "shall", "will",
            "must", "required", "mandatory", "deadline", "due date",
            "assign", "responsible", "task", "deliverable"
        ]

    def get_prompt_template(self) -> str:
        return """
        Extract all decisions, action items, and next steps from the following document. For each item found, identify:

        1. **Decision/Action**: What was decided or what needs to be done?
        2. **Responsible Party**: Who is responsible (if mentioned)?
        3. **Timeline**: Any deadlines or timeframes mentioned?
        4. **Priority**: High/Medium/Low (if determinable)
        5. **Status**: Completed/Pending/Future

        Look for:
        - Explicit decisions made
        - Action items assigned
        - Next steps outlined
        - Deadlines and timelines
        - Responsibilities and assignments

        Document text:
        {text}

        Decisions and Actions:
        """

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Extract decisions and action items from the document."""
        self.set_status("analyzing")

        try:
            prompt = self.get_prompt_template().format(text=text[:3000])

            if self.llama_service:
                analysis = await self.generate_response(prompt)
                decisions = self._parse_llama_decisions(analysis)
            else:
                decisions = self._extract_keyword_decisions(text)

            self.set_status("completed")

            return {
                "agent": self.name,
                "decisions": decisions,
                "total_decisions": len(decisions),
                "action_items": self._filter_action_items(decisions),
                "deadlines": self._extract_deadlines(text)
            }

        except Exception as e:
            self.set_status("error")
            return {
                "agent": self.name,
                "decisions": [f"Error extracting decisions: {str(e)}"],
                "total_decisions": 0,
                "action_items": [],
                "deadlines": []
            }

    def _extract_keyword_decisions(self, text: str) -> List[str]:
        """Extract decisions using keyword matching."""
        decisions = []
        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue

            sentence_lower = sentence.lower()

            # Check for decision indicators
            for indicator in self.decision_indicators:
                if indicator in sentence_lower:
                    decisions.append(f"📋 {sentence}")
                    break

        # Look for numbered or bulleted action items
        action_pattern = r'(?:^|\n)\s*(?:\d+\.|•|-|\*)\s*(.+)'
        action_matches = re.findall(action_pattern, text, re.MULTILINE)

        for match in action_matches:
            if len(match.strip()) > 10:
                decisions.append(f"✅ Action: {match.strip()}")

        return decisions[:15]  # Limit to top 15 decisions

    def _parse_llama_decisions(self, analysis: str) -> List[str]:
        """Parse decisions from Llama3 analysis."""
        lines = analysis.split('\n')
        decisions = []

        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or
                         'decision' in line.lower() or 'action' in line.lower()):
                decisions.append(line)

        return decisions

    def _filter_action_items(self, decisions: List[str]) -> List[str]:
        """Filter out action items from decisions."""
        action_keywords = ["action", "task", "follow up", "next step", "assign"]
        action_items = []

        for decision in decisions:
            decision_lower = decision.lower()
            if any(keyword in decision_lower for keyword in action_keywords):
                action_items.append(decision)

        return action_items

    def _extract_deadlines(self, text: str) -> List[str]:
        """Extract deadline information from text."""
        deadline_patterns = [
            r'(?:deadline|due|expires?|by)\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(?:deadline|due|expires?|by)\s+(\w+\s+\d{1,2},?\s+\d{4})',
            r'(?:within|in)\s+(\d+\s+(?:days?|weeks?|months?))',
        ]

        deadlines = []
        for pattern in deadline_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                deadlines.append(f"📅 Deadline: {match}")

        return deadlines[:5]  # Limit to 5 deadlines

