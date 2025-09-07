"""
Ubiquitous Language Analyzer

Analyzes code for ubiquitous language consistency and domain terminology.
"""

import ast
import re
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter


@dataclass
class TermAnalysis:
    """Analysis of a domain term"""

    term: str
    occurrences: int = 0
    contexts: List[str] = field(default_factory=list)
    variations: List[str] = field(default_factory=list)
    consistency_score: float = 0.0
    is_domain_term: bool = False

    def add_occurrence(self, context: str):
        """Add occurrence of term in context"""
        self.occurrences += 1
        if context not in self.contexts:
            self.contexts.append(context)

    def add_variation(self, variation: str):
        """Add variation of term"""
        if variation not in self.variations:
            self.variations.append(variation)


@dataclass
class LanguageAnalysis:
    """Analysis of ubiquitous language in codebase"""

    domain_terms: Dict[str, TermAnalysis] = field(default_factory=dict)
    inconsistent_terms: List[str] = field(default_factory=list)
    missing_terms: List[str] = field(default_factory=list)
    overused_terms: List[str] = field(default_factory=list)
    consistency_score: float = 0.0
    coverage_score: float = 0.0

    def add_term(self, term: str, context: str):
        """Add term occurrence"""
        if term not in self.domain_terms:
            self.domain_terms[term] = TermAnalysis(term=term)

        self.domain_terms[term].add_occurrence(context)

    def get_consistency_score(self) -> float:
        """Calculate overall consistency score"""
        if not self.domain_terms:
            return 0.0

        total_score = 0.0
        for term_analysis in self.domain_terms.values():
            total_score += term_analysis.consistency_score

        return total_score / len(self.domain_terms)


