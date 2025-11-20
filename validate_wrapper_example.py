#!/usr/bin/env python3
"""Validate the type interpretation wrappers example file."""

import json
import jsonschema
import yaml
import sys

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2-pre-import.schema.json', 'r') as f:
    schema = json.load(f)

# Load example
with open('src/grasch/examples/lex-2026.0.3.2-type-interpretation-wrappers-example.yaml', 'r') as f:
    example = yaml.safe_load(f)

# Validate
try:
    jsonschema.validate(example, schema)
    print("✓ Type interpretation wrappers example validates successfully!")
    print("\nThe example demonstrates:")
    print("  - Zero-level wrappers (bare references)")
    print("  - One-level wrappers (abstract, concrete, properSubtypesOf)")
    print("  - Two-level wrappers (all four combinations)")
    print("  - Wrappers on both nodeTypes and edgeTypes")
    print("  - Mixed wrapped and unwrapped items in same array")
except jsonschema.ValidationError as e:
    print(f"✗ Validation failed: {e.message}")
    print(f"\nPath: {' -> '.join(str(p) for p in e.path)}")
    sys.exit(1)
