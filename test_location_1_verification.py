#!/usr/bin/env python3
"""
Verify that Location 1 (GraphSchemaContent) already supports TI wrappers.
"""

import json
import yaml
from jsonschema import validate, ValidationError

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'r') as f:
    schema = json.load(f)

# Test 1: Bare graphType (0-level)
test_bare = {
    "graphSchema": {
        "pathName": "/test/bare",
        "graphType": {
            "propertyGraphDataModel": {
                "valueTypeSystemName": "CANONICAL"
            },
            "nodeTypes": [
                {
                    "nodeType": {
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
                }
            ]
        }
    }
}

# Test 2: 1-level TI wrapper
test_one_level = {
    "graphSchema": {
        "pathName": "/test/one-level",
        "abstract": {
            "graphType": {
                "propertyGraphDataModel": {
                    "valueTypeSystemName": "CANONICAL"
                },
                "nodeTypes": [
                    {
                        "nodeType": {
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
                    }
                ]
            }
        }
    }
}

# Test 3: 2-level TI wrapper
test_two_level = {
    "graphSchema": {
        "pathName": "/test/two-level",
        "subtypesOf": {
            "abstract": {
                "graphType": {
                    "propertyGraphDataModel": {
                        "valueTypeSystemName": "CANONICAL"
                    },
                    "nodeTypes": [
                        {
                            "nodeType": {
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
                        }
                    ]
                }
            }
        }
    }
}

tests = [
    ("Bare graphType (0-level)", test_bare),
    ("1-level TI wrapper (abstract)", test_one_level),
    ("2-level TI wrapper (subtypesOf/abstract)", test_two_level)
]

print("Testing Location 1 (GraphSchemaContent) TI wrapper support...")
print("=" * 70)

all_passed = True
for name, test_data in tests:
    try:
        validate(instance=test_data, schema=schema)
        print(f"✓ {name}: PASS")
    except ValidationError as e:
        print(f"✗ {name}: FAIL")
        print(f"  Error: {e.message}")
        print(f"  Path: {list(e.path)}")
        all_passed = False

print("=" * 70)
if all_passed:
    print("SUCCESS: Location 1 already supports TI wrappers!")
else:
    print("FAILURE: Location 1 needs fixing")
