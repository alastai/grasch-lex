#!/usr/bin/env python3
"""
Debug why nodeTypes oneOf fails
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

# Get the nodeTypes schema from GraphType
graphtype_schema = schema['$defs']['GraphType']
nodetypes_schema = graphtype_schema['properties']['nodeTypes']

print("nodeTypes oneOf pattern:")
print(json.dumps(nodetypes_schema, indent=2)[:1000])
print("\n...")

# Test with failing file
test_file = Path("src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml")
data = preprocess_yaml_with_imports(test_file)
nodetypes_value = data['graphSchema']['graphType']['nodeTypes']

print(f"\nActual nodeTypes value type: {type(nodetypes_value)}")
print(f"Is array: {isinstance(nodetypes_value, list)}")
if isinstance(nodetypes_value, list):
    print(f"Array length: {len(nodetypes_value)}")
    print(f"First item type: {type(nodetypes_value[0])}")
    print(f"First item keys: {list(nodetypes_value[0].keys())}")
    print(f"First item: {json.dumps(nodetypes_value[0], indent=2)[:200]}")

# Try to validate against each oneOf option
validator = Draft202012Validator(schema)

print("\n" + "=" * 60)
print("Testing against each oneOf option:")
print("=" * 60)

for i, option in enumerate(nodetypes_schema['oneOf']):
    print(f"\nOption {i+1}:")
    print(f"  Type: {option.get('type', 'N/A')}")
    print(f"  Description: {option.get('description', 'N/A')[:60]}")
    
    # Create a validator for this specific option
    option_validator = Draft202012Validator(option, resolver=validator.resolver)
    errors = list(option_validator.iter_errors(nodetypes_value))
    
    if errors:
        print(f"  ✗ FAILS with {len(errors)} error(s):")
        for error in errors[:2]:
            print(f"    - {error.validator}: {error.message[:80]}")
    else:
        print(f"  ✓ PASSES")
