#!/usr/bin/env python3
"""
Debug why edgeTypes oneOf fails
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

# Get the edgeTypes schema from GraphType
graphtype_schema = schema['$defs']['GraphType']
edgetypes_schema = graphtype_schema['properties']['edgeTypes']

# Test with failing file
test_file = Path("src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml")
data = preprocess_yaml_with_imports(test_file)
edgetypes_value = data['graphSchema']['graphType']['edgeTypes']

print(f"edgeTypes value type: {type(edgetypes_value)}")
print(f"Is array: {isinstance(edgetypes_value, list)}")
if isinstance(edgetypes_value, list):
    print(f"Array length: {len(edgetypes_value)}")
    print(f"First item type: {type(edgetypes_value[0])}")
    print(f"First item keys: {list(edgetypes_value[0].keys())}")

# Try to validate against each oneOf option
validator = Draft202012Validator(schema)

print("\n" + "=" * 60)
print("Testing against each oneOf option:")
print("=" * 60)

for i, option in enumerate(edgetypes_schema['oneOf']):
    print(f"\nOption {i+1}:")
    print(f"  Type: {option.get('type', 'N/A')}")
    print(f"  Description: {option.get('description', 'N/A')[:60]}")
    
    # Create a validator for this specific option
    option_validator = Draft202012Validator(option, resolver=validator.resolver)
    errors = list(option_validator.iter_errors(edgetypes_value))
    
    if errors:
        print(f"  ✗ FAILS with {len(errors)} error(s):")
        for error in errors[:3]:
            print(f"    - {error.validator}: {error.message[:100]}")
    else:
        print(f"  ✓ PASSES")
