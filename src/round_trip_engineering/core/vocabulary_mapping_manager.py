#!/usr/bin/env python3
"""
Vocabulary Mapping Manager
Focused on managing vocabulary mappings and domain vocabularies.
"""

import logging
from typing import Dict, Any, Optional, Union, List, Set
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VocabularyMapping:
    """Represents a vocabulary mapping between domains."""

    source_term: str
    target_term: str
    transformation_rule: str
    confidence: float
    description: str


@dataclass
class DomainVocabulary:
    """Represents the vocabulary of a specific domain."""

    domain_name: str
    terms: Set[str]
    data_structures: Dict[str, Any]
    constraints: Dict[str, Any]


class VocabularyMappingManager:
    """Manages vocabulary mappings and domain vocabularies."""

    def __init__(self):
        """Initialize the vocabulary mapping manager."""
        self.reverse_engineering_vocabulary = (
            self._build_reverse_engineering_vocabulary()
        )
        self.code_generation_vocabulary = self._build_code_generation_vocabulary()
        self.vocabulary_mappings = self._build_vocabulary_mappings()

        logger.info("✅ Vocabulary mapping manager initialized")

    def _build_reverse_engineering_vocabulary(self) -> DomainVocabulary:
        """Build vocabulary for reverse engineering domain."""
        return DomainVocabulary(
            domain_name="reverse_engineering",
            terms={
                "components",
                "classes",
                "functions",
                "methods",
                "imports",
                "dependencies",
                "relationships",
                "complexity",
                "workflow",
                "nodes",
                "edges",
                "patterns",
                "structures",
            },
            data_structures={
                "components": "list",  # Reverse engineering produces lists
                "relationships": "list",
                "workflow": "dict",
            },
            constraints={
                "components": "must_have_name_and_type",
                "relationships": "must_have_source_and_target",
                "workflow": "must_have_nodes_and_edges",
            },
        )

    def _build_code_generation_vocabulary(self) -> DomainVocabulary:
        """Build vocabulary for code generation domain."""
        return DomainVocabulary(
            domain_name="code_generation",
            terms={
                "classes",
                "methods",
                "imports",
                "dependencies",
                "inheritance",
                "interfaces",
                "types",
                "annotations",
                "modules",
                "packages",
                "generators",
                "templates",
            },
            data_structures={
                "components": "dict",  # Code generation expects dicts
                "classes": "dict",
                "methods": "dict",
            },
            constraints={
                "components": "must_be_dict_with_name_keys",
                "classes": "must_have_methods_dict",
                "methods": "must_have_signature_and_body",
            },
        )

    def _build_vocabulary_mappings(self) -> Dict[str, VocabularyMapping]:
        """Build mappings between domain vocabularies."""
        return {
            "components_list_to_dict": VocabularyMapping(
                source_term="components (list)",
                target_term="components (dict)",
                transformation_rule="convert_list_to_dict_by_name",
                confidence=0.95,
                description="Convert component list to name-keyed dictionary",
            ),
            "relationships_list_to_dict": VocabularyMapping(
                source_term="relationships (list)",
                target_term="relationships (dict)",
                transformation_rule="convert_list_to_dict_by_id",
                confidence=0.90,
                description="Convert relationship list to ID-keyed dictionary",
            ),
            "workflow_enhancement": VocabularyMapping(
                source_term="workflow (basic)",
                target_term="workflow (enhanced)",
                transformation_rule="add_complexity_and_metrics",
                confidence=0.85,
                description="Enhance workflow with complexity metrics",
            ),
        }

    def get_vocabulary_mapping(self, mapping_key: str) -> Optional[VocabularyMapping]:
        """Get a specific vocabulary mapping by key."""
        return self.vocabulary_mappings.get(mapping_key)

    def get_all_mappings(self) -> Dict[str, VocabularyMapping]:
        """Get all vocabulary mappings."""
        return self.vocabulary_mappings.copy()

    def get_domain_vocabulary(self, domain_name: str) -> Optional[DomainVocabulary]:
        """Get vocabulary for a specific domain."""
        if domain_name == "reverse_engineering":
            return self.reverse_engineering_vocabulary
        elif domain_name == "code_generation":
            return self.code_generation_vocabulary
        return None

    def get_mapping_status(self) -> Dict[str, Any]:
        """Get the current status of vocabulary mappings."""
        try:
            return {
                "total_mappings": len(self.vocabulary_mappings),
                "domains_supported": ["reverse_engineering", "code_generation"],
                "mapping_confidence": {
                    key: mapping.confidence
                    for key, mapping in self.vocabulary_mappings.items()
                },
                "status": "healthy",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get mapping status: {e}")
            return {"error": str(e)}
