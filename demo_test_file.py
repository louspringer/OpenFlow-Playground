#!/usr/bin/env python3
"""
Demo test file for round trip engineering demonstration.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class UserProfile:
    """User profile data structure."""

    name: str
    email: str
    age: int
    preferences: Dict[str, str]


class UserManager:
    """Manages user operations and profiles."""

    def __init__(self):
        self.users: List[UserProfile] = []
        self.logger = logging.getLogger(__name__)

    def add_user(self, name: str, email: str, age: int, preferences: Dict[str, str]) -> UserProfile:
        """Add a new user to the system."""
        try:
            user = UserProfile(name=name, email=email, age=age, preferences=preferences)
            self.users.append(user)
            self.logger.info(f"✅ Added user: {name}")
            return user
        except Exception as e:
            self.logger.error(f"❌ Failed to add user: {e}")
            raise

    def get_user_by_email(self, email: str) -> Optional[UserProfile]:
        """Find user by email address."""
        for user in self.users:
            if user.email == email:
                return user
        return None

    def update_user_preferences(self, email: str, new_preferences: Dict[str, str]) -> bool:
        """Update user preferences."""
        user = self.get_user_by_email(email)
        if user:
            user.preferences.update(new_preferences)
            self.logger.info(f"✅ Updated preferences for: {email}")
            return True
        else:
            self.logger.warning(f"⚠️ User not found: {email}")
            return False

    def list_users(self) -> List[UserProfile]:
        """Get all users."""
        return self.users.copy()


def main():
    """Main function to demonstrate the user management system."""
    manager = UserManager()

    # Add some test users
    manager.add_user("Alice", "alice@example.com", 30, {"theme": "dark", "language": "en"})
    manager.add_user("Bob", "bob@example.com", 25, {"theme": "light", "language": "es"})

    # List all users
    users = manager.list_users()
    print(f"📋 Found {len(users)} users:")
    for user in users:
        print(f"  - {user.name} ({user.email})")


if __name__ == "__main__":
    main()
