"""
LangGraph Orchestrator for Gmail-to-Calendar System
==================================================

Implements the deterministic orchestration flow with proper state management,
conflict detection, confirmation gates, and auditability.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from .models import EventCandidate, IdempotencyKey, ConflictInfo, ConfirmationRequest, EventResult, AuditLog
from .connectors import GmailConnector, CalendarConnector, OAuthConfig
from .parsers import ICSParser, TimeNormalizer


@dataclass
class OrchestratorState:
    """State object for the orchestration graph"""

    # Input
    user_query: str = ""
    user_id: str = ""

    # Email processing
    search_query: str = ""
    messages: List[Dict[str, Any]] = field(default_factory=list)
    selected_message: Optional[Dict[str, Any]] = None
    thread_data: Optional[Dict[str, Any]] = None

    # Event extraction
    event_candidates: List[EventCandidate] = field(default_factory=list)
    selected_candidate: Optional[EventCandidate] = None

    # Time processing
    normalized_time: Optional[Dict[str, Any]] = None

    # Conflict detection
    conflict_info: Optional[ConflictInfo] = None

    # Confirmation
    confirmation_request: Optional[ConfirmationRequest] = None
    user_confirmation: Optional[bool] = None

    # Calendar operations
    event_result: Optional[EventResult] = None

    # Audit and logging
    audit_logs: List[AuditLog] = field(default_factory=list)

    # Error handling
    error_message: Optional[str] = None
    retry_count: int = 0


class GmailCalendarOrchestrator:
    """
    Main orchestrator for the Gmail-to-Calendar system.

    Implements the deterministic flow:
    1. Intent routing
    2. Email location
    3. Meeting extraction
    4. Time normalization
    5. Conflict checking
    6. Confirmation gate
    7. Calendar write
    8. Notification
    """

    def __init__(self, gmail_config: OAuthConfig, calendar_config: OAuthConfig, default_timezone: str = "America/Denver", confidence_threshold: float = 0.85):
        self.gmail_connector = GmailConnector(gmail_config)
        self.calendar_connector = CalendarConnector(calendar_config)
        self.ics_parser = ICSParser()
        self.time_normalizer = TimeNormalizer(default_timezone)
        self.confidence_threshold = confidence_threshold
        self.logger = logging.getLogger(__name__)

        # Build the orchestration graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph orchestration flow"""
        workflow = StateGraph(OrchestratorState)

        # Add nodes
        workflow.add_node("intent_router", self._intent_router)
        workflow.add_node("email_locator", self._email_locator)
        workflow.add_node("meeting_extractor", self._meeting_extractor)
        workflow.add_node("normalize_time", self._normalize_time)
        workflow.add_node("conflict_check", self._conflict_check)
        workflow.add_node("confirmation_gate", self._confirmation_gate)
        workflow.add_node("calendar_write", self._calendar_write)
        workflow.add_node("notifier", self._notifier)
        workflow.add_node("error_handler", self._error_handler)

        # Define the flow
        workflow.set_entry_point("intent_router")

        workflow.add_edge("intent_router", "email_locator")
        workflow.add_edge("email_locator", "meeting_extractor")
        workflow.add_edge("meeting_extractor", "normalize_time")
        workflow.add_edge("normalize_time", "conflict_check")
        workflow.add_edge("conflict_check", "confirmation_gate")

        # Conditional edges from confirmation gate
        workflow.add_conditional_edges("confirmation_gate", self._should_proceed, {"proceed": "calendar_write", "confirm": "confirmation_gate", "error": "error_handler"})  # Wait for user input

        workflow.add_edge("calendar_write", "notifier")
        workflow.add_edge("notifier", END)
        workflow.add_edge("error_handler", END)

        return workflow.compile()

    async def process_request(self, user_query: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        Process a user request to add events from Gmail to Calendar.

        Args:
            user_query: User's request (e.g., "put Megan's meeting on my calendar")
            user_id: User identifier for audit logging

        Returns:
            Result dictionary with event details and status
        """
        try:
            # Initialize state
            initial_state = OrchestratorState(user_query=user_query, user_id=user_id)

            # Run the orchestration
            final_state = await self.graph.ainvoke(initial_state)

            # Return result
            return {
                "success": final_state.event_result.success if final_state.event_result else False,
                "event_id": final_state.event_result.event_id if final_state.event_result else None,
                "event_link": final_state.event_result.event_link if final_state.event_result else None,
                "error_message": final_state.error_message,
                "audit_logs": [log.to_dict() for log in final_state.audit_logs],
            }

        except Exception as e:
            self.logger.error(f"❌ Orchestration failed: {e}")
            return {"success": False, "error_message": str(e), "audit_logs": []}

    async def _intent_router(self, state: OrchestratorState) -> OrchestratorState:
        """Route user intent and prepare search query"""
        try:
            query = state.user_query.lower()

            # Extract search terms from user query
            search_terms = []

            # Look for sender names
            if "megan" in query:
                search_terms.append("from:megan")
            if "jury" in query:
                search_terms.append("from:jury")

            # Look for meeting-related terms
            if any(word in query for word in ["meeting", "call", "appointment"]):
                search_terms.append("subject:(meeting OR call OR appointment)")

            # Look for probate-related terms
            if "probate" in query:
                search_terms.append("subject:probate")

            # Default search query
            if not search_terms:
                search_terms = ["subject:(meeting OR call)", "newer_than:30d"]

            state.search_query = " ".join(search_terms)

            self.logger.info(f"🎯 Intent routed: {state.search_query}")
            return state

        except Exception as e:
            state.error_message = f"Intent routing failed: {e}"
            return state

    async def _email_locator(self, state: OrchestratorState) -> OrchestratorState:
        """Locate relevant emails"""
        try:
            # Authenticate with Gmail
            if not await self.gmail_connector.authenticate():
                state.error_message = "Gmail authentication failed"
                return state

            # Search for messages
            messages = await self.gmail_connector.search_messages(state.search_query, max_results=25)

            if not messages:
                state.error_message = "No relevant emails found"
                return state

            state.messages = messages

            # Select the most recent message with time information
            state.selected_message = messages[0]  # For now, take the first one

            # Get full thread data
            thread_id = state.selected_message.get("threadId")
            if thread_id:
                state.thread_data = await self.gmail_connector.read_thread(thread_id)

            self.logger.info(f"📧 Located {len(messages)} messages")
            return state

        except Exception as e:
            state.error_message = f"Email location failed: {e}"
            return state

    async def _meeting_extractor(self, state: OrchestratorState) -> OrchestratorState:
        """Extract meeting information from emails"""
        try:
            if not state.selected_message:
                state.error_message = "No message selected for extraction"
                return state

            message_id = state.selected_message["id"]
            message_data = await self.gmail_connector.get_message(message_id)

            # Check for ICS attachments first
            attachments = await self.gmail_connector.get_attachments(message_id)
            ics_attachment = None

            for attachment in attachments:
                if attachment["filename"].endswith(".ics"):
                    ics_attachment = attachment
                    break

            if ics_attachment:
                # Parse ICS attachment
                ics_content = await self.gmail_connector.download_attachment(message_id, ics_attachment["attachmentId"])
                ics_text = ics_content.decode("utf-8")

                event_data = self.ics_parser.parse(ics_text, source="attachment")
                if event_data:
                    candidate = EventCandidate(
                        summary=event_data["summary"],
                        start_iso=event_data["start_iso"],
                        end_iso=event_data["end_iso"],
                        location=event_data.get("location"),
                        description=event_data.get("description"),
                        attendees=event_data.get("attendees", []),
                        source=SourceType.ICS,
                        idempotency_key=IdempotencyKey.from_ics_uid(event_data["uid"]).__str__(),
                        confidence=event_data["confidence"],
                        source_metadata={"message_id": message_id, "attachment_filename": ics_attachment["filename"]},
                    )
                    state.event_candidates.append(candidate)

            # If no ICS, try to extract from email body using LLM
            if not state.event_candidates:
                candidate = await self._extract_from_email_body(message_data)
                if candidate:
                    state.event_candidates.append(candidate)

            if state.event_candidates:
                state.selected_candidate = state.event_candidates[0]
                self.logger.info(f"📅 Extracted {len(state.event_candidates)} event candidates")
            else:
                state.error_message = "No meeting information found in email"

            return state

        except Exception as e:
            state.error_message = f"Meeting extraction failed: {e}"
            return state

    async def _extract_from_email_body(self, message_data: Dict[str, Any]) -> Optional[EventCandidate]:
        """Extract meeting info from email body using LLM"""
        # This would integrate with your LLM system
        # For now, return a placeholder
        return None

    async def _normalize_time(self, state: OrchestratorState) -> OrchestratorState:
        """Normalize time expressions to ISO format"""
        try:
            if not state.selected_candidate:
                state.error_message = "No candidate selected for time normalization"
                return state

            candidate = state.selected_candidate

            # If already has ISO times, skip normalization
            if candidate.start_iso and candidate.end_iso:
                state.normalized_time = {"start_iso": candidate.start_iso, "end_iso": candidate.end_iso, "confidence": candidate.confidence}
                return state

            # Extract time expressions from description or summary
            text_to_parse = f"{candidate.summary} {candidate.description or ''}"

            result = self.time_normalizer.normalize(text_to_parse, user_tz="America/Denver")

            if result.confidence > 0:
                state.normalized_time = {"start_iso": result.start_iso, "end_iso": result.end_iso, "confidence": result.confidence, "extracted": result.extracted}

                # Update candidate with normalized times
                candidate.start_iso = result.start_iso
                candidate.end_iso = result.end_iso
                candidate.confidence = result.confidence
            else:
                state.error_message = "Could not parse time from email content"

            return state

        except Exception as e:
            state.error_message = f"Time normalization failed: {e}"
            return state

    async def _conflict_check(self, state: OrchestratorState) -> OrchestratorState:
        """Check for calendar conflicts"""
        try:
            if not state.normalized_time:
                state.error_message = "No normalized time for conflict check"
                return state

            # Authenticate with Calendar
            if not await self.calendar_connector.authenticate():
                state.error_message = "Calendar authentication failed"
                return state

            # Check for conflicts
            conflict_result = await self.calendar_connector.find_conflicts(state.normalized_time["start_iso"], state.normalized_time["end_iso"])

            state.conflict_info = ConflictInfo(
                has_conflict=conflict_result["has_conflict"], conflicting_events=conflict_result["conflicting_events"], conflict_reason=f"Found {conflict_result['count']} conflicting events"
            )

            self.logger.info(f"🔍 Conflict check: {conflict_result['count']} conflicts found")
            return state

        except Exception as e:
            state.error_message = f"Conflict check failed: {e}"
            return state

    async def _confirmation_gate(self, state: OrchestratorState) -> OrchestratorState:
        """Determine if confirmation is needed"""
        try:
            if not state.selected_candidate or not state.normalized_time:
                state.error_message = "Missing candidate or time data for confirmation"
                return state

            candidate = state.selected_candidate
            confidence = state.normalized_time.get("confidence", 0)
            has_conflict = state.conflict_info.has_conflict if state.conflict_info else False

            # Determine if confirmation is needed
            needs_confirmation = confidence < self.confidence_threshold or has_conflict or len(state.event_candidates) > 1

            if needs_confirmation:
                # Create confirmation request
                confirmation_message = self._build_confirmation_message(candidate, state.normalized_time, state.conflict_info)

                state.confirmation_request = ConfirmationRequest(event_candidate=candidate, conflict_info=state.conflict_info, confirmation_message=confirmation_message, requires_confirmation=True)

                # For now, auto-confirm (in real system, this would wait for user input)
                state.user_confirmation = True
            else:
                state.user_confirmation = True  # Auto-proceed

            return state

        except Exception as e:
            state.error_message = f"Confirmation gate failed: {e}"
            return state

    def _build_confirmation_message(self, candidate: EventCandidate, normalized_time: Dict[str, Any], conflict_info: Optional[ConflictInfo]) -> str:
        """Build confirmation message for user"""
        start_dt = datetime.fromisoformat(normalized_time["start_iso"])
        end_dt = datetime.fromisoformat(normalized_time["end_iso"])

        message = f"Schedule '{candidate.summary}' "
        message += f"{start_dt.strftime('%a %b %d, %I:%M %p')} - "
        message += f"{end_dt.strftime('%I:%M %p')} MT"

        if candidate.attendees:
            attendee_names = ", ".join(candidate.attendees[:3])
            if len(candidate.attendees) > 3:
                attendee_names += f" and {len(candidate.attendees) - 3} others"
            message += f" with {attendee_names}"

        if conflict_info and conflict_info.has_conflict:
            message += f"\n⚠️ WARNING: {len(conflict_info.conflicting_events)} conflicting events found"

        message += "\n[Yes/No/Change time]"
        return message

    def _should_proceed(self, state: OrchestratorState) -> str:
        """Determine next step based on confirmation status"""
        if state.error_message:
            return "error"
        elif state.user_confirmation is None:
            return "confirm"  # Wait for user input
        elif state.user_confirmation:
            return "proceed"
        else:
            return "error"  # User declined

    async def _calendar_write(self, state: OrchestratorState) -> OrchestratorState:
        """Write event to calendar"""
        try:
            if not state.selected_candidate or not state.normalized_time:
                state.error_message = "Missing candidate or time data for calendar write"
                return state

            candidate = state.selected_candidate

            # Prepare event data
            event_data = {
                "summary": candidate.summary,
                "location": candidate.location,
                "description": candidate.description or f"From email. ID: {candidate.idempotency_key}",
                "start": {"dateTime": state.normalized_time["start_iso"], "timeZone": "America/Denver"},
                "end": {"dateTime": state.normalized_time["end_iso"], "timeZone": "America/Denver"},
                "attendees": [{"email": email} for email in candidate.attendees],
                "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": 10}]},
            }

            # Create event
            result = await self.calendar_connector.create_or_update_event(calendar_id="primary", event_data=event_data, idempotency_key=candidate.idempotency_key)

            # Create event result
            state.event_result = EventResult(success=True, event_id=result.get("id"), event_link=result.get("htmlLink"), idempotency_key=candidate.idempotency_key)

            # Log audit entry
            audit_log = AuditLog(
                timestamp=datetime.now(),
                user_id=state.user_id,
                action="create_event",
                event_id=result.get("id"),
                idempotency_key=candidate.idempotency_key,
                source_message_id=candidate.source_metadata.get("message_id"),
                success=True,
                details={"event_summary": candidate.summary},
            )
            state.audit_logs.append(audit_log)

            self.logger.info(f"✅ Created calendar event: {result.get('id')}")
            return state

        except Exception as e:
            state.error_message = f"Calendar write failed: {e}"

            # Log failed audit entry
            audit_log = AuditLog(
                timestamp=datetime.now(),
                user_id=state.user_id,
                action="create_event",
                event_id=None,
                idempotency_key=state.selected_candidate.idempotency_key if state.selected_candidate else None,
                source_message_id=state.selected_candidate.source_metadata.get("message_id") if state.selected_candidate else None,
                success=False,
                details={"error": str(e)},
            )
            state.audit_logs.append(audit_log)

            return state

    async def _notifier(self, state: OrchestratorState) -> OrchestratorState:
        """Send notification to user"""
        try:
            if state.event_result and state.event_result.success:
                message = f"✅ Booked '{state.selected_candidate.summary}' "
                message += f"on {datetime.fromisoformat(state.normalized_time['start_iso']).strftime('%a %b %d, %I:%M %p')} MT. "
                message += f"Event link: {state.event_result.event_link}"

                self.logger.info(f"📢 Notification: {message}")
                # In real system, this would send via chat/email

            return state

        except Exception as e:
            self.logger.error(f"❌ Notification failed: {e}")
            return state

    async def _error_handler(self, state: OrchestratorState) -> OrchestratorState:
        """Handle errors and provide user feedback"""
        self.logger.error(f"❌ Orchestration error: {state.error_message}")
        return state
