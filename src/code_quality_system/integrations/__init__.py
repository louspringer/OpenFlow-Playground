"""
Quality System Integrations

Integrations with various tools and systems for quality enforcement.
"""

from .ci_cd_integration import CICDIntegration
from .pre_commit_integration import PreCommitIntegration

__all__ = [
    "PreCommitIntegration",
    "CICDIntegration",
]
