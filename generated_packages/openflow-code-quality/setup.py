#!/usr/bin/env python3
"""
Setup script for openflow-code-quality
"""

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="openflow-code-quality",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
    )
