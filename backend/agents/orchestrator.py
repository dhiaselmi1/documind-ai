from agents.summary_agent import SummaryAgent
from agents.red_flag_agent import RedFlagAgent
from agents.decision_agent import DecisionAgent
from typing import Dict, Any,List
import asyncio

class AgentOrchestrator:
    """Orchestrates multiple agents to collaboratively analyze documents."""

    def __init__(self, llama_service="llama3"):
        self.llama_service = llama_service
        self.agents = {
            "summary": SummaryAgent(llama_service),
            "red_flag": RedFlagAgent(llama_service),
            "decision": DecisionAgent(llama_service)
        }
        self.analysis_history = []

    async def analyze_document(self, text: str) -> Dict[str, Any]:
        """Run all agents on the document and aggregate results."""
        print("[DEBUG] Agent results:")
        # Reset all agent statuses
        for agent in self.agents.values():
            agent.set_status("ready")

        try:
            # Run all agents concurrently
            tasks = []
            for agent_name, agent in self.agents.items():
                task = asyncio.create_task(agent.analyze(text))
                tasks.append((agent_name, task))

            # Wait for all agents to complete
            results = {}
            for agent_name, task in tasks:
                agent_result = await task
                results[agent_name] = agent_result

            # --- DEBUG: print results ---
            print("[DEBUG] Agent results:", results)

            # Aggregate results
            aggregated_results = self._aggregate_results(results, text)

            # Store in history
            self.analysis_history.append(aggregated_results)

            # --- DEBUG: print aggregated results ---
            print("[DEBUG] Aggregated results:", aggregated_results)

            return aggregated_results

        except Exception as e:
            print("[ERROR] Analysis failed:", str(e))
            return {
                "status": "error",
                "error": str(e),
                "summary": "Analysis failed",
                "red_flags": [],
                "decisions": []
            }


    def _aggregate_results(self, results: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Aggregate results from all agents into a unified response."""

        # Extract individual agent results
        summary_result = results.get("summary", {})
        red_flag_result = results.get("red_flag", {})
        decision_result = results.get("decision", {})

        # Create collaborative insights
        collaborative_insights = self._generate_collaborative_insights(results)

        return {
            "status": "completed",
            "summary": summary_result.get("summary", "No summary available"),
            "red_flags": red_flag_result.get("red_flags", []),
            "decisions": decision_result.get("decisions", []),
            "statistics": {
                "document_length": len(original_text),
                "word_count": len(original_text.split()),
                "total_red_flags": red_flag_result.get("total_flags", 0),
                "total_decisions": decision_result.get("total_decisions", 0),
                "key_topics": summary_result.get("key_topics", [])
            },
            "collaborative_insights": collaborative_insights,
            "agent_status": self.get_agent_status()
        }

    def _generate_collaborative_insights(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from collaborative agent analysis."""

        red_flags = results.get("red_flag", {}).get("red_flags", [])
        decisions = results.get("decision", {}).get("decisions", [])

        # Risk assessment
        risk_level = "Low"
        if len(red_flags) > 5:
            risk_level = "High"
        elif len(red_flags) > 2:
            risk_level = "Medium"

        # Urgency assessment
        urgency = "Normal"
        urgent_keywords = ["urgent", "immediate", "critical", "emergency", "deadline"]

        all_text = " ".join(red_flags + decisions).lower()
        if any(keyword in all_text for keyword in urgent_keywords):
            urgency = "High"

        # Document complexity
        total_items = len(red_flags) + len(decisions)
        if total_items > 10:
            complexity = "High"
        elif total_items > 5:
            complexity = "Medium"
        else:
            complexity = "Low"

        return {
            "risk_level": risk_level,
            "urgency": urgency,
            "complexity": complexity,
            "requires_attention": len(red_flags) > 0,
            "has_action_items": len(decisions) > 0,
            "confidence_score": self._calculate_confidence_score(results)
        }

    def _calculate_confidence_score(self, results: Dict[str, Any]) -> float:
        """Calculate confidence score based on agent results."""
        # Simple confidence calculation
        base_score = 0.7

        # Increase confidence if multiple agents found consistent results
        if results.get("summary", {}).get("summary") and len(results.get("summary", {}).get("summary", "")) > 50:
            base_score += 0.1

        if len(results.get("red_flag", {}).get("red_flags", [])) > 0:
            base_score += 0.1

        if len(results.get("decision", {}).get("decisions", [])) > 0:
            base_score += 0.1

        return min(base_score, 1.0)

    def get_agent_status(self) -> Dict[str, Dict[str, str]]:
        """Get status of all agents."""
        return {name: agent.get_status() for name, agent in self.agents.items()}

    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Get history of all analyses."""
        return self.analysis_history[-10:]  # Return last 10 analyses
