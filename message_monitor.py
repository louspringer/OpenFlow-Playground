#!/usr/bin/env python3
"""
Message Monitor - Watches for new messages from TIDB and other agents
"""

import redis
import json
import time
import sys
from datetime import datetime


def check_for_messages():
    """Check for new messages and responses"""
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)

        # Check for responses from TIDB
        responses = r.lrange("beast_mode_responses", 0, 10)
        tidb_responses = []

        for response in responses:
            try:
                data = json.loads(response)
                if data.get("sender") == "TIDB":
                    tidb_responses.append(data)
            except:
                continue

        # Check for any new messages in queue
        messages = r.lrange("beast_mode_messages", 0, 5)

        return {"tidb_responses": len(tidb_responses), "total_responses": len(responses), "messages_in_queue": len(messages), "latest_tidb": tidb_responses[0] if tidb_responses else None}

    except Exception as e:
        print(f"Error checking messages: {e}")
        return None


def main():
    """Main monitoring loop"""
    print("🔍 Message Monitor Started")
    print("📧 Watching for messages from TIDB and other agents...")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)

    last_tidb_count = 0

    try:
        while True:
            result = check_for_messages()
            if result:
                current_time = datetime.now().strftime("%H:%M:%S")

                # Check for new TIDB responses
                if result["tidb_responses"] > last_tidb_count:
                    print(f"🚨 [{current_time}] NEW MESSAGE FROM TIDB!")
                    if result["latest_tidb"]:
                        content = result["latest_tidb"].get("content", "No content")
                        print(f"   Content: {content[:100]}...")
                    print("-" * 50)
                    last_tidb_count = result["tidb_responses"]

                # Status update every 30 seconds
                if int(time.time()) % 30 == 0:
                    print(f"📊 [{current_time}] Status: {result['tidb_responses']} TIDB responses, {result['messages_in_queue']} messages in queue")

            time.sleep(5)  # Check every 5 seconds

    except KeyboardInterrupt:
        print("\n🛑 Message Monitor Stopped")


if __name__ == "__main__":
    main()
