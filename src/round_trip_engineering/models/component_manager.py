#!/usr/bin/env python3
"""
Component Manager
Manages model components (add, remove, update)
"""

import logging
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule


logger = logging.getLogger(__name__)


class ComponentManager(BaseReflectiveModule):
    """Manages model components (add, remove, update)"""

    def __init__(self) -> None:
        super().__init__()

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "component_management": [
                "add_component",
                "remove_component",
                "update_component",
                "validate_component"
            ],
            "component_operations": [
                "find_component",
                "list_components",
                "component_statistics"
            ]
        }

    def add_component(self, model_components: List[Any], component: Any) -> bool:
        """Add a component to a list of model components"""
        try:
            if not component or not hasattr(component, 'name'):
                logger.error("Invalid component: missing name attribute")
                return False

            # Check for duplicate names
            existing_names = {comp.name for comp in model_components if hasattr(comp, 'name')}
            if component.name in existing_names:
                logger.warning(f"Component {component.name} already exists")
                return False

            model_components.append(component)
            logger.info(f"✅ Added component {component.name}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to add component: {e}")
            return False

    def remove_component(self, model_components: List[Any], component_name: str) -> bool:
        """Remove a component from a list of model components"""
        try:
            for i, component in enumerate(model_components):
                if hasattr(component, 'name') and component.name == component_name:
                    del model_components[i]
                    logger.info(f"✅ Removed component {component_name}")
                    return True

            logger.warning(f"Component {component_name} not found")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to remove component {component_name}: {e}")
            return False

    def update_component(self, model_components: List[Any], component_name: str, updates: Dict[str, Any]) -> bool:
        """Update a component in a list of model components"""
        try:
            for component in model_components:
                if hasattr(component, 'name') and component.name == component_name:
                    for key, value in updates.items():
                        if hasattr(component, key):
                            setattr(component, key, value)
                    
                    logger.info(f"✅ Updated component {component_name}")
                    return True

            logger.warning(f"Component {component_name} not found")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to update component {component_name}: {e}")
            return False

    def find_component(self, model_components: List[Any], component_name: str) -> Optional[Any]:
        """Find a component by name"""
        try:
            for component in model_components:
                if hasattr(component, 'name') and component.name == component_name:
                    return component
            return None

        except Exception as e:
            logger.error(f"❌ Failed to find component {component_name}: {e}")
            return None

    def list_components(self, model_components: List[Any]) -> List[str]:
        """List all component names"""
        try:
            return [comp.name for comp in model_components if hasattr(comp, 'name')]
        except Exception as e:
            logger.error(f"❌ Failed to list components: {e}")
            return []

    def validate_component(self, component: Any) -> bool:
        """Validate a component has required attributes"""
        try:
            required_attrs = ['name', 'type', 'description']
            
            for attr in required_attrs:
                if not hasattr(component, attr):
                    logger.error(f"Component missing required attribute: {attr}")
                    return False
                
                value = getattr(component, attr)
                if not value:
                    logger.error(f"Component attribute {attr} is empty")
                    return False

            return True

        except Exception as e:
            logger.error(f"❌ Component validation failed: {e}")
            return False

    def component_statistics(self, model_components: List[Any]) -> Dict[str, Any]:
        """Get statistics about model components"""
        try:
            stats = {
                "total_components": len(model_components),
                "component_types": {},
                "components_by_type": {}
            }

            for component in model_components:
                if hasattr(component, 'type'):
                    comp_type = component.type
                    stats["component_types"][comp_type] = stats["component_types"].get(comp_type, 0) + 1
                    
                    if comp_type not in stats["components_by_type"]:
                        stats["components_by_type"][comp_type] = []
                    stats["components_by_type"][comp_type].append(component.name)

            return stats

        except Exception as e:
            logger.error(f"❌ Failed to generate component statistics: {e}")
            return {"error": str(e)}

    def filter_components_by_type(self, model_components: List[Any], component_type: str) -> List[Any]:
        """Filter components by type"""
        try:
            return [comp for comp in model_components if hasattr(comp, 'type') and comp.type == component_type]
        except Exception as e:
            logger.error(f"❌ Failed to filter components by type {component_type}: {e}")
            return []

    def sort_components_by_name(self, model_components: List[Any]) -> List[Any]:
        """Sort components by name"""
        try:
            return sorted(model_components, key=lambda x: getattr(x, 'name', ''))
        except Exception as e:
            logger.error(f"❌ Failed to sort components: {e}")
            return model_components
