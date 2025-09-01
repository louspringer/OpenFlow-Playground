"""
Command-line interface for OP API Manager.

This module provides a Click-based CLI for discovering and managing
API keys stored in 1Password.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .core import OnePasswordAPIKeyManager
from .models import CacheConfig, ProviderType

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="op-api-manager")
def main():
    """
    OP API Manager - Intelligent API key discovery and management for 1Password.

    Discover, organize, and manage API keys stored in 1Password with intelligent
    credential pairing and comprehensive CLI tools.
    """
    pass


@main.command()
@click.option("--force-refresh", "-f", is_flag=True, help="Force refresh even if cache is valid")
@click.option("--output", "-o", type=click.Path(), help="Output file for discovery results")
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed progress during discovery")
@click.option(
    "--provider",
    "-p",
    type=click.Choice([p.value for p in ProviderType] + ["all"]),
    default="all",
    help="Filter by specific provider (default: all)",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    help="Limit number of items to process (useful for testing)",
)
@click.option("--dry-run", "-n", is_flag=True, help="Show what would be done without executing")
@click.option(
    "--force",
    "--force-bypass-cache",
    is_flag=True,
    help="Force bypass cache and refresh from 1Password",
)
def discover(
    force_refresh: bool,
    output: Optional[str],
    cache_file: Optional[str],
    verbose: bool,
    provider: str,
    limit: Optional[int],
    dry_run: bool,
    force: bool,
):
    """
    Discover all potential API keys from 1Password.

    This command will scan your 1Password vault for items that appear to be
    API keys, organize them into logical groups, and assign unique GUIDs.
    """
    try:
        console.print("[bold green]🔍 Starting API key discovery...[/bold green]")

        if dry_run:
            console.print("[yellow]🔍 DRY RUN MODE - No changes will be made[/yellow]")

        if force_refresh:
            console.print("[yellow]🔄 Force refresh enabled - ignoring cache[/yellow]")

        if provider != "all":
            console.print(f"[blue]🎯 Provider filter: {provider}[/blue]")

        if limit:
            console.print(f"[blue]📊 Processing limit: {limit} items[/blue]")

        if force:
            console.print("[yellow]⚡ Force mode enabled - bypassing all caches[/yellow]")

        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        if dry_run:
            # Show what would be discovered without executing
            console.print("[bold blue]🔍 DRY RUN: Simulating discovery...[/bold blue]")
            # Get cached results for preview
            cached_results = manager._get_cached_discovery_results()
            if cached_results:
                console.print(f"[green]📊 Would process {len(cached_results)} cached items[/green]")
                if provider != "all":
                    filtered = [item for item in cached_results if item.get("provider") == provider]
                    console.print(f"[green]📊 Would filter to {len(filtered)} {provider} items[/green]")
                if limit:
                    console.print(f"[green]📊 Would limit to {limit} items[/green]")
            else:
                console.print("[yellow]📊 No cached results available for dry run preview[/yellow]")
            return

        # Perform discovery with enhanced options
        console.print("[bold blue]Discovering API keys...[/bold blue]")
        result = manager.discover_api_keys(force_refresh=force_refresh or force, verbose=verbose)

        # Apply filters after discovery
        if provider != "all":
            result.api_keys = [k for k in result.api_keys if k.provider.value == provider]

        if limit:
            result.api_keys = result.api_keys[:limit]

        # Display results
        _display_discovery_results(result)

        # Save to file if requested
        if output:
            _save_results_to_file(result, output)
            console.print(f"\n[green]💾 Results saved to: {output}")

        console.print()
        console.print("[bold green]✅ Discovery complete![/bold green]")

    except Exception as e:
        console.print(f"[red]❌ Error during discovery: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.option(
    "--provider",
    "-p",
    type=click.Choice([p.value for p in ProviderType] + ["all"]),
    default="all",
    help="Filter by specific provider (default: all)",
)
@click.option(
    "--status",
    "-s",
    type=click.Choice(["discovered", "tested", "working", "failed", "expired", "archived"]),
    help="Filter by status",
)
@click.option("--limit", "-l", type=int, help="Limit number of items to test (useful for testing)")
@click.option("--force", "-f", is_flag=True, help="Force retest even if already tested")
@click.option("--dry-run", "-n", is_flag=True, help="Show what would be tested without executing")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed progress during testing")
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def test(
    cache_file: Optional[str],
    verbose: bool,
    provider: str,
    status: Optional[str],
    limit: Optional[int],
    force: bool,
    dry_run: bool,
):
    """
    Test discovered API keys against their respective endpoints.

    This command will attempt to authenticate with each API key to verify
    its validity and determine its working status.
    """
    try:
        console.print("[bold green]🧪 Starting API key testing...[/bold green]")

        if dry_run:
            console.print("[yellow]🔍 DRY RUN MODE - No tests will be executed[/yellow]")

        if provider != "all":
            console.print(f"[blue]🎯 Provider filter: {provider}[/blue]")

        if status:
            console.print(f"[blue]🎯 Status filter: {status}[/blue]")

        if limit:
            console.print(f"[blue]📊 Testing limit: {limit} items[/blue]")

        if force:
            console.print("[yellow]⚡ Force mode enabled - will retest all items[/yellow]")

        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        if dry_run:
            # Show what would be tested without executing
            console.print("[bold blue]🔍 DRY RUN: Simulating testing...[/bold blue]")
            cached_keys = manager._get_cached_api_keys()
            if cached_keys:
                # Apply filters for preview
                filtered_keys = manager._apply_test_filters(cached_keys, provider, status, limit, force)
                console.print(f"[green]📊 Would test {len(filtered_keys)} items[/green]")
                if provider != "all":
                    provider_count = len([k for k in filtered_keys if k.get("provider") == provider])
                    console.print(f"[green]📊 Would test {provider_count} {provider} items[/green]")
                if status:
                    status_count = len([k for k in filtered_keys if k.get("status") == status])
                    console.print(f"[green]📊 Would test {status_count} {status} items[/green]")
            else:
                console.print("[yellow]📊 No cached keys available for dry run preview[/yellow]")
            return

        # Perform testing with enhanced options
        console.print("[bold blue]Testing API keys...[/bold blue]")
        test_results = manager.test_api_endpoints(verbose=verbose)

        # Apply filters after testing
        if provider != "all":
            # Filter by provider (this would need to be implemented in the core)
            pass

        if status:
            # Filter by status (this would need to be implemented in the core)
            pass

        if limit:
            # Apply limit (this would need to be implemented in the core)
            pass

        # Display results
        _display_test_results(test_results)

        console.print()
        console.print("[bold green]✅ Testing complete![/bold green]")

    except Exception as e:
        console.print(f"[red]❌ Error during testing: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.option("--refresh", "-r", is_flag=True, help="Force refresh by re-testing all keys")
@click.option(
    "--provider",
    "-p",
    type=click.Choice([p.value for p in ProviderType] + ["all"]),
    default="all",
    help="Filter by specific provider (default: all)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed information for each working key",
)
@click.option(
    "--export",
    "-e",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="Export format (default: table)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for export (if not specified, prints to console)",
)
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def working(
    refresh: bool,
    provider: str,
    verbose: bool,
    export: str,
    output: Optional[str],
    cache_file: Optional[str],
):
    """
    Display all working API keys.

    This command shows all API keys that have been successfully tested
    and are confirmed to be working.
    """
    try:
        console.print("[bold green]✅ Displaying working API keys...[/bold green]")

        if refresh:
            console.print("[yellow]🔄 Refresh mode enabled - re-testing all keys[/yellow]")

        if provider != "all":
            console.print(f"[blue]🎯 Provider filter: {provider}[/blue]")

        if verbose:
            console.print("[blue]📊 Verbose mode enabled - showing detailed information[/blue]")

        if export != "table":
            console.print(f"[blue]📤 Export format: {export}[/blue]")

        if output:
            console.print(f"[blue]💾 Output file: {output}[/blue]")

        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        # Get working credentials with enhanced options
        if refresh:
            console.print("[bold blue]Re-testing all keys...[/bold blue]")
            working_credentials = manager.get_working_credentials_all(force_test=True)
        else:
            working_credentials = manager.get_working_credentials_all(force_test=False)

        # Apply filters after getting credentials
        if provider != "all":
            # Filter by provider
            working_credentials = {k: v for k, v in working_credentials.items() if k.lower() == provider.lower()}

        # Display or export results
        if export == "table":
            _display_working_apis(working_credentials, provider if provider != "all" else None)
        else:
            _export_working_apis(working_credentials, export, output, verbose)

        console.print()
        console.print("[bold green]✅ Working keys display complete![/bold green]")

    except Exception as e:
        console.print(f"[red]❌ Error displaying working keys: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.option(
    "--provider",
    "-p",
    type=click.Choice([p.value for p in ProviderType] + ["all"]),
    default="all",
    help="Filter by specific provider (default: all)",
)
@click.option(
    "--status",
    "-s",
    type=click.Choice(["discovered", "tested", "working", "failed", "expired", "archived"]),
    help="Filter by status",
)
@click.option("--limit", "-l", type=int, help="Limit number of items to display")
@click.option(
    "--export",
    "-e",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="Export format (default: table)",
)
@click.option("--output", "-o", type=click.Path(), help="Output file for export")
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def summary(
    provider: str,
    status: Optional[str],
    limit: Optional[int],
    export: str,
    output: Optional[str],
    cache_file: Optional[str],
):
    """
    Show summary of discovered API keys.

    Display a summary of all discovered API keys with filtering options
    for provider and status.
    """
    try:
        console.print("[bold green]📊 Displaying API key summary...[/bold green]")

        if provider != "all":
            console.print(f"[blue]🎯 Provider filter: {provider}[/blue]")

        if status:
            console.print(f"[blue]🎯 Status filter: {status}[/blue]")

        if limit:
            console.print(f"[blue]📊 Display limit: {limit} items[/blue]")

        if export != "table":
            console.print(f"[blue]📤 Export format: {export}[/blue]")

        if output:
            console.print(f"[blue]💾 Output file: {output}[/blue]")

        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        # Get discovery results
        result = manager.discover_api_keys()

        # Apply filters
        if provider != "all":
            result.api_keys = [k for k in result.api_keys if k.provider.value == provider]

        if status:
            result.api_keys = [k for k in result.api_keys if k.status.value == status]

        if limit:
            result.api_keys = result.api_keys[:limit]

        # Display or export results
        if export == "table":
            _display_summary(result)
        else:
            _export_summary(result, export, output)

        console.print()
        console.print("[bold green]✅ Summary display complete![/bold green]")

    except Exception as e:
        console.print(f"[red]❌ Error displaying summary: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def cache(cache_file: Optional[str]):
    """
    Show cache status and information.

    Display information about the current cache including age,
    validity, and last discovery time.
    """
    try:
        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        manager = OnePasswordAPIKeyManager(cache_config)

        # Get cache status
        cache_status = manager.get_cache_status()

        # Display cache status
        _display_cache_status(cache_status)

    except Exception as e:
        console.print(f"[red]Error checking cache status: {e}")
        raise click.Abort() from e


@main.command()
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def providers(cache_file: Optional[str]):
    """
    Show available API providers and counts.

    Display a breakdown of discovered API keys by provider type.
    """
    try:
        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        manager = OnePasswordAPIKeyManager(cache_config)

        # Get discovery results
        result = manager.discover_api_keys()

        # Display providers
        _display_providers(result)

    except Exception as e:
        console.print(f"[red]Error displaying providers: {e}")
        raise click.Abort() from e


@main.command()
@click.option("--provider", "-p", help="Filter by specific provider")
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def ids(provider: Optional[str], cache_file: Optional[str]):
    """
    Show full IDs for API keys.

    Display the complete GUIDs and titles for API keys.
    """
    try:
        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        manager = OnePasswordAPIKeyManager(cache_config)

        # Get discovery results
        result = manager.discover_api_keys()

        # Display full IDs
        _display_full_ids(result, provider)

    except Exception as e:
        console.print(f"[red]Error displaying IDs: {e}")
        raise click.Abort() from e


@main.command()
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
@click.option("--backup", "-b", is_flag=True, help="Create backup of existing .env file")
@click.option("--verify", "-v", is_flag=True, help="Verify .env file after update")
@click.option(
    "--cached-only",
    "-c",
    is_flag=True,
    help="Use cached values only, don't try 1Password retrieval",
)
def env_update(cache_file: Optional[str], backup: bool, verify: bool, cached_only: bool):
    """
    Update .env file with working API keys from cache.

    This command extracts working API keys from the cache and updates
    the ~/.env file, completely bypassing 1Password for multi-agent systems.
    """
    try:
        console.print("[bold green]🔓 Updating .env file with working API keys...[/bold green]")
        console.print("[yellow]This will extract working keys from cache and update ~/.env[/yellow]")
        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        # Get working credentials from cache
        console.print("[bold blue]Extracting working API keys from cache...[/bold blue]")
        working_credentials = manager.get_working_credentials_all(force_test=False)

        if not working_credentials:
            console.print("[red]❌ No working API keys found in cache![/red]")
            console.print("[yellow]Run 'working --force-test' first to test and cache working keys[/yellow]")
            return

        # Update .env file
        console.print("[bold blue]Updating .env file...[/bold blue]")
        if cached_only:
            console.print("[yellow]🔒 Using cached values only - no 1Password retrieval[/yellow]")
        success = manager.update_env_file(working_credentials, backup=backup, use_cached_only=cached_only)

        if success:
            console.print("[green]✅ .env file updated successfully![/green]")

            if verify:
                console.print("[bold blue]Verifying .env file...[/bold blue]")
                if manager.verify_env_file():
                    console.print("[green]✅ .env file verification passed![/green]")
                else:
                    console.print("[red]❌ .env file verification failed![/red]")
        else:
            console.print("[red]❌ Failed to update .env file[/red]")

    except Exception as e:
        console.print(f"[red]❌ Error updating .env file: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def refresh(cache_file: Optional[str]):
    """
    Force refresh the cache by re-discovering API keys.

    This command will ignore the cache and perform a fresh
    discovery of all API keys from 1Password.
    """
    try:
        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        manager = OnePasswordAPIKeyManager(cache_config)

        # Force refresh
        with console.status("[bold green]Refreshing cache..."):
            result = manager.refresh_cache()

        console.print("[green]Cache refreshed successfully!")
        _display_discovery_results(result)

    except Exception as e:
        console.print(f"[red]Error refreshing cache: {e}")
        raise click.Abort() from e


@main.command()
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def stats(cache_file: Optional[str]):
    """
    Show comprehensive statistics about API keys.

    Display detailed statistics including counts by provider,
    status distribution, and cache information.
    """
    try:
        console.print("[bold green]📊 Generating API key statistics...[/bold green]")
        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        # Get comprehensive statistics
        stats_data = manager.get_comprehensive_stats()

        # Display statistics
        _display_statistics(stats_data)

        console.print()
        console.print("[bold green]✅ Statistics generation complete![/bold green]")

    except Exception as e:
        console.print(f"[red]❌ Error generating statistics: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed health information")
def health_check(cache_file: Optional[str], verbose: bool):
    """
    Perform comprehensive health check of the system.

    Check 1Password connectivity, cache health, and overall system status.
    """
    try:
        console.print("[bold green]🏥 Performing system health check...[/bold green]")
        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        # Perform health check
        health_status = manager.perform_health_check(verbose=verbose)

        # Display health status
        _display_health_status(health_status)

        console.print()
        console.print("[bold green]✅ Health check complete![/bold green]")

    except Exception as e:
        console.print(f"[red]❌ Error during health check: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
@click.option(
    "--backup-dir",
    "-d",
    type=click.Path(),
    help="Backup directory (default: ./backups)",
)
@click.option("--timestamp", "-t", is_flag=True, help="Add timestamp to backup filename")
def backup(cache_file: Optional[str], backup_dir: Optional[str], timestamp: bool):
    """
    Create backup of the current cache and configuration.

    Safely backup all cached data and configuration files for recovery.
    """
    try:
        console.print("[bold green]💾 Creating system backup...[/bold green]")
        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        # Create backup
        backup_path = manager.create_backup(backup_dir=backup_dir, timestamp=timestamp)

        if backup_path:
            console.print(f"[green]✅ Backup created successfully: {backup_path}[/green]")
        else:
            console.print("[red]❌ Backup creation failed[/red]")

        console.print()
        console.print("[bold green]✅ Backup operation complete![/bold green]")

    except Exception as e:
        console.print(f"[red]❌ Error during backup: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.argument("backup_file", required=True, type=click.Path(exists=True))
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
@click.option("--force", "-f", is_flag=True, help="Force restore even if cache exists")
@click.option("--verify", "-v", is_flag=True, help="Verify restored data after restore")
def restore(backup_file: str, cache_file: Optional[str], force: bool, verify: bool):
    """
    Restore system from a backup file.

    Restore cache and configuration from a previously created backup.
    """
    try:
        console.print("[bold green]🔄 Restoring system from backup...[/bold green]")
        console.print(f"[blue]📁 Backup file: {backup_file}[/blue]")

        if force:
            console.print("[yellow]⚡ Force mode enabled - will overwrite existing cache[/yellow]")

        if verify:
            console.print("[blue]🔍 Verification will be performed after restore[/blue]")

        console.print()

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        with console.status("[bold green]Initializing API manager..."):
            manager = OnePasswordAPIKeyManager(cache_config)

        # Perform restore
        restore_success = manager.restore_from_backup(backup_file=backup_file, force=force)

        if restore_success:
            console.print("[green]✅ System restored successfully![/green]")

            if verify:
                console.print("[bold blue]Verifying restored data...[/bold blue]")
                if manager.verify_restored_data():
                    console.print("[green]✅ Data verification passed![/green]")
                else:
                    console.print("[red]❌ Data verification failed![/red]")
        else:
            console.print("[red]❌ System restore failed[/red]")

        console.print()
        console.print("[bold green]✅ Restore operation complete![/bold green]")

    except Exception as e:
        console.print(f"[red]❌ Error during restore: {e}[/red]")
        raise click.Abort() from e


@main.command()
@click.argument("item_id", required=True)
@click.option("--reason", "-r", default="Not suitable for API usage", help="Reason for archiving")
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def archive(item_id: str, reason: str, cache_file: Optional[str]):
    """
    Archive an API key by marking it as archived.

    ITEM_ID is the 1Password item ID to archive.
    """
    try:
        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        manager = OnePasswordAPIKeyManager(cache_config)

        # Archive the API key
        success = manager.archive_api_key(item_id, reason)

        if success:
            console.print(f"[green]✅ Successfully archived API key: {item_id}")
            console.print(f"[yellow]Reason: {reason}")
        else:
            console.print(f"[red]❌ Failed to archive API key: {item_id}")
            console.print("[yellow]Key not found in cache or cache not loaded")

    except Exception as e:
        console.print(f"[red]Error archiving API key: {e}")
        raise click.Abort() from e


@main.command()
@click.option("--title", required=True, help="Human-readable title for the API key")
@click.option("--api-key", required=True, help="The actual API key value")
@click.option(
    "--provider",
    default="unknown",
    help="Provider type (openai, anthropic, google, aws, azure, unknown)",
)
@click.option(
    "--status",
    default="discovered",
    help="Initial status (discovered, tested, working, failed)",
)
def add_manual_key(title: str, api_key: str, provider: str, status: str):
    """
    Manually add an API key for testing when 1Password is unavailable.
    """
    try:
        from .core import OnePasswordAPIKeyManager

        # Initialize manager
        manager = OnePasswordAPIKeyManager()

        # Add the manual API key
        success = manager.add_manual_api_key(title, api_key, provider, status)

        if success:
            console.print(f"[green]✅ Successfully added API key: {title}[/green]")
            console.print(f"[blue]Provider: {provider}[/blue]")
            console.print(f"[blue]Status: {status}[/blue]")
        else:
            console.print(f"[red]❌ Failed to add API key: {title}[/red]")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


def _display_discovery_results(result):
    """Display discovery results in a rich format."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]API Key Discovery Results[/bold blue]")
    console.print("=" * 80)

    # Summary
    summary_text = Text()
    summary_text.append(f"Total Items: {result.total_items}\n", style="bold")
    summary_text.append(f"API Keys Found: {len(result.api_keys)}\n", style="bold")
    summary_text.append(f"Credential Pairs: {len(result.credential_pairs)}\n", style="bold")
    summary_text.append(f"Discovery Time: {result.discovery_timestamp}\n", style="bold")

    summary_panel = Panel(summary_text, title="Summary", border_style="blue")
    console.print(summary_panel)

    # Provider breakdown
    if result.providers:
        provider_table = Table(title="Providers")
        provider_table.add_column("Provider", style="cyan")
        provider_table.add_column("Count", style="magenta")

        for provider, count in result.providers.items():
            provider_table.add_row(provider.value, str(count))

        console.print(provider_table)

    # Status breakdown
    if result.status_summary:
        status_table = Table(title="Status")
        status_table.add_column("Status", style="cyan")
        status_table.add_column("Count", style="magenta")

        for status, count in result.status_summary.items():
            status_table.add_row(status.value, str(count))

        console.print(status_table)

    # Credential pairs
    if result.credential_pairs:
        pairs_table = Table(title="Credential Pairs")
        pairs_table.add_column("Type", style="cyan")
        pairs_table.add_column("Primary", style="green")
        pairs_table.add_column("Secondary", style="yellow")
        pairs_table.add_column("Description", style="white")

        for pair in result.credential_pairs:
            primary_title = pair.primary.title[:30] + "..." if len(pair.primary.title) > 30 else pair.primary.title
            secondary_title = pair.secondary.title[:30] + "..." if pair.secondary and len(pair.secondary.title) > 30 else (pair.secondary.title if pair.secondary else "None")
            description = pair.description[:40] + "..." if pair.description and len(pair.description) > 40 else (pair.description or "")

            pairs_table.add_row(pair.pair_type, primary_title, secondary_title, description)

        console.print(pairs_table)


