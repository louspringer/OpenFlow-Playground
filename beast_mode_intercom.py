#!/usr/bin/env python3
"""
Beast Mode Intercom - Direct message sending tool
No more creating scripts for every message!
"""

import redis
import json
import uuid
import sys
from datetime import datetime


class BeastModeIntercom:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)

    def send_message(self, message_type="simple_message", target=None, payload=None):
        """Send a message directly to the Beast Mode network"""
        message = {"id": str(uuid.uuid4()), "type": message_type, "source": "beast_mode_intercom", "target": target, "payload": payload or {}, "timestamp": datetime.now().isoformat(), "priority": 5}

        try:
            self.client.ping()
            self.client.publish("beast_mode_network", json.dumps(message))
            print(f"✅ Message sent: {message_type} to {target or 'broadcast'}")
            return True
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False

    def send_technical_exchange(self, target, message_text):
        """Send a technical exchange message"""
        return self.send_message(message_type="technical_exchange", target=target, payload={"message": message_text})

    def send_collaboration_request(self, target, request_details):
        """Send a collaboration request"""
        return self.send_message(message_type="collaboration_request", target=target, payload=request_details)

    def send_status_update(self, status_info):
        """Send a status update"""
        return self.send_message(message_type="status_update", payload=status_info)


def main():
    if len(sys.argv) < 2:
        print("Usage: python beast_mode_intercom.py <command> [args...]")
        print("Commands:")
        print("  send <type> <target> <message>")
        print("  tech <target> <message>")
        print("  collab <target> <request>")
        print("  status <status_info>")
        return

    intercom = BeastModeIntercom()
    command = sys.argv[1]

    if command == "send" and len(sys.argv) >= 5:
        intercom.send_message(sys.argv[2], sys.argv[3], {"message": sys.argv[4]})
    elif command == "tech" and len(sys.argv) >= 4:
        intercom.send_technical_exchange(sys.argv[2], sys.argv[3])
    elif command == "collab" and len(sys.argv[2], sys.argv[3]):
        intercom.send_collaboration_request(sys.argv[2], {"request": sys.argv[3]})
    elif command == "status" and len(sys.argv) >= 3:
        intercom.send_status_update({"status": sys.argv[2]})
    else:
        print("Invalid command or arguments")


if __name__ == "__main__":
    main()
