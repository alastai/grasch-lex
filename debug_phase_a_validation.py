#!/usr/bin/env python3
"""Debug Phase A validation"""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
TEST_PATH = Path("src/grasch/examples/test-phase-a-nodetype-ti.yaml")

def main():
    # Load schema
    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)
    
    # Load test YAML
    with open(TEST_PATH, 'r') as f:
        test_data = yaml.safe_load(f)
    
    # Check what the root schema expects
    print("Root schema oneOf options:")
    for i, option in enumerate(schema["oneOf"]):
        print(f"\n{i+1}. Required: {option.get('required', [])}")
        if "properties" in option:
            for prop_name in option["properties"]:
                print(f"   - {prop_name}: {option['properties'][prop_name]}")
    
    print("\n" + "="*60)
    print("Test data root keys:", list(test_data.keys()))
    
    # Try to validate
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(test_data))
    
    print(f"\nTotal errors: {len(errors)}")
    
    if errors:
        print("\nFirst few errors:")
        for i, error in enumerate(errors[:3]):
            print(f"\n{i+1}. Path: {list(error.path)}")
            print(f"   Message: {error.message}")
            print(f"   Validator: {error.validator}")
            if error.validator_value:
                print(f"   Validator value: {error.validator_value}")

if __name__ == "__main__":
    main()