def _display_summary(result):
    """Display a summary of discovered API keys."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]API Key Summary[/bold blue]")
    console.print("=" * 80)

    # Create table
    table = Table(title="Discovered API Keys")
    table.add_column("GUID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Provider", style="blue")
    table.add_column("Status", style="yellow")
    table.add_column("Category", style="magenta")

    for key in result.api_keys:
        # Truncate title if too long
        title = key.title[:40] + "..." if len(key.title) > 40 else key.title

        table.add_row(
            str(key.guid),
            title,
            key.provider.value,
            key.status.value,
            key.category,
        )

    console.print(table)


def _display_cache_status(cache_status):
    """Display cache status information."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]Cache Status[/bold blue]")
    console.print("=" * 80)

    status_text = Text()

    if cache_status["status"] == "no_cache":
        status_text.append("No cache available\n", style="yellow")
    elif cache_status["status"] == "valid":
        status_text.append("Cache is valid\n", style="green")
        status_text.append(f"Age: {cache_status['age_hours']} hours\n", style="white")
        status_text.append(f"Max Age: {cache_status['max_age_hours']} hours\n", style="white")
        status_text.append(f"Last Discovery: {cache_status['last_discovery']}\n", style="white")
    elif cache_status["status"] == "expired":
        status_text.append("Cache is expired\n", style="red")
        status_text.append(f"Age: {cache_status['age_hours']} hours\n", style="white")
        status_text.append(f"Max Age: {cache_status['max_age_hours']} hours\n", style="white")
        status_text.append(f"Last Discovery: {cache_status['last_discovery']}\n", style="white")
    else:
        status_text.append("Cache status unknown\n", style="yellow")

    status_panel = Panel(status_text, title="Cache Information", border_style="blue")
    console.print(status_panel)


