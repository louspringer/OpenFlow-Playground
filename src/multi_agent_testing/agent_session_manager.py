#!/usr/bin/env python3
"""
Agent Session Manager - Enables context-aware, collaborative multi-agent analysis

This system provides:
1. Session context for each agent type
2. Cross-posting of findings between agents
3. Iteration-to-iteration learning
4. Collaborative analysis synthesis
"""

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class AgentType(Enum):
    """Types of agents in the multi-agent system"""

    SECURITY = "security_expert"
    QUALITY = "code_quality_expert"
    DEVOPS = "devops_expert"


@dataclass
class AgentFinding:
    """Represents a finding from an agent"""

    agent_type: AgentType
    finding_id: str
    category: str
    severity: str
    description: str
    recommendations: list[str]
    confidence: float
    timestamp: str
    metadata: dict[str, Any]
    cross_references: list[str] | None = None  # IDs of related findings from other agents


@dataclass
class AgentSession:
    """Session context for a specific agent"""

    agent_type: AgentType
    session_id: str
    iteration_number: int
    previous_findings: list[AgentFinding]
    learning_context: dict[str, Any]
    collaboration_history: list[dict[str, Any]]
    current_context: dict[str, Any]
    created_at: str
    updated_at: str


@dataclass
class IterationContext:
    """Context for a complete PDCA iteration"""

    iteration_number: int
    start_time: str
    end_time: str
    agent_sessions: dict[AgentType, AgentSession]
    cross_agent_insights: list[dict[str, Any]]
    synthesis: dict[str, Any]
    learning_outcomes: list[str]


