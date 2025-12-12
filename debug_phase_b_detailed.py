#!/usr/bin/env python3
"""Debug Phase B validation with detailed error reporting"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
TEST_PATH = Path("src/grasch/examples/test-phase-b-edgetype-ti.yaml")

def main():
    print("=" * 70)
    print("PHASE B DETAILED VALIDATION DEBUG")
    print("=" * 70)
    
    # Load schema
    print(f"\nLoading schema: {SCHEMA_PATH}")
    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)
    print("✓ Schema loaded")
    
    # Load test YAML
    print(f"\nLoading test file: {TEST_PATH}")
    with open(TEST_PATH, 'r') as f:
        test_data = yaml.safe_load(f)
    print("✓ Test file loaded")
    
    # Validate
    print("\nValidating with detailed errors...")
    resolver = RefResolver.from_schema(schema)
    validator = Draft202012Validator(schema, resolver=resolver)
    
    errors = list(validator.iter_errors(test_data))
    
    if errors:
        print(f"\n❌ VALIDATION FAILED with {len(errors)} errors\n")
        for i, error in enumerate(errors):
            print(f"Error {i+1}:")
            print(f"  Path: {' -> '.join(str(p) for p in error.path) if error.path else 'ROOT'}")
            print(f"  Validator: {error.validator}")
            print(f"  Schema Path: {' -> '.join(str(p) for p in error.schema_path) if error.schema_path else 'ROOT'}")
            print(f"  Message: {error.message}")
            if hasattr(error, 'validator_value'):
                print(f"  Validator Value: {error.validator_value}")
            print(f"  Failed Value: {error.instance}")
            print("-" * 50)
        return False
    else:
        print("\n✅ VALIDATION PASSED!")
        return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)