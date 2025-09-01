#!/usr/bin/env python3
"""
Ontology Model Manager Reflective Module
Ontology/RDF implementation of model CRUD operations.
"""

import logging
import time
from typing import Any, Dict, List, Optional
from pathlib import Path

from ..generators.base_reflective_module import BaseReflectiveModule
from .interface import IModelCrud


class OntologyModelManager(BaseReflectiveModule, IModelCrud):
    """Ontology/RDF implementation of model CRUD operations."""

    def __init__(
        self,
        ontology_file: str = "model.ttl",
        format: str = "turtle",
        namespace: str = "http://example.org/model#",
    ) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.ontology_file = Path(ontology_file)
        self.format = format
        self.namespace = namespace

        # Lazy import to avoid dependency issues
        self._graph = None

        self.logger.info(f"✅ OntologyModelManager initialized for {self.ontology_file}")

    def _get_graph(self):
        """Get RDF graph with lazy initialization."""
        if self._graph is None:
            try:
                import rdflib
                from rdflib import Graph, Namespace, Literal, URIRef

                self._graph = Graph()
                self._ns = Namespace(self.namespace)
                self._graph.bind("model", self._ns)

                # Load existing ontology if it exists
                if self.ontology_file.exists():
                    self._graph.parse(self.ontology_file, format=self.format)

            except ImportError:
                raise ImportError("rdflib package not installed. Run: pip install rdflib")
        return self._graph

    async def get_module_capabilities(self) -> List[Any]:
        """Return module capabilities."""
        try:
            from src.reflective_modules.health import ModuleCapability
        except ImportError:
            return [
                {
                    "name": "ontology_crud",
                    "description": "Ontology/RDF-based CRUD operations",
                    "available": True,
                    "methods": ["add_item", "update_section", "remove_item"],
                }
            ]

        return [
            ModuleCapability(
                name="ontology_crud",
                description="Ontology/RDF-based CRUD operations",
                available=True,
                version="1.0.0",
                dependencies=["rdflib"],
            )
        ]

    def add_item(
        self,
        item_id: str,
        description: str,
        title: Optional[str] = None,
        priority: str = "medium",
        collection: str = "items",
        **kwargs,
    ) -> bool:
        """Add a new item to a collection in ontology."""
        try:
            graph = self._get_graph()

            # Create item URI
            item_uri = self._ns[item_id]

            # Add basic properties
            graph.add((item_uri, self._ns.description, Literal(description)))
            if title:
                graph.add((item_uri, self._ns.title, Literal(title)))
            graph.add((item_uri, self._ns.priority, Literal(priority)))
            graph.add((item_uri, self._ns.status, Literal("pending")))
            graph.add((item_uri, self._ns.createdAt, Literal(int(time.time()))))
            graph.add((item_uri, self._ns.collection, Literal(collection)))

            # Add additional properties
            for key, value in kwargs.items():
                graph.add((item_uri, self._ns[key], Literal(str(value))))

            # Save to file
            graph.serialize(self.ontology_file, format=self.format)

            self._track_success()
            self.logger.info(f"✅ Item added to ontology collection {collection}: {item_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add item to ontology: {e}")
            raise

    def update_section(self, section_name: str, updates: Dict[str, Any]) -> bool:
        """Update a section configuration in ontology."""
        try:
            graph = self._get_graph()

            # Create section URI
            section_uri = self._ns[section_name]

            # Remove existing properties
            for s, p, o in graph.triples((section_uri, None, None)):
                graph.remove((s, p, o))

            # Add new properties
            for key, value in updates.items():
                graph.add((section_uri, self._ns[key], Literal(str(value))))

            # Save to file
            graph.serialize(self.ontology_file, format=self.format)

            self._track_success()
            self.logger.info(f"✅ Section updated in ontology: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to update section in ontology: {e}")
            raise

    def remove_item(self, item_id: str, collection: str = "items") -> bool:
        """Remove an item from a collection in ontology."""
        try:
            graph = self._get_graph()

            # Find and remove item
            item_uri = self._ns[item_id]

            # Remove all triples involving this item
            for s, p, o in list(graph.triples((item_uri, None, None))):
                graph.remove((s, p, o))

            # Save to file
            graph.serialize(self.ontology_file, format=self.format)

            self._track_success()
            self.logger.info(f"✅ Item removed from ontology collection {collection}: {item_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove item from ontology: {e}")
            raise

    def add_section(self, section_name: str, section_config: Dict[str, Any]) -> bool:
        """Add a new section in ontology."""
        try:
            graph = self._get_graph()

            # Create section URI
            section_uri = self._ns[section_name]

            # Add section type
            graph.add((section_uri, self._ns.type, self._ns.Section))
            graph.add((section_uri, self._ns.createdAt, Literal(int(time.time()))))

            # Add configuration properties
            for key, value in section_config.items():
                graph.add((section_uri, self._ns[key], Literal(str(value))))

            # Save to file
            graph.serialize(self.ontology_file, format=self.format)

            self._track_success()
            self.logger.info(f"✅ Section added to ontology: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add section to ontology: {e}")
            raise

    def remove_section(self, section_name: str) -> bool:
        """Remove a section from ontology."""
        try:
            graph = self._get_graph()

            # Find and remove section
            section_uri = self._ns[section_name]

            # Remove all triples involving this section
            for s, p, o in list(graph.triples((section_uri, None, None))):
                graph.remove((s, p, o))

            # Save to file
            graph.serialize(self.ontology_file, format=self.format)

            self._track_success()
            self.logger.info(f"✅ Section removed from ontology: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove section from ontology: {e}")
            raise

    def create_backup(self) -> str:
        """Create a backup of the ontology."""
        try:
            backup_file = f"ontology_backup_{int(time.time())}.{self.format}"

            graph = self._get_graph()
            graph.serialize(backup_file, format=self.format)

            self._track_success()
            self.logger.info(f"✅ Ontology backup created: {backup_file}")
            return backup_file

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Ontology backup failed: {e}")
            raise

    def list_backups(self) -> List[str]:
        """List available ontology backups."""
        try:
            import glob

            backup_files = glob.glob(f"ontology_backup_*.{self.format}")
            return sorted(backup_files)

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to list ontology backups: {e}")
            raise

    def restore_backup(self, backup_file: str) -> bool:
        """Restore from an ontology backup."""
        try:
            graph = self._get_graph()

            # Clear existing graph
            graph.remove((None, None, None))

            # Load from backup
            graph.parse(backup_file, format=self.format)

            # Save to current file
            graph.serialize(self.ontology_file, format=self.format)

            self._track_success()
            self.logger.info(f"✅ Ontology backup restored: {backup_file}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Ontology backup restore failed: {e}")
            raise

    def validate(self) -> bool:
        """Validate the ontology structure."""
        try:
            graph = self._get_graph()

            # Basic validation - check if graph is accessible
            if len(graph) == 0:
                self.logger.warning("⚠️ Ontology is empty")

            self._track_success()
            self.logger.info("✅ Ontology validation passed")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Ontology validation failed: {e}")
            raise

    def load_model(self) -> Dict[str, Any]:
        """Load the current model from ontology."""
        try:
            graph = self._get_graph()

            # Convert RDF to dictionary structure
            model_data = {}

            # Group by collection
            collections = {}
            for s, p, o in graph.triples((None, self._ns.collection, None)):
                collection_name = str(o)
                if collection_name not in collections:
                    collections[collection_name] = []
                collections[collection_name].append(str(s).split("#")[-1])

            # Build items for each collection
            for collection_name, item_uris in collections.items():
                model_data[collection_name] = []
                for item_uri in item_uris:
                    item_data = {}
                    for s, p, o in graph.triples((self._ns[item_uri], None, None)):
                        if str(p).startswith(self.namespace):
                            key = str(p).split("#")[-1]
                            item_data[key] = str(o)
                    if item_data:
                        model_data[collection_name].append(item_data)

            # Add sections
            for s, p, o in graph.triples((None, self._ns.type, self._ns.Section)):
                section_name = str(s).split("#")[-1]
                section_data = {}
                for s2, p2, o2 in graph.triples((s, None, None)):
                    if str(p2).startswith(self.namespace):
                        key = str(p2).split("#")[-1]
                        section_data[key] = str(o2)
                if section_data:
                    model_data[section_name] = section_data

            self._track_success()
            self.logger.info("✅ Model loaded from ontology")
            return model_data

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to load model from ontology: {e}")
            raise
