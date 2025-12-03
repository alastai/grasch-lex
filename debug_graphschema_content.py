#!/usr/bin/env python3
"""Debug GraphSchemaContent validation"""

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
    
    # Get GraphSchemaContent definition
    graphschema_content_def = schema["$defs"]["GraphSchemaContent"]
    
    # Try to validate just the graphSchema content
    graphschema_data = test_data["graphSchema"]
    
    print("Validating graphSchema content directly...")
    validator = Draft202012Validator(graphschema_content_def, resolver=Draft202012Validator.ID_OF(schema))
    errors = list(validator.iter_errors(graphschema_data))
    
    print(f"Total errors: {len(errors)}")
    
    if errors:
        print("\nErrors:")
        for i, error in enumerate(errors[:5]):
            print(f"\n{i+1}. Path: {list(error.path)}")
            print(f"   Message: {error.message[:200]}")
            print(f"   Validator: {error.validator}")
            if hasattr(error, 'schema_path'):
                print(f"   Schema path: {list(error.schema_path)}")

if __name__ == "__main__":
    main()
