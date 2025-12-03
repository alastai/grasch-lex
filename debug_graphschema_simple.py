#!/usr/bin/env python3
"""Simple debug of GraphSchemaContent validation"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
TEST_PATH = Path("src/grasch/examples/test-phase-a-nodetype-ti.yaml")

def main():
    # Load schema
    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)
    
    # Load test YAML
    with open(TEST_PATH, 'r') as f:
        test_data = yaml.safe_load(f)
    
    # Create validator with resolver
    resolver = RefResolver.from_schema(schema)
    validator = Draft202012Validator(schema, resolver=resolver)
    
    # Validate and collect errors
    errors = list(validator.iter_errors(test_data))
    
    print(f"Total validation errors: {len(errors)}\n")
    
    # Group errors by path
    error_paths = {}
    for error in errors:
        path_str = " -> ".join(str(p) for p in error.path) if error.path else "root"
        if path_str not in error_paths:
            error_paths[path_str] = []
        error_paths[path_str].append(error.message[:150])
    
    # Show unique error locations
    print("Error locations:")
    for path, messages in sorted(error_paths.items())[:10]:
        print(f"\n{path}:")
        for msg in messages[:2]:
            print(f"  - {msg}")

if __name__ == "__main__":
    main()
