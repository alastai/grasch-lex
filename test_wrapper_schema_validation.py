#!/usr/bin/env python3
"""
Test script to validate that the updated schema accepts type interpretation wrapper patterns.
"""

import json
import yaml
from jsonschema import validate, ValidationError
from pathlib import Path

# Load the schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path) as f:
    schema = json.load(f)

def test_wrapper_pattern(name, yaml_content):
    """Test a specific wrapper pattern."""
    try:
        data = yaml.safe_load(yaml_content)
        validate(instance=data, schema=schema)
        print(f"✓ {name}: PASSED")
        return True
    except ValidationError as e:
        print(f"✗ {name}: FAILED")
        print(f"  Error: {e.message}")
        print(f"  Path: {list(e.path)}")
        return False
    except Exception as e:
        print(f"✗ {name}: ERROR - {e}")
        return False

# Test cases
tests = []

# Test 1: Zero-level wrapper (bare nodeType)
tests.append(("Zero-level wrapper (bare)", """
graphSchema:
  pathName: /test/zero-level
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes:
              - name: id
                valueType: STRING
"""))

# Test 2: One-level wrapper - abstract
tests.append(("One-level wrapper: abstract", """
graphSchema:
  pathName: /test/one-level-abstract
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - abstract:
          nodeType:
            typeLabel: Entity
            implies:
              propertyTypes:
                - name: id
                  valueType: STRING
"""))

# Test 3: One-level wrapper - concrete
tests.append(("One-level wrapper: concrete", """
graphSchema:
  pathName: /test/one-level-concrete
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - concrete:
          nodeType:
            typeLabel: Company
            implies:
              propertyTypes:
                - name: name
                  valueType: STRING
"""))

# Test 4: One-level wrapper - properSubtypesOf
tests.append(("One-level wrapper: properSubtypesOf", """
graphSchema:
  pathName: /test/one-level-proper
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - properSubtypesOf:
          nodeType:
            typeLabel: Organization
            implies:
              propertyTypes:
                - name: name
                  valueType: STRING
"""))

# Test 5: Two-level wrapper - exactlyOf: concrete:
tests.append(("Two-level wrapper: exactlyOf: concrete:", """
graphSchema:
  pathName: /test/two-level-exactly-concrete
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - exactlyOf:
          concrete:
            nodeType:
              typeLabel: Product
              implies:
                propertyTypes:
                  - name: name
                    valueType: STRING
"""))

# Test 6: Two-level wrapper - subtypesOf: abstract:
tests.append(("Two-level wrapper: subtypesOf: abstract:", """
graphSchema:
  pathName: /test/two-level-subtypes-abstract
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - subtypesOf:
          abstract:
            nodeType:
              typeLabel: Vehicle
              implies:
                propertyTypes:
                  - name: make
                    valueType: STRING
"""))

# Test 7: Wrapper around entire nodeTypes array
tests.append(("Wrapper around nodeTypes array", """
graphSchema:
  pathName: /test/array-wrapper
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    abstract:
      nodeTypes:
        - nodeType:
            typeLabel: BaseType
            implies:
              propertyTypes:
                - name: id
                  valueType: STRING
"""))

# Test 8: Mixed wrapped and unwrapped items
tests.append(("Mixed wrapped/unwrapped items", """
graphSchema:
  pathName: /test/mixed
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes:
              - name: name
                valueType: STRING
      - abstract:
          nodeType:
            typeLabel: Entity
            implies:
              propertyTypes:
                - name: id
                  valueType: STRING
      - concrete:
          nodeType:
            typeLabel: Company
            implies:
              propertyTypes:
                - name: name
                  valueType: STRING
"""))

# Test 9: Edge type with directed syntax
tests.append(("Edge type with directed syntax", """
graphSchema:
  pathName: /test/directed-edge
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
    edgeTypes:
      - edgeType:
          directed:
            from: Person
            via: KNOWS
            to: Person
          implies:
            propertyTypes:
              - name: since
                valueType: DATE
"""))

# Test 10: Edge type with undirected syntax
tests.append(("Edge type with undirected syntax", """
graphSchema:
  pathName: /test/undirected-edge
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
    edgeTypes:
      - edgeType:
          undirected:
            between: Person
            via: COLLABORATES_WITH
            and: Person
          implies:
            propertyTypes:
              - name: project
                valueType: STRING
"""))

# Test 11: Edge type with abstract wrapper
tests.append(("Edge type with abstract wrapper", """
graphSchema:
  pathName: /test/abstract-edge
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
    edgeTypes:
      - abstract:
          edgeType:
            directed:
              from: Person
              via: RELATIONSHIP
              to: Person
            implies:
              propertyTypes:
                - name: since
                  valueType: DATE
"""))

# Test 12: Endpoint with abstract wrapper
tests.append(("Endpoint with abstract wrapper", """
graphSchema:
  pathName: /test/abstract-endpoint
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
      - nodeType:
          typeLabel: Employee
          extends: Person
          adding:
            propertyTypes: []
    edgeTypes:
      - edgeType:
          directed:
            from: Employee
            via: MANAGES
            to:
              abstract: Person
          implies:
            propertyTypes: []
"""))

# Run all tests
print("=" * 60)
print("Testing Type Interpretation Wrapper Schema Validation")
print("=" * 60)
print()

passed = 0
failed = 0

for name, yaml_content in tests:
    if test_wrapper_pattern(name, yaml_content):
        passed += 1
    else:
        failed += 1
    print()

print("=" * 60)
print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
print("=" * 60)

exit(0 if failed == 0 else 1)
