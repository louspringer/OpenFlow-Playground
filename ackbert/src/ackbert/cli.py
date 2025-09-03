"""
Command-line interface for Ack-Bert framework.

Provides CLI tools for ontology management, comparison generation,
and report creation.
"""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from .ontology import OntologyManager
from .comparison import ComparisonEngine
from .evidence import EvidenceCollector
from .visualization import DiagramGenerator


app = typer.Typer(help="Ack-Bert: Structured Candidate Comparison & Evaluation Framework")
console = Console()


@app.command()
def validate(ontology_path: Path = typer.Argument(..., help="Path to ontology file"), verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")) -> None:
    """Validate ontology file structure and content."""
    try:
        ontology = OntologyManager(ontology_path)
        issues = ontology.validate_ontology()

        if not issues:
            console.print("✅ [green]Ontology validation passed![/green]")
        else:
            console.print("❌ [red]Ontology validation failed:[/red]")
            for issue in issues:
                console.print(f"  • {issue}")

        if verbose:
            candidates = ontology.get_candidates()
            requirements = ontology.get_requirements()

            console.print(f"\n📊 [blue]Ontology Summary:[/blue]")
            console.print(f"  • Candidates: {len(candidates)}")
            console.print(f"  • Requirements: {len(requirements)}")

            for candidate in candidates:
                console.print(f"  • {candidate.name}: {len(candidate.strengths)} strengths, {len(candidate.gaps)} gaps")

    except Exception as e:
        console.print(f"❌ [red]Error validating ontology: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def compare(
    ontology_path: Path = typer.Argument(..., help="Path to ontology file"),
    output_path: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, table)"),
    generate_diagrams: bool = typer.Option(False, "--diagrams", "-d", help="Generate Mermaid diagrams"),
) -> None:
    """Generate candidate comparison report."""
    try:
        # Load ontology and create comparison engine
        ontology = OntologyManager(ontology_path)
        engine = ComparisonEngine(ontology)

        # Generate comparison report
        report = engine.generate_report()

        # Display results
        if format == "table":
            _display_comparison_table(report)
        else:
            if output_path:
                with open(output_path, "w") as f:
                    json.dump(report, f, indent=2)
                console.print(f"📄 [green]Report saved to {output_path}[/green]")
            else:
                console.print(json.dumps(report, indent=2))

        # Generate diagrams if requested
        if generate_diagrams:
            diagram_gen = DiagramGenerator()
            diagrams = diagram_gen.generate_all_diagrams(ontology, engine)

            console.print("\n🎨 [blue]Generated diagrams:[/blue]")
            for name, path in diagrams.items():
                console.print(f"  • {name}: {path}")

    except Exception as e:
        console.print(f"❌ [red]Error generating comparison: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def candidates(ontology_path: Path = typer.Argument(..., help="Path to ontology file")) -> None:
    """List all candidates in the ontology."""
    try:
        ontology = OntologyManager(ontology_path)
        candidates = ontology.get_candidates()

        if not candidates:
            console.print("📭 [yellow]No candidates found in ontology[/yellow]")
            return

        table = Table(title="Candidates")
        table.add_column("Name", style="cyan")
        table.add_column("Evidence Level", style="green")
        table.add_column("Strengths", style="blue")
        table.add_column("Gaps", style="red")

        for candidate in candidates:
            strengths_str = ", ".join(candidate.strengths) if candidate.strengths else "None"
            gaps_str = ", ".join(candidate.gaps) if candidate.gaps else "None"

            table.add_row(candidate.name, candidate.evidence_strength.label, strengths_str, gaps_str)

        console.print(table)

    except Exception as e:
        console.print(f"❌ [red]Error listing candidates: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def requirements(ontology_path: Path = typer.Argument(..., help="Path to ontology file")) -> None:
    """List all job requirements in the ontology."""
    try:
        ontology = OntologyManager(ontology_path)
        requirements = ontology.get_requirements()

        if not requirements:
            console.print("📭 [yellow]No requirements found in ontology[/yellow]")
            return

        table = Table(title="Job Requirements")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Weight", style="green")

        for req in requirements:
            table.add_row(req.name, req.description or "No description", str(req.weight))

        console.print(table)

    except Exception as e:
        console.print(f"❌ [red]Error listing requirements: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def evidence(candidate_name: str = typer.Argument(..., help="Candidate name"), ontology_path: Path = typer.Argument(..., help="Path to ontology file")) -> None:
    """Show evidence summary for a specific candidate."""
    try:
        ontology = OntologyManager(ontology_path)
        candidates = ontology.get_candidates()

        candidate = next((c for c in candidates if c.name == candidate_name), None)
        if not candidate:
            console.print(f"❌ [red]Candidate '{candidate_name}' not found[/red]")
            raise typer.Exit(1)

        # Display candidate evidence summary
        panel_content = f"""
[bold]Evidence Level:[/bold] {candidate.evidence_strength.label}
[bold]Strengths:[/bold] {', '.join(candidate.strengths) if candidate.strengths else 'None'}
[bold]Gaps:[/bold] {', '.join(candidate.gaps) if candidate.gaps else 'None'}
[bold]Comment:[/bold] {candidate.comment or 'No additional comments'}
"""

        panel = Panel(panel_content, title=f"Evidence Summary: {candidate_name}")
        console.print(panel)

    except Exception as e:
        console.print(f"❌ [red]Error showing evidence: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def init(output_dir: Path = typer.Argument(..., help="Output directory for new ontology")) -> None:
    """Initialize a new Ack-Bert ontology template."""
    try:
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create basic ontology template
        ontology_template = """@prefix ab: <http://example.org/ackbert#> .
@prefix cand: <http://example.org/candidate#> .
@prefix jd: <http://example.org/jd#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

### Core Classes
ab:Candidate a owl:Class ; rdfs:label "Candidate" .
ab:JDRequirement a owl:Class ; rdfs:label "Job Description Requirement" .
ab:EvidenceStrength a owl:Class ; rdfs:label "Evidence Strength Level" .

### Evidence Levels
ab:Level1 a ab:EvidenceStrength ; ab:level 1 ; ab:label "Self-asserted resume evidence" .
ab:Level2 a ab:EvidenceStrength ; ab:level 2 ; ab:label "Partial demo / internal artifact" .
ab:Level3 a ab:EvidenceStrength ; ab:level 3 ; ab:label "Third-party/public validation" .

### Example Requirements (customize as needed)
jd:LLMTraining a ab:JDRequirement ; rdfs:label "LLM training at scale" .
jd:PostTraining a ab:JDRequirement ; rdfs:label "Post-training (RL/contrastive/IT)" .
jd:Multimodal a ab:JDRequirement ; rdfs:label "Multimodal (graphs/3D/time-series)" .
jd:Governance a ab:JDRequirement ; rdfs:label "Governance / provenance / eval hygiene" .

### Add your candidates here following this pattern:
# cand:ExampleCandidate a ab:Candidate ;
#     rdfs:label "Example Candidate" ;
#     ab:hasEvidenceStrength ab:Level1 ;
#     ab:showsStrength jd:LLMTraining ;
#     ab:lacksArtifact jd:PostTraining .
"""

        ontology_file = output_dir / "ontology.ttl"
        with open(ontology_file, "w") as f:
            f.write(ontology_template)

        console.print(f"✅ [green]Initialized new ontology at {ontology_file}[/green]")
        console.print("📝 [blue]Edit the ontology file to add your candidates and requirements[/blue]")

    except Exception as e:
        console.print(f"❌ [red]Error initializing ontology: {e}[/red]")
        raise typer.Exit(1)


def _display_comparison_table(report: dict) -> None:
    """Display comparison report as a rich table."""
    # Summary
    summary = report["summary"]
    console.print(f"\n📊 [bold]Comparison Summary[/bold]")
    console.print(f"Candidates: {summary['total_candidates']}")
    console.print(f"Requirements: {summary['total_requirements']}")

    # Comparison matrix
    matrix = report["comparison_matrix"]
    table = Table(title="Comparison Matrix")

    # Add columns
    table.add_column("Candidate", style="cyan")
    for req in matrix["requirements"]:
        table.add_column(req, style="white")

    # Add rows
    for candidate, scores in matrix["candidates"].items():
        row = [candidate]
        for req in matrix["requirements"]:
            score = scores.get(req, "? Unknown")
            if "✓" in score:
                row.append(f"[green]{score}[/green]")
            elif "✗" in score:
                row.append(f"[red]{score}[/red]")
            else:
                row.append(f"[yellow]{score}[/yellow]")
        table.add_row(*row)

    console.print(table)

    # Recommendations
    console.print(f"\n🎯 [bold]Recommendations[/bold]")
    for rec in report["recommendations"]:
        action_color = "green" if rec["type"] == "advance" else "yellow" if rec["type"] == "keep_warm" else "red"
        console.print(f"• [bold {action_color}]{rec['candidate']}[/bold {action_color}]: {rec['action']}")


def main() -> None:
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()
