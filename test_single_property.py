#!/usr/bin/env python3
"""Test single property (edgeTypes only)."""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator, RefResolver

def main():
    # Load schema
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        full_schema = json.load(f)
    
    # Extract just the GraphType definition
    graphtype_schema = full_schema['$defs']['GraphType']
    
    # Load test file
    test_file = Path("test_edgetypes_only.yaml")
    with open(test_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Extract just the graphType
    graphtype_data = data['graphSchema']['graphType']
    
    print(f"Testing graphType from: {test_file.name}")
    print("="*70)
    print("\nGraphType structure:")
    print(f"  - propertyGraphDataModel: {bool(graphtype_data.get('propertyGraphDataModel'))}")
    print(f"  - nodeTypes: {len(graphtype_data.get('nodeTypes', []))} items")
    print(f"  - edgeTypes: {len(graphtype_data.get('edgeTypes', []))} items")
    print()
    
    try:
        # Create resolver for $ref resolution
        resolver = RefResolver.from_schema(full_schema)
        validator = Draft202012Validator(graphtype_schema, resolver=resolver)
        validator.validate(graphtype_data)
        print("✅ VALIDATION PASSED - edgeTypes alone works!")
        return 0
    except ValidationError as e:
        print(f"❌ VALIDATION FAILED")
        print(f"\nError message: {e.message}")
        print(f"\nFailed at path: {list(e.absolute_path)}")
        print(f"\nSchema path: {list(e.absolute_schema_path)}")
        
        if e.context:
            print(f"\nContext errors ({len(e.context)} total):")
            for i, ctx_error in enumerate(e.context[:5], 1):
                print(f"  {i}. {ctx_error.message}")
        
        return 1

if __name__ == "__main__":
    exit(main())
