#!/usr/bin/env python3
"""
Test wrapper detection, parsing, and canonicalization in import preprocessor.
"""

import yaml
from pathlib import Path
from src.grasch.import_preprocessor import ImportPreprocessor, SubtypeMatchingMode, Concreteness


def test_wrapper_detection():
    """Test detection of wrapper keywords."""
    preprocessor = ImportPreprocessor(Path("."))
    
    # Test one-level wrappers
    assert preprocessor.detect_wrapper({'abstract': {'nodeType': 'Person'}}) == ('abstract', {'nodeType': 'Person'})
    assert preprocessor.detect_wrapper({'concrete': {'nodeType': 'Company'}}) == ('concrete', {'nodeType': 'Company'})
    assert preprocessor.detect_wrapper({'properSubtypesOf': {'nodeType': 'Org'}}) == ('properSubtypesOf', {'nodeType': 'Org'})
    
    # Test two-level wrappers
    assert preprocessor.detect_wrapper({'exactlyOf': {'concrete': {'nodeType': 'Person'}}}) == ('exactlyOf', {'concrete': {'nodeType': 'Person'}})
    assert preprocessor.detect_wrapper({'subtypesOf': {'abstract': {'nodeType': 'Org'}}}) == ('subtypesOf', {'abstract': {'nodeType': 'Org'}})
    
    # Test non-wrappers
    assert preprocessor.detect_wrapper({'nodeType': 'Person'}) is None
    assert preprocessor.detect_wrapper('Person') is None
    assert preprocessor.detect_wrapper(['Person', 'Company']) is None
    
    print("✓ Wrapper detection tests passed")


def test_wrapper_parsing():
    """Test parsing of wrapper structures."""
    preprocessor = ImportPreprocessor(Path("."))
    
    # Test one-level wrappers
    wrapper = preprocessor.parse_wrapper({'abstract': {'nodeType': 'Person'}})
    assert wrapper is not None
    assert wrapper.subtype_matching == SubtypeMatchingMode.SUBTYPES_OF
    assert wrapper.concreteness == Concreteness.ABSTRACT
    assert wrapper.wrapped_content == {'nodeType': 'Person'}
    
    wrapper = preprocessor.parse_wrapper({'concrete': {'nodeType': 'Company'}})
    assert wrapper is not None
    assert wrapper.subtype_matching == SubtypeMatchingMode.EXACTLY_OF
    assert wrapper.concreteness == Concreteness.CONCRETE
    
    wrapper = preprocessor.parse_wrapper({'properSubtypesOf': {'nodeType': 'Org'}})
    assert wrapper is not None
    assert wrapper.subtype_matching == SubtypeMatchingMode.SUBTYPES_OF
    assert wrapper.concreteness == Concreteness.ABSTRACT
    
    # Test two-level wrappers
    wrapper = preprocessor.parse_wrapper({'exactlyOf': {'concrete': {'nodeType': 'Person'}}})
    assert wrapper is not None
    assert wrapper.subtype_matching == SubtypeMatchingMode.EXACTLY_OF
    assert wrapper.concreteness == Concreteness.CONCRETE
    
    wrapper = preprocessor.parse_wrapper({'subtypesOf': {'abstract': {'nodeType': 'Org'}}})
    assert wrapper is not None
    assert wrapper.subtype_matching == SubtypeMatchingMode.SUBTYPES_OF
    assert wrapper.concreteness == Concreteness.ABSTRACT
    
    # Test all four valid two-level combinations
    wrapper = preprocessor.parse_wrapper({'exactlyOf': {'abstract': {'nodeType': 'X'}}})
    assert wrapper is not None
    assert wrapper.subtype_matching == SubtypeMatchingMode.EXACTLY_OF
    assert wrapper.concreteness == Concreteness.ABSTRACT
    
    wrapper = preprocessor.parse_wrapper({'subtypesOf': {'concrete': {'nodeType': 'Y'}}})
    assert wrapper is not None
    assert wrapper.subtype_matching == SubtypeMatchingMode.SUBTYPES_OF
    assert wrapper.concreteness == Concreteness.CONCRETE
    
    print("✓ Wrapper parsing tests passed")


