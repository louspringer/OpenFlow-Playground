#!/usr/bin/env python3
"""Simple test file to check if Ghostbusters is working properly"""


def hello_world() -> str:
    """Simple function that should pass all checks"""
    return "Hello, World!"


def add_numbers(a: int, b: int) -> int:
    """Simple typed function"""
    return a + b


if __name__ == "__main__":
    print(hello_world())
    print(add_numbers(5, 3))