class UbiquitousLanguageAnalyzer:
    """Analyzes code for ubiquitous language patterns"""

    def __init__(self):
        self.domain_patterns = {
            "business_terms": [
                "customer",
                "user",
                "order",
                "product",
                "payment",
                "invoice",
                "account",
                "profile",
                "subscription",
                "membership",
                "tier",
                "transaction",
                "balance",
                "credit",
                "debit",
                "refund",
                "shipping",
                "delivery",
                "inventory",
                "stock",
                "warehouse",
                "catalog",
                "category",
                "brand",
                "vendor",
                "supplier",
            ],
            "technical_terms": [
                "entity",
                "aggregate",
                "repository",
                "service",
                "factory",
                "handler",
                "processor",
                "validator",
                "converter",
                "mapper",
                "adapter",
                "facade",
                "proxy",
                "decorator",
                "observer",
            ],
            "process_terms": [
                "workflow",
                "process",
                "step",
                "stage",
                "phase",
                "milestone",
                "approval",
                "review",
                "validation",
                "verification",
                "confirmation",
                "notification",
                "alert",
                "reminder",
                "escalation",
                "timeout",
            ],
        }

        self.inconsistency_patterns = [
            r"user|customer|client",  # User terminology
            r"order|purchase|transaction",  # Order terminology
            r"product|item|goods",  # Product terminology
            r"payment|charge|billing",  # Payment terminology
            r"service|handler|processor",  # Service terminology
        ]

        self.stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "up",
            "about",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "between",
            "among",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            "me",
            "him",
            "her",
            "us",
            "them",
            "my",
            "your",
            "his",
            "her",
            "its",
            "our",
            "their",
        }

    def analyze_file(self, tree: ast.AST, file_path: str) -> LanguageAnalysis:
        """Analyze file for ubiquitous language patterns"""
        analysis = LanguageAnalysis()

        # Extract all text content from the file
        text_content = self._extract_text_content(tree)

        # Analyze domain terms
        self._analyze_domain_terms(text_content, file_path, analysis)

        # Check for inconsistencies
        self._check_inconsistencies(text_content, analysis)

        # Calculate scores
        analysis.consistency_score = analysis.get_consistency_score()
        analysis.coverage_score = self._calculate_coverage_score(analysis)

        return analysis

    def _extract_text_content(self, tree: ast.AST) -> str:
        """Extract all text content from AST"""
        content_parts = []

        for node in ast.walk(tree):
            # Extract from docstrings
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                if isinstance(node.value.value, str):
                    content_parts.append(node.value.value)

            # Extract from string literals
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                content_parts.append(node.value)

            # Extract from comments (if available)
            elif hasattr(node, "comment") and node.comment:
                content_parts.append(node.comment)

            # Extract from names and identifiers
            elif isinstance(node, ast.Name):
                content_parts.append(node.id)

            # Extract from class and function names
            elif isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                content_parts.append(node.name)

        return " ".join(content_parts)

    def _analyze_domain_terms(self, text: str, context: str, analysis: LanguageAnalysis):
        """Analyze text for domain terms"""
        # Normalize text
        normalized_text = self._normalize_text(text)

        # Find domain terms
        for category, terms in self.domain_patterns.items():
            for term in terms:
                if self._find_term_variations(term, normalized_text):
                    analysis.add_term(term, context)
                    term_analysis = analysis.domain_terms[term]
                    term_analysis.is_domain_term = True

                    # Find variations
                    variations = self._find_term_variations(term, normalized_text, return_variations=True)
                    for variation in variations:
                        term_analysis.add_variation(variation)

        # Calculate consistency scores for each term
        for term_analysis in analysis.domain_terms.values():
            term_analysis.consistency_score = self._calculate_term_consistency(term_analysis)

    def _normalize_text(self, text: str) -> str:
        """Normalize text for analysis"""
        # Convert to lowercase
        text = text.lower()

        # Remove special characters but keep spaces
        text = re.sub(r"[^\w\s]", " ", text)

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _find_term_variations(self, term: str, text: str, return_variations: bool = False) -> bool | List[str]:
        """Find variations of a term in text"""
        variations = []

        # Exact match
        if term in text:
            if return_variations:
                variations.append(term)
            else:
                return True

        # Plural forms
        plural_form = term + "s"
        if plural_form in text:
            if return_variations:
                variations.append(plural_form)
            else:
                return True

        # Singular forms (if term is plural)
        if term.endswith("s") and len(term) > 3:
            singular_form = term[:-1]
            if singular_form in text:
                if return_variations:
                    variations.append(singular_form)
                else:
                    return True

        # CamelCase variations
        camel_case = self._to_camel_case(term)
        if camel_case in text:
            if return_variations:
                variations.append(camel_case)
            else:
                return True

        # Snake_case variations
        snake_case = self._to_snake_case(term)
        if snake_case in text:
            if return_variations:
                variations.append(snake_case)
            else:
                return True

        # PascalCase variations
        pascal_case = self._to_pascal_case(term)
        if pascal_case in text:
            if return_variations:
                variations.append(pascal_case)
            else:
                return True

        return variations if return_variations else len(variations) > 0

    def _to_camel_case(self, text: str) -> str:
        """Convert text to camelCase"""
        words = text.split("_")
        return words[0] + "".join(word.capitalize() for word in words[1:])

    def _to_snake_case(self, text: str) -> str:
        """Convert text to snake_case"""
        # Insert underscore before uppercase letters
        text = re.sub(r"([a-z])([A-Z])", r"\1_\2", text)
        return text.lower()

    def _to_pascal_case(self, text: str) -> str:
        """Convert text to PascalCase"""
        words = text.split("_")
        return "".join(word.capitalize() for word in words)

    def _calculate_term_consistency(self, term_analysis: TermAnalysis) -> float:
        """Calculate consistency score for a term"""
        if term_analysis.occurrences < 2:
            return 1.0  # Single occurrence is consistent

        # Check for variations
        if len(term_analysis.variations) > 1:
            # Penalize for having multiple variations
            variation_penalty = (len(term_analysis.variations) - 1) * 0.2
            return max(0.0, 1.0 - variation_penalty)

        # Check for context consistency
        if len(term_analysis.contexts) > 1:
            # Bonus for being used in multiple contexts consistently
            return 1.0

        return 0.8  # Single context usage

    def _check_inconsistencies(self, text: str, analysis: LanguageAnalysis):
        """Check for terminology inconsistencies"""
        for pattern in self.inconsistency_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if len(set(matches)) > 1:
                # Multiple variations of the same concept found
                analysis.inconsistent_terms.extend(matches)

    def _calculate_coverage_score(self, analysis: LanguageAnalysis) -> float:
        """Calculate coverage score for domain terms"""
        total_expected_terms = sum(len(terms) for terms in self.domain_patterns.values())
        found_terms = len(analysis.domain_terms)

        return found_terms / total_expected_terms if total_expected_terms > 0 else 0.0

    def analyze_multiple_files(self, file_analyses: List[LanguageAnalysis]) -> LanguageAnalysis:
        """Combine analyses from multiple files"""
        combined_analysis = LanguageAnalysis()

        # Merge domain terms
        for file_analysis in file_analyses:
            for term, term_analysis in file_analysis.domain_terms.items():
                if term not in combined_analysis.domain_terms:
                    combined_analysis.domain_terms[term] = TermAnalysis(term=term)

                combined_term = combined_analysis.domain_terms[term]
                combined_term.occurrences += term_analysis.occurrences
                combined_term.contexts.extend(term_analysis.contexts)
                combined_term.variations.extend(term_analysis.variations)
                combined_term.is_domain_term = term_analysis.is_domain_term

        # Merge inconsistencies
        for file_analysis in file_analyses:
            combined_analysis.inconsistent_terms.extend(file_analysis.inconsistent_terms)

        # Calculate final scores
        combined_analysis.consistency_score = combined_analysis.get_consistency_score()
        combined_analysis.coverage_score = self._calculate_coverage_score(combined_analysis)

        return combined_analysis

    def generate_language_report(self, analysis: LanguageAnalysis) -> Dict[str, Any]:
        """Generate comprehensive language report"""
        return {
            "summary": {
                "total_terms": len(analysis.domain_terms),
                "consistency_score": analysis.consistency_score,
                "coverage_score": analysis.coverage_score,
                "inconsistent_terms_count": len(analysis.inconsistent_terms),
            },
            "domain_terms": {
                term: {
                    "occurrences": term_analysis.occurrences,
                    "contexts": term_analysis.contexts,
                    "variations": term_analysis.variations,
                    "consistency_score": term_analysis.consistency_score,
                    "is_domain_term": term_analysis.is_domain_term,
                }
                for term, term_analysis in analysis.domain_terms.items()
            },
            "inconsistencies": analysis.inconsistent_terms,
            "recommendations": self._generate_recommendations(analysis),
        }

    def _generate_recommendations(self, analysis: LanguageAnalysis) -> List[str]:
        """Generate recommendations for improving ubiquitous language"""
        recommendations = []

        # Consistency recommendations
        if analysis.consistency_score < 0.8:
            recommendations.append("Improve terminology consistency across the codebase")

        # Coverage recommendations
        if analysis.coverage_score < 0.5:
            recommendations.append("Increase domain terminology coverage")

        # Inconsistency recommendations
        if analysis.inconsistent_terms:
            recommendations.append("Resolve terminology inconsistencies")

        # Specific term recommendations
        for term, term_analysis in analysis.domain_terms.items():
            if term_analysis.consistency_score < 0.7:
                recommendations.append(f"Standardize usage of '{term}' term")

        return recommendations
