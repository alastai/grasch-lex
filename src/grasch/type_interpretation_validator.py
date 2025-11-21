"""
Type Interpretation Validation for Grasch

This module provides semantic validation for type interpretations in graph schemas.
It validates that abstract types are not directly instantiated, exact match types
don't accept subtypes, and other type interpretation constraints.
"""

from typing import Optional, List, Dict, Any
from .type_interpretation import TypeInterpretation
from .types import NodeType, EdgeType, GraphType


class TypeInterpretationError(Exception):
    """Raised when type interpretation validation fails."""
    
    def __init__(self, message: str, type_name: Optional[str] = None):
        super().__init__(message)
        self.type_name = type_name


class AbstractTypeInstantiationError(TypeInterpretationError):
    """Raised when attempting to directly instantiate an abstract type."""
    
    def __init__(self, type_name: str):
        message = (
            f"Cannot instantiate abstract type '{type_name}'. "
            f"Only subtypes of '{type_name}' can be instantiated."
        )
        super().__init__(message, type_name)


class ExactMatchViolationError(TypeInterpretationError):
    """Raised when a subtype is provided where exact match is required."""
    
    def __init__(self, expected_type: str, actual_type: str):
        message = (
            f"Exact type match required. Expected '{expected_type}', "
            f"but got subtype '{actual_type}'."
        )
        super().__init__(message, expected_type)
        self.actual_type = actual_type