class AgentSessionManager:
    """Manages agent sessions, context, and collaborative learning"""

    def __init__(self, storage_dir: str = "agent_sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

        # Current iteration tracking
        self.current_iteration = 0
        self.iteration_contexts: dict[int, IterationContext] = {}

        # Active agent sessions
        self.active_sessions: dict[AgentType, AgentSession] = {}

        # Cross-agent collaboration tracking
        self.collaboration_graph: dict[str, set[str]] = {}

        # Load existing context
        self._load_existing_context()

    def _load_existing_context(self) -> None:
        """Load existing iteration contexts from storage"""
        try:
            context_files = list(self.storage_dir.glob("iteration_*.json"))
            if context_files:
                # Find the highest iteration number
                max_iteration = max(int(f.stem.split("_")[1]) for f in context_files if f.stem.startswith("iteration_"))
                self.current_iteration = max_iteration

                # Load the most recent context
                latest_context_file = self.storage_dir / f"iteration_{max_iteration}.json"
                if latest_context_file.exists():
                    with open(latest_context_file) as f:
                        context_data = json.load(f)
                        self.iteration_contexts[max_iteration] = self._deserialize_context(context_data)
                        print(f"📋 Loaded existing context from iteration {max_iteration}")
        except Exception as e:
            print(f"⚠️ Error loading existing context: {e}")

    def start_new_iteration(self) -> int:
        """Start a new PDCA iteration"""
        self.current_iteration += 1
        print(f"🔄 Starting new iteration {self.current_iteration}")

        # Create new iteration context
        iteration_context = IterationContext(
            iteration_number=self.current_iteration,
            start_time=datetime.now().isoformat(),
            end_time="",
            agent_sessions={},
            cross_agent_insights=[],
            synthesis={},
            learning_outcomes=[],
        )

        self.iteration_contexts[self.current_iteration] = iteration_context

        # Initialize agent sessions for this iteration
        for agent_type in AgentType:
            session = self._create_agent_session(agent_type, self.current_iteration)
            self.active_sessions[agent_type] = session
            iteration_context.agent_sessions[agent_type] = session

        return self.current_iteration

    def _create_agent_session(self, agent_type: AgentType, iteration_number: int) -> AgentSession:
        """Create a new session for an agent"""
        session_id = f"{agent_type.value}_{iteration_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Load learning context from previous iterations
        learning_context = self._build_learning_context(agent_type, iteration_number)

        # Load previous findings from this agent type
        previous_findings = self._get_agent_previous_findings(agent_type, iteration_number)

        return AgentSession(
            agent_type=agent_type,
            session_id=session_id,
            iteration_number=iteration_number,
            previous_findings=previous_findings,
            learning_context=learning_context,
            collaboration_history=[],
            current_context={},
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

    def _build_learning_context(self, agent_type: AgentType, iteration_number: int) -> dict[str, Any]:
        """Build learning context for an agent based on previous iterations"""
        learning_context = {
            "previous_iterations": [],
            "successful_strategies": [],
            "failed_approaches": [],
            "cross_agent_insights": [],
            "cumulative_findings": {},
        }

        # Analyze previous iterations for learning
        for iter_num in range(1, iteration_number):
            if iter_num in self.iteration_contexts:
                context = self.iteration_contexts[iter_num]

                # Get this agent's previous session
                if agent_type in context.agent_sessions:
                    prev_session = context.agent_sessions[agent_type]

                    # Analyze what worked and what didn't
                    if prev_session.previous_findings:
                        learning_context["previous_iterations"].append(
                            {
                                "iteration": iter_num,
                                "findings_count": len(prev_session.previous_findings),
                                "key_insights": self._extract_key_insights(prev_session.previous_findings),
                            }
                        )

                        # Track successful vs failed approaches
                        for finding in prev_session.previous_findings:
                            if finding.confidence > 0.7:
                                learning_context["successful_strategies"].append(
                                    {
                                        "category": finding.category,
                                        "approach": finding.description,
                                        "confidence": finding.confidence,
                                    }
                                )
                            else:
                                learning_context["failed_approaches"].append(
                                    {
                                        "category": finding.category,
                                        "approach": finding.description,
                                        "confidence": finding.confidence,
                                    }
                                )

        return learning_context

    def _get_agent_previous_findings(self, agent_type: AgentType, iteration_number: int) -> list[AgentFinding]:
        """Get previous findings from this agent type across iterations"""
        previous_findings = []

        for iter_num in range(1, iteration_number):
            if iter_num in self.iteration_contexts:
                context = self.iteration_contexts[iter_num]
                if agent_type in context.agent_sessions:
                    session = context.agent_sessions[agent_type]
                    previous_findings.extend(session.previous_findings)

        return previous_findings

    def get_agent_previous_findings(self, agent_type: AgentType, iteration_number: int) -> list[AgentFinding]:
        """Get previous findings for a specific agent from a specific iteration"""
        try:
            if iteration_number in self.iteration_contexts:
                context = self.iteration_contexts[iteration_number]
                if agent_type in context.agent_sessions:
                    return context.agent_sessions[agent_type].previous_findings
            return []
        except Exception as e:
            print(f"⚠️ Error getting previous findings for {agent_type.value}: {e}")
            return []

    def _extract_key_insights(self, findings: list[AgentFinding]) -> list[str]:
        """Extract key insights from a list of findings"""
        insights = []
        for finding in findings:
            if finding.confidence > 0.8:
                insights.append(f"{finding.category}: {finding.description[:100]}...")
        return insights[:5]  # Top 5 insights

    def update_agent_context(self, agent_type: AgentType, context: dict[str, Any]) -> None:
        """Update the current context for an agent"""
        if agent_type in self.active_sessions:
            session = self.active_sessions[agent_type]
            session.current_context.update(context)
            session.updated_at = datetime.now().isoformat()

    def add_agent_finding(self, agent_type: AgentType, finding: AgentFinding) -> str:
        """Add a finding from an agent and return the finding ID"""
        if agent_type in self.active_sessions:
            session = self.active_sessions[agent_type]
            session.previous_findings.append(finding)
            session.updated_at = datetime.now().isoformat()

            # Add to iteration context
            if self.current_iteration in self.iteration_contexts:
                self.iteration_contexts[self.current_iteration].agent_sessions[agent_type] = session

            # Generate finding ID if not provided
            if not finding.finding_id:
                finding.finding_id = self._generate_finding_id(finding)

            return finding.finding_id

        return ""

    def _generate_finding_id(self, finding: AgentFinding) -> str:
        """Generate a unique ID for a finding"""
        content = f"{finding.agent_type.value}_{finding.category}_{finding.description[:50]}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def get_cross_agent_context(self, agent_type: AgentType) -> dict[str, Any]:
        """Get context from other agents for cross-posting analysis"""
        cross_context = {
            "other_agents_findings": {},
            "collaborative_insights": [],
            "shared_context": {},
        }

        if self.current_iteration in self.iteration_contexts:
            context = self.iteration_contexts[self.current_iteration]

            for other_agent_type, other_session in context.agent_sessions.items():
                if other_agent_type != agent_type:
                    cross_context["other_agents_findings"][other_agent_type.value] = {
                        "findings": [asdict(f) for f in other_session.previous_findings],
                        "key_insights": self._extract_key_insights(other_session.previous_findings),
                        "learning_context": other_session.learning_context,
                    }

            # Add cross-agent insights from previous iterations
            cross_context["collaborative_insights"] = context.cross_agent_insights

        return cross_context

    def add_cross_agent_insight(self, insight: dict[str, Any]) -> None:
        """Add a cross-agent insight to the current iteration"""
        if self.current_iteration in self.iteration_contexts:
            self.iteration_contexts[self.current_iteration].cross_agent_insights.append(insight)

    def synthesize_iteration_results(self) -> dict[str, Any]:
        """Synthesize results from all agents in the current iteration"""
        if self.current_iteration not in self.iteration_contexts:
            return {}

        context = self.iteration_contexts[self.current_iteration]
        context.end_time = datetime.now().isoformat()

        # Collect all findings
        all_findings = []
        for agent_type, session in context.agent_sessions.items():
            for finding in session.previous_findings:
                all_findings.append({"agent": agent_type.value, "finding": asdict(finding)})

        # Analyze patterns across agents
        patterns = self._analyze_cross_agent_patterns(all_findings)

        # Generate collaborative insights
        collaborative_insights = self._generate_collaborative_insights(all_findings)

        # Create synthesis
        synthesis = {
            "total_findings": len(all_findings),
            "findings_by_agent": {agent_type.value: len(session.previous_findings) for agent_type, session in context.agent_sessions.items()},
            "cross_agent_patterns": patterns,
            "collaborative_insights": collaborative_insights,
            "recommendations": self._generate_synthesis_recommendations(all_findings, patterns),
            "learning_outcomes": self._extract_learning_outcomes(context),
        }

        context.synthesis = synthesis

        # Save iteration context
        self._save_iteration_context(self.current_iteration)

        return synthesis

    def _analyze_cross_agent_patterns(self, all_findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Analyze patterns across different agents' findings"""
        patterns = []

        # Group findings by category
        categories = {}
        for finding_data in all_findings:
            category = finding_data["finding"]["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(finding_data)

        # Find categories with multiple agent perspectives
        for category, findings in categories.items():
            if len(findings) > 1:
                agents = list({f["agent"] for f in findings})
                if len(agents) > 1:
                    patterns.append(
                        {
                            "category": category,
                            "agents_involved": agents,
                            "findings_count": len(findings),
                            "consensus_level": self._calculate_consensus(findings),
                            "key_insights": self._extract_category_insights(findings),
                        }
                    )

        return patterns

    def _calculate_consensus(self, findings: list[dict[str, Any]]) -> float:
        """Calculate consensus level among findings in a category"""
        if not findings:
            return 0.0

        # Simple consensus based on confidence levels
        avg_confidence = sum(f["finding"]["confidence"] for f in findings) / len(findings)
        return min(avg_confidence, 1.0)

    def _extract_category_insights(self, findings: list[dict[str, Any]]) -> list[str]:
        """Extract key insights from findings in a category"""
        insights = []
        for finding_data in findings:
            finding = finding_data["finding"]
            if finding["confidence"] > 0.7:
                insights.append(f"{finding_data['agent']}: {finding['description'][:100]}...")
        return insights[:3]

    def _generate_collaborative_insights(self, all_findings: list[dict[str, Any]]) -> list[str]:
        """Generate insights from collaborative analysis"""
        insights = []

        # Find findings that complement each other
        for i, finding1 in enumerate(all_findings):
            for j, finding2 in enumerate(all_findings[i + 1 :], i + 1):
                if self._findings_complement(finding1, finding2):
                    insight = f"Collaborative insight: {finding1['agent']} and {finding2['agent']} findings complement each other on {finding1['finding']['category']}"
                    insights.append(insight)

        return insights[:5]

    def _findings_complement(self, finding1: dict[str, Any], finding2: dict[str, Any]) -> bool:
        """Check if two findings complement each other"""
        # Simple heuristic: different agents, same category, high confidence
        return (
            finding1["agent"] != finding2["agent"]
            and finding1["finding"]["category"] == finding2["finding"]["category"]
            and finding1["finding"]["confidence"] > 0.7
            and finding2["finding"]["confidence"] > 0.7
        )

    def _generate_synthesis_recommendations(self, all_findings: list[dict[str, Any]], patterns: list[dict[str, Any]]) -> list[str]:
        """Generate recommendations based on synthesis"""
        recommendations = []

        # High-priority recommendations based on cross-agent consensus
        for pattern in patterns:
            if pattern["consensus_level"] > 0.8:
                recommendations.append(f"High priority: Address {pattern['category']} - {len(pattern['agents_involved'])} agents agree")

        # Recommendations based on high-confidence findings
        high_confidence_findings = [f for f in all_findings if f["finding"]["confidence"] > 0.9]

        for finding_data in high_confidence_findings:
            finding = finding_data["finding"]
            recommendations.append(f"Critical: {finding['description'][:100]}... (from {finding_data['agent']})")

        return recommendations[:10]

    def _extract_learning_outcomes(self, context: IterationContext) -> list[str]:
        """Extract learning outcomes from the iteration"""
        outcomes = []

        # Analyze what was learned
        total_findings = sum(len(session.previous_findings) for session in context.agent_sessions.values())
        if total_findings > 0:
            outcomes.append(f"Generated {total_findings} findings across {len(context.agent_sessions)} agents")

        if context.cross_agent_insights:
            outcomes.append(f"Identified {len(context.cross_agent_insights)} cross-agent insights")

        # Add specific learning outcomes
        for agent_type, session in context.agent_sessions.items():
            if session.learning_context.get("successful_strategies"):
                outcomes.append(f"{agent_type.value}: {len(session.learning_context['successful_strategies'])} successful strategies identified")

        return outcomes

    def _save_iteration_context(self, iteration_number: int) -> None:
        """Save iteration context to file"""
        try:
            context = self.iteration_contexts[iteration_number]

            # Convert to serializable format
            context_data = {
                "iteration_number": context.iteration_number,
                "start_time": context.start_time,
                "end_time": context.end_time,
                "agent_sessions": {},
                "cross_agent_insights": context.cross_agent_insights,
                "synthesis": context.synthesis,
                "learning_outcomes": context.learning_outcomes,
            }

            # Convert agent sessions to serializable format
            for agent_type, session in context.agent_sessions.items():
                context_data["agent_sessions"][agent_type.value] = {
                    "agent_type": session.agent_type.value,
                    "session_id": session.session_id,
                    "iteration_number": session.iteration_number,
                    "previous_findings": [
                        {
                            "agent_type": finding.agent_type.value,
                            "finding_id": finding.finding_id,
                            "category": finding.category,
                            "severity": finding.severity,
                            "description": finding.description,
                            "recommendations": finding.recommendations,
                            "confidence": finding.confidence,
                            "timestamp": finding.timestamp,
                            "metadata": finding.metadata,
                            "cross_references": finding.cross_references or [],
                        }
                        for finding in session.previous_findings
                    ],
                    "learning_context": session.learning_context,
                    "collaboration_history": session.collaboration_history,
                    "current_context": session.current_context,
                    "created_at": session.created_at,
                    "updated_at": session.updated_at,
                }

            # Save to file
            context_file = self.storage_dir / f"iteration_{iteration_number}_context.json"
            with open(context_file, "w") as f:
                json.dump(context_data, f, indent=2)

        except Exception as e:
            print(f"⚠️ Failed to save iteration {iteration_number} context: {e}")

    def _deserialize_context(self, context_data: dict[str, Any]) -> IterationContext:
        """Deserialize context data back to IterationContext object"""
        try:
            # Parse agent sessions
            agent_sessions = {}
            for agent_type_str, session_data in context_data.get("agent_sessions", {}).items():
                try:
                    agent_type = AgentType(agent_type_str)
                    # Reconstruct agent session
                    session = AgentSession(
                        agent_type=agent_type,
                        session_id=session_data["session_id"],
                        iteration_number=session_data["iteration_number"],
                        previous_findings=[
                            AgentFinding(
                                agent_type=AgentType(finding_data["agent_type"]),
                                finding_id=finding_data["finding_id"],
                                category=finding_data["category"],
                                severity=finding_data["severity"],
                                description=finding_data["description"],
                                recommendations=finding_data["recommendations"],
                                confidence=finding_data["confidence"],
                                timestamp=finding_data["timestamp"],
                                metadata=finding_data["metadata"],
                                cross_references=finding_data.get("cross_references", []),
                            )
                            for finding_data in session_data.get("previous_findings", [])
                        ],
                        learning_context=session_data.get("learning_context", {}),
                        collaboration_history=session_data.get("collaboration_history", []),
                        current_context=session_data.get("current_context", {}),
                        created_at=session_data.get("created_at", ""),
                        updated_at=session_data.get("updated_at", ""),
                    )
                    agent_sessions[agent_type] = session
                except Exception as e:
                    print(f"⚠️ Failed to deserialize agent session for {agent_type_str}: {e}")
                    continue

            # Create iteration context
            return IterationContext(
                iteration_number=context_data["iteration_number"],
                start_time=context_data["start_time"],
                end_time=context_data["end_time"],
                agent_sessions=agent_sessions,
                cross_agent_insights=context_data.get("cross_agent_insights", []),
                synthesis=context_data.get("synthesis", {}),
                learning_outcomes=context_data.get("learning_outcomes", []),
            )

        except Exception as e:
            print(f"⚠️ Failed to deserialize context: {e}")
            return None

    def get_iteration_summary(self, iteration_number: int) -> dict[str, Any]:
        """Get a summary of a specific iteration"""
        if iteration_number in self.iteration_contexts:
            context = self.iteration_contexts[iteration_number]
            return {
                "iteration": iteration_number,
                "start_time": context.start_time,
                "end_time": context.end_time,
                "total_findings": sum(len(session.previous_findings) for session in context.agent_sessions.values()),
                "agents_used": list(context.agent_sessions.keys()),
                "cross_agent_insights_count": len(context.cross_agent_insights),
                "synthesis_available": bool(context.synthesis),
            }
        return {}

    def get_learning_summary(self) -> dict[str, Any]:
        """Get a summary of learning across all iterations"""
        summary = {
            "total_iterations": len(self.iteration_contexts),
            "iterations": [],
            "cumulative_findings": 0,
            "learning_trends": [],
        }

        for iter_num in sorted(self.iteration_contexts.keys()):
            self.iteration_contexts[iter_num]
            iter_summary = self.get_iteration_summary(iter_num)
            summary["iterations"].append(iter_summary)
            summary["cumulative_findings"] += iter_summary["total_findings"]

        return summary
