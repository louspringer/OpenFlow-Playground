"""
Gmail-to-Calendar System - Protocol-Driven Design
================================================

A comprehensive system for reading Gmail and adding events to Google Calendar
with conflict checks, confirmations, and auditability.

Key Features:
- OAuth2 connectors for Gmail and Calendar APIs
- ICS parser for RFC 5545 compliance
- Natural language time parsing
- Conflict detection and resolution
- Idempotency and reconciliation
- LangGraph orchestration
- MCP tool integration
"""

__version__ = "1.0.0"
__author__ = "OpenFlow-Playground"

from .connectors import GmailConnector, CalendarConnector
from .parsers import ICSParser, TimeNormalizer
from .orchestrator import GmailCalendarOrchestrator
from .models import EventCandidate, IdempotencyKey

__all__ = [
    "GmailConnector",
    "CalendarConnector",
    "ICSParser",
    "TimeNormalizer",
    "GmailCalendarOrchestrator",
    "EventCandidate",
    "IdempotencyKey",
]
