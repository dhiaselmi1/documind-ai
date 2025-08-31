# ===============================
# backend/agents/red_flag_agent.py
# ===============================

from agents.base import BaseAgent
from typing import Dict, Any, List
import re


class RedFlagAgent(BaseAgent):
    """Agent responsible for detecting potential issues, risks, and red flags."""

    def __init__(self, llama_service="llama3"):
        super().__init__("Red Flag Detector", llama_service)
        self.red_flag_keywords = [
            # Legal/Compliance
            "lawsuit", "litigation", "violation", "breach", "penalty", "fine",
            "non-compliance", "illegal", "unauthorized", "fraud", "corruption",

            # Financial risks
            "debt", "bankruptcy", "loss", "deficit", "overdue", "unpaid",
            "financial distress", "cash flow", "insolvency",

            # Operational risks
            "security breach", "data leak", "system failure", "outage",
            "safety incident", "accident", "injury", "emergency",

            # Contractual issues
            "termination", "cancellation", "default", "dispute", "conflict",
            "disagreement", "renegotiation", "amendment",

            # Time-sensitive
            "urgent", "immediate", "deadline", "expires", "overdue",
            "critical", "emergency", "asap"
        ]

    def get_prompt_template(self) -> str:
        return """
        Analyze the following document for potential red flags, risks, and issues that require attention. Look for:

        1. Legal or compliance issues
        2. Financial risks or problems
        3. Operational risks
        4. Contractual disputes or issues
        5. Time-sensitive matters
        6. Safety or security concerns
        7. Any unusual or concerning patterns

        For each red flag found, provide:
        - Type of issue
        - Severity level (High/Medium/Low)
        - Brief description
        - Recommended action

        Document text:
        {text}

        Red Flags Analysis:
        """

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Detect red flags and potential issues in the document."""
        self.set_status("analyzing")

        try:
            prompt = self.get_prompt_template().format(text=text[:3000])

            if self.llama_service:
                analysis = await self.generate_response(prompt)
                red_flags = self._parse_llama_red_flags(analysis)
            else:
                red_flags = self._detect_keyword_red_flags(text)

            self.set_status("completed")

            return {
                "agent": self.name,
                "red_flags": red_flags,
                "total_flags": len(red_flags),
                "severity_breakdown": self._categorize_severity(red_flags)
            }

        except Exception as e:
            self.set_status("error")
            return {
                "agent": self.name,
                "red_flags": [f"Error in analysis: {str(e)}"],
                "total_flags": 0,
                "severity_breakdown": {"high": 0, "medium": 0, "low": 0}
            }

    def _detect_keyword_red_flags(self, text: str) -> List[str]:
        """Detect red flags using keyword matching (fallback method)."""
        text_lower = text.lower()
        found_flags = []

        for keyword in self.red_flag_keywords:
            if keyword in text_lower:
                # Find context around the keyword
                pattern = re.compile(f'.{{0,50}}{re.escape(keyword)}.{{0,50}}', re.IGNORECASE)
                matches = pattern.findall(text)

                for match in matches[:2]:  # Limit to 2 matches per keyword
                    found_flags.append(f"⚠️ {keyword.title()}: ...{match.strip()}...")

        # Add some basic checks
        if "confidential" in text_lower:
            found_flags.append("🔒 Confidential Information: Document contains confidential data")

        if re.search(r'\$[\d,]+|\d+\.\d+%', text):
            found_flags.append("💰 Financial Data: Document contains financial figures")

        # Check for dates that might be deadlines
        date_pattern = r'\b(?:deadline|due|expires?|by)\s+(?:on\s+)?(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})'
        if re.search(date_pattern, text, re.IGNORECASE):
            found_flags.append("⏰ Time Sensitive: Document contains deadline information")

        return found_flags[:10]  # Limit to top 10 flags

    def _parse_llama_red_flags(self, analysis: str) -> List[str]:
        """Parse red flags from Llama3 analysis."""
        # Simple parsing - in production, use more sophisticated parsing
        lines = analysis.split('\n')
        red_flags = []

        for line in lines:
            line = line.strip()
            if line and ('red flag' in line.lower() or 'risk' in line.lower() or 'issue' in line.lower()):
                red_flags.append(line)

        return red_flags[:10]

    def _categorize_severity(self, red_flags: List[str]) -> Dict[str, int]:
        """Categorize red flags by severity."""
        high_keywords = ["lawsuit", "breach", "violation", "fraud", "bankruptcy", "critical", "emergency"]
        medium_keywords = ["risk", "issue", "concern", "deadline", "dispute"]

        severity = {"high": 0, "medium": 0, "low": 0}

        for flag in red_flags:
            flag_lower = flag.lower()
            if any(keyword in flag_lower for keyword in high_keywords):
                severity["high"] += 1
            elif any(keyword in flag_lower for keyword in medium_keywords):
                severity["medium"] += 1
            else:
                severity["low"] += 1

        return severity
