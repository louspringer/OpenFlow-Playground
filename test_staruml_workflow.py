#!/usr/bin/env python3
"""
Simple workflow test file for StarUML activity diagram generation.
This file has clear control flow that should generate a good activity diagram.
"""


def validate_user_input(username: str, password: str) -> bool:
    """Validate user input with clear workflow."""
    if not username or not password:
        return False

    if len(username) < 3:
        return False

    if len(password) < 8:
        return False

    return True


def authenticate_user(username: str, password: str) -> dict:
    """Authenticate user with clear decision flow."""
    # Validate input
    if not validate_user_input(username, password):
        return {"success": False, "error": "Invalid input"}

    # Check credentials
    if username == "admin" and password == "admin123":
        return {"success": True, "role": "admin"}
    elif username == "user" and password == "user123":
        return {"success": True, "role": "user"}
    else:
        return {"success": False, "error": "Invalid credentials"}


def process_user_request(user_role: str, request_type: str) -> dict:
    """Process user request based on role and type."""
    if user_role == "admin":
        if request_type == "read":
            return {"allowed": True, "data": "Admin read access"}
        elif request_type == "write":
            return {"allowed": True, "data": "Admin write access"}
        else:
            return {"allowed": False, "error": "Unknown request type"}

    elif user_role == "user":
        if request_type == "read":
            return {"allowed": True, "data": "User read access"}
        elif request_type == "write":
            return {"allowed": False, "error": "User write not allowed"}
        else:
            return {"allowed": False, "error": "Unknown request type"}

    else:
        return {"allowed": False, "error": "Unknown user role"}


def main():
    """Main workflow function."""
    # Get user input
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Authenticate user
    auth_result = authenticate_user(username, password)

    if not auth_result["success"]:
        print(f"Authentication failed: {auth_result['error']}")
        return

    print(f"Welcome, {username}!")

    # Process requests
    while True:
        request_type = input("Enter request type (read/write/quit): ")

        if request_type == "quit":
            break

        result = process_user_request(auth_result["role"], request_type)

        if result["allowed"]:
            print(f"Request successful: {result['data']}")
        else:
            print(f"Request denied: {result['error']}")

    print("Goodbye!")


if __name__ == "__main__":
    main()
