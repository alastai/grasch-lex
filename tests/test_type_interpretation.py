#!/usr/bin/env python3
"""
Tests for TypeInterpretation class and related enumerations.
"""

import pytest
from src.grasch.type_interpretation import (
    TypeInterpretation,
    SubtypeMatchingMode,
    Concreteness
)


class TestSubtypeMatchingMode:
    """Tests for SubtypeMatchingMode enumeration."""
    
    def test_values(self):
        """Test enumeration values."""
        assert SubtypeMatchingMode.EXACTLY_OF.value == "exactlyOf"
        assert SubtypeMatchingMode.SUBTYPES_OF.value == "subtypesOf"
    
    def test_from_value(self):
        """Test creating from string value."""
        assert SubtypeMatchingMode("exactlyOf") == SubtypeMatchingMode.EXACTLY_OF
        assert SubtypeMatchingMode("subtypesOf") == SubtypeMatchingMode.SUBTYPES_OF


class TestConcreteness:
    """Tests for Concreteness enumeration."""
    
    def test_values(self):
        """Test enumeration values."""
        assert Concreteness.CONCRETE.value == "concrete"
        assert Concreteness.ABSTRACT.value == "abstract"
    
    def test_from_value(self):
        """Test creating from string value."""
        assert Concreteness("concrete") == Concreteness.CONCRETE
        assert Concreteness("abstract") == Concreteness.ABSTRACT


