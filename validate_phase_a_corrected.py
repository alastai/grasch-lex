#!/usr/bin/env python3
"""Validate Phase A corrected test file"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
TEST_PATH = Path("src/grasch/examples/test-phase-a-corrected.yaml")

def main():
    print("=" * 70)
    print("PHASE A VALIDATION TEST - CORRECTED SYNTAX")
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
    
    # Count nodeTypes
    node_types = test_data['graphSchema']['graphType']['nodeTypes']
    print(f"\nTest file contains {len(node_types)} nodeType definitions")
    
    # Validate
    print("\nValidating...")
    resolver = RefResolver.from_schema(schema)
    validator = Draft202012Validator(schema, resolver=resolver)
    
    errors = list(validator.iter_errors(test_data))
    
    if errors:
        print(f"\n❌ VALIDATION FAILED with {len(errors)} errors\n")
        for i, error in enumerate(errors[:5]):
            print(f"Error {i+1}:")
            print(f"  Path: {' -> '.join(str(p) for p in error.path) if error.path else 'ROOT'}")
            print(f"  Validator: {error.validator}")
            print(f"  Message: {error.message[:150]}")
            print()
        return False
    else:
        print("\n" + "=" * 70)
        print("✅ VALIDATION PASSED!")
        print("=" * 70)
        print("\nPhase A is COMPLETE! The schema now supports:")
        print("  • 0-level (bare) nodeType")
        print("  • 1-level (shorthand) TI wrappers:")
        print("    - abstract")
        print("    - concrete")
        print("    - final")
        print("    - properSubtypesOf")
        print("  • 2-level (explicit) TI wrappers:")
        print("    - exactlyOf: {concrete/abstract}")
        print("    - subtypesOf: {concrete/abstract}")
        print("    - properSubtypesOf: {concrete/abstract} ← NEW!")
        print("\n" + "=" * 70)
        return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
