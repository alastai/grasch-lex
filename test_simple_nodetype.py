#!/usr/bin/env python3
"""Test simple nodeType validation"""

import json
import yaml
from jsonschema import Draft202012Validator, RefResolver

# Simple test with just one bare nodeType
test_yaml = """
graphSchema:
  graphType:
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            labels: [Person]
            properties:
              name: STRING
"""

def main():
    # Load schema
    with open("src/grasch/schemas/lex-2026.0.3.2.schema.json", 'r') as f:
        schema = json.load(f)
    
    # Parse test
    test_data = yaml.safe_load(test_yaml)
    
    # Validate
    resolver = RefResolver.from_schema(schema)
    validator = Draft202012Validator(schema, resolver=resolver)
    
    errors = list(validator.iter_errors(test_data))
    
    if errors:
        print(f"❌ FAILED with {len(errors)} errors")
        for error in errors[:3]:
            print(f"\nPath: {list(error.path)}")
            print(f"Message: {error.message[:200]}")
    else:
        print("✅ PASSED - Simple nodeType validates!")
        
        # Now try with abstract wrapper
        test_yaml2 = """
graphSchema:
  graphType:
    nodeTypes:
      - abstract:
          nodeType:
            typeLabel: Vehicle
            implies:
              labels: [Vehicle]
              properties:
                make: STRING
"""
        test_data2 = yaml.safe_load(test_yaml2)
        errors2 = list(validator.iter_errors(test_data2))
        
        if errors2:
            print(f"\n❌ Abstract wrapper FAILED with {len(errors2)} errors")
            for error in errors2[:2]:
                print(f"\nPath: {list(error.path)}")
                print(f"Message: {error.message[:200]}")
        else:
            print("✅ Abstract wrapper also validates!")

if __name__ == "__main__":
    main()
