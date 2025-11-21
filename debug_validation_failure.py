#!/usr/bin/env python3
"""
Debug why preprocessed files fail validation
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

# Test with minimal-test.yaml (which passes)
print("=" * 60)
print("Testing: minimal-test.yaml (PASSES)")
print("=" * 60)

test_file = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")
preprocessed = preprocess_yaml_with_imports(test_file)

errors = list(validator.iter_errors(preprocessed))
if errors:
    print(f"✗ {len(errors)} errors found:")
    for error in errors[:3]:
        print(f"\n  Path: {'.'.join(str(p) for p in error.absolute_path)}")
        print(f"  Message: {error.message}")
        print(f"  Validator: {error.validator}")
else:
    print("✓ No errors - validates successfully")

# Test with all-import-patterns.yaml (which fails)
print("\n" + "=" * 60)
print("Testing: all-import-patterns.yaml (FAILS)")
print("=" * 60)

test_file2 = Path("src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml")
preprocessed2 = preprocess_yaml_with_imports(test_file2)

errors2 = list(validator.iter_errors(preprocessed2))
if errors2:
    print(f"✗ {len(errors2)} errors found:")
    for error in errors2[:3]:
        print(f"\n  Path: {'.'.join(str(p) for p in error.absolute_path)}")
        print(f"  Message: {error.message[:200]}...")
        print(f"  Validator: {error.validator}")
        if error.schema_path:
            print(f"  Schema path: {'.'.join(str(p) for p in error.schema_path)}")
else:
    print("✓ No errors - validates successfully")

# Compare structures
print("\n" + "=" * 60)
print("Structure Comparison")
print("=" * 60)

print("\nminimal-test (PASSES):")
print(f"  Keys: {list(preprocessed.keys())}")
if 'graphSchema' in preprocessed:
    gs = preprocessed['graphSchema']
    print(f"  graphSchema keys: {list(gs.keys())}")
    if 'graphType' in gs:
        gt = gs['graphType']
        print(f"  graphType keys: {list(gt.keys())}")

print("\nall-import-patterns (FAILS):")
print(f"  Keys: {list(preprocessed2.keys())}")
if 'graphSchema' in preprocessed2:
    gs2 = preprocessed2['graphSchema']
    print(f"  graphSchema keys: {list(gs2.keys())}")
    if 'graphType' in gs2:
        gt2 = gs2['graphType']
        print(f"  graphType keys: {list(gt2.keys())}")
