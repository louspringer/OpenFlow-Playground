"""
OAuth2 Connectors for Gmail and Google Calendar APIs
===================================================

Provides secure, least-privilege access to Google services with proper
token management and scoped permissions.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

import httpx
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


@dataclass
class OAuthConfig:
    """OAuth2 configuration for Google APIs"""

    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: List[str]
    token_file: str = "token.json"
    credentials_file: str = "credentials.json"


class GmailConnector:
    """
    Gmail API connector with read-only access.

    Scopes:
    - https://www.googleapis.com/auth/gmail.readonly
    """

    def __init__(self, config: OAuthConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.service = None
        self._credentials = None

    async def authenticate(self) -> bool:
        """Authenticate with Gmail API"""
        try:
            self._credentials = await self._load_or_create_credentials()
            if not self._credentials or not self._credentials.valid:
                if self._credentials and self._credentials.expired and self._credentials.refresh_token:
                    self._credentials.refresh(Request())
                else:
                    self._credentials = await self._run_oauth_flow()

                await self._save_credentials()

            self.service = build("gmail", "v1", credentials=self._credentials)
            return True

        except Exception as e:
            self.logger.error(f"❌ Gmail authentication failed: {e}")
            return False

    async def search_messages(self, query: str, max_results: int = 25) -> List[Dict[str, Any]]:
        """
        Search Gmail messages using Gmail search syntax.

        Args:
            query: Gmail search query (e.g., "from:megan subject:meeting newer_than:30d")
            max_results: Maximum number of results to return

        Returns:
            List of message metadata dictionaries
        """
        if not self.service:
            await self.authenticate()

        try:
            results = self.service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()

            messages = results.get("messages", [])
            self.logger.info(f"📧 Found {len(messages)} messages for query: {query}")

            return messages

        except HttpError as e:
            self.logger.error(f"❌ Gmail search failed: {e}")
            return []

    async def read_thread(self, thread_id: str) -> Dict[str, Any]:
        """
        Read a complete email thread.

        Args:
            thread_id: Gmail thread ID

        Returns:
            Thread data with messages and metadata
        """
        if not self.service:
            await self.authenticate()

        try:
            thread = self.service.users().threads().get(userId="me", id=thread_id, format="full").execute()

            return thread

        except HttpError as e:
            self.logger.error(f"❌ Failed to read thread {thread_id}: {e}")
            return {}

    async def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        Get a specific message by ID.

        Args:
            message_id: Gmail message ID

        Returns:
            Message data with headers and body
        """
        if not self.service:
            await self.authenticate()

        try:
            message = self.service.users().messages().get(userId="me", id=message_id, format="full").execute()

            return message

        except HttpError as e:
            self.logger.error(f"❌ Failed to get message {message_id}: {e}")
            return {}

    async def get_attachments(self, message_id: str) -> List[Dict[str, Any]]:
        """
        Get attachments from a message.

        Args:
            message_id: Gmail message ID

        Returns:
            List of attachment metadata
        """
        if not self.service:
            await self.authenticate()

        try:
            message = await self.get_message(message_id)
            attachments = []

            for part in message.get("payload", {}).get("parts", []):
                if part.get("filename"):
                    attachment_id = part.get("body", {}).get("attachmentId")
                    if attachment_id:
                        attachments.append({"filename": part["filename"], "mimeType": part.get("mimeType", ""), "attachmentId": attachment_id, "size": part.get("body", {}).get("size", 0)})

            return attachments

        except Exception as e:
            self.logger.error(f"❌ Failed to get attachments for {message_id}: {e}")
            return []

    async def download_attachment(self, message_id: str, attachment_id: str) -> bytes:
        """
        Download an attachment.

        Args:
            message_id: Gmail message ID
            attachment_id: Attachment ID

        Returns:
            Attachment content as bytes
        """
        if not self.service:
            await self.authenticate()

        try:
            attachment = self.service.users().messages().attachments().get(userId="me", messageId=message_id, id=attachment_id).execute()

            import base64

            return base64.urlsafe_b64decode(attachment["data"])

        except Exception as e:
            self.logger.error(f"❌ Failed to download attachment {attachment_id}: {e}")
            return b""

    async def _load_or_create_credentials(self) -> Optional[Credentials]:
        """Load existing credentials or create new ones"""
        if os.path.exists(self.config.token_file):
            try:
                return Credentials.from_authorized_user_file(self.config.token_file, self.config.scopes)
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to load credentials: {e}")

        return None

    async def _run_oauth_flow(self) -> Credentials:
        """Run OAuth2 flow to get new credentials"""
        flow = Flow.from_client_secrets_file(self.config.credentials_file, scopes=self.config.scopes)
        flow.redirect_uri = self.config.redirect_uri

        # Get authorization URL
        auth_url, _ = flow.authorization_url(prompt="consent")
        print(f"🔐 Please visit this URL to authorize the application: {auth_url}")

        # Get authorization code from user
        auth_code = input("Enter the authorization code: ")

        # Exchange code for credentials
        flow.fetch_token(code=auth_code)
        return flow.credentials

    async def _save_credentials(self):
        """Save credentials to file"""
        if self._credentials:
            with open(self.config.token_file, "w") as token:
                token.write(self._credentials.to_json())