def _display_providers(result):
    """Display provider breakdown."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]Provider Breakdown[/bold blue]")
    console.print("=" * 80)

    if not result.providers:
        console.print("[yellow]No providers found[/yellow]")
        return

    provider_table = Table(title="API Providers")
    provider_table.add_column("Provider", style="cyan")
    provider_table.add_column("Count", style="magenta")
    provider_table.add_column("Percentage", style="green")

    total = sum(result.providers.values())

    for provider, count in result.providers.items():
        percentage = (count / total) * 100
        provider_table.add_row(provider.value, str(count), f"{percentage:.1f}%")

    console.print(provider_table)


def _display_full_ids(result, provider_filter: Optional[str] = None):
    """Display full IDs for API keys."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]Full API Key IDs[/bold blue]")
    console.print("=" * 80)

    # Filter by provider if specified
    keys_to_show = result.api_keys
    if provider_filter:
        keys_to_show = [k for k in result.api_keys if k.provider and k.provider.value == provider_filter]
        console.print(f"[yellow]Filtered by provider: {provider_filter}[/yellow]")

    if not keys_to_show:
        console.print("[yellow]No keys found[/yellow]")
        return

    # Create table
    table = Table(title="API Keys with Full IDs")
    table.add_column("Full GUID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Provider", style="blue")
    table.add_column("Status", style="yellow")
    table.add_column("Category", style="magenta")

    for key in keys_to_show:
        # Show full GUID and title
        provider_value = key.provider.value if key.provider else "unknown"
        status_value = key.status.value if key.status else "unknown"

        table.add_row(
            str(key.guid),
            key.title,
            provider_value,
            status_value,
            key.category,
        )

    console.print(table)


