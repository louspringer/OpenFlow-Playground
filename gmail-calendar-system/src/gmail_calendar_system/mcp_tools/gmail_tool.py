"""
MCP Tool: Gmail
===============

Provides MCP-compatible interface for Gmail operations including
message search, thread reading, and attachment handling.
"""

import json
import logging
from typing import Any, Dict, List, Optional
import base64

from ..connectors import GmailConnector, OAuthConfig


class GmailMCPTool:
    """
    MCP tool for Gmail operations.

    Provides the following MCP functions:
    - gmail.search_messages
    - gmail.read_thread
    - gmail.get_message
    - gmail.get_attachments
    - gmail.download_attachment
    """

    def __init__(self, config: OAuthConfig):
        self.connector = GmailConnector(config)
        self.logger = logging.getLogger(__name__)

    async def search_messages(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search Gmail messages using Gmail search syntax.

        Args:
            query: Gmail search query (e.g., "from:megan subject:meeting newer_than:30d")
            max_results: Maximum number of results to return

        Returns:
            List of message metadata dictionaries
        """
        try:
            query = args.get("query", "")
            max_results = args.get("max_results", 25)

            if not query:
                return {"error": "query parameter is required", "messages": []}

            # Search for messages
            messages = await self.connector.search_messages(query, max_results)

            return {"success": True, "messages": messages, "count": len(messages), "query": query}

        except Exception as e:
            self.logger.error(f"❌ Gmail search failed: {e}")
            return {"success": False, "error": str(e), "messages": []}

    async def read_thread(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read a complete email thread.

        Args:
            thread_id: Gmail thread ID

        Returns:
            Thread data with messages and metadata
        """
        try:
            thread_id = args.get("thread_id")

            if not thread_id:
                return {"error": "thread_id parameter is required"}

            # Read thread
            thread_data = await self.connector.read_thread(thread_id)

            if not thread_data:
                return {"error": "Thread not found or could not be read"}

            return {"success": True, "thread_data": thread_data, "thread_id": thread_id}

        except Exception as e:
            self.logger.error(f"❌ Thread reading failed: {e}")
            return {"success": False, "error": str(e)}

    async def get_message(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a specific message by ID.

        Args:
            message_id: Gmail message ID

        Returns:
            Message data with headers and body
        """
        try:
            message_id = args.get("message_id")

            if not message_id:
                return {"error": "message_id parameter is required"}

            # Get message
            message_data = await self.connector.get_message(message_id)

            if not message_data:
                return {"error": "Message not found or could not be read"}

            return {"success": True, "message_data": message_data, "message_id": message_id}

        except Exception as e:
            self.logger.error(f"❌ Message retrieval failed: {e}")
            return {"success": False, "error": str(e)}

    async def get_attachments(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get attachments from a message.

        Args:
            message_id: Gmail message ID

        Returns:
            List of attachment metadata
        """
        try:
            message_id = args.get("message_id")

            if not message_id:
                return {"error": "message_id parameter is required", "attachments": []}

            # Get attachments
            attachments = await self.connector.get_attachments(message_id)

            return {"success": True, "attachments": attachments, "count": len(attachments), "message_id": message_id}

        except Exception as e:
            self.logger.error(f"❌ Attachment listing failed: {e}")
            return {"success": False, "error": str(e), "attachments": []}

    async def download_attachment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Download an attachment.

        Args:
            message_id: Gmail message ID
            attachment_id: Attachment ID

        Returns:
            Attachment content as base64 encoded string
        """
        try:
            message_id = args.get("message_id")
            attachment_id = args.get("attachment_id")

            if not message_id or not attachment_id:
                return {"error": "message_id and attachment_id parameters are required"}

            # Download attachment
            content = await self.connector.download_attachment(message_id, attachment_id)

            if not content:
                return {"error": "Attachment not found or could not be downloaded"}

            # Encode as base64 for JSON transport
            content_b64 = base64.b64encode(content).decode("utf-8")

            return {"success": True, "content_base64": content_b64, "size": len(content), "message_id": message_id, "attachment_id": attachment_id}

        except Exception as e:
            self.logger.error(f"❌ Attachment download failed: {e}")
            return {"success": False, "error": str(e)}


# MCP Tool Manifest
GMAIL_MANIFEST = {
    "name": "gmail",
    "version": "1.0.0",
    "description": "Gmail integration for email processing and attachment handling",
    "functions": [
        {
            "name": "search_messages",
            "description": "Search Gmail messages using Gmail search syntax",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Gmail search query (e.g., 'from:megan subject:meeting newer_than:30d')"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return", "default": 25, "minimum": 1, "maximum": 100},
                },
                "required": ["query"],
            },
        },
        {
            "name": "read_thread",
            "description": "Read a complete email thread",
            "parameters": {"type": "object", "properties": {"thread_id": {"type": "string", "description": "Gmail thread ID"}}, "required": ["thread_id"]},
        },
        {
            "name": "get_message",
            "description": "Get a specific message by ID",
            "parameters": {"type": "object", "properties": {"message_id": {"type": "string", "description": "Gmail message ID"}}, "required": ["message_id"]},
        },
        {
            "name": "get_attachments",
            "description": "Get attachments from a message",
            "parameters": {"type": "object", "properties": {"message_id": {"type": "string", "description": "Gmail message ID"}}, "required": ["message_id"]},
        },
        {
            "name": "download_attachment",
            "description": "Download an attachment",
            "parameters": {
                "type": "object",
                "properties": {"message_id": {"type": "string", "description": "Gmail message ID"}, "attachment_id": {"type": "string", "description": "Attachment ID"}},
                "required": ["message_id", "attachment_id"],
            },
        },
    ],
}
