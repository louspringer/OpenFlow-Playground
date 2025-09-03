#!/usr/bin/env python3
"""
MCP Server for Gmail-to-Calendar System
=======================================

Provides MCP server interface for the complete Gmail-to-Calendar system
with all tools and orchestration capabilities.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.gmail_calendar_system.orchestrator import GmailCalendarOrchestrator
from src.gmail_calendar_system.connectors import OAuthConfig
from src.gmail_calendar_system.mcp_tools.google_calendar_tool import GoogleCalendarMCPTool
from src.gmail_calendar_system.mcp_tools.gmail_tool import GmailMCPTool
from src.gmail_calendar_system.mcp_tools.ics_tool import ICSMCPTool


class GmailCalendarMCPServer:
    """
    MCP Server for Gmail-to-Calendar System.

    Provides all tools and orchestration capabilities through MCP interface.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        # Load configuration from environment
        self.config = self.load_config_from_env()

        # Initialize connectors and tools
        self.setup_connectors()
        self.setup_tools()
        self.setup_orchestrator()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def load_config_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        return {
            "gmail": {
                "client_id": os.getenv("GMAIL_CLIENT_ID", ""),
                "client_secret": os.getenv("GMAIL_CLIENT_SECRET", ""),
                "redirect_uri": os.getenv("GMAIL_REDIRECT_URI", "http://localhost:8080/callback"),
                "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
                "token_file": "gmail_token.json",
                "credentials_file": "gmail_credentials.json",
            },
            "calendar": {
                "client_id": os.getenv("CALENDAR_CLIENT_ID", ""),
                "client_secret": os.getenv("CALENDAR_CLIENT_SECRET", ""),
                "redirect_uri": os.getenv("CALENDAR_REDIRECT_URI", "http://localhost:8080/callback"),
                "scopes": ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar.events"],
                "token_file": "calendar_token.json",
                "credentials_file": "calendar_credentials.json",
            },
            "default_timezone": os.getenv("DEFAULT_TIMEZONE", "America/Denver"),
            "confidence_threshold": float(os.getenv("CONFIDENCE_THRESHOLD", "0.85")),
        }

    def setup_connectors(self):
        """Setup OAuth connectors"""
        self.gmail_config = OAuthConfig(**self.config["gmail"])
        self.calendar_config = OAuthConfig(**self.config["calendar"])

    def setup_tools(self):
        """Setup MCP tools"""
        self.gmail_tool = GmailMCPTool(self.gmail_config)
        self.calendar_tool = GoogleCalendarMCPTool(self.calendar_config)
        self.ics_tool = ICSMCPTool()

    def setup_orchestrator(self):
        """Setup orchestrator"""
        self.orchestrator = GmailCalendarOrchestrator(
            gmail_config=self.gmail_config, calendar_config=self.calendar_config, default_timezone=self.config["default_timezone"], confidence_threshold=self.config["confidence_threshold"]
        )

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle MCP request and route to appropriate tool or orchestrator.

        Args:
            request: MCP request dictionary

        Returns:
            Response dictionary
        """
        try:
            method = request.get("method")
            params = request.get("params", {})

            if method == "tools/list":
                return await self.list_tools()

            elif method == "tools/call":
                return await self.call_tool(params)

            elif method == "orchestrator/process":
                return await self.process_orchestration(params)

            else:
                return {"error": {"code": -32601, "message": f"Method not found: {method}"}}

        except Exception as e:
            self.logger.error(f"❌ Request handling failed: {e}")
            return {"error": {"code": -32603, "message": f"Internal error: {str(e)}"}}

    async def list_tools(self) -> Dict[str, Any]:
        """List all available tools"""
        return {
            "tools": [
                {
                    "name": "gmail.search_messages",
                    "description": "Search Gmail messages using Gmail search syntax",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"query": {"type": "string", "description": "Gmail search query"}, "max_results": {"type": "integer", "description": "Maximum results", "default": 25}},
                        "required": ["query"],
                    },
                },
                {
                    "name": "gmail.read_thread",
                    "description": "Read a complete email thread",
                    "inputSchema": {"type": "object", "properties": {"thread_id": {"type": "string", "description": "Gmail thread ID"}}, "required": ["thread_id"]},
                },
                {
                    "name": "calendar.find_conflicts",
                    "description": "Find conflicting events in a time range",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "start_iso": {"type": "string", "format": "date-time", "description": "Start time"},
                            "end_iso": {"type": "string", "format": "date-time", "description": "End time"},
                            "calendar_id": {"type": "string", "description": "Calendar ID", "default": "primary"},
                        },
                        "required": ["start_iso", "end_iso"],
                    },
                },
                {
                    "name": "calendar.create_or_update_event",
                    "description": "Create or update a calendar event with idempotency",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string", "description": "Event title"},
                            "start": {"type": "object", "description": "Start time object"},
                            "end": {"type": "object", "description": "End time object"},
                            "attendees": {"type": "array", "items": {"type": "string"}, "description": "Attendee emails"},
                            "idempotency_key": {"type": "string", "description": "Idempotency key"},
                        },
                        "required": ["summary", "start", "end"],
                    },
                },
                {
                    "name": "ics.parse",
                    "description": "Parse ICS content and extract event information",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "enum": ["inline", "attachment"], "default": "inline"},
                            "content_base64": {"type": "string", "description": "ICS content as base64"},
                            "content": {"type": "string", "description": "ICS content as text"},
                        },
                    },
                },
                {
                    "name": "orchestrator.process_request",
                    "description": "Process a complete email-to-calendar request",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"user_query": {"type": "string", "description": "User's request"}, "user_id": {"type": "string", "description": "User ID", "default": "mcp_user"}},
                        "required": ["user_query"],
                    },
                },
            ]
        }

    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "gmail.search_messages":
                return await self.gmail_tool.search_messages(arguments)

            elif tool_name == "gmail.read_thread":
                return await self.gmail_tool.read_thread(arguments)

            elif tool_name == "gmail.get_message":
                return await self.gmail_tool.get_message(arguments)

            elif tool_name == "gmail.get_attachments":
                return await self.gmail_tool.get_attachments(arguments)

            elif tool_name == "gmail.download_attachment":
                return await self.gmail_tool.download_attachment(arguments)

            elif tool_name == "calendar.find_conflicts":
                return await self.calendar_tool.find_conflicts(arguments)

            elif tool_name == "calendar.create_or_update_event":
                return await self.calendar_tool.create_or_update_event(arguments)

            elif tool_name == "calendar.list_events":
                return await self.calendar_tool.list_events(arguments)

            elif tool_name == "calendar.get_event":
                return await self.calendar_tool.get_event(arguments)

            elif tool_name == "calendar.delete_event":
                return await self.calendar_tool.delete_event(arguments)

            elif tool_name == "ics.parse":
                return await self.ics_tool.parse(arguments)

            elif tool_name == "ics.generate":
                return await self.ics_tool.generate(arguments)

            elif tool_name == "ics.validate":
                return await self.ics_tool.validate(arguments)

            else:
                return {"error": {"code": -32601, "message": f"Tool not found: {tool_name}"}}

        except Exception as e:
            self.logger.error(f"❌ Tool call failed for {tool_name}: {e}")
            return {"error": {"code": -32603, "message": f"Tool execution error: {str(e)}"}}

    async def process_orchestration(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process a complete orchestration request"""
        user_query = params.get("user_query")
        user_id = params.get("user_id", "mcp_user")

        if not user_query:
            return {"error": {"code": -32602, "message": "user_query parameter is required"}}

        try:
            result = await self.orchestrator.process_request(user_query, user_id)
            return {"success": True, "result": result}

        except Exception as e:
            self.logger.error(f"❌ Orchestration failed: {e}")
            return {"error": {"code": -32603, "message": f"Orchestration error: {str(e)}"}}


async def main():
    """Main entry point for MCP server"""
    server = GmailCalendarMCPServer()

    # Simple JSON-RPC over stdin/stdout
    while True:
        try:
            # Read request from stdin
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break

            request = json.loads(line.strip())

            # Handle request
            response = await server.handle_request(request)

            # Send response to stdout
            print(json.dumps(response))
            sys.stdout.flush()

        except json.JSONDecodeError as e:
            error_response = {"error": {"code": -32700, "message": f"Parse error: {str(e)}"}}
            print(json.dumps(error_response))
            sys.stdout.flush()

        except Exception as e:
            error_response = {"error": {"code": -32603, "message": f"Internal error: {str(e)}"}}
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
