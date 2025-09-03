"""
Visualization tools for Ack-Bert framework.

Generates Mermaid diagrams and other visual representations of
comparison data and methodology flows.
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from pathlib import Path

from .ontology import OntologyManager
from .comparison import ComparisonEngine, ComparisonMatrix


@dataclass
class DiagramConfig:
    """Configuration for diagram generation."""

    theme: str = "default"
    direction: str = "TD"  # Top-Down
    node_style: str = "rounded"
    edge_style: str = "solid"


class DiagramGenerator:
    """Generates Mermaid diagrams for Ack-Bert framework."""

    def __init__(self, config: Optional[DiagramConfig] = None):
        self.config = config or DiagramConfig()

    def generate_methodology_flow(self) -> str:
        """Generate methodology flow diagram."""
        mermaid = """flowchart TD
    A[JD Requirements] --> B[Candidate Evidence Review]
    B --> C[Comparison Matrix]
    C --> D[Risk Assessment]
    D --> E[Recommendation Synthesis]
    E --> F[One-Pager Report]
    
    B --> G[Evidence Strength Levels]
    G --> G1[Level 1: Self-asserted]
    G --> G2[Level 2: Partial demo]
    G --> G3[Level 3: Public validation]
    
    C --> H[Requirements Mapping]
    H --> H1[Strengths]
    H --> H2[Gaps]
    H --> H3[Unknown]
    
    D --> I[Risk Levels]
    I --> I1[Low Risk]
    I --> I2[Medium Risk]
    I --> I3[High Risk]
    
    E --> J[Recommendation Types]
    J --> J1[Advance]
    J --> J2[Keep Warm]
    J --> J3[Request More Info]
    J --> J4[Reject]
"""
        return mermaid

    def generate_domain_model(self) -> str:
        """Generate domain model class diagram."""
        mermaid = """classDiagram
    class Candidate {
        +name: string
        +evidenceStrength: EvidenceStrength
        +strengths: JDRequirement[*]
        +gaps: JDRequirement[*]
        +comment: string
    }
    
    class EvidenceStrength {
        +level: int
        +label: string
        +description: string
    }
    
    class JDRequirement {
        +name: string
        +description: string
        +weight: float
    }
    
    class Artifact {
        +type: string
        +generatedBy: Procedure
        +concernsCandidate: Candidate
        +targetsRequirement: JDRequirement
    }
    
    class Recommendation {
        +candidateName: string
        +type: RecommendationType
        +action: string
        +reasoning: string
        +nextSteps: string[*]
    }
    
    class RiskAssessment {
        +candidateName: string
        +level: RiskLevel
        +description: string
        +mitigationStrategies: string[*]
    }
    
    class Procedure {
        +steps: string
        +requestedBy: Stakeholder
        +performedBy: Stakeholder
        +producedArtifact: Artifact
    }
    
    class Stakeholder {
        +name: string
    }
    
    Candidate --> EvidenceStrength : hasEvidenceStrength
    Candidate --> JDRequirement : showsStrength
    Candidate --> JDRequirement : lacksArtifact
    Artifact --> Candidate : concernsCandidate
    Artifact --> Recommendation : supportsRecommendation
    Artifact --> JDRequirement : targetsRequirement
    Artifact --> Procedure : generatedBy
    Procedure --> Stakeholder : requestedBy/performedBy
    RiskAssessment --> Candidate : concernsCandidate
    Recommendation --> Candidate : concernsCandidate
"""
        return mermaid

    def generate_comparison_matrix_diagram(self, matrix: ComparisonMatrix) -> str:
        """Generate comparison matrix visualization."""
        candidates = list(matrix.matrix.keys())
        requirements = matrix.requirements

        mermaid = f"""graph TD
    subgraph "Comparison Matrix"
        subgraph "Requirements"
"""

        for req in requirements:
            mermaid += f'            R_{req.name.replace(" ", "_")}["{req.name}"]\n'

        mermaid += '        end\n\n        subgraph "Candidates"\n'

        for candidate in candidates:
            mermaid += f'            C_{candidate.replace(" ", "_")}["{candidate}"]\n'

        mermaid += "        end\n    end\n\n"

        # Add connections based on matrix data
        for candidate, req_scores in matrix.matrix.items():
            for req, score in req_scores.items():
                req_id = req.replace(" ", "_")
                cand_id = candidate.replace(" ", "_")

                if "✓" in score:
                    mermaid += f'    R_{req_id} -->|"Strength"| C_{cand_id}\n'
                elif "✗" in score:
                    mermaid += f'    R_{req_id} -.->|"Gap"| C_{cand_id}\n'
                else:
                    mermaid += f'    R_{req_id} -.-|"Unknown"| C_{cand_id}\n'

        return mermaid

    def generate_evidence_flow(self, candidate_name: str, evidence_summary: Dict) -> str:
        """Generate evidence flow diagram for a candidate."""
        mermaid = f"""flowchart TD
    A["{candidate_name}"] --> B[Evidence Collection]
    
    B --> C[Evidence Sources]
    C --> C1[Resume]
    C --> C2[Portfolio]
    C --> C3[Public Repository]
    C --> C4[Publications]
    C --> C5[Demos]
    C --> C6[References]
    
    B --> D[Evidence Strength]
    D --> D1[Level 1: Self-asserted]
    D --> D2[Level 2: Partial demo]
    D --> D3[Level 3: Public validation]
    
    B --> E[Requirements Coverage]
    E --> E1[Covered: {len(evidence_summary.get('requirements_covered', []))}]
    E --> E2[Gaps: TBD]
    
    B --> F[Overall Assessment]
    F --> F1["Strength: {evidence_summary.get('overall_strength', {}).get('label', 'Unknown')}"]
    F --> F2["Total Items: {evidence_summary.get('total_items', 0)}"]
