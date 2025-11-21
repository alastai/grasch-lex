#!/usr/bin/env python3
"""
Test canonicalization of type interpretation wrappers.
"""

import yaml
from pathlib import Path
from src.grasch.import_preprocessor import ImportPreprocessor

def test_canonicalization(name, input_yaml, expected_output):
    """Test a canonicalization pattern."""
    try:
        # Parse input
        data = yaml.safe_load(input_yaml)
        
        # Create preprocessor
        preprocessor = ImportPreprocessor(Path("."), canonicalize_wrappers=True)
        
        # Canonicalize
        result = preprocessor.canonicalize_content(data, "test")
        
        # Parse expected
        expected = yaml.safe_load(expected_output)
        
        # Compare
        if result == expected:
            print(f"✓ {name}: PASSED")
            return True
        else:
            print(f"✗ {name}: FAILED")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
            return False
    except Exception as e:
        print(f"✗ {name}: ERROR - {e}")
        return False

# Test cases
tests = []

# Test 1: Zero-level (bare) → exactlyOf: concrete:
tests.append(("Zero-level canonicalization", """
nodeType:
  typeLabel: Person
  implies:
    propertyTypes: []
""", """
exactlyOf:
  concrete:
    nodeType:
      typeLabel: Person
      implies:
        propertyTypes: []
"""))

# Test 2: abstract: → subtypesOf: abstract:
tests.append(("abstract: canonicalization", """
abstract:
  nodeType:
    typeLabel: Entity
    implies:
      propertyTypes: []
""", """
subtypesOf:
  abstract:
    nodeType:
      typeLabel: Entity
      implies:
        propertyTypes: []
"""))

# Test 3: concrete: → exactlyOf: concrete:
tests.append(("concrete: canonicalization", """
concrete:
  nodeType:
    typeLabel: Company
    implies:
      propertyTypes: []
""", """
exactlyOf:
  concrete:
    nodeType:
      typeLabel: Company
      implies:
        propertyTypes: []
"""))

# Test 4: properSubtypesOf: → subtypesOf: abstract:
tests.append(("properSubtypesOf: canonicalization", """
properSubtypesOf:
  nodeType:
    typeLabel: Organization
    implies:
      propertyTypes: []
""", """
subtypesOf:
  abstract:
    nodeType:
      typeLabel: Organization
      implies:
        propertyTypes: []
"""))

# Test 5: Two-level wrapper preserved
tests.append(("Two-level wrapper preservation", """
exactlyOf:
  concrete:
    nodeType:
      typeLabel: Product
      implies:
        propertyTypes: []
""", """
exactlyOf:
  concrete:
    nodeType:
      typeLabel: Product
      implies:
        propertyTypes: []
"""))

# Test 6: Array with mixed wrappers
tests.append(("Array with mixed wrappers", """
nodeTypes:
  - nodeType:
      typeLabel: Person
      implies:
        propertyTypes: []
  - abstract:
      nodeType:
        typeLabel: Entity
        implies:
          propertyTypes: []
""", """
nodeTypes:
  - exactlyOf:
      concrete:
        nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
  - subtypesOf:
      abstract:
        nodeType:
          typeLabel: Entity
          implies:
            propertyTypes: []
"""))

# Run all tests
print("=" * 60)
print("Testing Type Interpretation Wrapper Canonicalization")
print("=" * 60)
print()

passed = 0
failed = 0

for name, input_yaml, expected_output in tests:
    if test_canonicalization(name, input_yaml, expected_output):
        passed += 1
    else:
        failed += 1
    print()

print("=" * 60)
print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
print("=" * 60)

exit(0 if failed == 0 else 1)
