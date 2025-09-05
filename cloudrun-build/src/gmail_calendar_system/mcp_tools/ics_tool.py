"""
MCP Tool: ICS Parser
===================

Provides MCP-compatible interface for ICS (iCalendar) parsing and generation
with RFC 5545 compliance.
"""

import json
import logging
from typing import Any, Dict, List, Optional
import base64

from ..parsers import ICSParser


class ICSMCPTool:
    """
    MCP tool for ICS parsing and generation.

    Provides the following MCP functions:
    - ics.parse
    - ics.generate
    - ics.validate
    """

    def __init__(self):
        self.parser = ICSParser()
        self.logger = logging.getLogger(__name__)

    async def parse(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse ICS content and extract event information.

        Args:
            source: Source type ("inline" or "attachment")
            content_base64: ICS content as base64 encoded string
            content: ICS content as plain text (alternative to content_base64)

        Returns:
            Parsed event data or null if parsing fails
        """
        try:
            source = args.get("source", "inline")
            content_base64 = args.get("content_base64")
            content = args.get("content")

            # Decode content if base64 encoded
            if content_base64:
                content = base64.b64decode(content_base64).decode("utf-8")

            if not content:
                return {"error": "content or content_base64 parameter is required"}

            # Parse ICS content
            event_data = self.parser.parse(content, source)

            if event_data:
                return {"success": True, "event_data": event_data, "source": source}
            else:
                return {"success": False, "error": "No valid event found in ICS content", "source": source}

        except Exception as e:
            self.logger.error(f"❌ ICS parsing failed: {e}")
            return {"success": False, "error": str(e), "source": args.get("source", "inline")}

    async def generate(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate ICS content from event data.

        Args:
            summary: Event title
            description: Event description
            location: Event location
            start_iso: Start time in ISO format
            end_iso: End time in ISO format
            attendees: List of attendee email addresses
            uid: Unique identifier for the event

        Returns:
            Generated ICS content as base64 encoded string
        """
        try:
            # Validate required fields
            required_fields = ["summary", "start_iso", "end_iso"]
            for field in required_fields:
                if field not in args:
                    return {"error": f"Missing required field: {field}"}

            # Generate ICS content
            ics_content = self._generate_ics_content(args)

            # Encode as base64 for JSON transport
            content_b64 = base64.b64encode(ics_content.encode("utf-8")).decode("utf-8")

            return {"success": True, "content_base64": content_b64, "size": len(ics_content)}

        except Exception as e:
            self.logger.error(f"❌ ICS generation failed: {e}")
            return {"success": False, "error": str(e)}

    async def validate(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate ICS content for RFC 5545 compliance.

        Args:
            content_base64: ICS content as base64 encoded string
            content: ICS content as plain text (alternative to content_base64)

        Returns:
            Validation result with errors and warnings
        """
        try:
            content_base64 = args.get("content_base64")
            content = args.get("content")

            # Decode content if base64 encoded
            if content_base64:
                content = base64.b64decode(content_base64).decode("utf-8")

            if not content:
                return {"error": "content or content_base64 parameter is required"}

            # Validate ICS content
            validation_result = self._validate_ics_content(content)

            return {"success": True, "valid": validation_result["valid"], "errors": validation_result["errors"], "warnings": validation_result["warnings"]}

        except Exception as e:
            self.logger.error(f"❌ ICS validation failed: {e}")
            return {"success": False, "error": str(e)}

    def _generate_ics_content(self, event_data: Dict[str, Any]) -> str:
        """Generate ICS content from event data"""
        from datetime import datetime
        import uuid

        # Generate UID if not provided
        uid = event_data.get("uid", str(uuid.uuid4()))

        # Parse dates
        start_dt = datetime.fromisoformat(event_data["start_iso"].replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(event_data["end_iso"].replace("Z", "+00:00"))

        # Format dates for ICS
        start_ics = start_dt.strftime("%Y%m%dT%H%M%SZ")
        end_ics = end_dt.strftime("%Y%m%dT%H%M%SZ")
        now_ics = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        # Build ICS content
        ics_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Gmail Calendar System//EN",
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART:{start_ics}",
            f"DTEND:{end_ics}",
            f"DTSTAMP:{now_ics}",
            f"SUMMARY:{event_data['summary']}",
        ]

        if event_data.get("description"):
            ics_lines.append(f"DESCRIPTION:{event_data['description']}")

        if event_data.get("location"):
            ics_lines.append(f"LOCATION:{event_data['location']}")

        # Add attendees
        for attendee in event_data.get("attendees", []):
            ics_lines.append(f"ATTENDEE:mailto:{attendee}")

        ics_lines.extend(["END:VEVENT", "END:VCALENDAR"])

        return "\r\n".join(ics_lines)

    def _validate_ics_content(self, content: str) -> Dict[str, Any]:
        """Validate ICS content for RFC 5545 compliance"""
        errors = []
        warnings = []

        try:
            # Basic structure validation
            if "BEGIN:VCALENDAR" not in content:
                errors.append("Missing BEGIN:VCALENDAR")

            if "END:VCALENDAR" not in content:
                errors.append("Missing END:VCALENDAR")

            if "BEGIN:VEVENT" not in content:
                errors.append("Missing BEGIN:VEVENT")

            if "END:VEVENT" not in content:
                errors.append("Missing END:VEVENT")

            # Check for required VEVENT properties
            if "UID:" not in content:
                errors.append("Missing UID property")

            if "DTSTART:" not in content:
                errors.append("Missing DTSTART property")

            if "DTEND:" not in content and "DURATION:" not in content:
                errors.append("Missing DTEND or DURATION property")

            # Check for line ending compliance (should be CRLF)
            if "\r\n" not in content and "\n" in content:
                warnings.append("Line endings should be CRLF (\\r\\n) for RFC 5545 compliance")

            # Try to parse with icalendar library for deeper validation
            try:
                from icalendar import Calendar

                Calendar.from_ical(content)
            except Exception as parse_error:
                errors.append(f"Parsing error: {str(parse_error)}")

        except Exception as e:
            errors.append(f"Validation error: {str(e)}")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


# MCP Tool Manifest
ICS_MANIFEST = {
    "name": "ics",
    "version": "1.0.0",
    "description": "ICS (iCalendar) parser and generator with RFC 5545 compliance",
    "functions": [
        {
            "name": "parse",
            "description": "Parse ICS content and extract event information",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "enum": ["inline", "attachment"], "description": "Source type", "default": "inline"},
                    "content_base64": {"type": "string", "description": "ICS content as base64 encoded string"},
                    "content": {"type": "string", "description": "ICS content as plain text (alternative to content_base64)"},
                },
                "required": [],
            },
        },
        {
            "name": "generate",
            "description": "Generate ICS content from event data",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "Event title", "maxLength": 180},
                    "description": {"type": "string", "description": "Event description"},
                    "location": {"type": "string", "description": "Event location"},
                    "start_iso": {"type": "string", "format": "date-time", "description": "Start time in ISO format"},
                    "end_iso": {"type": "string", "format": "date-time", "description": "End time in ISO format"},
                    "attendees": {"type": "array", "items": {"type": "string", "format": "email"}, "description": "List of attendee email addresses"},
                    "uid": {"type": "string", "description": "Unique identifier for the event"},
                },
                "required": ["summary", "start_iso", "end_iso"],
            },
        },
        {
            "name": "validate",
            "description": "Validate ICS content for RFC 5545 compliance",
            "parameters": {
                "type": "object",
                "properties": {
                    "content_base64": {"type": "string", "description": "ICS content as base64 encoded string"},
                    "content": {"type": "string", "description": "ICS content as plain text (alternative to content_base64)"},
                },
                "required": [],
            },
        },
    ],
}
