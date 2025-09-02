#!/usr/bin/env python3
"""
Model CRUD CLI - Domain Implementation

This module provides the CLI interface for model management operations.
All operations are delegated to appropriate domain components.

Single responsibility: CLI orchestration for model_management domain.
"""

import sys
from typing import Any, Dict
from .cli_parser import create_parser
from .domain_operations import DomainOperations
from .model_operations import ModelOperations
from .crud_operations import CrudOperations


class ModelManagementCLI:
    """Parameterized CLI interface for model management operations."""

    def __init__(self):
        """Initialize CLI with domain components."""
        self.domain_ops = DomainOperations()
        self.model_ops = ModelOperations()
        self.crud_ops = CrudOperations()

    def run(self) -> int:
        """Run the CLI application."""
        parser = create_parser()
        args = parser.parse_args()

        # Validate arguments
        is_valid, error_msg = parser.validate_args(args)
        if not is_valid:
            print(f"❌ {error_msg}")
            return 1

        try:
            # Route to appropriate domain operation
            return self._route_operation(args)
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1

    def _route_operation(self, args) -> int:
        """Route operation to appropriate domain component."""
        if args.action == "read":
            return self._handle_read_operation()
        elif args.action in ["list-domains", "list-domain-requirements"]:
            return self._handle_domain_operations(args)
        elif args.action in ["register-model", "list-models", "unregister-model", "get-model-info"]:
            return self._handle_model_operations(args)
        else:
            return self._handle_crud_operations(args)

    def _handle_read_operation(self) -> int:
        """Handle read operations - delegate to model operations."""
        try:
            result = self.model_ops.read_model_registry()
            print(result)
            return 0
        except Exception as e:
            print(f"❌ Error reading model: {e}")
            return 1

    def _handle_domain_operations(self, args) -> int:
        """Handle domain-specific operations - delegate to domain operations."""
        if args.action == "list-domains":
            result = self.domain_ops.list_domains()
            print(result)
            return 0 if not result.startswith("❌") else 1

        elif args.action == "list-domain-requirements":
            result = self.domain_ops.list_domain_requirements(
                domain=args.domain,
                search=args.search,
                category=args.category,
                format=args.format,
            )
            print(result)
            return 0 if not result.startswith("❌") else 1

        return 1

    def _handle_model_operations(self, args) -> int:
        """Handle model registry operations - delegate to model operations."""
        if args.action == "register-model":
            success, message = self.model_ops.register_model(args.model_name, args.implementation, args.config)
            print(message)
            return 0 if success else 1

        elif args.action == "unregister-model":
            success, message = self.model_ops.unregister_model(args.model_name)
            print(message)
            return 0 if success else 1

        elif args.action == "list-models":
            success, message = self.model_ops.list_models()
            print(message)
            return 0 if success else 1

        elif args.action == "get-model-info":
            success, message = self.model_ops.get_model_info(args.model_name)
            print(message)
            return 0 if success else 1

        return 1

    def _handle_crud_operations(self, args) -> int:
        """Handle business CRUD operations - delegate to CRUD operations."""
        if args.action == "add-item":
            success, message = self.crud_ops.add_item(
                args.model_name,
                args.id,
                args.description,
                title=args.title,
                priority=args.priority,
                collection=args.collection,
            )
            print(message)
            return 0 if success else 1

        elif args.action == "update-section":
            success, message = self.crud_ops.update_section(args.model_name, args.section, args.updates)
            print(message)
            return 0 if success else 1

        elif args.action == "remove-item":
            success, message = self.crud_ops.remove_item(args.model_name, args.id, args.collection)
            print(message)
            return 0 if success else 1

        elif args.action == "add-section":
            success, message = self.crud_ops.add_section(args.model_name, args.section, args.updates)
            print(message)
            return 0 if success else 1

        elif args.action == "remove-section":
            success, message = self.crud_ops.remove_section(args.model_name, args.section)
            print(message)
            return 0 if success else 1

        elif args.action == "create-backup":
            success, message = self.crud_ops.create_backup(args.model_name)
            print(message)
            return 0 if success else 1

        elif args.action == "list-backups":
            success, message = self.crud_ops.list_backups(args.model_name)
            print(message)
            return 0 if success else 1

        elif args.action == "restore-backup":
            success, message = self.crud_ops.restore_backup(args.model_name, args.backup_file)
            print(message)
            return 0 if success else 1

        elif args.action == "validate":
            success, message = self.crud_ops.validate(args.model_name)
            print(message)
            return 0 if success else 1

        return 1


def main():
    """Main entry point for backward compatibility."""
    cli = ModelManagementCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
