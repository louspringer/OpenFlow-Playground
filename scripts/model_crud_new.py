#!/usr/bin/env python3
"""
Main orchestration for model CRUD system.
Single responsibility: Orchestrate operations and provide main entry point.
"""

import sys
from cli_parser import create_parser
from domain_operations import create_domain_operations
from model_operations import create_model_registry_operations
from crud_operations import create_crud_operations


def main():
    """Main entry point for model CRUD operations."""

    # Create parser and parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Validate arguments
    is_valid, error_msg = parser.validate_args(args)
    if not is_valid:
        print(f"❌ {error_msg}")
        return 1

    try:
        # Route to appropriate operation handler
        if args.action in ["list-domains", "list-domain-requirements"]:
            return _handle_domain_operations(args)
        elif args.action in [
            "register-model",
            "list-models",
            "unregister-model",
            "get-model-info",
        ]:
            return _handle_model_operations(args)
        else:
            return _handle_crud_operations(args)

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def _handle_domain_operations(args):
    """Handle domain-specific operations."""
    domain_ops = create_domain_operations()

    if args.action == "list-domains":
        result = domain_ops.list_domains()
        print(result)
        return 0 if not result.startswith("❌") else 1

    elif args.action == "list-domain-requirements":
        result = domain_ops.list_domain_requirements(
            domain=args.domain,
            search=args.search,
            category=args.category,
            format=args.format,
        )
        print(result)
        return 0 if not result.startswith("❌") else 1


def _handle_model_operations(args):
    """Handle model registry operations."""
    model_ops = create_model_registry_operations()

    if args.action == "register-model":
        success, message = model_ops.register_model(
            args.model_name, args.implementation, args.config
        )
        print(message)
        return 0 if success else 1

    elif args.action == "unregister-model":
        success, message = model_ops.unregister_model(args.model_name)
        print(message)
        return 0 if success else 1

    elif args.action == "list-models":
        success, message = model_ops.list_models()
        print(message)
        return 0 if success else 1

    elif args.action == "get-model-info":
        success, message = model_ops.get_model_info(args.model_name)
        print(message)
        return 0 if success else 1


def _handle_crud_operations(args):
    """Handle business CRUD operations."""
    crud_ops = create_crud_operations()

    if args.action == "add-item":
        success, message = crud_ops.add_item(
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
        success, message = crud_ops.update_section(
            args.model_name, args.section, args.updates
        )
        print(message)
        return 0 if success else 1

    elif args.action == "remove-item":
        success, message = crud_ops.remove_item(
            args.model_name, args.id, args.collection
        )
        print(message)
        return 0 if success else 1

    elif args.action == "add-section":
        success, message = crud_ops.add_section(
            args.model_name, args.section, args.updates
        )
        print(message)
        return 0 if success else 1

    elif args.action == "remove-section":
        success, message = crud_ops.remove_section(args.model_name, args.section)
        print(message)
        return 0 if success else 1

    elif args.action == "create-backup":
        success, message = crud_ops.create_backup(args.model_name)
        print(message)
        return 0 if success else 1

    elif args.action == "list-backups":
        success, message = crud_ops.list_backups(args.model_name)
        print(message)
        return 0 if success else 1

    elif args.action == "restore-backup":
        success, message = crud_ops.restore_backup(args.model_name, args.backup_file)
        print(message)
        return 0 if success else 1

    elif args.action == "validate":
        success, message = crud_ops.validate(args.model_name)
        print(message)
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
