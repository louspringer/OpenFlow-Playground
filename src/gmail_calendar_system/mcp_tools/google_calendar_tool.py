"""
MCP Tool: Google Calendar
========================

Provides MCP-compatible interface for Google Calendar operations including
event creation, conflict detection, and calendar management.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..connectors import CalendarConnector, OAuthConfig
from ..models import EventCandidate, ConflictInfo


class GoogleCalendarMCPTool:
    """
    MCP tool for Google Calendar operations.

    Provides the following MCP functions:
    - calendar.find_conflicts
    - calendar.create_or_update_event
    - calendar.list_events
    - calendar.get_event
    - calendar.delete_event
    """

    def __init__(self, config: OAuthConfig):
        self.connector = CalendarConnector(config)
        self.logger = logging.getLogger(__name__)

    async def find_conflicts(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find conflicting events in the specified time range.

        Args:
            start_iso: Start time in ISO format
            end_iso: End time in ISO format
            calendar_id: Calendar ID (default: 'primary')

        Returns:
            Conflict information with suggested alternatives
        """
        try:
            start_iso = args.get("start_iso")
            end_iso = args.get("end_iso")
            calendar_id = args.get("calendar_id", "primary")

            if not start_iso or not end_iso:
                return {"error": "start_iso and end_iso are required", "has_conflict": False}

            # Check for conflicts
            conflict_result = await self.connector.find_conflicts(start_iso, end_iso, calendar_id)

            # Generate suggested alternative times if conflicts exist
            suggested_times = []
            if conflict_result["has_conflict"]:
                suggested_times = await self._generate_alternative_times(start_iso, end_iso, calendar_id)

            return {"has_conflict": conflict_result["has_conflict"], "conflicting_events": conflict_result["conflicting_events"], "count": conflict_result["count"], "suggested_times": suggested_times}

        except Exception as e:
            self.logger.error(f"❌ Conflict check failed: {e}")
            return {"error": str(e), "has_conflict": False}

    async def create_or_update_event(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update a calendar event with idempotency.

        Args:
            calendar_id: Calendar ID
            idempotency_key: Idempotency key for deduplication
            summary: Event title
            location: Event location
            description: Event description
            start: Start time object with dateTime and timeZone
            end: End time object with dateTime and timeZone
            attendees: List of attendee email addresses
            reminders: Reminder configuration

        Returns:
            Created/updated event data
        """
        try:
            # Validate required fields
            required_fields = ["summary", "start", "end"]
            for field in required_fields:
                if field not in args:
                    return {"error": f"Missing required field: {field}"}

            # Build event data
            event_data = {
                "summary": args["summary"],
                "location": args.get("location"),
                "description": args.get("description"),
                "start": args["start"],
                "end": args["end"],
                "attendees": [{"email": email} for email in args.get("attendees", [])],
                "reminders": args.get("reminders", {"useDefault": False, "overrides": [{"method": "popup", "minutes": 10}]}),
            }

            # Create or update event
            result = await self.connector.create_or_update_event(calendar_id=args.get("calendar_id", "primary"), event_data=event_data, idempotency_key=args.get("idempotency_key"))

            return {"success": True, "event_id": result.get("id"), "event_link": result.get("htmlLink"), "event_data": result}

        except Exception as e:
            self.logger.error(f"❌ Event creation failed: {e}")
            return {"success": False, "error": str(e)}

    async def list_events(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        List events in a calendar within a time range.

        Args:
            calendar_id: Calendar ID (default: 'primary')
            time_min: Start time for search (ISO format)
            time_max: End time for search (ISO format)
            max_results: Maximum number of results

        Returns:
            List of events
        """
        try:
            # This would be implemented in the connector
            # For now, return a placeholder
            return {"events": [], "count": 0}

        except Exception as e:
            self.logger.error(f"❌ Event listing failed: {e}")
            return {"error": str(e), "events": []}

    async def get_event(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a specific event by ID.

        Args:
            calendar_id: Calendar ID
            event_id: Event ID

        Returns:
            Event data
        """
        try:
            # This would be implemented in the connector
            # For now, return a placeholder
            return {"error": "Not implemented yet"}

        except Exception as e:
            self.logger.error(f"❌ Event retrieval failed: {e}")
            return {"error": str(e)}

    async def delete_event(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete an event.

        Args:
            calendar_id: Calendar ID
            event_id: Event ID

        Returns:
            Deletion result
        """
        try:
            # This would be implemented in the connector
            # For now, return a placeholder
            return {"error": "Not implemented yet"}

        except Exception as e:
            self.logger.error(f"❌ Event deletion failed: {e}")
            return {"error": str(e)}

    async def _generate_alternative_times(self, start_iso: str, end_iso: str, calendar_id: str) -> List[Dict[str, str]]:
        """Generate alternative time suggestions when conflicts exist"""
        try:
            from datetime import timedelta
            import dateutil.parser

            start_dt = dateutil.parser.parse(start_iso)
            end_dt = dateutil.parser.parse(end_iso)
            duration = end_dt - start_dt

            alternatives = []

            # Try 30 minutes later
            alt_start = start_dt + timedelta(minutes=30)
            alt_end = alt_start + duration

            # Check if this time is free
            conflict_check = await self.connector.find_conflicts(alt_start.isoformat(), alt_end.isoformat(), calendar_id)

            if not conflict_check["has_conflict"]:
                alternatives.append({"start_iso": alt_start.isoformat(), "end_iso": alt_end.isoformat(), "description": "30 minutes later"})

            # Try 1 hour later
            alt_start = start_dt + timedelta(hours=1)
            alt_end = alt_start + duration

            conflict_check = await self.connector.find_conflicts(alt_start.isoformat(), alt_end.isoformat(), calendar_id)

            if not conflict_check["has_conflict"]:
                alternatives.append({"start_iso": alt_start.isoformat(), "end_iso": alt_end.isoformat(), "description": "1 hour later"})

            return alternatives

        except Exception as e:
            self.logger.error(f"❌ Failed to generate alternatives: {e}")
            return []


# MCP Tool Manifest
GOOGLE_CALENDAR_MANIFEST = {
    "name": "google-calendar",
    "version": "1.0.0",
    "description": "Google Calendar integration for event management",
    "functions": [
        {
            "name": "find_conflicts",
            "description": "Find conflicting events in a time range",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_iso": {"type": "string", "format": "date-time", "description": "Start time in ISO format"},
                    "end_iso": {"type": "string", "format": "date-time", "description": "End time in ISO format"},
                    "calendar_id": {"type": "string", "description": "Calendar ID (default: 'primary')", "default": "primary"},
                },
                "required": ["start_iso", "end_iso"],
            },
        },
        {
            "name": "create_or_update_event",
            "description": "Create or update a calendar event with idempotency",
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {"type": "string", "description": "Calendar ID", "default": "primary"},
                    "idempotency_key": {"type": "string", "description": "Idempotency key for deduplication"},
                    "summary": {"type": "string", "description": "Event title", "maxLength": 180},
                    "location": {"type": "string", "description": "Event location"},
                    "description": {"type": "string", "description": "Event description"},
                    "start": {"type": "object", "properties": {"dateTime": {"type": "string", "format": "date-time"}, "timeZone": {"type": "string"}}, "required": ["dateTime", "timeZone"]},
                    "end": {"type": "object", "properties": {"dateTime": {"type": "string", "format": "date-time"}, "timeZone": {"type": "string"}}, "required": ["dateTime", "timeZone"]},
                    "attendees": {"type": "array", "items": {"type": "string", "format": "email"}, "description": "List of attendee email addresses"},
                    "reminders": {"type": "object", "description": "Reminder configuration"},
                },
                "required": ["summary", "start", "end"],
            },
        },
        {
            "name": "list_events",
            "description": "List events in a calendar within a time range",
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {"type": "string", "description": "Calendar ID", "default": "primary"},
                    "time_min": {"type": "string", "format": "date-time", "description": "Start time for search"},
                    "time_max": {"type": "string", "format": "date-time", "description": "End time for search"},
                    "max_results": {"type": "integer", "description": "Maximum number of results", "default": 25},
                },
            },
        },
        {
            "name": "get_event",
            "description": "Get a specific event by ID",
            "parameters": {
                "type": "object",
                "properties": {"calendar_id": {"type": "string", "description": "Calendar ID", "default": "primary"}, "event_id": {"type": "string", "description": "Event ID"}},
                "required": ["event_id"],
            },
        },
        {
            "name": "delete_event",
            "description": "Delete an event",
            "parameters": {
                "type": "object",
                "properties": {"calendar_id": {"type": "string", "description": "Calendar ID", "default": "primary"}, "event_id": {"type": "string", "description": "Event ID"}},
                "required": ["event_id"],
            },
        },
    ],
}
