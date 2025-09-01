"""
Cache Manager CLI

This module provides the command-line interface for cache management operations.
"""

from pathlib import Path
from typing import Optional

import click

from .core import CacheManager
from .models import CacheConfig, CacheFormat


@click.group()
@click.option(
    "--cache-dir",
    type=click.Path(path_type=Path),
    default=Path.cwd(),
    help="Cache directory",
)
@click.option("--format", type=click.Choice(["json", "yaml"]), default="json", help="Cache format")
@click.option("--ttl-hours", type=int, default=24, help="Time to live in hours")
@click.option("--max-size-mb", type=int, default=100, help="Maximum cache size in MB")
@click.pass_context
def cli(ctx, cache_dir: Path, format: str, ttl_hours: int, max_size_mb: int):
    """Cache Manager - Manage cache operations independently."""
    # Create cache config
    config = CacheConfig(
        cache_dir=cache_dir,
        format=CacheFormat(format),
        ttl_hours=ttl_hours,
        max_size_mb=max_size_mb,
    )

    # Create cache manager
    ctx.obj = CacheManager(config)


@cli.command()
@click.argument("cache_key")
@click.argument("data_file", type=click.Path(exists=True, path_type=Path))
@click.pass_obj
def load(cache_manager: CacheManager, cache_key: str, data_file: Path):
    """Load data into cache from a file."""
    try:
        # Read data file
        if data_file.suffix == ".json":
            import json

            with open(data_file) as f:
                data = json.load(f)
        elif data_file.suffix in [".yaml", ".yml"]:
            import yaml

            with open(data_file) as f:
                data = yaml.safe_load(f)
        else:
            click.echo(f"❌ Unsupported file format: {data_file.suffix}")
            return

        # Save to cache
        success = cache_manager.save_cache(cache_key, data)
        if success:
            click.echo(f"✅ Successfully loaded '{cache_key}' into cache")
        else:
            click.echo(f"❌ Failed to load '{cache_key}' into cache")

    except Exception as e:
        click.echo(f"❌ Error loading cache: {e}")


@cli.command()
@click.argument("cache_key")
@click.pass_obj
def get(cache_manager: CacheManager, cache_key: str):
    """Get data from cache."""
    try:
        data = cache_manager.load_cache(cache_key)
        if data is not None:
            click.echo(f"✅ Cache hit for '{cache_key}'")
            click.echo(f"📊 Data type: {type(data).__name__}")
            if isinstance(data, dict):
                click.echo(f"📊 Keys: {list(data.keys())}")
            elif isinstance(data, list):
                click.echo(f"📊 Items: {len(data)}")
        else:
            click.echo(f"❌ Cache miss for '{cache_key}'")

    except Exception as e:
        click.echo(f"❌ Error getting cache: {e}")


@cli.command()
@click.argument("cache_key")
@click.pass_obj
def validate(cache_manager: CacheManager, cache_key: str):
    """Validate cache integrity and health."""
    try:
        health = cache_manager.validate_cache(cache_key)

        click.echo(f"🔍 Cache Health for '{cache_key}':")
        click.echo(f"   Status: {health.status.value}")
        click.echo(f"   Performance Score: {health.performance_score:.2f}")
        click.echo(f"   Integrity Score: {health.integrity_score:.2f}")
        click.echo(f"   Maintenance Needed: {health.maintenance_needed}")

        if health.issues:
            click.echo(f"   Issues:")
            for issue in health.issues:
                click.echo(f"     ❌ {issue}")

        if health.recommendations:
            click.echo(f"   Recommendations:")
            for rec in health.recommendations:
                click.echo(f"     💡 {rec}")

    except Exception as e:
        click.echo(f"❌ Error validating cache: {e}")


@cli.command()
@click.argument("cache_key")
@click.pass_obj
def repair(cache_manager: CacheManager, cache_key: str):
    """Attempt to repair corrupted cache."""
    try:
        click.echo(f"🔧 Attempting to repair cache '{cache_key}'...")
        success = cache_manager.repair_cache(cache_key)

        if success:
            click.echo(f"✅ Successfully repaired cache '{cache_key}'")
        else:
            click.echo(f"❌ Failed to repair cache '{cache_key}'")

    except Exception as e:
        click.echo(f"❌ Error repairing cache: {e}")


