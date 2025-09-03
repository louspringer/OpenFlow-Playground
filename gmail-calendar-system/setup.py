#!/usr/bin/env python3
"""
Setup script for gmail-calendar-system package
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Read requirements from pyproject.toml
def get_requirements():
    """Extract requirements from pyproject.toml"""
    requirements = [
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.2.0",
        "google-api-python-client>=2.0.0",
        "icalendar>=5.0.0",
        "python-dateutil>=2.8.0",
        "langgraph>=0.1.0",
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
    ]
    return requirements


setup(
    name="gmail-calendar-system",
    version="1.0.0",
    author="OpenFlow-Playground",
    author_email="contact@openflow-playground.dev",
    description="Protocol-driven Gmail-to-Calendar system with MCP tools for LLM integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openflow-playground/gmail-calendar-system",
    project_urls={
        "Homepage": "https://github.com/openflow-playground/gmail-calendar-system",
        "Documentation": "https://gmail-calendar-system.readthedocs.io",
        "Repository": "https://github.com/openflow-playground/gmail-calendar-system.git",
        "Issues": "https://github.com/openflow-playground/gmail-calendar-system/issues",
        "Changelog": "https://github.com/openflow-playground/gmail-calendar-system/blob/main/CHANGELOG.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Email",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.9",
    install_requires=get_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gmail-calendar=gmail_calendar_system.cli:main",
        ],
    },
    keywords=[
        "gmail",
        "calendar",
        "mcp",
        "llm",
        "agent",
        "automation",
        "oauth",
        "google",
        "api",
        "integration",
    ],
    include_package_data=True,
    zip_safe=False,
)
