"""
Quality System Integrations

Integrations with various tools and systems for quality enforcement.
"""

from .pre_commit_integration import PreCommitIntegration
from .ci_cd_integration import CICDIntegration

__all__ = [
    "PreCommitIntegration",
    "CICDIntegration",
]