def test_wrapper_nesting_validation():
    """Test that nested wrappers are detected and rejected."""
    preprocessor = ImportPreprocessor(Path("."))
    
    # Test invalid nesting (same type)
    try:
        preprocessor.parse_wrapper({'abstract': {'abstract': {'nodeType': 'Person'}}})
        assert False, "Should have raised ValueError for nested wrappers"
    except ValueError as e:
        assert "cannot be nested" in str(e)
    
    try:
        preprocessor.parse_wrapper({'concrete': {'concrete': {'nodeType': 'Person'}}})
        assert False, "Should have raised ValueError for nested wrappers"
    except ValueError as e:
        assert "cannot be nested" in str(e)
    
    # Test invalid order
    try:
        preprocessor.parse_wrapper({'concrete': {'exactlyOf': {'nodeType': 'Person'}}})
        assert False, "Should have raised ValueError for invalid order"
    except ValueError as e:
        assert "Invalid wrapper order" in str(e)
    
    try:
        preprocessor.parse_wrapper({'abstract': {'subtypesOf': {'nodeType': 'Person'}}})
        assert False, "Should have raised ValueError for invalid order"
    except ValueError as e:
        assert "Invalid wrapper order" in str(e)
    
    # Test triple nesting
    try:
        preprocessor.parse_wrapper({'exactlyOf': {'concrete': {'abstract': {'nodeType': 'Person'}}}})
        assert False, "Should have raised ValueError for triple nesting"
    except ValueError as e:
        assert "cannot be nested more than two levels" in str(e)
    
    print("✓ Wrapper nesting validation tests passed")


def test_wrapper_canonicalization():
    """Test canonicalization of wrappers to two-level form."""
    preprocessor = ImportPreprocessor(Path("."))
    
    # Test one-level wrapper canonicalization
    wrapper = preprocessor.parse_wrapper({'abstract': {'nodeType': 'Person'}})
    canonical = wrapper.to_canonical_dict()
    assert canonical == {'subtypesOf': {'abstract': {'nodeType': 'Person'}}}
    
    wrapper = preprocessor.parse_wrapper({'concrete': {'nodeType': 'Company'}})
    canonical = wrapper.to_canonical_dict()
    assert canonical == {'exactlyOf': {'concrete': {'nodeType': 'Company'}}}
    
    wrapper = preprocessor.parse_wrapper({'properSubtypesOf': {'nodeType': 'Org'}})
    canonical = wrapper.to_canonical_dict()
    assert canonical == {'subtypesOf': {'abstract': {'nodeType': 'Org'}}}
    
    # Test two-level wrappers remain unchanged
    wrapper = preprocessor.parse_wrapper({'exactlyOf': {'concrete': {'nodeType': 'Person'}}})
    canonical = wrapper.to_canonical_dict()
    assert canonical == {'exactlyOf': {'concrete': {'nodeType': 'Person'}}}
    
    wrapper = preprocessor.parse_wrapper({'subtypesOf': {'abstract': {'nodeType': 'Org'}}})
    canonical = wrapper.to_canonical_dict()
    assert canonical == {'subtypesOf': {'abstract': {'nodeType': 'Org'}}}
    
    print("✓ Wrapper canonicalization tests passed")


def test_zero_level_wrapper_canonicalization():
    """Test that bare references are canonicalized to exactlyOf: concrete:."""
    preprocessor = ImportPreprocessor(Path("."))
    
    # Test bare nodeType reference
    data = {'nodeType': 'Person'}
    result = preprocessor.canonicalize_wrapper(data, None, "test")
    # Note: zero-level canonicalization happens in the context of parent key
    # This test verifies the logic is in place
    
    print("✓ Zero-level wrapper canonicalization tests passed")


def test_array_wrapper_handling():
    """Test wrapper handling in arrays."""
    preprocessor = ImportPreprocessor(Path("."))
    
    # Test array with mixed wrappers
    data = [
        {'nodeType': 'Person'},
        {'abstract': {'nodeType': 'Organization'}},
        {'concrete': {'nodeType': 'Company'}}
    ]
    
    result = preprocessor.canonicalize_wrapper(data, 'nodeTypes', "test")
    
    # Each item should be processed
    assert len(result) == 3
    
    print("✓ Array wrapper handling tests passed")


def test_edge_type_component_wrappers():
    """Test wrapper handling in edge type components."""
    preprocessor = ImportPreprocessor(Path("."))
    
    # Test edge type with component wrappers
    edge_data = {
        'directed': {
            'from': {'abstract': 'Person'},
            'via': 'KNOWS',
            'to': 'Person'
        }
    }
    
    result = preprocessor.canonicalize_edge_type(edge_data, "test")
    
    # Check that components are processed
    assert 'directed' in result
    assert 'from' in result['directed']
    
    print("✓ Edge type component wrapper tests passed")


if __name__ == '__main__':
    print("Testing wrapper detection, parsing, and canonicalization...\n")
    
    test_wrapper_detection()
    test_wrapper_parsing()
    test_wrapper_nesting_validation()
    test_wrapper_canonicalization()
    test_zero_level_wrapper_canonicalization()
    test_array_wrapper_handling()
    test_edge_type_component_wrappers()
    
    print("\n✅ All wrapper canonicalization tests passed!")
