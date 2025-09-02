"""
Model Management System
Consistent model CRUD operations and project model registry management.
"""

from .model_crud import main as model_crud_main
from .cli_parser import ModelCrudArgumentParser

__all__ = ["model_crud_main", "ModelCrudArgumentParser"]
__version__ = "1.0.0"