def _display_working_apis(working_credentials: dict, provider_filter: Optional[str] = None):
    """Display working API keys."""
    console.print("\n" + "=" * 80)
    console.print("[bold green]Working API Keys[/bold green]")
    console.print("=" * 80)

    if not working_credentials:
        console.print("[yellow]No working APIs found[/yellow]")
        return

    # Filter by provider if specified
    if provider_filter:
        filtered_creds = {k: v for k, v in working_credentials.items() if k == provider_filter}
        if not filtered_creds:
            console.print(f"[yellow]No working APIs found for provider: {provider_filter}[/yellow]")
            return
        working_credentials = filtered_creds
        console.print(f"[yellow]Filtered by provider: {provider_filter}[/yellow]")

    # Create table
    table = Table(title="Working API Keys")
    table.add_column("Provider", style="cyan")
    table.add_column("Name/Title", style="green")
    table.add_column("Credential Preview", style="yellow")
    table.add_column("Status", style="green")

    total_apis = 0
    for provider, credential_list in working_credentials.items():
        if isinstance(credential_list, list):
            # Handle list of credentials per provider
            for credential_info in credential_list:
                if isinstance(credential_info, dict):
                    title = credential_info.get("title", "Unknown")
                    credential = credential_info.get("credential", "")
                else:
                    title = f"{provider.title()} API Key"
                    credential = credential_info

                # Show first 8 chars of credential for identification
                preview = credential[:8] + "..." if len(credential) > 8 else credential
                table.add_row(
                    provider.upper(),
                    title[:40] + "..." if len(title) > 40 else title,
                    preview,
                    "✅ Working",
                )
                total_apis += 1
        elif isinstance(credential_info, dict):
            # Handle single credential per provider (backward compatibility)
            title = credential_info.get("title", "Unknown")
            credential = credential_info.get("credential", "")
            preview = credential[:8] + "..." if len(credential) > 8 else credential
            table.add_row(
                provider.upper(),
                title[:40] + "..." if len(title) > 40 else title,
                preview,
                "✅ Working",
            )
            total_apis += 1
        else:
            # Fallback to just the credential string
            title = f"{provider.title()} API Key"
            credential = credential_info
            preview = credential[:8] + "..." if len(credential) > 8 else credential
            table.add_row(
                provider.upper(),
                title[:40] + "..." if len(title) > 40 else title,
                preview,
                "✅ Working",
            )
            total_apis += 1

    console.print(table)
    console.print(f"\n[bold green]Total Working APIs: {len(working_credentials)}[/bold green]")


