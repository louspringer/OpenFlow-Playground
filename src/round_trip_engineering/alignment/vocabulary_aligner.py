#!/usr/bin/env python3
"""
Vocabulary Aligner
Handles vocabulary alignment between different domains and ontologies
"""

import logging
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule


logger = logging.getLogger(__name__)


class VocabularyAligner(BaseReflectiveModule):
    """Handles vocabulary alignment between different domains and ontologies"""

    def __init__(self) -> None:
        super().__init__()
        self.vocabulary_mappings: Dict[str, Dict[str, str]] = {}
        self.domain_vocabularies: Dict[str, List[str]] = {}

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "vocabulary_alignment": [
                "align_vocabulary_ontologically",
                "align_vocabulary_manually",
                "create_vocabulary_mapping",
            ],
            "domain_management": [
                "add_domain_vocabulary",
                "get_domain_vocabulary",
                "validate_vocabulary",
            ],
        }

    def add_domain_vocabulary(self, domain: str, vocabulary: List[str]) -> bool:
        """Add vocabulary for a specific domain"""
        if not domain or not vocabulary:
            logger.error("Domain and vocabulary must be provided")
            return False

        self.domain_vocabularies[domain] = vocabulary
        logger.info(f"✅ Added vocabulary for domain {domain}: {len(vocabulary)} terms")
        return True

    def get_domain_vocabulary(self, domain: str) -> Optional[List[str]]:
        """Get vocabulary for a specific domain"""
        return self.domain_vocabularies.get(domain)

    def create_vocabulary_mapping(self, source_domain: str, target_domain: str, mappings: Dict[str, str]) -> bool:
        """Create a vocabulary mapping between two domains"""
        if not source_domain or not target_domain:
            logger.error("Source and target domains must be provided")
            return False

        mapping_key = f"{source_domain}_to_{target_domain}"
        self.vocabulary_mappings[mapping_key] = mappings
        logger.info(f"✅ Created vocabulary mapping {mapping_key}: {len(mappings)} terms")
        return True

    def align_vocabulary_ontologically(self, source_text: str, target_domain: str) -> str:
        """Align vocabulary using ontological principles"""
        logger.info(f"🎯 Aligning vocabulary to domain {target_domain} using ontological principles")

        # Get target domain vocabulary
        target_vocab = self.domain_vocabularies.get(target_domain, [])
        if not target_vocab:
            logger.warning(f"No vocabulary found for domain {target_domain}")
            return source_text

        # Simple ontological alignment (can be enhanced with more sophisticated NLP)
        aligned_text = source_text

        # Look for domain-specific terms and suggest alternatives
        for term in target_vocab:
            if term.lower() in source_text.lower():
                logger.info(f"Found domain term: {term}")
                # In a real implementation, this would use ontology relationships
                # For now, we'll just log the alignment
                aligned_text = aligned_text.replace(term, f"[{term}]")

        logger.info(f"✅ Vocabulary aligned to domain {target_domain}")
        return aligned_text

    def align_vocabulary_manually(self, source_text: str, target_domain: str, manual_mappings: Dict[str, str]) -> str:
        """Align vocabulary using manual mappings"""
        logger.info(f"🎯 Aligning vocabulary to domain {target_domain} using manual mappings")

        aligned_text = source_text

        # Apply manual mappings
        for source_term, target_term in manual_mappings.items():
            if source_term in aligned_text:
                aligned_text = aligned_text.replace(source_term, target_term)
                logger.info(f"Applied manual mapping: {source_term} -> {target_term}")

        logger.info(f"✅ Vocabulary aligned to domain {target_domain} using manual mappings")
        return aligned_text

    def validate_vocabulary(self, domain: str, vocabulary: List[str]) -> Dict[str, Any]:
        """Validate vocabulary for a domain"""
        logger.info(f"🎯 Validating vocabulary for domain {domain}")

        validation_result = {
            "domain": domain,
            "total_terms": len(vocabulary),
            "valid_terms": [],
            "invalid_terms": [],
            "warnings": [],
        }

        for term in vocabulary:
            if term and isinstance(term, str) and len(term.strip()) > 0:
                validation_result["valid_terms"].append(term)
            else:
                validation_result["invalid_terms"].append(term)

        # Check for duplicates
        unique_terms = set(validation_result["valid_terms"])
        if len(unique_terms) != len(validation_result["valid_terms"]):
            validation_result["warnings"].append("Duplicate terms found")

        # Check for very long terms
        long_terms = [term for term in validation_result["valid_terms"] if len(term) > 50]
        if long_terms:
            validation_result["warnings"].append(f"Found {len(long_terms)} very long terms")

        validation_result["unique_terms"] = len(unique_terms)
        validation_result["is_valid"] = len(validation_result["invalid_terms"]) == 0

        logger.info(f"✅ Vocabulary validation completed for domain {domain}")
        return validation_result

    def get_vocabulary_statistics(self) -> Dict[str, Any]:
        """Get statistics about all vocabularies"""
        stats = {
            "total_domains": len(self.domain_vocabularies),
            "total_mappings": len(self.vocabulary_mappings),
            "domains": {},
            "mappings": {},
        }

        for domain, vocabulary in self.domain_vocabularies.items():
            stats["domains"][domain] = {
                "term_count": len(vocabulary),
                "sample_terms": vocabulary[:5] if vocabulary else [],
            }

        for mapping_key, mappings in self.vocabulary_mappings.items():
            stats["mappings"][mapping_key] = {
                "mapping_count": len(mappings),
                "sample_mappings": list(mappings.items())[:3] if mappings else [],
            }

        return stats

    def export_vocabulary(self, domain: str, format: str = "json") -> Optional[str]:
        """Export vocabulary for a domain in specified format"""
        vocabulary = self.domain_vocabularies.get(domain)
        if not vocabulary:
            logger.error(f"No vocabulary found for domain {domain}")
            return None

        if format.lower() == "json":
            import json

            return json.dumps({"domain": domain, "vocabulary": vocabulary}, indent=2)
        elif format.lower() == "txt":
            return "\n".join(vocabulary)
        else:
            logger.error(f"Unsupported export format: {format}")
            return None

    def import_vocabulary(self, domain: str, vocabulary_data: Any, format: str = "json") -> bool:
        """Import vocabulary for a domain from specified format"""
        try:
            if format.lower() == "json":
                if isinstance(vocabulary_data, str):
                    import json

                    data = json.loads(vocabulary_data)
                    vocabulary = data.get("vocabulary", [])
                else:
                    vocabulary = vocabulary_data.get("vocabulary", [])
            elif format.lower() == "txt":
                if isinstance(vocabulary_data, str):
                    vocabulary = [line.strip() for line in vocabulary_data.split("\n") if line.strip()]
                else:
                    vocabulary = vocabulary_data
            else:
                logger.error(f"Unsupported import format: {format}")
                return False

            return self.add_domain_vocabulary(domain, vocabulary)

        except Exception as e:
            logger.error(f"Failed to import vocabulary for domain {domain}: {e}")
            return False
