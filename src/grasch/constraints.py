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
    
    def __init__(self, constraintType: str, targetElements: List[str]):
        self.constraintType = constraintType
        self.targetElements = targetElements
    
    @abstractmethod
    def createConstraint(self, graphContext: Any) -> 'Constraint':
        """Create a runtime constraint instance for a specific graph"""
        pass


class Constraint(ABC):
    """Base class for runtime constraints that validate graph values"""
    
    def __init__(self, specification: ConstraintSpecification, graphContext: Any):
        self.specification = specification
        self.graphContext = graphContext
    
    @abstractmethod
    def validate(self, elementData: Dict[str, Any]) -> bool:
        """Validate element data against this constraint"""
        pass
    
    @abstractmethod
    def getErrorMessage(self, elementData: Dict[str, Any]) -> str:
        """Get error message for constraint violation"""
        pass


class KeyConstraintSpecification(ConstraintSpecification):
    """Specification for LEX key constraints on element types"""
    
    def __init__(self, elementType: str, keyAttributes: List[str]):
        super().__init__("KEY_CONSTRAINT", [elementType])
        self.elementType = elementType
        self.keyAttributes = keyAttributes
    
    def createConstraint(self, graphContext: Any) -> 'KeyConstraint':
        """Create a runtime key constraint for a specific graph"""
        return KeyConstraint(self, graphContext)


class KeyConstraint(Constraint):
    """Runtime key constraint that validates element data"""
    
    def __init__(self, elementType: str, keyAttributes: List[str]):
        """Simple constructor for direct KeyConstraint creation"""
        specification = KeyConstraintSpecification(elementType, keyAttributes)
        super().__init__(specification, None)
    
    @property
    def elementType(self) -> str:
        """Get the element type this constraint applies to"""
        return self.specification.elementType
    
    def validate(self, elementData: Dict[str, Any]) -> bool:
        """Validate that all key attributes are present and not null"""
        labels = elementData.get('labels', [])
        properties = elementData.get('properties', {})
        
        # Check that all key attributes are present
        for keyAttr in self.specification.keyAttributes:
            # Key attributes can be labels or properties
            if keyAttr in labels:
                continue
            elif keyAttr in properties and properties[keyAttr] is not None:
                continue
            else:
                return False
        
        return True
    
    def getErrorMessage(self, elementData: Dict[str, Any]) -> str:
        """Get error message for key constraint violation"""
        missingAttrs = []
        labels = elementData.get('labels', [])
        properties = elementData.get('properties', {})
        
        for keyAttr in self.specification.keyAttributes:
            if keyAttr not in labels and (keyAttr not in properties or properties[keyAttr] is None):
                missingAttrs.append(keyAttr)
        
        return f"Key constraint violation on {self.specification.elementType}: missing key attributes {missingAttrs}"


class CardinalityConstraintSpecification(ConstraintSpecification):
    """Specification for LEX cardinality constraints on relationships"""
    
    def __init__(self, relationshipType: str, minCardinality: int, maxCardinality: Optional[int] = None):
        super().__init__("CARDINALITY_CONSTRAINT", [relationshipType])
        self.relationshipType = relationshipType
        self.minCardinality = minCardinality
        self.maxCardinality = maxCardinality
    
    def createConstraint(self, graphContext: Any) -> 'CardinalityConstraint':
        """Create a runtime cardinality constraint for a specific graph"""
        return CardinalityConstraint(self, graphContext)


class CardinalityConstraint(Constraint):
    """Runtime cardinality constraint that validates relationship counts"""
    
    def validate(self, elementData: Dict[str, Any]) -> bool:
        """Validate cardinality constraints (implementation depends on graph context)"""
        # This would need graph-wide context to validate properly
        # For now, return True as placeholder
        return True
    
    def getErrorMessage(self, elementData: Dict[str, Any]) -> str:
        """Get error message for cardinality constraint violation"""
        return f"Cardinality constraint violation on {self.specification.relationshipType}"