class TypeInterpretationValidator:
    """
    Validates type interpretations in graph schemas.
    
    This validator checks semantic constraints on type interpretations:
    - Abstract types cannot be directly instantiated
    - Exact match types do not accept subtypes
    - Subtype match types accept the type or any subtype
    - Concrete types can be directly instantiated
    """

    
    def __init__(self):
        """Initialize the type interpretation validator."""
        pass
    
    def validate_abstract_type_not_instantiated(
        self,
        type_interpretation: TypeInterpretation,
        is_direct_instance: bool
    ) -> None:
        """
        Validate that abstract types are not directly instantiated.
        
        Args:
            type_interpretation: The type interpretation to check
            is_direct_instance: True if this is a direct instance (not a subtype)
            
        Raises:
            AbstractTypeInstantiationError: If attempting to instantiate abstract type
        """
        if type_interpretation.isAbstract() and is_direct_instance:
            raise AbstractTypeInstantiationError(type_interpretation.typeReference)
    
    def validate_exact_match(
        self,
        type_interpretation: TypeInterpretation,
        expected_type: str,
        actual_type: str
    ) -> None:
        """
        Validate that exact match types do not accept subtypes.
        
        Args:
            type_interpretation: The type interpretation to check
            expected_type: The expected type name
            actual_type: The actual type name provided
            
        Raises:
            ExactMatchViolationError: If subtype provided where exact match required
        """
        if type_interpretation.isExactMatch() and expected_type != actual_type:
            raise ExactMatchViolationError(expected_type, actual_type)
    
    def validate_subtype_match(
        self,
        type_interpretation: TypeInterpretation,
        expected_type: str,
        actual_type: str,
        is_subtype: bool
    ) -> bool:
        """
        Validate that subtype match types accept the type or any subtype.
        
        Args:
            type_interpretation: The type interpretation to check
            expected_type: The expected type name
            actual_type: The actual type name provided
            is_subtype: True if actual_type is a subtype of expected_type
            
        Returns:
            True if the match is valid
        """
        if type_interpretation.allowsSubtypes():
            # Accept exact match or subtype
            return actual_type == expected_type or is_subtype
        return False

    
    def validate_concrete_type_instantiation(
        self,
        type_interpretation: TypeInterpretation
    ) -> bool:
        """
        Validate that concrete types can be directly instantiated.
        
        Args:
            type_interpretation: The type interpretation to check
            
        Returns:
            True if the type can be directly instantiated
        """
        return type_interpretation.isConcrete()
    
    def validate_node_type(
        self,
        node_type: NodeType,
        instance_type: str,
        is_direct_instance: bool,
        is_subtype: bool = False
    ) -> None:
        """
        Validate a node type instance against its type interpretation.
        
        Args:
            node_type: The node type definition
            instance_type: The type of the instance being validated
            is_direct_instance: True if this is a direct instance (not a subtype)
            is_subtype: True if instance_type is a subtype of node_type
            
        Raises:
            AbstractTypeInstantiationError: If instantiating abstract type
            ExactMatchViolationError: If subtype provided where exact match required
        """
        interpretation = node_type.interpretation
        
        # Check abstract type instantiation
        self.validate_abstract_type_not_instantiated(interpretation, is_direct_instance)
        
        # Check exact match requirement
        if interpretation.isExactMatch():
            self.validate_exact_match(
                interpretation,
                interpretation.typeReference,
                instance_type
            )
    
    def validate_edge_type(
        self,
        edge_type: EdgeType,
        instance_type: str,
        is_direct_instance: bool,
        is_subtype: bool = False
    ) -> None:
        """
        Validate an edge type instance against its type interpretation.
        
        Args:
            edge_type: The edge type definition
            instance_type: The type of the instance being validated
            is_direct_instance: True if this is a direct instance (not a subtype)
            is_subtype: True if instance_type is a subtype of edge_type
            
        Raises:
            AbstractTypeInstantiationError: If instantiating abstract type
            ExactMatchViolationError: If subtype provided where exact match required
        """
        interpretation = edge_type.interpretation
        
        # Check abstract type instantiation
        self.validate_abstract_type_not_instantiated(interpretation, is_direct_instance)
        
        # Check exact match requirement
        if interpretation.isExactMatch():
            self.validate_exact_match(
                interpretation,
                interpretation.typeReference,
                instance_type
            )

    
    def validate_edge_component(
        self,
        edge_type: EdgeType,
        component: str,
        instance_type: str,
        is_direct_instance: bool,
        is_subtype: bool = False
    ) -> None:
        """
        Validate an edge type component against its type interpretation.
        
        Args:
            edge_type: The edge type definition
            component: The component name ('from', 'via', 'to')
            instance_type: The type of the instance being validated
            is_direct_instance: True if this is a direct instance (not a subtype)
            is_subtype: True if instance_type is a subtype
            
        Raises:
            AbstractTypeInstantiationError: If instantiating abstract type
            ExactMatchViolationError: If subtype provided where exact match required
            ValueError: If invalid component name
        """
        # Get the appropriate component interpretation
        if component == 'from':
            interpretation = edge_type.fromInterpretation
        elif component == 'via':
            interpretation = edge_type.viaInterpretation
        elif component == 'to':
            interpretation = edge_type.toInterpretation
        else:
            raise ValueError(f"Invalid edge component: {component}")
        
        # Check abstract type instantiation
        self.validate_abstract_type_not_instantiated(interpretation, is_direct_instance)
        
        # Check exact match requirement
        if interpretation.isExactMatch():
            self.validate_exact_match(
                interpretation,
                interpretation.typeReference,
                instance_type
            )
    
    def validate_graph_type(
        self,
        graph_type: GraphType,
        instance_type: str,
        is_direct_instance: bool,
        is_subtype: bool = False
    ) -> None:
        """
        Validate a graph type instance against its type interpretation.
        
        Args:
            graph_type: The graph type definition
            instance_type: The type of the instance being validated
            is_direct_instance: True if this is a direct instance (not a subtype)
            is_subtype: True if instance_type is a subtype of graph_type
            
        Raises:
            AbstractTypeInstantiationError: If instantiating abstract type
            ExactMatchViolationError: If subtype provided where exact match required
        """
        interpretation = graph_type.interpretation
        
        # Check abstract type instantiation
        self.validate_abstract_type_not_instantiated(interpretation, is_direct_instance)
        
        # Check exact match requirement
        if interpretation.isExactMatch():
            self.validate_exact_match(
                interpretation,
                interpretation.typeReference,
                instance_type
            )