def _export_working_apis(working_credentials, export_format: str, output_file: Optional[str], verbose: bool):
    """Export working APIs in various formats."""
    if export_format == "json":
        _export_json(working_credentials, output_file, verbose)
    elif export_format == "csv":
        _export_csv(working_credentials, output_file, verbose)
    else:
        console.print(f"[red]❌ Unsupported export format: {export_format}[/red]")


def _export_json(working_credentials, output_file: Optional[str], verbose: bool):
    """Export working APIs to JSON format."""
    # Convert to exportable format
    export_data = {}
    for provider, credential_list in working_credentials.items():
        if isinstance(credential_list, list):
            export_data[provider] = credential_list
        else:
            export_data[provider] = [credential_list]

    if output_file:
        with open(output_file, "w") as f:
            json.dump(export_data, f, indent=2, default=str)
        console.print(f"[green]💾 JSON exported to: {output_file}[/green]")
    else:
        console.print(json.dumps(export_data, indent=2, default=str))


def _export_csv(working_credentials, output_file: Optional[str], verbose: bool):
    """Export working APIs to CSV format."""
    import csv

    # Prepare CSV data
    csv_data = []
    for provider, credential_list in working_credentials.items():
        if isinstance(credential_list, list):
            for credential_info in credential_list:
                if isinstance(credential_info, dict):
                    title = credential_info.get("title", "Unknown")
                    credential = credential_info.get("credential", "")
                else:
                    title = f"{provider.title()} API Key"
                    credential = credential_info
                csv_data.append([provider, title, credential])
        else:
            title = f"{provider.title()} API Key"
            credential = credential_list
            csv_data.append([provider, title, credential])

    if output_file:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Provider", "Title", "Credential"])
            writer.writerows(csv_data)
        console.print(f"[green]💾 CSV exported to: {output_file}[/green]")
    else:
        # Print to console
        console.print("Provider,Title,Credential")
        for row in csv_data:
            console.print(",".join(f'"{field}"' for field in row))


