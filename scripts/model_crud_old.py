#!/usr/bin/env python3
"""
Model CRUD CLI
Generic command-line interface for model CRUD operations using model registry.
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from round_trip_engineering.tools import get_model_registry


def main():
    """CLI interface for Model CRUD operations."""
    parser = argparse.ArgumentParser(description="Model CRUD CLI")
    parser.add_argument(
        "action",
        choices=[
            "register-model",
            "list-models",
            "unregister-model",
            "get-model-info",
            "list-domains",
            "list-domain-requirements",
            "add-item",
            "update-section",
            "remove-item",
            "add-section",
            "remove-section",
            "create-backup",
            "list-backups",
            "restore-backup",
            "validate",
        ],
    )

    # Registry Management Parameters (ONLY for registration)
    parser.add_argument("--model-name", help="Model name")
    parser.add_argument(
        "--implementation",
        choices=[
            "json_model_manager",
            "neo4j_model_manager",
            "ontology_model_manager",
            "project_model_manager",
        ],
        help="Implementation name (for registration only)",
    )
    parser.add_argument("--config", help="JSON configuration (for registration only)")

    # Model CRUD Parameters (business operations - NO auth/config needed)
    parser.add_argument("--id", help="Item ID")
    parser.add_argument("--title", help="Item title")
    parser.add_argument("--description", help="Item description")
    parser.add_argument("--priority", help="Priority level")
    parser.add_argument("--collection", help="Collection name")
    parser.add_argument("--section", help="Section name")
    parser.add_argument("--updates", help="JSON updates")
    parser.add_argument("--backup-file", help="Backup file path")
    parser.add_argument("--domain", help="Domain name for list-domain-requirements")
    parser.add_argument("--search", help="Search term for filtering requirements")
    parser.add_argument("--category", help="Category filter (demo_core, demo_tools, etc.)")
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format",
    )

    args = parser.parse_args()

    try:
        registry = get_model_registry()

        if args.action == "register-model":
            if not all([args.model_name, args.implementation]):
                print("❌ --model-name and --implementation required for register-model")
                return 1

            # Parse configuration (ONLY for registration)
            config = {}
            if args.config:
                try:
                    config = json.loads(args.config)
                except json.JSONDecodeError:
                    print("❌ Invalid --config JSON")
                    return 1

            # Register model with config
            success = registry.register_model(args.model_name, args.implementation, **config)
            print(f"✅ Model registered: {args.model_name} ({args.implementation})")

        elif args.action == "list-models":
            models = registry.list_models()
            print("📋 Registered models:")
            for model_name in models:
                info = registry.get_model_info(model_name)
                print(f"  - {model_name}")
                if info.get("config"):
                    print(f"    Config: {list(info['config'].keys())}")

        elif args.action == "unregister-model":
            if not args.model_name:
                print("❌ --model-name required for unregister-model")
                return 1
            success = registry.unregister_model(args.model_name)
            print(f"✅ Model unregistered: {args.model_name}")

        elif args.action == "get-model-info":
            if not args.model_name:
                print("❌ --model-name required for get-model-info")
                return 1
            info = registry.get_model_info(args.model_name)
            print(f"📋 Model info for '{args.model_name}':")
            print(f"  Implementation: {info.get('implementation', 'N/A')}")
            print(f"  Config: {info.get('config', {})}")
            print(f"  Instance: {'Initialized' if info.get('instance') else 'Lazy (not initialized)'}")

        elif args.action == "list-domains":
            # Load project model registry to get domains
            try:
                from pathlib import Path

                project_root = Path(__file__).parent.parent
                registry_file = project_root / "project_model_registry.json"

                if not registry_file.exists():
                    print("❌ project_model_registry.json not found")
                    return 1

                with open(registry_file, "r") as f:
                    project_model = json.load(f)

                domains = project_model.get("domains", {})

                if not domains:
                    print("📋 No domains found in project model registry")
                    return 0

                print("📋 Project Domains:")
                print("=" * 50)

                # Group domains by architecture category
                domain_architecture = project_model.get("domain_architecture", {})

                for category, category_info in domain_architecture.items():
                    # Skip if category_info is None
                    if category_info is None:
                        continue
                    category_domains = category_info.get("domains", [])
                    if category_domains:
                        print(f"\n🏗️  {category.replace('_', ' ').title()}:")
                        print(f"   Purpose: {category_info.get('description', 'N/A')}")
                        print("   Domains:")
                        for domain_name in category_domains:
                            domain_info = domains.get(domain_name, {})
                            patterns = domain_info.get("patterns", [])
                            linter = domain_info.get("linter", "N/A")
                            formatter = domain_info.get("formatter", "N/A")
                            validator = domain_info.get("validator", "N/A")

                            print(f"     • {domain_name}")
                            print(f"       - Patterns: {len(patterns)} file patterns")
                            print(f"       - Linter: {linter}")
                            print(f"       - Formatter: {formatter}")
                            print(f"       - Validator: {validator}")

                            # Show extraction potential if available
                            extraction = domain_info.get("extraction_candidate", False)
                            if extraction:
                                print(f"       - Extraction: {extraction}")

                            # Show package potential if available
                            package_potential = domain_info.get("package_potential", {})
                            if package_potential:
                                score = package_potential.get("score", 0)
                                package_name = package_potential.get("package_name", "N/A")
                                print(f"       - Package Potential: {score}/10 ({package_name})")

                # Show domains not in architecture categories
                categorized_domains = set()
                for category_info in domain_architecture.values():
                    # Skip if category_info is None
                    if category_info is None:
                        continue
                    categorized_domains.update(category_info.get("domains", []))

                uncategorized = set(domains.keys()) - categorized_domains
                if uncategorized:
                    print(f"\n📁 Uncategorized Domains:")
                    for domain_name in sorted(uncategorized):
                        domain_info = domains.get(domain_name, {})
                        print(f"     • {domain_name}")
                        if domain_info and domain_info.get("description"):
                            print(f"       - {domain_info['description']}")

                print(f"\n📊 Summary:")
                print(f"   Total Domains: {len(domains)}")
                print(f"   Categorized: {len(domains) - len(uncategorized)}")
                print(f"   Uncategorized: {len(uncategorized)}")

            except Exception as e:
                import traceback

                print(f"❌ Error loading domains: {e}")
                print(f"🔍 Error details: {traceback.format_exc()}")
                return 1

        elif args.action in [
            "add-item",
            "update-section",
            "remove-item",
            "add-section",
            "remove-section",
            "create-backup",
            "list-backups",
            "restore-backup",
            "validate",
        ]:
            if not args.model_name:
                print(f"❌ --model-name required for {args.action}")
                return 1

            # Get model instance for business CRUD operations (NO auth/config needed)
            manager = registry.get_model(args.model_name)

            if args.action == "add-item":
                if not all([args.id, args.description]):
                    print("❌ --id and --description required for add-item")
                    return 1

                # Let the model manager handle defaults
                kwargs = {}
                if args.title:
                    kwargs["title"] = args.title
                if args.priority:
                    kwargs["priority"] = args.priority
                if args.collection:
                    kwargs["collection"] = args.collection

                success = manager.add_item(args.id, args.description, **kwargs)
                print(f"✅ Item added: {success}")

            elif args.action == "update-section":
                if not all([args.section, args.updates]):
                    print("❌ --section and --updates required for update-section")
                    return 1
                updates = json.loads(args.updates)
                success = manager.update_section(args.section, updates)
                print(f"✅ Section updated: {success}")

            elif args.action == "remove-item":
                if not args.id:
                    print("❌ --id required for remove-item")
                    return 1
                success = manager.remove_item(args.id, args.collection or "items")
                print(f"✅ Item removed: {success}")

            elif args.action == "add-section":
                if not all([args.section, args.updates]):
                    print("❌ --section and --updates required for add-section")
                    return 1
                section_config = json.loads(args.updates)
                success = manager.add_section(args.section, section_config)
                print(f"✅ Section added: {success}")

            elif args.action == "remove-section":
                if not args.section:
                    print("❌ --section required for remove-section")
                    return 1
                success = manager.remove_section(args.section)
                print(f"✅ Section removed: {success}")

            elif args.action == "create-backup":
                backup_file = manager.create_backup()
                print(f"✅ Backup created: {backup_file}")

            elif args.action == "list-backups":
                backups = manager.list_backups()
                print("📋 Available backups:")
                for backup in backups:
                    print(f"  - {backup}")

            elif args.action == "restore-backup":
                if not args.backup_file:
                    print("❌ --backup-file required for restore-backup")
                    return 1
                success = manager.restore_backup(args.backup_file)
                print(f"✅ Backup restored: {success}")

            elif args.action == "validate":
                success = manager.validate()
                print(f"✅ Model validation: {success}")

        elif args.action == "list-domain-requirements":
            # Load project model registry to get domain requirements
            try:
                from pathlib import Path

                project_root = Path(__file__).parent.parent
                registry_file = project_root / "project_model_registry.json"

                if not registry_file.exists():
                    print("❌ project_model_registry.json not found")
                    return 1

                with open(registry_file, "r") as f:
                    project_model = json.load(f)

                domains = project_model.get("domains", {})
                domain_architecture = project_model.get("domain_architecture", {})

                if not domains:
                    print("📋 No domains found in project model registry")
                    return 0

                # Filter domains if specified
                if args.domain:
                    if args.domain not in domains:
                        print(f"❌ Domain '{args.domain}' not found")
                        return 1
                    domains_to_show = {args.domain: domains[args.domain]}
                else:
                    domains_to_show = domains

                # Filter by category if specified
                if args.category:
                    if args.category not in domain_architecture:
                        print(f"❌ Category '{args.category}' not found")
                        return 1
                    category_domains = domain_architecture[args.category].get("domains", [])
                    domains_to_show = {k: v for k, v in domains_to_show.items() if k in category_domains}

                # Filter by search term if specified
                if args.search:
                    search_term = args.search.lower()
                    filtered_domains = {}
                    for domain_name, domain_info in domains_to_show.items():
                        if domain_info and isinstance(domain_info, dict):
                            reqs = domain_info.get("requirements", [])
                            # Check if search term appears in domain name or requirements
                            if search_term in domain_name.lower() or any(search_term in req.lower() for req in reqs):
                                filtered_domains[domain_name] = domain_info
                    domains_to_show = filtered_domains

                # Output format handling
                if args.format == "json":
                    output_data = {}
                    for domain_name, domain_info in domains_to_show.items():
                        if domain_info and isinstance(domain_info, dict):
                            output_data[domain_name] = {
                                "requirements": domain_info.get("requirements", []),
                                "description": domain_info.get("description", ""),
                                "patterns": domain_info.get("patterns", []),
                                "linter": domain_info.get("linter", "N/A"),
                                "formatter": domain_info.get("formatter", "N/A"),
                                "validator": domain_info.get("validator", "N/A"),
                            }
                    print(json.dumps(output_data, indent=2))
                elif args.format == "csv":
                    import csv
                    import sys

                    writer = csv.writer(sys.stdout)
                    writer.writerow(["Domain", "Requirement"])
                    for domain_name, domain_info in domains_to_show.items():
                        if domain_info and isinstance(domain_info, dict):
                            reqs = domain_info.get("requirements", [])
                            for req in reqs:
                                writer.writerow([domain_name, req])
                else:  # text format
                    print("📋 Domain Requirements:")
                    print("=" * 60)

                    for domain_name, domain_info in domains_to_show.items():
                        if domain_info and isinstance(domain_info, dict):
                            reqs = domain_info.get("requirements", [])
                            if reqs:
                                print(f"\n🏗️  {domain_name} ({len(reqs)} requirements):")
                                if domain_info.get("description"):
                                    print(f"   Description: {domain_info['description']}")
                                print("   Requirements:")
                                for i, req in enumerate(reqs, 1):
                                    print(f"     {i}. {req}")

                    print(f"\n📊 Summary:")
                    print(f"   Total Domains: {len(domains_to_show)}")
                    total_reqs = sum(len(domain_info.get("requirements", [])) for domain_info in domains_to_show.values() if domain_info and isinstance(domain_info, dict))
                    print(f"   Total Requirements: {total_reqs}")

            except Exception as e:
                import traceback

                print(f"❌ Error loading domain requirements: {e}")
                print(f"🔍 Error details: {traceback.format_exc()}")
                return 1

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
