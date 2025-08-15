#!/usr/bin/env python3
"""
Setup script for openflow-security-first
"""

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="openflow-security-first",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
    )
