# Ack-Bert: Structured Candidate Comparison & Evaluation Framework

Ack-Bert is a methodology and toolset for systematic candidate evaluation using ontology-based comparison frameworks. It provides structured procedures for job requirement extraction, evidence review, comparison matrix generation, and recommendation synthesis.

## 🎯 Overview

Ack-Bert transforms subjective hiring decisions into structured, evidence-based evaluations through:

- **Ontology-driven modeling** of candidates, requirements, and evidence
- **Systematic evidence collection** with strength level classification
- **Automated comparison matrix generation**
- **Risk assessment and recommendation synthesis**
- **Traceable decision provenance** using W3C PROV standards

## 📁 Repository Structure

```
ackbert/
├── docs/                    # Documentation and examples
│   ├── ackbert-one-pager.md # Original session documentation
│   └── methodology.md       # Detailed methodology guide
├── ontology/               # RDF/Turtle ontology files
│   ├── ackbert-ontology.ttl # Core ontology
│   └── schemas/            # Validation schemas
├── src/ackbert/           # Python implementation
│   ├── __init__.py
│   ├── ontology.py        # Ontology management
│   ├── comparison.py      # Comparison engine
│   ├── evidence.py        # Evidence collection
│   └── visualization.py   # Diagram generation
├── tests/                 # Test suite
├── examples/              # Example comparisons
├── scripts/               # Utility scripts
└── pyproject.toml         # Project configuration
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ackbert

# Install dependencies
uv sync

# Run tests
uv run pytest tests/
```

### Basic Usage

```python
from ackbert import ComparisonEngine, OntologyManager

# Initialize the system
ontology = OntologyManager("ontology/ackbert-ontology.ttl")
engine = ComparisonEngine(ontology)

# Load job requirements
requirements = engine.extract_requirements("job_description.md")

# Add candidates
engine.add_candidate("candidate1", evidence_data)
engine.add_candidate("candidate2", evidence_data)

# Generate comparison
matrix = engine.generate_comparison_matrix()
recommendations = engine.synthesize_recommendations()
```

## 🔧 Core Components

### 1. Ontology Management

- RDF/Turtle-based candidate and requirement modeling
- Evidence strength level classification (Level 1-3)
- Provenance tracking using W3C PROV standards

### 2. Evidence Collection

- Structured evidence gathering from resumes, portfolios, public sources
- Strength level assessment (self-asserted → partial demo → public validation)
- Gap analysis against job requirements

### 3. Comparison Engine

- Automated comparison matrix generation
- Risk assessment and mitigation strategies
- Recommendation synthesis with traceable reasoning

### 4. Visualization

- Mermaid diagram generation for process flows
- Interactive comparison matrices
- Decision tree visualization

## 📊 Methodology

The Ack-Bert methodology follows a structured 4-step process:

1. **JD Extraction** → Enumerate requirements and success criteria
1. **Evidence Review** → Collect and classify candidate evidence
1. **Comparison Matrix** → Synthesize head-to-head analysis
1. **Recommendation Synthesis** → Generate actionable hiring recommendations

## 🎨 Example Output

See `docs/ackbert-one-pager.md` for a complete example of the methodology applied to a real candidate comparison scenario.

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/

# Run with coverage
uv run pytest --cov=src/ackbert tests/

# Validate ontology
uv run python scripts/validate_ontology.py
```

## 📚 Documentation

- [Methodology Guide](docs/methodology.md) - Detailed process documentation
- [API Reference](docs/api.md) - Python API documentation
- [Ontology Schema](ontology/ackbert-ontology.ttl) - RDF ontology definition
- [Examples](examples/) - Sample comparisons and use cases

## 🤝 Contributing

1. Fork the repository
1. Create a feature branch
1. Add tests for new functionality
1. Ensure all tests pass
1. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- W3C PROV for provenance standards
- RDF/Turtle for semantic modeling
- Mermaid for diagram generation
