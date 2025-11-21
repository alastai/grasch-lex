#!/usr/bin/env python3
"""
Test advanced wrapper patterns including endpoint wrappers and edge cases.
"""

import json
import yaml
from jsonschema import validate, ValidationError
from pathlib import Path

# Load the schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path) as f:
    schema = json.load(f)

def test_wrapper_pattern(name, yaml_content, should_pass=True):
    """Test a specific wrapper pattern."""
    try:
        data = yaml.safe_load(yaml_content)
        validate(instance=data, schema=schema)
        if should_pass:
            print(f"✓ {name}: PASSED (as expected)")
            return True
        else:
            print(f"✗ {name}: FAILED (should have been rejected)")
            return False
    except ValidationError as e:
        if not should_pass:
            print(f"✓ {name}: REJECTED (as expected)")
            print(f"  Reason: {e.message}")
            return True
        else:
            print(f"✗ {name}: FAILED (should have passed)")
            print(f"  Error: {e.message}")
            print(f"  Path: {list(e.path)}")
            return False
    except Exception as e:
        print(f"✗ {name}: ERROR - {e}")
        return False

# Test cases
tests = []

# Test 1: Two-level wrapper on endpoint - exactlyOf: concrete:
tests.append(("Endpoint: exactlyOf: concrete:", True, """
graphSchema:
  pathName: /test/endpoint-two-level
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
            to:
              exactlyOf:
                concrete: Person
          implies:
            propertyTypes: []
"""))

# Test 2: Two-level wrapper on endpoint - subtypesOf: abstract:
tests.append(("Endpoint: subtypesOf: abstract:", True, """
graphSchema:
  pathName: /test/endpoint-subtypes-abstract
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
            from:
              subtypesOf:
                abstract: Person
            via: MANAGES
            to: Person
          implies:
            propertyTypes: []
"""))

# Test 3: Endpoint with concrete wrapper
tests.append(("Endpoint: concrete wrapper", True, """
graphSchema:
  pathName: /test/endpoint-concrete
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
            from:
              concrete: Person
            via: WORKS_FOR
            to: Person
          implies:
            propertyTypes: []
"""))

# Test 4: Endpoint with properSubtypesOf wrapper
tests.append(("Endpoint: properSubtypesOf wrapper", True, """
graphSchema:
  pathName: /test/endpoint-proper
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
            from:
              properSubtypesOf: Person
            via: REPORTS_TO
            to: Person
          implies:
            propertyTypes: []
"""))

# Test 5: Multiple endpoints with different wrappers
tests.append(("Multiple endpoints with different wrappers", True, """
graphSchema:
  pathName: /test/mixed-endpoints
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
      - nodeType:
          typeLabel: Company
          implies:
            propertyTypes: []
    edgeTypes:
      - edgeType:
          directed:
            from:
              abstract: Person
            via: WORKS_FOR
            to:
              concrete: Company
          implies:
            propertyTypes: []
"""))

# Test 6: Undirected edge with wrapped endpoints
tests.append(("Undirected edge with wrapped endpoints", True, """
graphSchema:
  pathName: /test/undirected-wrapped
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
            between:
              abstract: Person
            via: COLLABORATES_WITH
            and:
              concrete: Person
          implies:
            propertyTypes: []
"""))

# Test 7: Edge type with arc synonym
tests.append(("Edge type with arc synonym", True, """
graphSchema:
  pathName: /test/arc-synonym
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
            arc: KNOWS
            to: Person
          implies:
            propertyTypes: []
"""))

# Test 8: Endpoint with integer index
tests.append(("Endpoint with integer index", True, """
graphSchema:
  pathName: /test/endpoint-index
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          index: 0
          implies:
            propertyTypes: []
    edgeTypes:
      - edgeType:
          directed:
            from: 0
            via: LINKS_TO
            to: 0
          implies:
            propertyTypes: []
"""))

# Test 9: Endpoint with array of labels (typeIdentifier)
tests.append(("Endpoint with array of labels", True, """
graphSchema:
  pathName: /test/endpoint-array
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
            from: ["Person", "Employee"]
            via: CREATED_BY
            to: Person
          implies:
            propertyTypes: []
"""))

# Test 10: Wrapper around entire edgeTypes array
tests.append(("Wrapper around edgeTypes array", True, """
graphSchema:
  pathName: /test/edgetypes-wrapper
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
    abstract:
      edgeTypes:
        - edgeType:
            directed:
              from: Person
              via: RELATIONSHIP
              to: Person
            implies:
              propertyTypes: []
"""))

# Test 11: Two-level wrapper around edgeTypes array
tests.append(("Two-level wrapper around edgeTypes array", True, """
graphSchema:
  pathName: /test/edgetypes-two-level
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
    subtypesOf:
      abstract:
        edgeTypes:
          - edgeType:
              directed:
                from: Person
                via: CONNECTION
                to: Person
              implies:
                propertyTypes: []
"""))

# Test 12: exactlyOf: abstract: combination
tests.append(("exactlyOf: abstract: combination", True, """
graphSchema:
  pathName: /test/exactly-abstract
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - exactlyOf:
          abstract:
            nodeType:
              typeLabel: Asset
              implies:
                propertyTypes:
                  - name: value
                    valueType: FLOAT
"""))

# Test 13: subtypesOf: concrete: combination
tests.append(("subtypesOf: concrete: combination", True, """
graphSchema:
  pathName: /test/subtypes-concrete
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - subtypesOf:
          concrete:
            nodeType:
              typeLabel: Employee
              implies:
                propertyTypes:
                  - name: id
                    valueType: STRING
"""))

# Run all tests
print("=" * 60)
print("Testing Advanced Type Interpretation Wrapper Patterns")
print("=" * 60)
print()

passed = 0
failed = 0

for name, should_pass, yaml_content in tests:
    if test_wrapper_pattern(name, yaml_content, should_pass):
        passed += 1
    else:
        failed += 1
    print()

print("=" * 60)
print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
print("=" * 60)

exit(0 if failed == 0 else 1)
