#!/usr/bin/env python3
"""
Debug why root GraphSchema documents are failing oneOf validation
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

# Check one failing file in detail
filename = "lex-2026.0.3.2-minimal-import-example.yaml"
file_path = Path(f"src/grasch/examples/{filename}")

print(f"Detailed analysis of: {filename}")
print("=" * 70)

preprocessed = preprocess_yaml_with_imports(file_path)

print(f"Root keys: {list(preprocessed.keys())}")
print(f"Root structure: {type(preprocessed)}")
print()

# Test against each root oneOf option
print("Testing against root oneOf options:")
print()

for i, option in enumerate(schema['oneOf']):
    print(f"Option {i+1}:")
    
    # Show what this option requires
    if 'required' in option:
        print(f"  Required: {option['required']}")
    if 'properties' in option:
        print(f"  Properties: {list(option['properties'].keys())}")
    
    # Test validation
    option_validator = Draft202012Validator(option, resolver=validator.resolver)
    errors = list(option_validator.iter_errors(preprocessed))
    
    if errors:
        print(f"  Result: FAILS")
        for j, error in enumerate(errors[:2]):
            print(f"    Error {j+1}: {error.validator} - {error.message[:100]}")
    else:
        print(f"  Result: PASSES ✓")
    
    print()

# Now check if the graphSchema content itself is valid
print("\nChecking graphSchema content validation:")
print("=" * 70)

if 'graphSchema' in preprocessed:
    gs_content = preprocessed['graphSchema']
    print(f"GraphSchema keys: {list(gs_content.keys())}")
    
    # Try to validate against GraphSchemaContent
    if 'GraphSchemaContent' in schema['$defs']:
        gs_schema = schema['$defs']['GraphSchemaContent']
        gs_validator = Draft202012Validator(gs_schema, resolver=validator.resolver)
        gs_errors = list(gs_validator.iter_errors(gs_content))
        
        if gs_errors:
            print(f"\nGraphSchemaContent validation: FAILS ({len(gs_errors)} errors)")
            for i, error in enumerate(gs_errors[:3]):
                print(f"  Error {i+1}:")
                print(f"    Path: {'.'.join(str(p) for p in error.absolute_path)}")
                print(f"    Validator: {error.validator}")
                print(f"    Message: {error.message[:150]}")
        else:
            print("\nGraphSchemaContent validation: PASSES ✓")