@cli.command()
@click.option("--cache-key", help="Specific cache key to clear")
@click.pass_obj
def clear(cache_manager: CacheManager, cache_key: Optional[str]):
    """Clear cache data."""
    try:
        if cache_key:
            click.echo(f"🗑️  Clearing cache key '{cache_key}'...")
        else:
            click.echo("🗑️  Clearing all cache data...")

        success = cache_manager.clear_cache(cache_key)

        if success:
            click.echo("✅ Cache cleared successfully")
        else:
            click.echo("❌ Failed to clear cache")

    except Exception as e:
        click.echo(f"❌ Error clearing cache: {e}")


@cli.command()
@click.pass_obj
def stats(cache_manager: CacheManager):
    """Show cache performance statistics."""
    try:
        stats = cache_manager.get_stats()

        click.echo("📊 Cache Statistics:")
        click.echo(f"   Total Entries: {stats.total_entries}")
        click.echo(f"   Total Size: {stats.total_size_bytes / 1024:.2f} KB")
        click.echo(f"   Hit Count: {stats.hit_count}")
        click.echo(f"   Miss Count: {stats.miss_count}")
        click.echo(f"   Hit Rate: {stats.hit_rate:.2%}")
        click.echo(f"   Avg Load Time: {stats.avg_load_time_ms:.2f} ms")
        click.echo(f"   Avg Save Time: {stats.avg_save_time_ms:.2f} ms")
        click.echo(f"   Corruption Count: {stats.corruption_count}")

        if stats.last_cleanup:
            click.echo(f"   Last Cleanup: {stats.last_cleanup}")

    except Exception as e:
        click.echo(f"❌ Error getting stats: {e}")


@cli.command()
@click.argument("cache_key")
@click.option("--output", type=click.Path(path_type=Path), help="Output file path")
@click.pass_obj
def export(cache_manager: CacheManager, cache_key: str, output: Optional[Path]):
    """Export cache data to a file."""
    try:
        data = cache_manager.load_cache(cache_key)
        if data is None:
            click.echo(f"❌ Cache key '{cache_key}' not found")
            return

        # Determine output format and path
        if output is None:
            output = Path(f"{cache_key}_export.{cache_manager.config.format.value}")

        # Export based on format
        if cache_manager.config.format == CacheFormat.JSON:
            import json

            with open(output, "w") as f:
                json.dump(data, f, indent=2, default=str)
        elif cache_manager.config.format == CacheFormat.YAML:
            import yaml

            with open(output, "w") as f:
                yaml.dump(data, f, default_flow_style=False)

        click.echo(f"✅ Exported cache '{cache_key}' to {output}")

    except Exception as e:
        click.echo(f"❌ Error exporting cache: {e}")


@cli.command()
@click.argument("cache_key")
@click.option("--backup/--no-backup", default=True, help="Create backup before migration")
@click.pass_obj
def migrate(cache_manager: CacheManager, cache_key: str, backup: bool):
    """Migrate cache to a different format."""
    try:
        click.echo(f"🔄 Migrating cache '{cache_key}'...")

        # Load current data
        data = cache_manager.load_cache(cache_key)
        if data is None:
            click.echo(f"❌ Cache key '{cache_key}' not found")
            return

        # Create backup if requested
        if backup:
            backup_path = Path(f"{cache_key}_backup.{cache_manager.config.format.value}")
            if cache_manager.config.format == CacheFormat.JSON:
                import json

                with open(backup_path, "w") as f:
                    json.dump(data, f, indent=2, default=str)
            elif cache_manager.config.format == CacheFormat.YAML:
                import yaml

                with open(backup_path, "w") as f:
                    yaml.dump(data, f, default_flow_style=False)
            click.echo(f"💾 Backup created at {backup_path}")

        # Save in new format
        success = cache_manager.save_cache(cache_key, data)
        if success:
            click.echo(f"✅ Successfully migrated cache '{cache_key}'")
        else:
            click.echo(f"❌ Failed to migrate cache '{cache_key}'")

    except Exception as e:
        click.echo(f"❌ Error migrating cache: {e}")


if __name__ == "__main__":
    cli()
