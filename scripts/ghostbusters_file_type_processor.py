#!/usr/bin/env python3
"""
Ghostbusters File Type Processor - Paranormal Investigation for Unknown File Types

This module implements Ghostbusters technology for file type discovery:
- PKE Meter: Detects file type patterns and measures confidence
- Ghost Classification: Categorizes files by type and threat level
- Proton Pack: Handles parsing exceptions gracefully
- Paranormal Investigation: Systematic discovery with learning
"""

import ast
import configparser
import json
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import tomllib
import yaml


class PKEEnergyLevel(Enum):
    """PKE Meter energy levels for file type detection"""

    ZERO = "zero"  # No detectable patterns
    LOW = "low"  # Weak patterns detected
    MEDIUM = "medium"  # Moderate pattern strength
    HIGH = "high"  # Strong pattern signals
    CRITICAL = "critical"  # Overwhelming pattern evidence


class GhostClass(Enum):
    """Ghost classification system for file types"""

    CLASS_1 = "class_1"  # Harmless (simple text, generic)
    CLASS_2 = "class_2"  # Mild (basic structured files)
    CLASS_3 = "class_3"  # Moderate (complex structured files)
    CLASS_4 = "class_4"  # Dangerous (malformed, corrupted)
    CLASS_5 = "class_5"  # Lethal (unparseable, unknown)


class ProtonStreamMode(Enum):
    """Proton Pack stream modes for exception handling"""

    STUN = "stun"  # Graceful degradation
    CAPTURE = "capture"  # Force parsing attempt
    NEUTRALIZE = "neutralize"  # Skip problematic files
    CONTAIN = "contain"  # Isolate and analyze


@dataclass
class PKEMeterReading:
    """PKE Meter reading for file type detection"""

    energy_level: PKEEnergyLevel
    pattern_strength: float
    detected_patterns: list[str]
    confidence_score: float
    threat_assessment: str


@dataclass
class GhostClassification:
    """Ghost classification result for file type"""

    ghost_class: GhostClass
    threat_level: str
    containment_strategy: str
    recommended_approach: str
    risk_factors: list[str] = field(default_factory=list)


@dataclass
class ProtonPackStatus:
    """Proton Pack status for exception handling"""

    stream_mode: ProtonStreamMode
    energy_level: float
    containment_success: bool
    recovery_strategy: str
    damage_assessment: str


