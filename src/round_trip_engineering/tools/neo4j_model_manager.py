#!/usr/bin/env python3
"""
Neo4j Model Manager Reflective Module
Neo4j implementation of model CRUD operations.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule
from .interface import IModelCrud


class Neo4jModelManager(BaseReflectiveModule, IModelCrud):
    """Neo4j implementation of model CRUD operations."""

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        username: str = "neo4j",
        password: str = "password",
        database: str = "neo4j",
    ) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database

        # Lazy import to avoid dependency issues
        self._driver = None

        self.logger.info(f"✅ Neo4jModelManager initialized for {self.uri}")

    def _get_driver(self):
        """Get Neo4j driver with lazy initialization."""
        if self._driver is None:
            try:
                from neo4j import GraphDatabase

                self._driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            except ImportError:
                raise ImportError("neo4j package not installed. Run: pip install neo4j")
        return self._driver

    async def get_module_capabilities(self) -> List[Any]:
        """Return module capabilities."""
        try:
            from src.reflective_modules.health import ModuleCapability
        except ImportError:
            return [
                {
                    "name": "neo4j_crud",
                    "description": "Neo4j-based CRUD operations",
                    "available": True,
                    "methods": ["add_item", "update_section", "remove_item"],
                }
            ]

        return [
            ModuleCapability(
                name="neo4j_crud",
                description="Neo4j-based CRUD operations",
                available=True,
                version="1.0.0",
                dependencies=["neo4j"],
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
        """Add a new item to a collection in Neo4j."""
        try:
            driver = self._get_driver()

            with driver.session(database=self.database) as session:
                # Create item node
                query = """
                CREATE (i:Item {
                    id: $item_id,
                    description: $description,
                    title: $title,
                    priority: $priority,
                    status: 'pending',
                    created_at: $created_at,
                    collection: $collection
                })
                """

                session.run(
                    query,
                    {
                        "item_id": item_id,
                        "description": description,
                        "title": title,
                        "priority": priority,
                        "created_at": int(time.time()),
                        "collection": collection,
                    },
                )

                # Add additional properties
                if kwargs:
                    for key, value in kwargs.items():
                        query = f"""
                        MATCH (i:Item {{id: $item_id}})
                        SET i.{key} = $value
                        """
                        session.run(query, {"item_id": item_id, "value": value})

            self._track_success()
            self.logger.info(f"✅ Item added to Neo4j collection {collection}: {item_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add item to Neo4j: {e}")
            raise

    def update_section(self, section_name: str, updates: Dict[str, Any]) -> bool:
        """Update a section configuration in Neo4j."""
        try:
            driver = self._get_driver()

            with driver.session(database=self.database) as session:
                # Create or update section node
                query = """
                MERGE (s:Section {name: $section_name})
                SET s += $updates
                """

                session.run(query, {"section_name": section_name, "updates": updates})

            self._track_success()
            self.logger.info(f"✅ Section updated in Neo4j: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to update section in Neo4j: {e}")
            raise

    def remove_item(self, item_id: str, collection: str = "items") -> bool:
        """Remove an item from a collection in Neo4j."""
        try:
            driver = self._get_driver()

            with driver.session(database=self.database) as session:
                query = """
                MATCH (i:Item {id: $item_id, collection: $collection})
                DETACH DELETE i
                """

                result = session.run(query, {"item_id": item_id, "collection": collection})

            self._track_success()
            self.logger.info(f"✅ Item removed from Neo4j collection {collection}: {item_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove item from Neo4j: {e}")
            raise

    def add_section(self, section_name: str, section_config: Dict[str, Any]) -> bool:
        """Add a new section in Neo4j."""
        try:
            driver = self._get_driver()

            with driver.session(database=self.database) as session:
                query = """
                CREATE (s:Section {
                    name: $section_name,
                    config: $section_config,
                    created_at: $created_at
                })
                """

                session.run(
                    query,
                    {
                        "section_name": section_name,
                        "section_config": section_config,
                        "created_at": int(time.time()),
                    },
                )

            self._track_success()
            self.logger.info(f"✅ Section added to Neo4j: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add section to Neo4j: {e}")
            raise

    def remove_section(self, section_name: str) -> bool:
        """Remove a section from Neo4j."""
        try:
            driver = self._get_driver()

            with driver.session(database=self.database) as session:
                query = """
                MATCH (s:Section {name: $section_name})
                DETACH DELETE s
                """

                session.run(query, {"section_name": section_name})

            self._track_success()
            self.logger.info(f"✅ Section removed from Neo4j: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove section from Neo4j: {e}")
            raise

    def create_backup(self) -> str:
        """Create a backup of the Neo4j database."""
        try:
            # Neo4j backup would typically use neo4j-admin or enterprise features
            # For demo purposes, we'll export to JSON
            backup_file = f"neo4j_backup_{int(time.time())}.json"

            driver = self._get_driver()
            with driver.session(database=self.database) as session:
                # Export all data to JSON
                query = """
                MATCH (n)
                RETURN n
                """
                result = session.run(query)

                # Convert to JSON format
                import json

                data = [dict(record["n"].items()) for record in result]

                with open(backup_file, "w") as f:
                    json.dump(data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Neo4j backup created: {backup_file}")
            return backup_file

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Neo4j backup failed: {e}")
            raise

    def list_backups(self) -> List[str]:
        """List available Neo4j backups."""
        try:
            import glob

            backup_files = glob.glob("neo4j_backup_*.json")
            return sorted(backup_files)

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to list Neo4j backups: {e}")
            raise

    def restore_backup(self, backup_file: str) -> bool:
        """Restore from a Neo4j backup."""
        try:
            import json

            with open(backup_file, "r") as f:
                data = json.load(f)

            driver = self._get_driver()
            with driver.session(database=self.database) as session:
                # Clear existing data
                session.run("MATCH (n) DETACH DELETE n")

                # Restore from backup
                for item in data:
                    if "id" in item:
                        # Restore item
                        query = """
                        CREATE (i:Item $properties)
                        """
                        session.run(query, {"properties": item})
                    elif "name" in item:
                        # Restore section
                        query = """
                        CREATE (s:Section $properties)
                        """
                        session.run(query, {"properties": item})

            self._track_success()
            self.logger.info(f"✅ Neo4j backup restored: {backup_file}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Neo4j backup restore failed: {e}")
            raise

    def validate(self) -> bool:
        """Validate the Neo4j database structure."""
        try:
            driver = self._get_driver()

            with driver.session(database=self.database) as session:
                # Check if database is accessible
                query = "RETURN 1 as test"
                result = session.run(query)
                result.single()

            self._track_success()
            self.logger.info("✅ Neo4j validation passed")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Neo4j validation failed: {e}")
            raise

    def load_model(self) -> Dict[str, Any]:
        """Load the current model from Neo4j."""
        try:
            driver = self._get_driver()

            with driver.session(database=self.database) as session:
                # Load all items
                items_query = "MATCH (i:Item) RETURN i"
                items_result = session.run(items_query)
                items = [dict(record["i"].items()) for record in items_result]

                # Load all sections
                sections_query = "MATCH (s:Section) RETURN s"
                sections_result = session.run(sections_query)
                sections = [dict(record["s"].items()) for record in sections_result]

                # Organize by collection
                model_data = {}
                for item in items:
                    collection = item.get("collection", "items")
                    if collection not in model_data:
                        model_data[collection] = []
                    model_data[collection].append(item)

                # Add sections
                for section in sections:
                    section_name = section.get("name", "unknown")
                    model_data[section_name] = section.get("config", {})

            self._track_success()
            self.logger.info("✅ Model loaded from Neo4j")
            return model_data

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to load model from Neo4j: {e}")
            raise

    def __del__(self):
        """Clean up Neo4j driver."""
        if self._driver:
            self._driver.close()
