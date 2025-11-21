#!/usr/bin/env python3
"""
Detailed validation check to see exactly what's failing
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from jsonschema import Draft202012Validator
from grasch.import_preprocessor import preprocess_yaml_with_imports

# Load schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Check one file in detail
file_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml")

print("=" * 70)
print(f"Analyzing: {file_path.name}")
print("=" * 70)

preprocessed = preprocess_yaml_with_imports(file_path)

# Get ALL validation errors
errors = list(validator.iter_errors(preprocessed))

print(f"\nTotal errors: {len(errors)}\n")

# Show all errors
for i, error in enumerate(errors):
    print(f"Error {i+1}:")
    print(f"  Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
    print(f"  Validator: {error.validator}")
    print(f"  Schema path: {'.'.join(str(p) for p in error.schema_path)}")
    
    # For oneOf errors, show which schemas failed
    if error.validator == 'oneOf':
        print(f"  Context: {error.context}")
        if error.context:
            print(f"  Number of failing schemas: {len(error.context)}")
            for j, ctx_error in enumerate(error.context[:3]):
                print(f"    Sub-error {j+1}: {ctx_error.validator} - {ctx_error.message[:100]}")
    else:
        print(f"  Message: {error.message[:200]}")
    
    print()
