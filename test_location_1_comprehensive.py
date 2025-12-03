#!/usr/bin/env python3
"""
Comprehensive test for Location 1 (GraphSchemaContent):
1. Positive tests: 0-level, 1-level, 2-level graphType (should all pass)
2. Negative test: Multiple graphTypes (should fail)
"""

import json
from jsonschema import validate, ValidationError

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'r') as f:
    schema = json.load(f)

# Minimal valid graphType content
minimal_graphtype = {
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

# POSITIVE TESTS
positive_tests = [
    ("0-level (bare graphType)", {
        "graphSchema": {
            "pathName": "/test/bare",
            "graphType": minimal_graphtype
        }
    }),
    ("1-level (abstract wrapper)", {
        "graphSchema": {
            "pathName": "/test/one-level",
            "abstract": {
                "graphType": minimal_graphtype
            }
        }
    }),
    ("2-level (subtypesOf/abstract wrapper)", {
        "graphSchema": {
            "pathName": "/test/two-level",
            "subtypesOf": {
                "abstract": {
                    "graphType": minimal_graphtype
                }
            }
        }
    })
]

# NEGATIVE TESTS
negative_tests = [
    ("Two graphTypes: bare + abstract (should fail)", {
        "graphSchema": {
            "pathName": "/test/invalid",
            "graphType": minimal_graphtype,
            "abstract": {
                "graphType": minimal_graphtype
            }
        }
    }),
    ("No graphType at all (should fail)", {
        "graphSchema": {
            "pathName": "/test/invalid"
        }
    }),
    ("Two graphTypes: bare + 2-level (should fail)", {
        "graphSchema": {
            "pathName": "/test/invalid",
            "graphType": minimal_graphtype,
            "subtypesOf": {
                "abstract": {
                    "graphType": minimal_graphtype
                }
            }
        }
    })
]

print("=" * 70)
print("LOCATION 1 COMPREHENSIVE TEST")
print("=" * 70)

print("\n" + "=" * 70)
print("POSITIVE TESTS (should all PASS)")
print("=" * 70)

all_positive_passed = True
for name, test_data in positive_tests:
    try:
        validate(instance=test_data, schema=schema)
        print(f"✓ {name}: PASS")
    except ValidationError as e:
        print(f"✗ {name}: FAIL")
        print(f"  Error: {e.message}")
        all_positive_passed = False

print("\n" + "=" * 70)
print("NEGATIVE TESTS (should all FAIL)")
print("=" * 70)

all_negative_failed = True
for name, test_data in negative_tests:
    try:
        validate(instance=test_data, schema=schema)
        print(f"✗ {name}: INCORRECTLY PASSED (should have failed!)")
        all_negative_failed = False
    except ValidationError as e:
        print(f"✓ {name}: CORRECTLY FAILED")
        print(f"  Reason: {e.message[:100]}...")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if all_positive_passed and all_negative_failed:
    print("✅ ALL TESTS PASSED")
    print("   - All valid forms accepted (0/1/2-level)")
    print("   - All invalid forms rejected (multiple/zero graphTypes)")
else:
    print("❌ SOME TESTS FAILED")
    if not all_positive_passed:
        print("   - Some valid forms were rejected")
    if not all_negative_failed:
        print("   - Some invalid forms were accepted")