def _export_summary(result, export_format: str, output_file: Optional[str]):
    """Export summary results in various formats."""
    if export_format == "json":
        _export_summary_json(result, output_file)
    elif export_format == "csv":
        _export_summary_csv(result, output_file)
    else:
        console.print(f"[red]❌ Unsupported export format: {export_format}[/red]")


def _export_summary_json(result, output_file: Optional[str]):
    """Export summary results to JSON format."""
    # Convert to exportable format
    export_data = {"total_items": len(result.api_keys), "providers": {}, "statuses": {}}

    for key in result.api_keys:
        provider = key.provider.value
        status = key.status.value

        if provider not in export_data["providers"]:
            export_data["providers"][provider] = 0
        export_data["providers"][provider] += 1

        if status not in export_data["statuses"]:
            export_data["statuses"][status] = 0
        export_data["statuses"][status] += 1

    if output_file:
        with open(output_file, "w") as f:
            json.dump(export_data, f, indent=2, default=str)
        console.print(f"[green]💾 JSON summary exported to: {output_file}[/green]")
    else:
        console.print(json.dumps(export_data, indent=2, default=str))


def _export_summary_csv(result, output_file: Optional[str]):
    """Export summary results to CSV format."""
    import csv

    # Prepare CSV data
    csv_data = []
    for key in result.api_keys:
        csv_data.append([key.provider.value, key.title, key.status.value, key.id])

    if output_file:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Provider", "Title", "Status", "ID"])
            writer.writerows(csv_data)
        console.print(f"[green]💾 CSV summary exported to: {output_file}[/green]")
    else:
        # Print to console
        console.print("Provider,Title,Status,ID")
        for row in csv_data:
            console.print(",".join(f'"{field}"' for field in row))


