"""
Command-line interface for OP API Manager.

This module provides a Click-based CLI for discovering and managing
API keys stored in 1Password.
"""

import json
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
@click.option(
    "--force-refresh", "-f", is_flag=True, help="Force refresh even if cache is valid"
)
@click.option(
    "--output", "-o", type=click.Path(), help="Output file for discovery results"
)
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def discover(force_refresh: bool, output: Optional[str], cache_file: Optional[str]):
    """
    Discover all potential API keys from 1Password.

    This command will scan your 1Password vault for items that appear to be
    API keys, organize them into logical groups, and assign unique GUIDs.
    """
    try:
        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        manager = OnePasswordAPIKeyManager(cache_config)

        # Perform discovery
        with console.status("[bold green]Discovering API keys..."):
            result = manager.discover_api_keys(force_refresh=force_refresh)

        # Display results
        _display_discovery_results(result)

        # Save to file if requested
        if output:
            _save_results_to_file(result, output)
            console.print(f"\n[green]Results saved to: {output}")

    except Exception as e:
        console.print(f"[red]Error during discovery: {e}")
        raise click.Abort() from e


@main.command()
@click.option(
    "--provider",
    "-p",
    type=click.Choice([p.value for p in ProviderType]),
    help="Filter by specific provider",
)
@click.option(
    "--status",
    "-s",
    type=click.Choice(["discovered", "tested", "working", "failed", "expired"]),
    help="Filter by status",
)
@click.option("--cache-file", type=click.Path(), help="Custom cache file location")
def summary(provider: Optional[str], status: Optional[str], cache_file: Optional[str]):
    """
    Show summary of discovered API keys.

    Display a summary of all discovered API keys with filtering options
    for provider and status.
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

        # Apply filters
        if provider:
            result.api_keys = [
                k for k in result.api_keys if k.provider.value == provider
            ]

        if status:
            result.api_keys = [k for k in result.api_keys if k.status.value == status]

        # Display summary
        _display_summary(result)

    except Exception as e:
        console.print(f"[red]Error displaying summary: {e}")
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


def _display_discovery_results(result):
    """Display discovery results in a rich format."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]API Key Discovery Results[/bold blue]")
    console.print("=" * 80)

    # Summary
    summary_text = Text()
    summary_text.append(f"Total Items: {result.total_items}\n", style="bold")
    summary_text.append(f"API Keys Found: {len(result.api_keys)}\n", style="bold")
    summary_text.append(
        f"Credential Pairs: {len(result.credential_pairs)}\n", style="bold"
    )
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
            primary_title = (
                pair.primary.title[:30] + "..."
                if len(pair.primary.title) > 30
                else pair.primary.title
            )
            secondary_title = (
                pair.secondary.title[:30] + "..."
                if pair.secondary and len(pair.secondary.title) > 30
                else (pair.secondary.title if pair.secondary else "None")
            )
            description = (
                pair.description[:40] + "..."
                if pair.description and len(pair.description) > 40
                else (pair.description or "")
            )

            pairs_table.add_row(
                pair.pair_type, primary_title, secondary_title, description
            )

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
            str(key.guid)[:8] + "...",
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
        status_text.append(
            f"Max Age: {cache_status['max_age_hours']} hours\n", style="white"
        )
        status_text.append(
            f"Last Discovery: {cache_status['last_discovery']}\n", style="white"
        )
    elif cache_status["status"] == "expired":
        status_text.append("Cache is expired\n", style="red")
        status_text.append(f"Age: {cache_status['age_hours']} hours\n", style="white")
        status_text.append(
            f"Max Age: {cache_status['max_age_hours']} hours\n", style="white"
        )
        status_text.append(
            f"Last Discovery: {cache_status['last_discovery']}\n", style="white"
        )
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
