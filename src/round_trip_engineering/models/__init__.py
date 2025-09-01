#!/usr/bin/env python3
"""
Models Package
Contains modules for managing different types of models
"""

from .design_model_manager import DesignModelManager
from .extracted_model_processor import ExtractedModelProcessor
from .model_persistence import ModelPersistence
from .component_manager import ComponentManager
from .type_normalizer import TypeNormalizer
from .data_cleaner import DataCleaner

__all__ = [
    "DesignModelManager",
    "ExtractedModelProcessor",
    "ModelPersistence",
    "ComponentManager",
    "TypeNormalizer",
    "DataCleaner",
]

__version__ = "0.1.0"
__author__ = "OpenFlow Playground"
__description__ = "Model management modules for round-trip engineering"
