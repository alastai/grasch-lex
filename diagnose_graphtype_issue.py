#!/usr/bin/env python3
"""
Diagnose why GraphType validation is failing after canonicalization.
"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

# Load schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Load a simple canonical example
canon_path = Path("src/grasch/examples/CANON_lex-2026.0.3.2-minimal-test.yaml")
with open(canon_path, 'r') as f:
    data = yaml.safe_load(f)

print("="*80)
print("DIAGNOSING GRAPHTYPE VALIDATION ISSUE")
print("="*80)
print()

# Check what the graphType property schema looks like
print("GraphSchemaContent.graphType schema:")
print("-"*80)
graphschema_content = schema['$defs']['GraphSchemaContent']
graphtype_prop = graphschema_content['properties']['graphType']
print(json.dumps(graphtype_prop, indent=2))
print()

# Check if GraphType definition exists
print("GraphType definition exists:", 'GraphType' in schema['$defs'])
print()

# Try to validate just the graphType part
print("Validating graphType content:")
print("-"*80)
graphtype_data = data['graphSchema']['graphType']
print("GraphType data keys:", list(graphtype_data.keys()))
print()

# Validate against GraphType definition directly
graphtype_def = schema['$defs']['GraphType']
graphtype_validator = Draft202012Validator(graphtype_def)
graphtype_errors = list(graphtype_validator.iter_errors(graphtype_data))

if graphtype_errors:
    print("❌ GraphType validation FAILED:")
    for error in graphtype_errors:
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path)}")
        print(f"  Error: {error.message}")
        print()
else:
    print("✅ GraphType validates against GraphType definition")
    print()

# Now validate against the oneOf wrapper
print("Validating against GraphSchemaContent.graphType oneOf:")
print("-"*80)
graphtype_prop_validator = Draft202012Validator(graphtype_prop)
graphtype_prop_errors = list(graphtype_prop_validator.iter_errors(graphtype_data))

if graphtype_prop_errors:
    print("❌ GraphType validation FAILED against oneOf:")
    for error in graphtype_prop_errors:
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path)}")
        print(f"  Error: {error.message}")
        print()
        
        # Check which oneOf options failed
        if hasattr(error, 'context') and error.context:
            print("  OneOf failures:")
            for i, ctx_error in enumerate(error.context):
                print(f"    Option {i}: {ctx_error.message}")
        print()
else:
    print("✅ GraphType validates against oneOf wrapper")
    print()

# Validate the full document
print("Validating full document:")
print("-"*80)
full_errors = list(validator.iter_errors(data))

if full_errors:
    print(f"❌ Full document validation FAILED ({len(full_errors)} errors)")
    for error in full_errors[:3]:  # Show first 3 errors
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path)}")
        print(f"  Error: {error.message[:200]}")
        print()
else:
    print("✅ Full document validates")
