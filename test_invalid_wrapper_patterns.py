#!/usr/bin/env python3
"""
Test that the schema properly rejects invalid wrapper patterns.
"""

import json
import yaml
from jsonschema import validate, ValidationError
from pathlib import Path

# Load the schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path) as f:
    schema = json.load(f)

def test_invalid_pattern(name, yaml_content):
    """Test that an invalid pattern is rejected."""
    try:
        data = yaml.safe_load(yaml_content)
        validate(instance=data, schema=schema)
        print(f"✗ {name}: FAILED (should have been rejected)")
        return False
    except ValidationError as e:
        print(f"✓ {name}: REJECTED (as expected)")
        return True
    except Exception as e:
        print(f"✗ {name}: ERROR - {e}")
        return False

# Test cases that should be rejected
tests = []

# Test 1: Nested wrappers (abstract inside concrete)
tests.append(("Nested wrappers (abstract in concrete)", """
graphSchema:
  pathName: /test/nested
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - concrete:
          abstract:
            nodeType:
              typeLabel: Person
              implies:
                propertyTypes: []
"""))

# Test 2: Wrong wrapper order (concrete before exactlyOf)
# Note: This is actually allowed by the schema as it's a different pattern
# Let's test triple nesting instead
tests.append(("Triple nested wrappers", """
graphSchema:
  pathName: /test/triple-nested
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - exactlyOf:
          concrete:
            abstract:
              nodeType:
                typeLabel: Person
                implies:
                  propertyTypes: []
"""))

# Test 3: Wrapper inside nodeType definition (not around reference)
# This should be caught by the schema structure
tests.append(("Wrapper inside nodeType definition", """
graphSchema:
  pathName: /test/wrapper-inside
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          abstract:
            typeLabel: Person
          implies:
            propertyTypes: []
"""))

# Run all tests
print("=" * 60)
print("Testing Invalid Type Interpretation Wrapper Patterns")
print("=" * 60)
print()

passed = 0
failed = 0

for name, yaml_content in tests:
    if test_invalid_pattern(name, yaml_content):
        passed += 1
    else:
        failed += 1
    print()

print("=" * 60)
print(f"Results: {passed} rejected (correct), {failed} accepted (incorrect) out of {len(tests)} tests")
print("=" * 60)

exit(0 if failed == 0 else 1)
