#!/usr/bin/env python3
"""Investigate the root validation issue"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

def main():
    print("INVESTIGATING ROOT VALIDATION ISSUE\n")
    
    # Load schema
    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)
    
    # Create validator
    resolver = RefResolver.from_schema(schema)
    validator = Draft202012Validator(schema, resolver=resolver)
    
    # Test 1: Minimal catalog
    print("Test 1: Minimal catalog")
    minimal_catalog = {"catalog": {"IRI": "https://example.com/catalog"}}
    errors = list(validator.iter_errors(minimal_catalog))
    print(f"  Result: {'✅ PASS' if not errors else f'❌ FAIL ({len(errors)} errors)'}\n")
    
    # Test 2: Minimal graph
    print("Test 2: Minimal graph")
    minimal_graph = {"graph": {"IRI": "https://example.com/graph"}}
    errors = list(validator.iter_errors(minimal_graph))
    print(f"  Result: {'✅ PASS' if not errors else f'❌ FAIL ({len(errors)} errors)'}\n")
    
    # Test 3: Empty graphSchema
    print("Test 3: Empty graphSchema")
    empty_gs = {"graphSchema": {"graphType": {}}}
    errors = list(validator.iter_errors(empty_gs))
    print(f"  Result: {'✅ PASS' if not errors else f'❌ FAIL ({len(errors)} errors)'}")
    if errors:
        for e in errors[:2]:
            print(f"    Path: {list(e.path)}")
            print(f"    Message: {e.message[:100]}")
    print()
    
    # Test 4: graphSchema with empty nodeTypes
    print("Test 4: graphSchema with empty nodeTypes")
    gs_empty_nodes = {"graphSchema": {"graphType": {"nodeTypes": []}}}
    errors = list(validator.iter_errors(gs_empty_nodes))
    print(f"  Result: {'✅ PASS' if not errors else f'❌ FAIL ({len(errors)} errors)'}")
    if errors:
        for e in errors[:2]:
            print(f"    Path: {list(e.path)}")
            print(f"    Message: {e.message[:100]}")
    print()
    
    # Test 5: graphSchema with one nodeType
    print("Test 5: graphSchema with one nodeType")
    gs_one_node = {
        "graphSchema": {
            "graphType": {
                "nodeTypes": [{
                    "nodeType": {
                        "typeLabel": "Person",
                        "implies": {
                            "labels": ["Person"],
                            "properties": {"name": "STRING"}
                        }
                    }
                }]
            }
        }
    }
    errors = list(validator.iter_errors(gs_one_node))
    print(f"  Result: {'✅ PASS' if not errors else f'❌ FAIL ({len(errors)} errors)'}")
    if errors:
        for i, e in enumerate(errors[:3]):
            print(f"\n    Error {i+1}:")
            print(f"      Path: {list(e.path)}")
            print(f"      Validator: {e.validator}")
            print(f"      Message: {e.message[:120]}")

if __name__ == "__main__":
    main()
