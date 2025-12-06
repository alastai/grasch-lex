#!/usr/bin/env python3
"""Test whether the schema supports sibling TI wrappers like abstract:nodeTypes and concrete:edgeTypes"""

import json
import yaml
from jsonschema import validate, ValidationError

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'r') as f:
    schema = json.load(f)

# Test 1: Can we have abstract:nodeTypes and concrete:edgeTypes as siblings?
test1 = {
    "graphSchema": {
        "pathName": "/test/sibling-ti",
        "graphType": {
            "propertyGraphDataModel": {
                "import": "imports/lex-2026.0.3.2-property-graph-data-model-defaults.yaml"
            },
            "abstract": {
                "nodeTypes": [
                    {"nodeType": {"typeLabel": "Entity"}}
                ]
            },
            "concrete": {
                "edgeTypes": [
                    {"edgeType": {
                        "typeLabel": "RELATES_TO",
                        "undirected": {
                            "between": {"nodeType": {"typeLabel": "Entity"}},
                            "and": {"nodeType": {"typeLabel": "Entity"}},
                            "via": {"typeLabel": "RELATES_TO"}
                        }
                    }}
                ]
            }
        }
    }
}

print("=" * 80)
print("Test 1: abstract:nodeTypes + concrete:edgeTypes as siblings")
print("=" * 80)
try:
    validate(instance=test1, schema=schema)
    print("✅ VALID - Schema supports sibling TI wrappers")
except ValidationError as e:
    print(f"❌ INVALID - Schema does NOT support sibling TI wrappers")
    print(f"Error: {e.message}")
    print()

# Test 2: What about bare nodeTypes + concrete:edgeTypes?
test2 = {
    "graphSchema": {
        "pathName": "/test/mixed-ti",
        "graphType": {
            "propertyGraphDataModel": {
                "import": "imports/lex-2026.0.3.2-property-graph-data-model-defaults.yaml"
            },
            "nodeTypes": [
                {"nodeType": {"typeLabel": "Person"}}
            ],
            "concrete": {
                "edgeTypes": [
                    {"edgeType": {
                        "typeLabel": "KNOWS",
                        "undirected": {
                            "between": {"nodeType": {"typeLabel": "Person"}},
                            "and": {"nodeType": {"typeLabel": "Person"}},
                            "via": {"typeLabel": "KNOWS"}
                        }
                    }}
                ]
            }
        }
    }
}

print("=" * 80)
print("Test 2: bare nodeTypes + concrete:edgeTypes")
print("=" * 80)
try:
    validate(instance=test2, schema=schema)
    print("✅ VALID - Schema supports bare + TI wrapper mix")
except ValidationError as e:
    print(f"❌ INVALID - Schema does NOT support bare + TI wrapper mix")
    print(f"Error: {e.message}")
    print()

# Test 3: What DOES work? subtypesOf with nested abstract?
test3 = {
    "graphSchema": {
        "pathName": "/test/subtypesof-abstract",
        "graphType": {
            "propertyGraphDataModel": {
                "import": "imports/lex-2026.0.3.2-property-graph-data-model-defaults.yaml"
            },
            "subtypesOf": {
                "abstract": {
                    "nodeTypes": [
                        {"nodeType": {"typeLabel": "Entity"}}
                    ],
                    "edgeTypes": [
                        {"edgeType": {
                            "typeLabel": "RELATES_TO",
                            "undirected": {
                                "between": {"nodeType": {"typeLabel": "Entity"}},
                                "and": {"nodeType": {"typeLabel": "Entity"}},
                                "via": {"typeLabel": "RELATES_TO"}
                            }
                        }}
                    ]
                }
            }
        }
    }
}

print("=" * 80)
print("Test 3: subtypesOf:abstract with both nodeTypes and edgeTypes nested")
print("=" * 80)
try:
    validate(instance=test3, schema=schema)
    print("✅ VALID - Schema supports subtypesOf:abstract pattern")
except ValidationError as e:
    print(f"❌ INVALID - Schema does NOT support subtypesOf:abstract pattern")
    print(f"Error: {e.message}")
