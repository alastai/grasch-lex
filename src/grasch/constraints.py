"""
Constraint system for LEX extensions.

This module defines:
- ConstraintSpecification: Rules that can be associated with graph types
- Constraint: Runtime instances that validate actual graph values
"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional
from .types import AttributeType, ElementType


class ConstraintSpecification(ABC):
    """Base class for constraint specifications that can be associated with graph types"""
    
    def __init__(self, constraint_type: str, target_elements: List[str]):
        self.constraint_type = constraint_type
        self.target_elements = target_elements
    
    @abstractmethod
    def create_constraint(self, graph_context: Any) -> 'Constraint':
        """Create a runtime constraint instance for a specific graph"""
        pass


class Constraint(ABC):
    """Base class for runtime constraints that validate graph values"""
    
    def __init__(self, specification: ConstraintSpecification, graph_context: Any):
        self.specification = specification
        self.graph_context = graph_context
    
    @abstractmethod
    def validate(self, element_data: Dict[str, Any]) -> bool:
        """Validate element data against this constraint"""
        pass
    
    @abstractmethod
    def get_error_message(self, element_data: Dict[str, Any]) -> str:
        """Get error message for constraint violation"""
        pass


class KeyConstraintSpecification(ConstraintSpecification):
    """Specification for LEX key constraints on element types"""
    
    def __init__(self, element_type: str, key_attributes: List[str]):
        super().__init__("KEY_CONSTRAINT", [element_type])
        self.element_type = element_type
        self.key_attributes = key_attributes
    
    def create_constraint(self, graph_context: Any) -> 'KeyConstraint':
        """Create a runtime key constraint for a specific graph"""
        return KeyConstraint(self, graph_context)


class KeyConstraint(Constraint):
    """Runtime key constraint that validates element data"""
    
    def validate(self, element_data: Dict[str, Any]) -> bool:
        """Validate that all key attributes are present and not null"""
        labels = element_data.get('labels', [])
        properties = element_data.get('properties', {})
        
        # Check that all key attributes are present
        for key_attr in self.specification.key_attributes:
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
        
        for key_attr in self.specification.key_attributes:
            if key_attr not in labels and (key_attr not in properties or properties[key_attr] is None):
                missing_attrs.append(key_attr)
        
        return f"Key constraint violation on {self.specification.element_type}: missing key attributes {missing_attrs}"


class CardinalityConstraintSpecification(ConstraintSpecification):
    """Specification for LEX cardinality constraints on relationships"""
    
    def __init__(self, relationship_type: str, min_cardinality: int, max_cardinality: Optional[int] = None):
        super().__init__("CARDINALITY_CONSTRAINT", [relationship_type])
        self.relationship_type = relationship_type
        self.min_cardinality = min_cardinality
        self.max_cardinality = max_cardinality
    
    def create_constraint(self, graph_context: Any) -> 'CardinalityConstraint':
        """Create a runtime cardinality constraint for a specific graph"""
        return CardinalityConstraint(self, graph_context)


class CardinalityConstraint(Constraint):
    """Runtime cardinality constraint that validates relationship counts"""
    
    def validate(self, element_data: Dict[str, Any]) -> bool:
        """Validate cardinality constraints (implementation depends on graph context)"""
        # This would need graph-wide context to validate properly
        # For now, return True as placeholder
        return True
    
    def get_error_message(self, element_data: Dict[str, Any]) -> str:
        """Get error message for cardinality constraint violation"""
        return f"Cardinality constraint violation on {self.specification.relationship_type}"