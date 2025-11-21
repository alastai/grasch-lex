#!/usr/bin/env python3
"""
Test if GraphSchemaContent validates correctly
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

# Get the GraphSchemaContent definition
graphschema_schema = schema['$defs']['GraphSchemaContent']

# Create a validator for just GraphSchemaContent
validator = Draft202012Validator(graphschema_schema, resolver=Draft202012Validator(schema).resolver)

# Test with a passing file
print("Testing minimal-test (PASSES):")
test1 = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")
data1 = preprocess_yaml_with_imports(test1)
graphschema1 = data1['graphSchema']

errors1 = list(validator.iter_errors(graphschema1))
if errors1:
    print(f"  ✗ {len(errors1)} errors in GraphSchemaContent")
    for error in errors1[:2]:
        print(f"    Path: {'.'.join(str(p) for p in error.relative_path)}")
        print(f"    {error.validator}: {error.message[:100]}")
else:
    print("  ✓ GraphSchemaContent validates")

# Test with a failing file
print("\nTesting all-import-patterns (FAILS):")
test2 = Path("src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml")
data2 = preprocess_yaml_with_imports(test2)
graphschema2 = data2['graphSchema']

errors2 = list(validator.iter_errors(graphschema2))
if errors2:
    print(f"  ✗ {len(errors2)} errors in GraphSchemaContent")
    for error in errors2[:3]:
        print(f"    Path: {'.'.join(str(p) for p in error.relative_path)}")
        print(f"    {error.validator}: {error.message[:100]}")
else:
    print("  ✓ GraphSchemaContent validates")
