#!/usr/bin/env python3
"""Test the minimal-import-example in detail."""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

# Load schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path) as f:
    schema = json.load(f)

# Load and preprocess the example
from src.grasch.import_preprocessor import preprocess_imports

example_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml")
with open(example_path) as f:
    data = yaml.safe_load(f)

print("Original data keys:", list(data.keys()))
print()

# Preprocess
preprocessed = preprocess_imports(data, example_path.parent)
print("Preprocessed data keys:", list(preprocessed.keys()))
print()

# Validate
validator = Draft202012Validator(schema)
errors = list(validator.iter_errors(preprocessed))

if errors:
    print(f"Found {len(errors)} validation errors:\n")
    for i, error in enumerate(errors[:5], 1):  # Show first 5
        print(f"Error {i}:")
        print(f"  Path: {' -> '.join(str(p) for p in error.path)}")
        print(f"  Message: {error.message}")
        print(f"  Validator: {error.validator}")
        print()
else:
    print("✓ Validation passed!")
