#!/usr/bin/env python3
"""Minimal test to understand Location 3 validation failure"""

import json
import yaml
from jsonschema import validate, ValidationError

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json') as f:
    schema = json.load(f)

# Minimal test document
test_doc = {
    'graphSchema': {
        'pathName': '/test/minimal',
        'graphType': {
            'propertyGraphDataModel': {
                'import': 'imports/lex-2026.0.3.2-property-graph-data-model-defaults.yaml'
            },
            'nodeTypes': [
                {
                    'nodeType': {
                        'typeLabel': 'Person'
                    }
                }
            ],
            'concrete': {
                'edgeTypes': [
                    {
                        'edgeType': {
                            'undirected': {
                                'between': {
                                    'nodeType': {
                                        'typeLabel': 'Person'
                                    }
                                },
                                'and': {
                                    'nodeType': {
                                        'typeLabel': 'Person'
                                    }
                                },
                                'via': {
                                    'typeLabel': 'KNOWS'
                                }
                            }
                        }
                    }
                ]
            }
        }
    }
}

print("Testing minimal document with concrete: { edgeTypes: [...] }")
print("=" * 70)

try:
    validate(instance=test_doc, schema=schema)
    print("✅ VALID - Document validates successfully!")
except ValidationError as e:
    print(f"❌ INVALID - Validation error:")
    print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
    print(f"   Message: {e.message}")
    print(f"\n   Schema path: {' -> '.join(str(p) for p in e.schema_path)}")
    if e.context:
        print(f"\n   Context errors ({len(e.context)} errors):")
        for ctx_err in e.context[:5]:  # Show first 5
            print(f"     - {ctx_err.message}")