"""
        return mermaid

    def generate_decision_tree(self, recommendations: List[Dict]) -> str:
        """Generate decision tree for recommendations."""
        mermaid = """flowchart TD
    A[Start Evaluation] --> B{Evidence Level?}
    
    B -->|Level 3| C{Strengths >= 3?}
    B -->|Level 2| D{Strengths >= 2?}
    B -->|Level 1| E{Any Strengths?}
    
    C -->|Yes| F[ADVANCE]
    C -->|No| G{Strengths >= 2?}
    
    D -->|Yes| H[KEEP WARM]
    D -->|No| I{Any Strengths?}
    
    E -->|Yes| J[REQUEST MORE INFO]
    E -->|No| K[REJECT]
    
    G -->|Yes| H
    G -->|No| J
    
    I -->|Yes| J
    I -->|No| K
    
    F --> L[Technical Screen]
    H --> M[Talent Pipeline]
    J --> N[Evidence Request]
    K --> O[Polite Rejection]
"""
        return mermaid

    def generate_risk_assessment_diagram(self, risks: List[Dict]) -> str:
        """Generate risk assessment visualization."""
        mermaid = """graph TD
    subgraph "Risk Assessment"
        subgraph "Risk Levels"
            LOW[Low Risk<br/>Strong evidence<br/>Many strengths]
            MEDIUM[Medium Risk<br/>Some gaps<br/>Moderate evidence]
            HIGH[High Risk<br/>Many gaps<br/>Weak evidence]
        end
        
        subgraph "Mitigation Strategies"
            M1[Address Knowledge Gaps]
            M2[Request Additional Evidence]
            M3[Technical Screening]
            M4[Trial Project]
        end
    end
    
    LOW --> M1
    MEDIUM --> M2
    HIGH --> M3
    HIGH --> M4
"""
        return mermaid

    def generate_process_sequence(self) -> str:
        """Generate process sequence diagram."""
        mermaid = """sequenceDiagram
    participant HM as Hiring Manager
    participant AB as Ack-Bert System
    participant C1 as Candidate 1
    participant C2 as Candidate 2
    participant Repo as Artifact Repository
    
    HM->>AB: Request candidate comparison
    AB->>C1: Gather evidence (resume/claims)
    AB->>C2: Gather evidence (public sources)
    AB->>Repo: Store evidence items
    AB->>AB: Generate comparison matrix
    AB->>AB: Assess risks
    AB->>AB: Synthesize recommendations
    AB->>Repo: Generate artifacts
    AB->>HM: Deliver one-pager report
"""
        return mermaid

    def save_diagram(self, content: str, filename: str, output_dir: Path = Path("docs/diagrams")) -> Path:
        """Save Mermaid diagram to file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / f"{filename}.mmd"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return file_path

    def generate_all_diagrams(self, ontology_manager: OntologyManager, comparison_engine: ComparisonEngine) -> Dict[str, Path]:
        """Generate all standard diagrams and return file paths."""
        diagrams = {}
        output_dir = Path("docs/diagrams")

        # Generate methodology flow
        methodology = self.generate_methodology_flow()
        diagrams["methodology"] = self.save_diagram(methodology, "methodology_flow", output_dir)

        # Generate domain model
        domain_model = self.generate_domain_model()
        diagrams["domain_model"] = self.save_diagram(domain_model, "domain_model", output_dir)

        # Generate comparison matrix
        matrix = comparison_engine.generate_comparison_matrix()
        matrix_diagram = self.generate_comparison_matrix_diagram(matrix)
        diagrams["comparison_matrix"] = self.save_diagram(matrix_diagram, "comparison_matrix", output_dir)

        # Generate decision tree
        recommendations = comparison_engine.synthesize_recommendations()
        rec_dicts = [{"candidate": rec.candidate_name, "type": rec.type.value, "action": rec.action} for rec in recommendations]
        decision_tree = self.generate_decision_tree(rec_dicts)
        diagrams["decision_tree"] = self.save_diagram(decision_tree, "decision_tree", output_dir)

        # Generate process sequence
        sequence = self.generate_process_sequence()
        diagrams["process_sequence"] = self.save_diagram(sequence, "process_sequence", output_dir)

        # Generate risk assessment
        risks = comparison_engine.assess_risks()
        risk_dicts = [{"candidate": risk.candidate_name, "level": risk.level.value, "description": risk.description} for risk in risks]
        risk_diagram = self.generate_risk_assessment_diagram(risk_dicts)
        diagrams["risk_assessment"] = self.save_diagram(risk_diagram, "risk_assessment", output_dir)

        return diagrams
