#!/usr/bin/env python3
"""
Type Interpretation System for LEX-2026

This module defines the type interpretation model that controls how types are matched
during validation. The system has two independent dimensions:
1. Subtype Matching Mode: exactlyOf vs subtypesOf
2. Concreteness: concrete vs abstract
"""

from __future__ import annotations
from enum import Enum
from typing import Optional


class SubtypeMatchingMode(Enum):
    """
    Subtype matching mode for type interpretation.
    
    Controls whether type matching requires exact type match or allows subtypes.
    """
    EXACTLY_OF = "exactlyOf"
    SUBTYPES_OF = "subtypesOf"


class Concreteness(Enum):
    """
    Concreteness for type interpretation.
    
    Controls whether a type can be directly instantiated or only through subtypes.
    """
    CONCRETE = "concrete"
    ABSTRACT = "abstract"


class TypeInterpretation:
    """
    Type interpretation combining subtype matching mode and concreteness.
    
    This class represents how a type reference should be interpreted during validation.
    It combines two independent dimensions:
    - Subtype matching mode (exactlyOf/subtypesOf)
    - Concreteness (concrete/abstract)
    
    The four valid combinations are:
    - exactlyOf: concrete: - Exact match, can be instantiated
    - exactlyOf: abstract: - Exact match, cannot be instantiated (edge case)
    - subtypesOf: concrete: - Allows subtypes, can be instantiated
    - subtypesOf: abstract: - Allows subtypes, cannot be instantiated (most common for abstract base types)
    """
    
    def __init__(
        self,
        type_reference: str,
        subtype_matching: SubtypeMatchingMode = SubtypeMatchingMode.EXACTLY_OF,
        concreteness: Concreteness = Concreteness.CONCRETE
    ):
        """
        Initialize type interpretation.
        
        Args:
            type_reference: The type being referenced (e.g., "Person", "Vehicle")
            subtype_matching: How to match subtypes (default: exactlyOf)
            concreteness: Whether type can be instantiated (default: concrete)
        """
        self._type_reference = type_reference
        self._subtype_matching = subtype_matching
        self._concreteness = concreteness
    
    @property
    def typeReference(self) -> str:
        """Get the type reference string."""
        return self._type_reference
    
    @property
    def subtypeMatching(self) -> SubtypeMatchingMode:
        """Get the subtype matching mode."""
        return self._subtype_matching
    
    @property
    def concreteness(self) -> Concreteness:
        """Get the concreteness."""
        return self._concreteness
    
    def isExactMatch(self) -> bool:
        """
        Check if this interpretation requires exact type match.
        
        Returns:
            True if exactlyOf matching mode, False if subtypesOf
        """
        return self._subtype_matching == SubtypeMatchingMode.EXACTLY_OF
    
    def allowsSubtypes(self) -> bool:
        """
        Check if this interpretation allows subtypes.
        
        Returns:
            True if subtypesOf matching mode, False if exactlyOf
        """
        return self._subtype_matching == SubtypeMatchingMode.SUBTYPES_OF
    
    def isConcrete(self) -> bool:
        """
        Check if this type can be directly instantiated.
        
        Returns:
            True if concrete, False if abstract
        """
        return self._concreteness == Concreteness.CONCRETE
    
    def isAbstract(self) -> bool:
        """
        Check if this type cannot be directly instantiated.
        
        Returns:
            True if abstract, False if concrete
        """
        return self._concreteness == Concreteness.ABSTRACT
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another TypeInterpretation."""
        if not isinstance(other, TypeInterpretation):
            return False
        return (
            self._type_reference == other._type_reference and
            self._subtype_matching == other._subtype_matching and
            self._concreteness == other._concreteness
        )
    
    def __hash__(self) -> int:
        """Compute hash for use in sets and dicts."""
        return hash((self._type_reference, self._subtype_matching, self._concreteness))
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"{self._subtype_matching.value}: {self._concreteness.value}: "
            f"{self._type_reference}"
        )
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"TypeInterpretation("
            f"type_reference={repr(self._type_reference)}, "
            f"subtype_matching={self._subtype_matching}, "
            f"concreteness={self._concreteness})"
        )
    
    @classmethod
    def fromCanonicalDict(cls, data: dict) -> Optional[TypeInterpretation]:
        """
        Create TypeInterpretation from canonical two-level wrapper dict.
        
        Args:
            data: Dictionary in form {subtypeMatching: {concreteness: typeReference}}
            
        Returns:
            TypeInterpretation instance or None if not a valid wrapper
            
        Example:
            >>> TypeInterpretation.fromCanonicalDict({
            ...     "subtypesOf": {"abstract": "Vehicle"}
            ... })
            TypeInterpretation(type_reference='Vehicle', ...)
        """
        if not isinstance(data, dict):
            return None
        
        # Check for subtype matching keywords
        for subtype_key in ["exactlyOf", "subtypesOf"]:
            if subtype_key in data:
                subtype_matching = SubtypeMatchingMode(subtype_key)
                concreteness_dict = data[subtype_key]
                
                if not isinstance(concreteness_dict, dict):
                    return None
                
                # Check for concreteness keywords
                for concreteness_key in ["concrete", "abstract"]:
                    if concreteness_key in concreteness_dict:
                        concreteness = Concreteness(concreteness_key)
                        type_reference = concreteness_dict[concreteness_key]
                        
                        if isinstance(type_reference, str):
                            return cls(type_reference, subtype_matching, concreteness)
                        
                        return None
        
        return None
    
    def toCanonicalDict(self) -> dict:
        """
        Convert to canonical two-level wrapper dict.
        
        Returns:
            Dictionary in form {subtypeMatching: {concreteness: typeReference}}
            
        Example:
            >>> interp = TypeInterpretation("Vehicle", SubtypeMatchingMode.SUBTYPES_OF, Concreteness.ABSTRACT)
            >>> interp.toCanonicalDict()
            {'subtypesOf': {'abstract': 'Vehicle'}}
        """
        return {
            self._subtype_matching.value: {
                self._concreteness.value: self._type_reference
            }
        }
    
    @classmethod
    def exactlyConcrete(cls, type_reference: str) -> TypeInterpretation:
        """
        Create interpretation for exact match, concrete type (default/zero-level).
        
        This is the default interpretation for bare type references.
        
        Args:
            type_reference: The type being referenced
            
        Returns:
            TypeInterpretation with exactlyOf: concrete:
        """
        return cls(type_reference, SubtypeMatchingMode.EXACTLY_OF, Concreteness.CONCRETE)
    
    @classmethod
    def exactlyAbstract(cls, type_reference: str) -> TypeInterpretation:
        """
        Create interpretation for exact match, abstract type.
        
        Edge case: type must match exactly but cannot be instantiated.
        
        Args:
            type_reference: The type being referenced
            
        Returns:
            TypeInterpretation with exactlyOf: abstract:
        """
        return cls(type_reference, SubtypeMatchingMode.EXACTLY_OF, Concreteness.ABSTRACT)
    
    @classmethod
    def subtypesConcrete(cls, type_reference: str) -> TypeInterpretation:
        """
        Create interpretation for subtype match, concrete type.
        
        Allows subtypes, and the type itself can be instantiated.
        
        Args:
            type_reference: The type being referenced
            
        Returns:
            TypeInterpretation with subtypesOf: concrete:
        """
        return cls(type_reference, SubtypeMatchingMode.SUBTYPES_OF, Concreteness.CONCRETE)
    
    @classmethod
    def subtypesAbstract(cls, type_reference: str) -> TypeInterpretation:
        """
        Create interpretation for subtype match, abstract type.
        
        Most common pattern for abstract base types: allows subtypes but
        the type itself cannot be instantiated.
        
        Args:
            type_reference: The type being referenced
            
        Returns:
            TypeInterpretation with subtypesOf: abstract:
        """
        return cls(type_reference, SubtypeMatchingMode.SUBTYPES_OF, Concreteness.ABSTRACT)
