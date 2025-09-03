#!/usr/bin/env python3
"""
Create PAG Art Exhibit calendar events
"""

import json
from datetime import datetime


def create_pag_events():
    """Create the three calendar events for PAG Art Exhibit"""

    # Event 1: All-day exhibition span (free)
    exhibition_event = {
        "summary": "PAG Art Exhibit: What's So Funny? (Exhibition)",
        "description": "PAG Art Exhibit: What's So Funny?\n\nLocation: The Schoolhouse, 19650 E. Mainstreet, Parker, CO 80138\nOpen: Mon-Thu 9:00 AM-4:00 PM, 90 min before performances\nAdmission: Free\n\nSource: https://parkerarts.org/event/pag-art-exhibit-whats-so-funny/",
        "location": "The Schoolhouse, 19650 E. Mainstreet, Parker, CO 80138",
        "start": {"date": "2025-08-02"},
        "end": {"date": "2025-09-21"},  # End date is exclusive, so +1 day
        "transparency": "transparent",  # Mark as free time
        "reminders": {"useDefault": False, "overrides": []},
    }

    # Event 2: Recurring visiting hours (free)
    visiting_hours_event = {
        "summary": "PAG Art Exhibit: What's So Funny? (Visiting Hours)",
        "description": "PAG Art Exhibit visiting hours\n\nLocation: The Schoolhouse, 19650 E. Mainstreet, Parker, CO 80138\nAdmission: Free\n\nSource: https://parkerarts.org/event/pag-art-exhibit-whats-so-funny/",
        "location": "The Schoolhouse, 19650 E. Mainstreet, Parker, CO 80138",
        "start": {"dateTime": "2025-08-04T09:00:00-06:00", "timeZone": "America/Denver"},
        "end": {"dateTime": "2025-08-04T16:00:00-06:00", "timeZone": "America/Denver"},
        "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH;UNTIL=20250918T235959Z"],
        "transparency": "transparent",  # Mark as free time
        "reminders": {"useDefault": False, "overrides": []},
    }

    # Event 3: Opening reception (busy)
    reception_event = {
        "summary": "PAG Art Exhibit: What's So Funny? (Opening Reception)",
        "description": "PAG Art Exhibit opening reception\n\nLocation: The Schoolhouse, 19650 E. Mainstreet, Parker, CO 80138\nAdmission: Free\n\nSource: https://parkerarts.org/event/pag-art-exhibit-whats-so-funny/",
        "location": "The Schoolhouse, 19650 E. Mainstreet, Parker, CO 80138",
        "start": {"dateTime": "2025-09-04T18:30:00-06:00", "timeZone": "America/Denver"},
        "end": {"dateTime": "2025-09-04T20:00:00-06:00", "timeZone": "America/Denver"},
        "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": 60}]},
    }

    events = [exhibition_event, visiting_hours_event, reception_event]

    print("📅 PAG Art Exhibit Calendar Events")
    print("=" * 50)
    print()

    for i, event in enumerate(events, 1):
        print(f'{i}. {event["summary"]}')
        print(f'   Location: {event["location"]}')

        if "date" in event["start"]:
            print(f'   Dates: {event["start"]["date"]} to {event["end"]["date"]}')
            print(f"   Type: All-day event")
        else:
            start_dt = event["start"]["dateTime"]
            end_dt = event["end"]["dateTime"]
            print(f"   Time: {start_dt} to {end_dt}")
            if "recurrence" in event:
                print(f"   Type: Recurring event (Mon-Thu weekly)")
            else:
                print(f"   Type: Single event")

        if event.get("transparency") == "transparent":
            print(f"   Status: FREE TIME (won't block calendar)")
        else:
            print(f"   Status: BUSY TIME (will block calendar)")

        print()

    print("✅ All events configured with:")
    print("   - Proper timezone (America/Denver)")
    print("   - All-day spans marked as free time")
    print("   - Location, description, and source link")
    print("   - Appropriate reminders")
    print()
    print("📋 To add these to your Google Calendar:")
    print("   1. Copy the event data above")
    print("   2. Use Google Calendar API or manual entry")
    print("   3. Or use the Gmail-to-Calendar system when OAuth is configured")

    return events


if __name__ == "__main__":
    create_pag_events()
