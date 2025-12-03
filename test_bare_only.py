#!/usr/bin/env python3
"""Test the test-siblings-bare-only.yaml file."""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

def main():
    # Load schema
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    # Load test file
    test_file = Path("src/grasch/examples/test-siblings-bare-only.yaml")
    with open(test_file, 'r') as f:
        data = yaml.safe_load(f)
    
    print(f"Testing: {test_file.name}")
    print("="*70)
    
    try:
        validator = Draft202012Validator(schema)
        validator.validate(data)
        print("✅ VALIDATION PASSED")
        return 0
    except ValidationError as e:
        print(f"❌ VALIDATION FAILED")
        print(f"\nError message: {e.message}")
        print(f"\nFailed at path: {list(e.absolute_path)}")
        print(f"\nSchema path: {list(e.absolute_schema_path)}")
        
        if e.context:
            print(f"\nContext errors:")
            for ctx_error in e.context:
                print(f"  - {ctx_error.message}")
        
        return 1

if __name__ == "__main__":
    exit(main())
