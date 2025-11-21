#!/usr/bin/env python3
"""
Get detailed error information
"""
import json
import yaml
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

# Test with all-import-patterns.yaml
test_file = Path("src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml")
preprocessed = preprocess_yaml_with_imports(test_file)

errors = list(validator.iter_errors(preprocessed))
if errors:
    print(f"Found {len(errors)} errors\n")
    for i, error in enumerate(errors):
        print(f"Error {i+1}:")
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
        print(f"  Validator: {error.validator}")
        print(f"  Message: {error.message[:500]}")
        
        # Check which oneOf option failed
        if error.validator == 'oneOf' and hasattr(error, 'context'):
            print(f"\n  oneOf context ({len(error.context)} sub-errors):")
            for j, sub_error in enumerate(error.context[:3]):
                print(f"    Option {j+1}: {sub_error.validator} - {sub_error.message[:100]}")
        
        print()