class CalendarConnector:
    """
    Google Calendar API connector with read/write access.

    Scopes:
    - https://www.googleapis.com/auth/calendar.readonly
    - https://www.googleapis.com/auth/calendar.events
    """

    def __init__(self, config: OAuthConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.service = None
        self._credentials = None

    async def authenticate(self) -> bool:
        """Authenticate with Calendar API"""
        try:
            self._credentials = await self._load_or_create_credentials()
            if not self._credentials or not self._credentials.valid:
                if self._credentials and self._credentials.expired and self._credentials.refresh_token:
                    self._credentials.refresh(Request())
                else:
                    self._credentials = await self._run_oauth_flow()

                await self._save_credentials()

            self.service = build("calendar", "v3", credentials=self._credentials)
            return True

        except Exception as e:
            self.logger.error(f"❌ Calendar authentication failed: {e}")
            return False

    async def find_conflicts(self, start_iso: str, end_iso: str, calendar_id: str = "primary") -> Dict[str, Any]:
        """
        Find conflicting events in the specified time range.

        Args:
            start_iso: Start time in ISO format
            end_iso: End time in ISO format
            calendar_id: Calendar ID (default: 'primary')

        Returns:
            Dictionary with conflict information
        """
        if not self.service:
            await self.authenticate()

        try:
            events_result = self.service.events().list(calendarId=calendar_id, timeMin=start_iso, timeMax=end_iso, singleEvents=True, orderBy="startTime").execute()

            events = events_result.get("items", [])

            return {"has_conflict": len(events) > 0, "conflicting_events": events, "count": len(events)}

        except HttpError as e:
            self.logger.error(f"❌ Failed to check conflicts: {e}")
            return {"has_conflict": False, "conflicting_events": [], "count": 0}

    async def create_or_update_event(self, calendar_id: str, event_data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Create or update a calendar event with idempotency.

        Args:
            calendar_id: Calendar ID
            event_data: Event data dictionary
            idempotency_key: Idempotency key for deduplication

        Returns:
            Created/updated event data
        """
        if not self.service:
            await self.authenticate()

        try:
            # Check if event already exists (idempotency)
            if idempotency_key:
                existing_event = await self._find_event_by_idempotency_key(calendar_id, idempotency_key)
                if existing_event:
                    self.logger.info(f"🔄 Event already exists, updating: {idempotency_key}")
                    return await self._update_event(calendar_id, existing_event["id"], event_data)

            # Create new event
            event = self.service.events().insert(calendarId=calendar_id, body=event_data).execute()

            self.logger.info(f"✅ Created event: {event.get('id')}")
            return event

        except HttpError as e:
            self.logger.error(f"❌ Failed to create/update event: {e}")
            raise

    async def _find_event_by_idempotency_key(self, calendar_id: str, idempotency_key: str) -> Optional[Dict[str, Any]]:
        """Find existing event by idempotency key"""
        try:
            # Search for events with the idempotency key in description
            events_result = self.service.events().list(calendarId=calendar_id, q=f"idempotency_key:{idempotency_key}", singleEvents=True).execute()

            events = events_result.get("items", [])
            return events[0] if events else None

        except Exception as e:
            self.logger.warning(f"⚠️ Failed to find event by idempotency key: {e}")
            return None

    async def _update_event(self, calendar_id: str, event_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing event"""
        try:
            event = self.service.events().update(calendarId=calendar_id, eventId=event_id, body=event_data).execute()

            self.logger.info(f"✅ Updated event: {event_id}")
            return event

        except HttpError as e:
            self.logger.error(f"❌ Failed to update event {event_id}: {e}")
            raise

    async def _load_or_create_credentials(self) -> Optional[Credentials]:
        """Load existing credentials or create new ones"""
        if os.path.exists(self.config.token_file):
            try:
                return Credentials.from_authorized_user_file(self.config.token_file, self.config.scopes)
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to load credentials: {e}")

        return None

    async def _run_oauth_flow(self) -> Credentials:
        """Run OAuth2 flow to get new credentials"""
        flow = Flow.from_client_secrets_file(self.config.credentials_file, scopes=self.config.scopes)
        flow.redirect_uri = self.config.redirect_uri

        # Get authorization URL
        auth_url, _ = flow.authorization_url(prompt="consent")
        print(f"🔐 Please visit this URL to authorize the application: {auth_url}")

        # Get authorization code from user
        auth_code = input("Enter the authorization code: ")

        # Exchange code for credentials
        flow.fetch_token(code=auth_code)
        return flow.credentials

    async def _save_credentials(self):
        """Save credentials to file"""
        if self._credentials:
            with open(self.config.token_file, "w") as token:
                token.write(self._credentials.to_json())
