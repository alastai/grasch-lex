#!/usr/bin/env python3
"""
Show the 4 errors that are occurring
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

# Check one file
file_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml")
preprocessed = preprocess_yaml_with_imports(file_path)

errors = list(validator.iter_errors(preprocessed))

print(f"Total errors: {len(errors)}\n")

for i, error in enumerate(errors):
    print(f"=" * 70)
    print(f"Error {i+1}/{len(errors)}")
    print(f"=" * 70)
    print(f"Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
    print(f"Validator: {error.validator}")
    print(f"Message: {error.message[:500]}")
    print()
