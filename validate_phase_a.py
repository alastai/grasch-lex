#!/usr/bin/env python3
"""Validate Phase A test file"""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
TEST_PATH = Path("src/grasch/examples/test-phase-a-nodetype-ti.yaml")

def main():
    print("Phase A Validation Test\n")
    print("=" * 60)
    
    # Load schema
    print(f"Loading schema: {SCHEMA_PATH}")
    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)
    print("✓ Schema loaded\n")
    
    # Load test YAML
    print(f"Loading test file: {TEST_PATH}")
    with open(TEST_PATH, 'r') as f:
        test_data = yaml.safe_load(f)
    print("✓ Test file loaded\n")
    
    # Validate
    print("Validating test file against schema...")
    try:
        validator = Draft202012Validator(schema)
        validator.validate(test_data)
        print("✅ VALIDATION PASSED!")
        print("\nPhase A is successful! The schema now supports:")
        print("  • 0-level (bare) nodeType")
        print("  • 1-level (shorthand) TI wrappers: abstract, concrete, final, sealed")
        print("  • 2-level (explicit) TI wrappers: exactlyOf, subtypesOf, properSubtypesOf")
        return True
    except ValidationError as e:
        print("❌ VALIDATION FAILED!")
        print(f"\nError: {e.message}")
        print(f"Path: {' -> '.join(str(p) for p in e.path)}")
        print(f"\nFailing instance:")
        print(json.dumps(e.instance, indent=2))
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
