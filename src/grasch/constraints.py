"""
Constraint system for LEX extensions.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict
from .types import AttributeType, ElementType


class Constraint(ABC):
    """Base class for all LEX constraints"""
    
    def __init__(self, constraint_type: str, target_elements: List[str]):
        self.constraint_type = constraint_type
        self.target_elements = target_elements
    
    @abstractmethod
    def validate(self, element_data: Dict[str, Any]) -> bool:
        """Validate element data against this constraint"""
        pass
    
    @abstractmethod
    def get_error_message(self, element_data: Dict[str, Any]) -> str:
        """Get error message for constraint violation"""
        pass


class KeyConstraint(Constraint):
    """LEX key constraint for element types"""
    
    def __init__(self, element_type: str, key_attributes: List[str]):
        super().__init__("KEY_CONSTRAINT", [element_type])
        self.element_type = element_type
        self.key_attributes = key_attributes
    
    def validate(self, element_data: Dict[str, Any]) -> bool:
        """Validate that all key attributes are present and not null"""
        labels = element_data.get('labels', [])
        properties = element_data.get('properties', {})
        
        # Check that all key attributes are present
        for key_attr in self.key_attributes:
            # Key attributes can be labels or properties
            if key_attr in labels:
                continue
            elif key_attr in properties and properties[key_attr] is not None:
                continue
            else:
                return False
        
        return True
    
    def get_error_message(self, element_data: Dict[str, Any]) -> str:
        """Get error message for key constraint violation"""
        missing_attrs = []
        labels = element_data.get('labels', [])
        properties = element_data.get('properties', {})
        
        for key_attr in self.key_attributes:
            if key_attr not in labels and (key_attr not in properties or properties[key_attr] is None):
                missing_attrs.append(key_attr)
        
        return f"Key constraint violation on {self.element_type}: missing key attributes {missing_attrs}"


class CardinalityConstraint(Constraint):
    """LEX cardinality constraint for relationships"""
    
    def __init__(self, relationship_type: str, min_cardinality: int, max_cardinality: int = None):
        super().__init__("CARDINALITY_CONSTRAINT", [relationship_type])
        self.relationship_type = relationship_type
        self.min_cardinality = min_cardinality
        self.max_cardinality = max_cardinality
    
    def validate(self, element_data: Dict[str, Any]) -> bool:
        """Validate cardinality constraints (implementation depends on graph context)"""
        # This would need graph-wide context to validate properly
        # For now, return True as placeholder
        return True
    
    def get_error_message(self, element_data: Dict[str, Any]) -> str:
        """Get error message for cardinality constraint violation"""
        return f"Cardinality constraint violation on {self.relationship_type}"