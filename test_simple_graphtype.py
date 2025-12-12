#!/usr/bin/env python3
"""
Test simple GraphType validation with the new schema
"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

def load_schema():
    """Load the schema"""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        return json.load(f)

def test_simple_graphtype():
    """Test a simple GraphType with the new single-level TI system"""
    
    # Simple test case using new single-level TI
    test_data = {
        "graphSchema": {
            "pathName": "/test/simple",
            "graphType": {
                "propertyGraphDataModel": {
                    "valueTypeSystemName": "CANONICAL"
                },
                "nodeTypes": [
                    {
                        "typeLabel": "Person",
                        "implies": {
                            "labels": ["Person"],
                            "propertyTypes": [
                                {
                                    "name": "name",
                                    "valueType": "STRING"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }
    
    print("Loading schema...")
    schema = load_schema()
    
    print("Creating validator...")
    resolver = RefResolver.from_schema(schema)
    validator = Draft202012Validator(schema, resolver=resolver)
    
    print("Validating simple GraphType...")
    errors = list(validator.iter_errors(test_data))
    
    if errors:
        print(f"❌ VALIDATION FAILED with {len(errors)} errors")
        for i, error in enumerate(errors, 1):
            print(f"Error {i}:")
            print(f"  Path: {' -> '.join(str(p) for p in error.absolute_path) or 'ROOT'}")
            print(f"  Validator: {error.validator}")
            print(f"  Message: {error.message}")
            print()
    else:
        print("✅ VALIDATION PASSED!")
        print("Simple GraphType with nodeTypes array works correctly")

if __name__ == "__main__":
    test_simple_graphtype()