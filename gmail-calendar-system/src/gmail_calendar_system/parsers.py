"""
Parsers for ICS and Natural Language Time Processing
===================================================

Handles RFC 5545 ICS parsing and natural language time normalization
with timezone resolution and confidence scoring.
"""

import re
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import dateutil.parser
import dateutil.tz
from icalendar import Calendar, Event as ICalEvent


@dataclass
class TimeParseResult:
    """Result of time parsing with confidence and metadata"""

    start_iso: str
    end_iso: str
    confidence: float
    extracted: Dict[str, Any]
    timezone: str
    is_all_day: bool = False


class ICSParser:
    """
    RFC 5545 compliant ICS parser for extracting calendar events.

    Handles both inline ICS content and attachment parsing.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, content: str, source: str = "inline") -> Optional[Dict[str, Any]]:
        """
        Parse ICS content and extract event information.

        Args:
            content: ICS content as string
            source: Source type ("inline" or "attachment")

        Returns:
            Parsed event data or None if parsing fails
        """
        try:
            calendar = Calendar.from_ical(content)

            for component in calendar.walk():
                if component.name == "VEVENT":
                    return self._extract_event_data(component)

            self.logger.warning("⚠️ No VEVENT found in ICS content")
            return None

        except Exception as e:
            self.logger.error(f"❌ ICS parsing failed: {e}")
            return None

    def _extract_event_data(self, event: ICalEvent) -> Dict[str, Any]:
        """Extract event data from ICS VEVENT component"""
        try:
            # Extract basic information
            summary = str(event.get("summary", ""))
            description = str(event.get("description", ""))
            location = str(event.get("location", ""))

            # Extract dates
            start_dt = event.get("dtstart")
            end_dt = event.get("dtend")

            if not start_dt:
                self.logger.warning("⚠️ No start time found in ICS event")
                return None

            # Convert to ISO format
            start_iso = self._datetime_to_iso(start_dt.dt)
            end_iso = self._datetime_to_iso(end_dt.dt) if end_dt else None

            # If no end time, assume 1 hour duration
            if not end_iso:
                start_dt_obj = start_dt.dt
                if isinstance(start_dt_obj, datetime):
                    end_dt_obj = start_dt_obj + timedelta(hours=1)
                else:
                    # All-day event
                    end_dt_obj = start_dt_obj + timedelta(days=1)
                end_iso = self._datetime_to_iso(end_dt_obj)

            # Extract attendees
            attendees = []
            for attendee in event.get("attendee", []):
                if hasattr(attendee, "params") and "CN" in attendee.params:
                    attendees.append(attendee.params["CN"])
                elif hasattr(attendee, "params") and "EMAIL" in attendee.params:
                    attendees.append(attendee.params["EMAIL"])
                else:
                    attendees.append(str(attendee))

            # Extract UID for idempotency
            uid = str(event.get("uid", ""))

            return {
                "summary": summary,
                "description": description,
                "location": location,
                "start_iso": start_iso,
                "end_iso": end_iso,
                "attendees": attendees,
                "uid": uid,
                "source": "ics",
                "confidence": 0.95,  # ICS is highly reliable
            }

        except Exception as e:
            self.logger.error(f"❌ Failed to extract ICS event data: {e}")
            return None

    def _datetime_to_iso(self, dt: Union[datetime, date]) -> str:
        """Convert datetime to ISO format string"""
        if isinstance(dt, datetime):
            return dt.isoformat()
        else:
            # Date only (all-day event)
            return f"{dt.isoformat()}T00:00:00"


class TimeNormalizer:
    """
    Natural language time parser with timezone resolution.

    Handles phrases like "this Friday 2:30-3pm", "tomorrow at noon",
    "next Thursday 9am" with confidence scoring.
    """

    def __init__(self, default_timezone: str = "America/Denver"):
        self.default_timezone = default_timezone
        self.logger = logging.getLogger(__name__)

        # Time patterns
        self.time_patterns = [
            # "2:30-3pm", "2:30-3:00pm", "2:30pm-3pm"
            r"(\d{1,2}):?(\d{2})?\s*([ap]m)?\s*[-–]\s*(\d{1,2}):?(\d{2})?\s*([ap]m)?",
            # "2:30pm", "2:30 PM", "14:30"
            r"(\d{1,2}):?(\d{2})?\s*([ap]m)?",
            # "noon", "midnight"
            r"\b(noon|midnight)\b",
        ]

        # Date patterns
        self.date_patterns = [
            # "this Friday", "next Thursday", "tomorrow"
            r"\b(this|next)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
            r"\b(tomorrow|today|yesterday)\b",
            # "Friday", "Fri" (assume this week)
            r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)\b",
        ]

    def normalize(self, text: str, user_tz: str = "America/Denver", reference_time_iso: Optional[str] = None) -> TimeParseResult:
        """
        Normalize natural language time to ISO format.

        Args:
            text: Natural language time text
            user_tz: User's timezone
            reference_time_iso: Reference time for relative dates

        Returns:
            TimeParseResult with parsed times and confidence
        """
        try:
            # Set reference time
            if reference_time_iso:
                ref_time = dateutil.parser.parse(reference_time_iso)
            else:
                ref_time = datetime.now(dateutil.tz.gettz(user_tz))

            # Extract date and time components
            date_info = self._extract_date(text, ref_time)
            time_info = self._extract_time(text)

            if not date_info or not time_info:
                return TimeParseResult(start_iso="", end_iso="", confidence=0.0, extracted={"error": "Could not parse date or time"}, timezone=user_tz)

            # Combine date and time
            start_dt = self._combine_date_time(date_info["date"], time_info["start_time"], user_tz)
            end_dt = self._combine_date_time(date_info["date"], time_info["end_time"], user_tz)

            # Calculate confidence
            confidence = self._calculate_confidence(date_info, time_info)

            return TimeParseResult(
                start_iso=start_dt.isoformat(),
                end_iso=end_dt.isoformat(),
                confidence=confidence,
                extracted={"date_info": date_info, "time_info": time_info, "original_text": text},
                timezone=user_tz,
                is_all_day=time_info.get("is_all_day", False),
            )

        except Exception as e:
            self.logger.error(f"❌ Time normalization failed: {e}")
            return TimeParseResult(start_iso="", end_iso="", confidence=0.0, extracted={"error": str(e)}, timezone=user_tz)

    def _extract_date(self, text: str, ref_time: datetime) -> Optional[Dict[str, Any]]:
        """Extract date information from text"""
        text_lower = text.lower()

        # Check for relative dates
        if "tomorrow" in text_lower:
            target_date = ref_time.date() + timedelta(days=1)
            return {"date": target_date, "type": "relative", "confidence": 0.9}

        if "today" in text_lower:
            target_date = ref_time.date()
            return {"date": target_date, "type": "relative", "confidence": 0.9}

        # Check for "this/next + weekday"
        for pattern in self.date_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if "this" in match.group(0):
                    return self._get_this_week_day(match.group(2), ref_time)
                elif "next" in match.group(0):
                    return self._get_next_week_day(match.group(2), ref_time)
                else:
                    # Just weekday, assume this week
                    return self._get_this_week_day(match.group(1), ref_time)

        return None

    def _extract_time(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract time information from text"""
        text_lower = text.lower()

        # Check for time ranges
        range_match = re.search(r"(\d{1,2}):?(\d{2})?\s*([ap]m)?\s*[-–]\s*(\d{1,2}):?(\d{2})?\s*([ap]m)?", text_lower)
        if range_match:
            start_time = self._parse_time_string(range_match.group(1, 2, 3))
            end_time = self._parse_time_string(range_match.group(4, 5, 6))
            return {"start_time": start_time, "end_time": end_time, "type": "range", "confidence": 0.9}

        # Check for single time
        time_match = re.search(r"(\d{1,2}):?(\d{2})?\s*([ap]m)?", text_lower)
        if time_match:
            start_time = self._parse_time_string(time_match.group(1, 2, 3))
            # Assume 1 hour duration
            end_time = start_time + timedelta(hours=1)
            return {"start_time": start_time, "end_time": end_time, "type": "single", "confidence": 0.8}

        # Check for special times
        if "noon" in text_lower:
            start_time = datetime.combine(datetime.today(), datetime.min.time().replace(hour=12))
            end_time = start_time + timedelta(hours=1)
            return {"start_time": start_time, "end_time": end_time, "type": "special", "confidence": 0.9}

        if "midnight" in text_lower:
            start_time = datetime.combine(datetime.today(), datetime.min.time())
            end_time = start_time + timedelta(hours=1)
            return {"start_time": start_time, "end_time": end_time, "type": "special", "confidence": 0.9}

        return None

    def _parse_time_string(self, time_parts: Tuple[str, str, str]) -> datetime:
        """Parse time string components into datetime"""
        hour = int(time_parts[0])
        minute = int(time_parts[1]) if time_parts[1] else 0
        ampm = time_parts[2].lower() if time_parts[2] else None

        # Handle AM/PM
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0

        return datetime.combine(datetime.today(), datetime.min.time().replace(hour=hour, minute=minute))

    def _get_this_week_day(self, weekday: str, ref_time: datetime) -> Dict[str, Any]:
        """Get date for this week's weekday"""
        weekday_map = {"monday": 0, "mon": 0, "tuesday": 1, "tue": 1, "wednesday": 2, "wed": 2, "thursday": 3, "thu": 3, "friday": 4, "fri": 4, "saturday": 5, "sat": 5, "sunday": 6, "sun": 6}

        target_weekday = weekday_map.get(weekday.lower(), 0)
        days_ahead = target_weekday - ref_time.weekday()

        if days_ahead <= 0:  # Target day already passed this week
            days_ahead += 7

        target_date = ref_time.date() + timedelta(days=days_ahead)
        return {"date": target_date, "type": "weekday", "confidence": 0.8}

    def _get_next_week_day(self, weekday: str, ref_time: datetime) -> Dict[str, Any]:
        """Get date for next week's weekday"""
        this_week = self._get_this_week_day(weekday, ref_time)
        next_week_date = this_week["date"] + timedelta(days=7)
        return {"date": next_week_date, "type": "weekday", "confidence": 0.9}

    def _combine_date_time(self, date: date, time: datetime, timezone: str) -> datetime:
        """Combine date and time with timezone"""
        combined = datetime.combine(date, time.time())
        tz = dateutil.tz.gettz(timezone)
        return combined.replace(tzinfo=tz)

    def _calculate_confidence(self, date_info: Dict[str, Any], time_info: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        date_confidence = date_info.get("confidence", 0.5)
        time_confidence = time_info.get("confidence", 0.5)

        # Weight time more heavily as it's usually more specific
        return (date_confidence * 0.4) + (time_confidence * 0.6)
