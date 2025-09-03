#!/usr/bin/env python3
"""
Gmail-to-Calendar System CLI
============================

Command-line interface for the Gmail-to-Calendar system with OAuth setup,
event processing, and audit capabilities.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any

from .orchestrator import GmailCalendarOrchestrator
from .connectors import OAuthConfig
from .models import SourceType


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("gmail_calendar.log")])


def load_config(config_file: str = "gmail_calendar_config.json") -> Dict[str, Any]:
    """Load configuration from file"""
    config_path = Path(config_file)

    if not config_path.exists():
        # Create default config
        default_config = {
            "gmail": {
                "client_id": "YOUR_GMAIL_CLIENT_ID",
                "client_secret": "YOUR_GMAIL_CLIENT_SECRET",
                "redirect_uri": "http://localhost:8080/callback",
                "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
                "token_file": "gmail_token.json",
                "credentials_file": "gmail_credentials.json",
            },
            "calendar": {
                "client_id": "YOUR_CALENDAR_CLIENT_ID",
                "client_secret": "YOUR_CALENDAR_CLIENT_SECRET",
                "redirect_uri": "http://localhost:8080/callback",
                "scopes": ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar.events"],
                "token_file": "calendar_token.json",
                "credentials_file": "calendar_credentials.json",
            },
            "default_timezone": "America/Denver",
            "confidence_threshold": 0.85,
        }

        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)

        print(f"📝 Created default config file: {config_path}")
        print("🔧 Please edit the config file with your OAuth credentials")
        return default_config

    with open(config_path, "r") as f:
        return json.load(f)


async def setup_oauth(config: Dict[str, Any]) -> None:
    """Setup OAuth credentials for Gmail and Calendar"""
    print("🔐 Setting up OAuth credentials...")

    # Gmail OAuth setup
    gmail_config = OAuthConfig(**config["gmail"])
    gmail_connector = GmailConnector(gmail_config)

    print("📧 Setting up Gmail access...")
    if await gmail_connector.authenticate():
        print("✅ Gmail authentication successful")
    else:
        print("❌ Gmail authentication failed")
        return

    # Calendar OAuth setup
    calendar_config = OAuthConfig(**config["calendar"])
    calendar_connector = CalendarConnector(calendar_config)

    print("📅 Setting up Calendar access...")
    if await calendar_connector.authenticate():
        print("✅ Calendar authentication successful")
    else:
        print("❌ Calendar authentication failed")
        return

    print("🎉 OAuth setup complete!")


async def process_email_request(query: str, config: Dict[str, Any], user_id: str = "cli_user") -> None:
    """Process an email-to-calendar request"""
    print(f"🎯 Processing request: {query}")

    # Create OAuth configs
    gmail_config = OAuthConfig(**config["gmail"])
    calendar_config = OAuthConfig(**config["calendar"])

    # Create orchestrator
    orchestrator = GmailCalendarOrchestrator(
        gmail_config=gmail_config, calendar_config=calendar_config, default_timezone=config.get("default_timezone", "America/Denver"), confidence_threshold=config.get("confidence_threshold", 0.85)
    )

    # Process request
    result = await orchestrator.process_request(query, user_id)

    # Display results
    if result["success"]:
        print("✅ Event created successfully!")
        print(f"📅 Event ID: {result['event_id']}")
        print(f"🔗 Event Link: {result['event_link']}")
    else:
        print("❌ Event creation failed")
        print(f"Error: {result['error_message']}")

    # Show audit logs
    if result.get("audit_logs"):
        print("\n📋 Audit Logs:")
        for log in result["audit_logs"]:
            print(f"  {log['timestamp']} - {log['action']} - {'✅' if log['success'] else '❌'}")


async def test_system(config: Dict[str, Any]) -> None:
    """Test the system with sample data"""
    print("🧪 Testing Gmail-to-Calendar system...")

    # Test queries
    test_queries = ["put Megan's meeting on my calendar", "add the probate call to my calendar", "schedule the meeting with Jury & Robinson"]

    for query in test_queries:
        print(f"\n🔍 Testing: {query}")
        await process_email_request(query, config, "test_user")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Gmail-to-Calendar System - Protocol-Driven Design")

    parser.add_argument("--config", default="gmail_calendar_config.json", help="Configuration file path")

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup OAuth credentials")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process email-to-calendar request")
    process_parser.add_argument("query", help="User query (e.g., 'put Megan's meeting on my calendar')")
    process_parser.add_argument("--user-id", default="cli_user", help="User ID for audit logging")

    # Test command
    test_parser = subparsers.add_parser("test", help="Test the system with sample data")

    # MCP command
    mcp_parser = subparsers.add_parser("mcp", help="Run as MCP server")
    mcp_parser.add_argument("--port", type=int, default=8080, help="MCP server port")

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Load configuration
    config = load_config(args.config)

    if args.command == "setup":
        asyncio.run(setup_oauth(config))

    elif args.command == "process":
        asyncio.run(process_email_request(args.query, config, args.user_id))

    elif args.command == "test":
        asyncio.run(test_system(config))

    elif args.command == "mcp":
        print("🚀 Starting MCP server...")
        # MCP server implementation would go here
        print("MCP server not implemented yet")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
