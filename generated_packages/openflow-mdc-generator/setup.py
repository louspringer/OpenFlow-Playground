#!/usr/bin/env python3
"""
Setup script for openflow-mdc-generator
"""

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="openflow-mdc-generator",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
    )
