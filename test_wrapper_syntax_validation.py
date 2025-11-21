#!/usr/bin/env python3
"""
Test that the updated schema validates type interpretation wrapper syntax correctly.
"""

import json
import jsonschema
import yaml

# Load the updated schema
with open('src/grasch/schemas/lex-2026.0.3.2-pre-import.schema.json', 'r') as f:
    schema = json.load(f)

def validate_yaml(yaml_content, description):
    """Validate a YAML document against the schema."""
    try:
        doc = yaml.safe_load(yaml_content)
        jsonschema.validate(doc, schema)
        print(f"✓ {description}")
        return True
    except jsonschema.ValidationError as e:
        print(f"✗ {description}")
        print(f"  Error: {e.message}")
        return False
    except Exception as e:
        print(f"✗ {description}")
        print(f"  Error: {e}")
        return False

print("Testing Type Interpretation Wrapper Syntax\n")
print("=" * 60)

# Test 1: Zero-level wrapper (bare reference)
test1 = """
graphSchema:
  pathName: /test/schema1
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
"""
validate_yaml(test1, "Test 1: Zero-level wrapper (bare nodeType)")

# Test 2: One-level wrapper - abstract
test2 = """
graphSchema:
  pathName: /test/schema2
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - abstract:
          nodeType:
            typeLabel: Person
            implies:
              propertyTypes: []
"""
validate_yaml(test2, "Test 2: One-level wrapper (abstract)")

# Test 3: One-level wrapper - concrete
test3 = """
graphSchema:
  pathName: /test/schema3
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - concrete:
          nodeType:
            typeLabel: Person
            implies:
              propertyTypes: []
"""
validate_yaml(test3, "Test 3: One-level wrapper (concrete)")

# Test 4: One-level wrapper - properSubtypesOf
test4 = """
graphSchema:
  pathName: /test/schema4
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - properSubtypesOf:
          nodeType:
            typeLabel: Person
            implies:
              propertyTypes: []
"""
validate_yaml(test4, "Test 4: One-level wrapper (properSubtypesOf)")

# Test 5: Two-level wrapper - exactlyOf: concrete
test5 = """
graphSchema:
  pathName: /test/schema5
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - exactlyOf:
          concrete:
            nodeType:
              typeLabel: Person
              implies:
                propertyTypes: []
"""
validate_yaml(test5, "Test 5: Two-level wrapper (exactlyOf: concrete)")

# Test 6: Two-level wrapper - subtypesOf: abstract
test6 = """
graphSchema:
  pathName: /test/schema6
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - subtypesOf:
          abstract:
            nodeType:
              typeLabel: Person
              implies:
                propertyTypes: []
"""
validate_yaml(test6, "Test 6: Two-level wrapper (subtypesOf: abstract)")

# Test 7: Mixed wrapped and unwrapped in same array
test7 = """
graphSchema:
  pathName: /test/schema7
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            propertyTypes: []
      - abstract:
          nodeType:
            typeLabel: Organization
            implies:
              propertyTypes: []
      - concrete:
          nodeType:
            typeLabel: Product
            implies:
              propertyTypes: []
"""
validate_yaml(test7, "Test 7: Mixed wrapped and unwrapped items")

# Test 8: EdgeType with wrapper
test8 = """
graphSchema:
  pathName: /test/schema8
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    edgeTypes:
      - abstract:
          edgeType:
            typeLabel: KNOWS
            implies:
              propertyTypes: []
            direction: DIRECTED
            firstEndpointNodeType:
              typeLabel: Person
            secondEndpointNodeType:
              typeLabel: Person
"""
validate_yaml(test8, "Test 8: EdgeType with abstract wrapper")

# Test 9: All four two-level combinations
test9 = """
graphSchema:
  pathName: /test/schema9
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - exactlyOf:
          concrete:
            nodeType:
              typeLabel: Person
              implies:
                propertyTypes: []
      - exactlyOf:
          abstract:
            nodeType:
              typeLabel: Entity
              implies:
                propertyTypes: []
      - subtypesOf:
          concrete:
            nodeType:
              typeLabel: Company
              implies:
                propertyTypes: []
      - subtypesOf:
          abstract:
            nodeType:
              typeLabel: Organization
              implies:
                propertyTypes: []
"""
validate_yaml(test9, "Test 9: All four two-level combinations")

print("\n" + "=" * 60)
print("Wrapper syntax validation tests complete!")
