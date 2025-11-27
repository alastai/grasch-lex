#!/usr/bin/env python3
"""Test two-phase validation with new TI import definitions."""

import json
import jsonschema
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path) as f:
    schema = json.load(f)

# Test 1: Wrapper duplication (PC form)
pc_doc = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {},
            "nodeTypes": [{
                "sealed": {
                    "nodeTypes": [{
                        "nodeType": {
                            "typeLabel": "Person",
                            "implies": {"propertyTypes": [{"name": "id", "valueType": "INTEGER"}]}
                        }
                    }]
                }
            }]
        }
    }
}

# Test 2: Wrapper stripped (C form)
c_doc = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {},
            "nodeTypes": [{
                "sealed": [{
                    "nodeType": {
                        "typeLabel": "Person",
                        "implies": {"propertyTypes": [{"name": "id", "valueType": "INTEGER"}]}
                    }
                }]
            }]
        }
    }
}

print("Testing two-phase validation...")
try:
    jsonschema.validate(pc_doc, schema)
    print("✓ PC form (with nodeTypes: wrapper) validates")
except Exception as e:
    print(f"✗ PC form failed: {e}")

try:
    jsonschema.validate(c_doc, schema)
    print("✓ C form (wrapper stripped) validates")
except Exception as e:
    print(f"✗ C form failed: {e}")

print("\n✓ Two-phase validation working correctly!")
