#!/usr/bin/env python3
"""
Test if inline nodeType in endpoints validates
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

# Get a specific edge with inline nodeType
test_file = Path("src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml")
data = preprocess_yaml_with_imports(test_file)
edges = data['graphSchema']['graphType']['edgeTypes']

# Find edge 12 (has inline nodeType)
edge_with_inline = edges[12]

print("Testing edge with inline nodeType:")
print(json.dumps(edge_with_inline, indent=2)[:300])
print("...")

# Validate just this edge
errors = list(validator.iter_errors(edge_with_inline, schema['$defs']['EdgeType']))
if errors:
    print(f"\n✗ {len(errors)} validation error(s):")
    for error in errors:
        print(f"  Path: {'.'.join(str(p) for p in error.relative_path)}")
        print(f"  Validator: {error.validator}")
        print(f"  Message: {error.message[:150]}")
else:
    print("\n✓ Edge validates successfully")