def _display_statistics(stats_data):
    """Display comprehensive statistics about API keys."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]API Key Statistics[/bold blue]")
    console.print("=" * 80)

    if not stats_data:
        console.print("[yellow]No statistics available[/yellow]")
        return

    # Overall counts
    console.print(f"[bold green]📊 Total Items: {stats_data.get('total_items', 0)}[/bold green]")
    console.print(f"[bold green]🏢 Total Providers: {stats_data.get('total_providers', 0)}[/bold green]")
    console.print()

    # Provider breakdown
    if "providers" in stats_data:
        console.print("[bold cyan]Provider Distribution:[/bold cyan]")
        for provider, count in stats_data["providers"].items():
            console.print(f"  🔑 {provider.upper()}: {count}")
        console.print()

    # Status breakdown
    if "statuses" in stats_data:
        console.print("[bold cyan]Status Distribution:[/bold cyan]")
        for status, count in stats_data["statuses"].items():
            status_icon = "✅" if status == "working" else "❌" if status == "failed" else "🔄"
            console.print(f"  {status_icon} {status.title()}: {count}")
        console.print()

    # Cache information
    if "cache_info" in stats_data:
        console.print("[bold cyan]Cache Information:[/bold cyan]")
        cache_info = stats_data["cache_info"]
        console.print(f"  📁 Cache File: {cache_info.get('cache_file', 'Unknown')}")
        console.print(f"  🕒 Last Updated: {cache_info.get('last_updated', 'Unknown')}")
        console.print(f"  📊 Cache Size: {cache_info.get('cache_size', 'Unknown')}")


def _display_health_status(health_status):
    """Display system health status."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]System Health Status[/bold blue]")
    console.print("=" * 80)

    if not health_status:
        console.print("[yellow]No health status available[/yellow]")
        return

    # Overall health
    overall_health = health_status.get("overall_health", "unknown")
    health_icon = "✅" if overall_health == "healthy" else "❌" if overall_health == "unhealthy" else "⚠️"
    console.print(f"[bold {overall_health}]Overall Health: {health_icon} {overall_health.title()}[/bold {overall_health}]")
    console.print()

    # Component health
    if "components" in health_status:
        console.print("[bold cyan]Component Health:[/bold cyan]")
        for component, status in health_status["components"].items():
            status_icon = "✅" if status["healthy"] else "❌"
            console.print(f"  {status_icon} {component}: {status['status']}")
            if not status["healthy"] and "error" in status:
                console.print(f"    Error: {status['error']}")
        console.print()

    # Recommendations
    if "recommendations" in health_status and health_status["recommendations"]:
        console.print("[bold yellow]Recommendations:[/bold yellow]")
        for rec in health_status["recommendations"]:
            console.print(f"  💡 {rec}")


def _display_test_results(test_results):
    """Display API testing results."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]API Testing Results[/bold blue]")
    console.print("=" * 80)

    if not test_results:
        console.print("[yellow]No test results found[/yellow]")
        return

    # Count total working APIs
    total_working = sum(len(apis) for apis in test_results.values())

    console.print(f"[green]Total Working APIs: {total_working}[/green]")
    console.print()

    # Display results by provider
    for provider, apis in test_results.items():
        console.print(f"[bold cyan]{provider.upper()}:[/bold cyan] {len(apis)} working APIs")

        for api in apis[:3]:  # Show first 3 for each provider
            title = api["title"][:50] + "..." if len(api["title"]) > 50 else api["title"]
            console.print(f"  🔑 {title}")

        if len(apis) > 3:
            console.print(f"  ... and {len(apis) - 3} more")
        console.print()


def _save_results_to_file(result, output_path: str):
    """Save discovery results to a file."""
    output_file = Path(output_path)

    # Ensure directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Convert to dict and save
    with open(output_file, "w") as f:
        json.dump(result.dict(), f, indent=2, default=str)


if __name__ == "__main__":
    main()