class GhostbustersFileTypeProcessor:
    """
    Ghostbusters-enhanced file type processor using paranormal investigation techniques
    """

    def __init__(self):
        self.pke_calibration = {
            "python": 0.95,
            "json": 0.90,
            "yaml": 0.85,
            "toml": 0.88,
            "ini": 0.80,
            "xml": 0.85,
            "markdown": 0.75,
            "shell": 0.80,
            "dockerfile": 0.85,
            "makefile": 0.70,
        }

        self.ghost_classification_rules = self._initialize_ghost_rules()
        self.proton_pack_modes = self._initialize_proton_modes()
        self.investigation_log = []

    def _initialize_ghost_rules(self) -> dict[str, dict[str, Any]]:
        """Initialize ghost classification rules"""
        return {
            "python": {
                "class": GhostClass.CLASS_3,
                "threat": "Moderate - Complex syntax, imports, functions",
                "containment": "AST parsing with error recovery",
                "approach": "Full semantic analysis",
            },
            "json": {
                "class": GhostClass.CLASS_2,
                "threat": "Low - Structured data, simple syntax",
                "containment": "Schema validation with error correction",
                "approach": "Syntax repair and validation",
            },
            "yaml": {
                "class": GhostClass.CLASS_3,
                "threat": "Moderate - Indentation sensitive, complex structure",
                "containment": "Structure analysis with indentation repair",
                "approach": "Pattern-based reconstruction",
            },
            "toml": {
                "class": GhostClass.CLASS_2,
                "threat": "Low - Simple key-value structure",
                "containment": "Syntax validation with section repair",
                "approach": "Direct parsing with error handling",
            },
            "ini": {
                "class": GhostClass.CLASS_1,
                "threat": "Minimal - Basic configuration format",
                "containment": "Simple validation and repair",
                "approach": "Direct parsing",
            },
            "xml": {
                "class": GhostClass.CLASS_3,
                "threat": "Moderate - Complex tag structure, namespaces",
                "containment": "DOM parsing with structure repair",
                "approach": "Tree-based analysis and repair",
            },
            "markdown": {
                "class": GhostClass.CLASS_2,
                "threat": "Low - Text-based with simple markup",
                "containment": "Pattern recognition and validation",
                "approach": "Content analysis and structure validation",
            },
            "shell": {
                "class": GhostClass.CLASS_3,
                "threat": "Moderate - Command syntax, variable expansion",
                "containment": "Syntax validation with command analysis",
                "approach": "Command structure analysis",
            },
            "dockerfile": {
                "class": GhostClass.CLASS_2,
                "threat": "Low - Simple instruction format",
                "containment": "Instruction validation and repair",
                "approach": "Direct parsing with instruction analysis",
            },
            "makefile": {
                "class": GhostClass.CLASS_2,
                "threat": "Low - Target-based structure",
                "containment": "Target analysis and dependency validation",
                "approach": "Structure analysis and target validation",
            },
        }

    def _initialize_proton_modes(self) -> dict[str, ProtonStreamMode]:
        """Initialize proton pack stream modes for different file types"""
        return {
            "python": ProtonStreamMode.CAPTURE,  # Full parsing attempt
            "json": ProtonStreamMode.STUN,  # Graceful degradation
            "yaml": ProtonStreamMode.CAPTURE,  # Structure repair
            "toml": ProtonStreamMode.STUN,  # Syntax repair
            "ini": ProtonStreamMode.STUN,  # Simple repair
            "xml": ProtonStreamMode.CAPTURE,  # Structure repair
            "markdown": ProtonStreamMode.STUN,  # Content validation
            "shell": ProtonStreamMode.CAPTURE,  # Syntax analysis
            "dockerfile": ProtonStreamMode.STUN,  # Instruction validation
            "makefile": ProtonStreamMode.STUN,  # Target validation
        }

    def investigate_file(self, file_path: Path) -> dict[str, Any]:
        """
        Full Ghostbusters investigation of a file
        """
        print(f"🔍 Ghostbusters Investigation: {file_path}")
        print("=" * 60)

        # Phase 1: PKE Meter Scan
        pke_reading = self._scan_with_pke_meter(file_path)
        print(f"📡 PKE Meter Reading: {pke_reading.energy_level.value}")
        print(f"   Pattern Strength: {pke_reading.pattern_strength:.2f}")
        print(f"   Confidence: {pke_reading.confidence_score:.2f}")
        print(f"   Threat: {pke_reading.threat_assessment}")

        # Phase 2: Ghost Classification
        ghost_class = self._classify_ghost(file_path, pke_reading)
        print(f"👻 Ghost Classification: {ghost_class.ghost_class.value}")
        print(f"   Threat Level: {ghost_class.threat_level}")
        print(f"   Containment: {ghost_class.containment_strategy}")
        print(f"   Approach: {ghost_class.recommended_approach}")

        # Phase 3: Proton Pack Engagement
        proton_status = self._engage_proton_pack(file_path, pke_reading, ghost_class)
        print(f"⚡ Proton Pack Status: {proton_status.stream_mode.value}")
        print(f"   Energy Level: {proton_status.energy_level:.2f}")
        print(f"   Containment: {'✅' if proton_status.containment_success else '❌'}")
        print(f"   Recovery: {proton_status.recovery_strategy}")

        # Phase 4: Investigation Report
        investigation_result = {
            "file_path": str(file_path),
            "pke_reading": pke_reading,
            "ghost_classification": ghost_class,
            "proton_pack_status": proton_status,
            "recommendations": self._generate_recommendations(
                pke_reading, ghost_class, proton_status
            ),
        }

        self.investigation_log.append(investigation_result)
        return investigation_result

    def _scan_with_pke_meter(self, file_path: Path) -> PKEMeterReading:
        """Scan file with PKE Meter for pattern detection"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return PKEMeterReading(
                energy_level=PKEEnergyLevel.ZERO,
                pattern_strength=0.0,
                detected_patterns=[],
                confidence_score=0.0,
                threat_assessment="File unreadable",
            )

        # Detect file type patterns
        patterns = self._detect_file_patterns(content)
        pattern_strength = sum(patterns.values())

        # Determine energy level
        if pattern_strength >= 0.8:
            energy_level = PKEEnergyLevel.CRITICAL
        elif pattern_strength >= 0.6:
            energy_level = PKEEnergyLevel.HIGH
        elif pattern_strength >= 0.4:
            energy_level = PKEEnergyLevel.MEDIUM
        elif pattern_strength >= 0.2:
            energy_level = PKEEnergyLevel.LOW
        else:
            energy_level = PKEEnergyLevel.ZERO

        # Calculate confidence score
        confidence_score = min(pattern_strength, 1.0)

        # Assess threat level
        if energy_level == PKEEnergyLevel.CRITICAL:
            threat = "High - Strong file type signals detected"
        elif energy_level == PKEEnergyLevel.HIGH:
            threat = "Moderate - Clear file type patterns"
        elif energy_level == PKEEnergyLevel.MEDIUM:
            threat = "Low - Some patterns detected"
        elif energy_level == PKEEnergyLevel.LOW:
            threat = "Minimal - Weak patterns"
        else:
            threat = "None - No patterns detected"

        return PKEMeterReading(
            energy_level=energy_level,
            pattern_strength=pattern_strength,
            detected_patterns=list(patterns.keys()),
            confidence_score=confidence_score,
            threat_assessment=threat,
        )

    def _detect_file_patterns(self, content: str) -> dict[str, float]:
        """Detect file type patterns in content"""
        patterns = {}

        # Python patterns
        python_score = 0
        if re.search(r"^#!/usr/bin/env python", content, re.MULTILINE):
            python_score += 0.3
        if re.search(r"^import\s+\w+", content, re.MULTILINE):
            python_score += 0.2
        if re.search(r"^def\s+\w+\s*\(", content, re.MULTILINE):
            python_score += 0.2
        if re.search(r"^class\s+\w+", content, re.MULTILINE):
            python_score += 0.2
        if python_score > 0:
            patterns["python"] = python_score

        # JSON patterns
        json_score = 0
        if re.search(r"^\s*\{", content, re.MULTILINE):
            json_score += 0.3
        if re.search(r'"[^"]*"\s*:', content, re.MULTILINE):
            json_score += 0.3
        if re.search(r"^\s*\[", content, re.MULTILINE):
            json_score += 0.2
        if json_score > 0:
            patterns["json"] = json_score

        # YAML patterns
        yaml_score = 0
        if re.search(r"^\s*[\w-]+\s*:", content, re.MULTILINE):
            yaml_score += 0.3
        if re.search(r"^\s*-\s+", content, re.MULTILINE):
            yaml_score += 0.2
        if re.search(r"^\s*#", content, re.MULTILINE):
            yaml_score += 0.1
        if yaml_score > 0:
            patterns["yaml"] = yaml_score

        # TOML patterns
        toml_score = 0
        if re.search(r"^\s*\[[\w.]+\]", content, re.MULTILINE):
            toml_score += 0.4
        if re.search(r"^\s*[\w-]+\s*=", content, re.MULTILINE):
            toml_score += 0.3
        if re.search(r"^\s*#.*$", content, re.MULTILINE):
            toml_score += 0.1
        if toml_score > 0:
            patterns["toml"] = toml_score

        # INI patterns
        ini_score = 0
        if re.search(r"^\s*\[[\w\s]+\]", content, re.MULTILINE):
            ini_score += 0.4
        if re.search(r"^\s*\w+\s*=", content, re.MULTILINE):
            ini_score += 0.3
        if re.search(r"^\s*;.*$", content, re.MULTILINE):
            ini_score += 0.1
        if ini_score > 0:
            patterns["ini"] = ini_score

        return patterns

    def _classify_ghost(
        self, file_path: Path, pke_reading: PKEMeterReading
    ) -> GhostClassification:
        """Classify file using ghost classification system"""
        # Determine file type from patterns
        if pke_reading.detected_patterns:
            detected_type = max(
                pke_reading.detected_patterns,
                key=lambda t: pke_reading.pattern_strength,
            )
        else:
            detected_type = "unknown"

        # Get ghost class rules
        if detected_type in self.ghost_classification_rules:
            rules = self.ghost_classification_rules[detected_type]
            ghost_class = rules["class"]
            threat_level = rules["threat"]
            containment_strategy = rules["containment"]
            recommended_approach = rules["approach"]
        else:
            ghost_class = GhostClass.CLASS_5
            threat_level = "Lethal - Unknown file type"
            containment_strategy = "Isolate and analyze"
            recommended_approach = "Manual investigation required"

        # Assess risk factors
        risk_factors = []
        if pke_reading.energy_level == PKEEnergyLevel.ZERO:
            risk_factors.append("No detectable patterns")
        if pke_reading.confidence_score < 0.5:
            risk_factors.append("Low confidence detection")
        if detected_type == "unknown":
            risk_factors.append("Unknown file type")

        return GhostClassification(
            ghost_class=ghost_class,
            threat_level=threat_level,
            containment_strategy=containment_strategy,
            recommended_approach=recommended_approach,
            risk_factors=risk_factors,
        )

    def _engage_proton_pack(
        self,
        file_path: Path,
        pke_reading: PKEMeterReading,
        ghost_class: GhostClassification,
    ) -> ProtonPackStatus:
        """Engage Proton Pack for file parsing and exception handling"""
        # Determine stream mode
        if pke_reading.detected_patterns:
            detected_type = max(
                pke_reading.detected_patterns,
                key=lambda t: pke_reading.pattern_strength,
            )
            stream_mode = self.proton_pack_modes.get(
                detected_type, ProtonStreamMode.STUN
            )
        else:
            stream_mode = ProtonStreamMode.NEUTRALIZE

        # Attempt parsing based on stream mode
        containment_success = False
        recovery_strategy = "No recovery attempted"
        damage_assessment = "File not processed"

        if stream_mode in [ProtonStreamMode.CAPTURE, ProtonStreamMode.STUN]:
            try:
                containment_success = self._attempt_parsing(file_path, detected_type)
                recovery_strategy = (
                    "Parsing successful" if containment_success else "Parsing failed"
                )
                damage_assessment = (
                    "File processed successfully"
                    if containment_success
                    else "File has parsing errors"
                )
            except Exception as e:
                containment_success = False
                recovery_strategy = f"Exception caught: {type(e).__name__}"
                damage_assessment = f"File processing failed: {e}"

        # Calculate energy level
        energy_level = pke_reading.confidence_score

        return ProtonPackStatus(
            stream_mode=stream_mode,
            energy_level=energy_level,
            containment_success=containment_success,
            recovery_strategy=recovery_strategy,
            damage_assessment=damage_assessment,
        )

    def _attempt_parsing(self, file_path: Path, file_type: str) -> bool:
        """Attempt to parse file with detected type"""
        try:
            if file_type == "python":
                with open(file_path, encoding="utf-8") as f:
                    ast.parse(f.read())
                return True

            if file_type == "json":
                with open(file_path, encoding="utf-8") as f:
                    json.load(f)
                return True

            if file_type == "yaml":
                with open(file_path, encoding="utf-8") as f:
                    yaml.safe_load(f)
                return True

            if file_type == "toml":
                with open(file_path, "rb") as f:
                    tomllib.load(f)
                return True

            if file_type == "ini":
                config = configparser.ConfigParser()
                config.read(file_path)
                return True

            if file_type == "xml":
                ET.parse(file_path)
                return True

            return False

        except Exception:
            return False

    def _generate_recommendations(
        self,
        pke_reading: PKEMeterReading,
        ghost_class: GhostClassification,
        proton_status: ProtonPackStatus,
    ) -> list[str]:
        """Generate recommendations based on investigation results"""
        recommendations = []

        if pke_reading.energy_level == PKEEnergyLevel.ZERO:
            recommendations.append(
                "🔍 Manual file inspection required - no patterns detected"
            )

        if pke_reading.confidence_score < 0.5:
            recommendations.append(
                "⚠️ Low confidence detection - consider manual verification"
            )

        if ghost_class.ghost_class in [GhostClass.CLASS_4, GhostClass.CLASS_5]:
            recommendations.append(
                "🚨 High threat file - isolate and analyze carefully"
            )

        if not proton_status.containment_success:
            recommendations.append(
                "💥 Parsing failed - implement error recovery strategies"
            )

        if pke_reading.detected_patterns:
            recommendations.append(
                f"✅ File type detected: {', '.join(pke_reading.detected_patterns)}"
            )

        return recommendations

    def get_investigation_summary(self) -> dict[str, Any]:
        """Get summary of all investigations"""
        if not self.investigation_log:
            return {"total_investigations": 0, "success_rate": 0.0}

        total = len(self.investigation_log)
        successful = sum(
            1
            for result in self.investigation_log
            if result["proton_pack_status"].containment_success
        )
        success_rate = successful / total

        # Ghost class distribution
        ghost_distribution = {}
        for result in self.investigation_log:
            ghost_class = result["ghost_classification"].ghost_class.value
            ghost_distribution[ghost_class] = ghost_distribution.get(ghost_class, 0) + 1

        # PKE energy level distribution
        pke_distribution = {}
        for result in self.investigation_log:
            energy_level = result["pke_reading"].energy_level.value
            pke_distribution[energy_level] = pke_distribution.get(energy_level, 0) + 1

        return {
            "total_investigations": total,
            "success_rate": success_rate,
            "ghost_class_distribution": ghost_distribution,
            "pke_energy_distribution": pke_distribution,
            "average_confidence": sum(
                r["pke_reading"].confidence_score for r in self.investigation_log
            )
            / total,
        }


def main():
    """Demo the Ghostbusters file type processor"""
    processor = GhostbustersFileTypeProcessor()

    # Test with various file types
    test_files = [
        "scripts/one_liner_linter.py",
        "project_model_registry.json",
        "pyproject.toml",
        "README.md",
        "scripts/heuristic_file_type_processor.py",
    ]

    print("👻 Ghostbusters File Type Investigation Squad")
    print("=" * 60)
    print("🔬 Investigating unknown file types with paranormal technology")
    print()

    for test_file in test_files:
        if os.path.exists(test_file):
            result = processor.investigate_file(Path(test_file))
            print()
            print("📋 Investigation Report:")
            for rec in result["recommendations"]:
                print(f"   {rec}")
            print("-" * 60)

    # Show investigation summary
    summary = processor.get_investigation_summary()
    print(f"\n📊 Investigation Summary")
    print(f"   Total Investigations: {summary['total_investigations']}")
    print(f"   Success Rate: {summary['success_rate']:.2%}")
    print(f"   Average Confidence: {summary['average_confidence']:.2f}")

    print(f"\n👻 Ghost Class Distribution:")
    for ghost_class, count in summary["ghost_class_distribution"].items():
        print(f"   {ghost_class}: {count}")

    print(f"\n📡 PKE Energy Distribution:")
    for energy_level, count in summary["pke_energy_distribution"].items():
        print(f"   {energy_level}: {count}")


if __name__ == "__main__":
    main()