class TestTypeInterpretation:
    """Tests for TypeInterpretation class."""
    
    def test_init_defaults(self):
        """Test initialization with default values."""
        interp = TypeInterpretation("Person")
        assert interp.typeReference == "Person"
        assert interp.subtypeMatching == SubtypeMatchingMode.EXACTLY_OF
        assert interp.concreteness == Concreteness.CONCRETE
    
    def test_init_custom(self):
        """Test initialization with custom values."""
        interp = TypeInterpretation(
            "Vehicle",
            SubtypeMatchingMode.SUBTYPES_OF,
            Concreteness.ABSTRACT
        )
        assert interp.typeReference == "Vehicle"
        assert interp.subtypeMatching == SubtypeMatchingMode.SUBTYPES_OF
        assert interp.concreteness == Concreteness.ABSTRACT
    
    def test_is_exact_match(self):
        """Test isExactMatch method."""
        exact = TypeInterpretation("Person", SubtypeMatchingMode.EXACTLY_OF)
        subtypes = TypeInterpretation("Person", SubtypeMatchingMode.SUBTYPES_OF)
        
        assert exact.isExactMatch() is True
        assert subtypes.isExactMatch() is False
    
    def test_allows_subtypes(self):
        """Test allowsSubtypes method."""
        exact = TypeInterpretation("Person", SubtypeMatchingMode.EXACTLY_OF)
        subtypes = TypeInterpretation("Person", SubtypeMatchingMode.SUBTYPES_OF)
        
        assert exact.allowsSubtypes() is False
        assert subtypes.allowsSubtypes() is True
    
    def test_is_concrete(self):
        """Test isConcrete method."""
        concrete = TypeInterpretation("Person", concreteness=Concreteness.CONCRETE)
        abstract = TypeInterpretation("Person", concreteness=Concreteness.ABSTRACT)
        
        assert concrete.isConcrete() is True
        assert abstract.isConcrete() is False
    
    def test_is_abstract(self):
        """Test isAbstract method."""
        concrete = TypeInterpretation("Person", concreteness=Concreteness.CONCRETE)
        abstract = TypeInterpretation("Person", concreteness=Concreteness.ABSTRACT)
        
        assert concrete.isAbstract() is False
        assert abstract.isAbstract() is True
    
    def test_equality(self):
        """Test equality comparison."""
        interp1 = TypeInterpretation("Person", SubtypeMatchingMode.EXACTLY_OF, Concreteness.CONCRETE)
        interp2 = TypeInterpretation("Person", SubtypeMatchingMode.EXACTLY_OF, Concreteness.CONCRETE)
        interp3 = TypeInterpretation("Person", SubtypeMatchingMode.SUBTYPES_OF, Concreteness.CONCRETE)
        interp4 = TypeInterpretation("Vehicle", SubtypeMatchingMode.EXACTLY_OF, Concreteness.CONCRETE)
        
        assert interp1 == interp2
        assert interp1 != interp3
        assert interp1 != interp4
        assert interp1 != "not a TypeInterpretation"
    
    def test_hash(self):
        """Test hashing for use in sets and dicts."""
        interp1 = TypeInterpretation("Person", SubtypeMatchingMode.EXACTLY_OF, Concreteness.CONCRETE)
        interp2 = TypeInterpretation("Person", SubtypeMatchingMode.EXACTLY_OF, Concreteness.CONCRETE)
        interp3 = TypeInterpretation("Vehicle", SubtypeMatchingMode.SUBTYPES_OF, Concreteness.ABSTRACT)
        
        # Same interpretations should have same hash
        assert hash(interp1) == hash(interp2)
        
        # Can be used in sets
        interp_set = {interp1, interp2, interp3}
        assert len(interp_set) == 2  # interp1 and interp2 are duplicates
    
    def test_str(self):
        """Test string representation."""
        interp = TypeInterpretation("Vehicle", SubtypeMatchingMode.SUBTYPES_OF, Concreteness.ABSTRACT)
        assert str(interp) == "subtypesOf: abstract: Vehicle"
    
    def test_repr(self):
        """Test detailed representation."""
        interp = TypeInterpretation("Vehicle", SubtypeMatchingMode.SUBTYPES_OF, Concreteness.ABSTRACT)
        repr_str = repr(interp)
        assert "TypeInterpretation" in repr_str
        assert "'Vehicle'" in repr_str
        assert "SUBTYPES_OF" in repr_str
        assert "ABSTRACT" in repr_str
    
    def test_from_canonical_dict_subtypes_abstract(self):
        """Test creating from canonical dict - subtypesOf: abstract:."""
        data = {"subtypesOf": {"abstract": "Vehicle"}}
        interp = TypeInterpretation.fromCanonicalDict(data)
        
        assert interp is not None
        assert interp.typeReference == "Vehicle"
        assert interp.subtypeMatching == SubtypeMatchingMode.SUBTYPES_OF
        assert interp.concreteness == Concreteness.ABSTRACT
    
    def test_from_canonical_dict_exactly_concrete(self):
        """Test creating from canonical dict - exactlyOf: concrete:."""
        data = {"exactlyOf": {"concrete": "Person"}}
        interp = TypeInterpretation.fromCanonicalDict(data)
        
        assert interp is not None
        assert interp.typeReference == "Person"
        assert interp.subtypeMatching == SubtypeMatchingMode.EXACTLY_OF
        assert interp.concreteness == Concreteness.CONCRETE
    
    def test_from_canonical_dict_invalid(self):
        """Test creating from invalid dict."""
        assert TypeInterpretation.fromCanonicalDict({}) is None
        assert TypeInterpretation.fromCanonicalDict({"invalid": "data"}) is None
        assert TypeInterpretation.fromCanonicalDict("not a dict") is None
        assert TypeInterpretation.fromCanonicalDict({"exactlyOf": "not a dict"}) is None
    
    def test_to_canonical_dict(self):
        """Test converting to canonical dict."""
        interp = TypeInterpretation("Vehicle", SubtypeMatchingMode.SUBTYPES_OF, Concreteness.ABSTRACT)
        data = interp.toCanonicalDict()
        
        assert data == {"subtypesOf": {"abstract": "Vehicle"}}
    
    def test_round_trip_canonical_dict(self):
        """Test round-trip conversion to/from canonical dict."""
        original = TypeInterpretation("Person", SubtypeMatchingMode.EXACTLY_OF, Concreteness.CONCRETE)
        data = original.toCanonicalDict()
        restored = TypeInterpretation.fromCanonicalDict(data)
        
        assert restored == original
    
    def test_exactly_concrete_factory(self):
        """Test exactlyConcrete factory method."""
        interp = TypeInterpretation.exactlyConcrete("Person")
        
        assert interp.typeReference == "Person"
        assert interp.isExactMatch() is True
        assert interp.isConcrete() is True
    
    def test_exactly_abstract_factory(self):
        """Test exactlyAbstract factory method."""
        interp = TypeInterpretation.exactlyAbstract("Asset")
        
        assert interp.typeReference == "Asset"
        assert interp.isExactMatch() is True
        assert interp.isAbstract() is True
    
    def test_subtypes_concrete_factory(self):
        """Test subtypesConcrete factory method."""
        interp = TypeInterpretation.subtypesConcrete("Employee")
        
        assert interp.typeReference == "Employee"
        assert interp.allowsSubtypes() is True
        assert interp.isConcrete() is True
    
    def test_subtypes_abstract_factory(self):
        """Test subtypesAbstract factory method."""
        interp = TypeInterpretation.subtypesAbstract("Vehicle")
        
        assert interp.typeReference == "Vehicle"
        assert interp.allowsSubtypes() is True
        assert interp.isAbstract() is True
    
    def test_all_four_combinations(self):
        """Test all four valid combinations of subtype matching and concreteness."""
        # exactlyOf: concrete: (default, zero-level)
        ec = TypeInterpretation.exactlyConcrete("Person")
        assert ec.isExactMatch() and ec.isConcrete()
        
        # exactlyOf: abstract: (edge case)
        ea = TypeInterpretation.exactlyAbstract("Asset")
        assert ea.isExactMatch() and ea.isAbstract()
        
        # subtypesOf: concrete:
        sc = TypeInterpretation.subtypesConcrete("Employee")
        assert sc.allowsSubtypes() and sc.isConcrete()
        
        # subtypesOf: abstract: (most common for abstract base types)
        sa = TypeInterpretation.subtypesAbstract("Vehicle")
        assert sa.allowsSubtypes() and sa.isAbstract()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
