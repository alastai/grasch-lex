#!/usr/bin/env python3
"""
Test wrapper canonicalization in the import preprocessor.
"""

import yaml
from pathlib import Path
from src.grasch.canonicalizing_preprocessor import ImportPreprocessor, SubtypeMatchingMode, Concreteness

def test_canonicalization(name, input_yaml, expected_output):
    """Test a canonicalization pattern."""
    try:
        # Parse input
        data = yaml.safe_load(input_yaml)
        
        # Create preprocessor
        preprocessor = ImportPreprocessor(Path("."), canonicalize_wrappers=True)
        
        # Process (canonicalize)
        result = preprocessor.process(data)
        
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
        import traceback
        traceback.print_exc()
        return False

# Test cases
tests = []

# Test 1: One-level wrapper - abstract
tests.append(("One-level: abstract", """
graphSchema:
  pathName: /test
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - abstract:
          nodeType:
            typeLabel: Entity
            implies:
              propertyTypes: []
""", """
graphSchema:
  pathName: /test
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - subtypesOf:
          abstract:
            nodeType:
              typeLabel: Entity
              implies:
                propertyTypes: []
"""))

# Test 2: One-level wrapper - concrete
tests.append(("One-level: concrete", """
graphSchema:
  pathName: /test
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - concrete:
          nodeType:
            typeLabel: Company
            implies:
              propertyTypes: []
""", """
graphSchema:
  pathName: /test
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - exactlyOf:
          concrete:
            nodeType:
              typeLabel: Company
              implies:
                propertyTypes: []
"""))

# Test 3: One-level wrapper - properSubtypesOf
tests.append(("One-level: properSubtypesOf", """
graphSchema:
  pathName: /test
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - properSubtypesOf:
          nodeType:
            typeLabel: Organization
            implies:
              propertyTypes: []
""", """
graphSchema:
  pathName: /test
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - subtypesOf:
          abstract:
            nodeType:
              typeLabel: Organization
              implies:
                propertyTypes: []
"""))

# Test 4: Two-level wrapper - already canonical
tests.append(("Two-level: already canonical", """
graphSchema:
  pathName: /test
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - subtypesOf:
          abstract:
            nodeType:
              typeLabel: Vehicle
              implies:
                propertyTypes: []
""", """
graphSchema:
  pathName: /test
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - subtypesOf:
          abstract:
            nodeType:
              typeLabel: Vehicle
              implies:
                propertyTypes: []
"""))

# Run tests
print("=" * 60)
print("Testing Wrapper Canonicalization")
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
