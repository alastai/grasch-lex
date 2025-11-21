#!/usr/bin/env python3
"""Test minimal C form validation to isolate the issue."""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

# Load schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Load C form
c_file = Path("src/grasch/examples/CANON_lex-2026.0.3.2-minimal-import-example.yaml")
with open(c_file, 'r') as f:
    c_data = yaml.safe_load(f)

print("Testing C form validation...")
print()

# Create validator
validator = Draft202012Validator(schema)

# Get all errors
errors = list(validator.iter_errors(c_data))

print(f"Total errors: {len(errors)}")
print()

if errors:
    for i, error in enumerate(errors[:5], 1):
        print(f"Error {i}:")
        print(f"  Validator: {error.validator}")
        print(f"  Path: {list(error.absolute_path)}")
        print(f"  Schema path: {list(error.schema_path)}")
        print(f"  Message: {error.message[:200]}")
        
        # For oneOf errors, show which branches failed
        if error.validator == 'oneOf':
            print(f"  Context: {len(error.context)} sub-errors")
            for j, sub_error in enumerate(error.context[:3], 1):
                print(f"    Sub-error {j}:")
                print(f"      Validator: {sub_error.validator}")
                print(f"      Message: {sub_error.message[:100]}")
        print()

# Try validating just the graphSchema content
print("="*80)
print("Testing just graphSchema content...")
print()

if 'graphSchema' in c_data:
    graph_schema_content = c_data['graphSchema']
    
    # Get the GraphSchemaContent definition
    graph_schema_def = schema['$defs']['GraphSchemaContent']
    
    # Create validator for just this part
    gs_validator = Draft202012Validator(graph_schema_def, resolver=validator.resolver)
    gs_errors = list(gs_validator.iter_errors(graph_schema_content))
    
    print(f"GraphSchemaContent errors: {len(gs_errors)}")
    
    if gs_errors:
        for i, error in enumerate(gs_errors[:3], 1):
            print(f"  Error {i}:")
            print(f"    Path: {list(error.absolute_path)}")
            print(f"    Message: {error.message[:150]}")
    else:
        print("  ✅ GraphSchemaContent validates!")

# Try validating just the graphType
print()
print("="*80)
print("Testing just graphType...")
print()

if 'graphSchema' in c_data and 'graphType' in c_data['graphSchema']:
    graph_type = c_data['graphSchema']['graphType']
    
    # Get the GraphType definition
    graph_type_def = schema['$defs']['GraphType']
    
    # Create validator for just this part
    gt_validator = Draft202012Validator(graph_type_def, resolver=validator.resolver)
    gt_errors = list(gt_validator.iter_errors(graph_type))
    
    print(f"GraphType errors: {len(gt_errors)}")
    
    if gt_errors:
        for i, error in enumerate(gt_errors[:5], 1):
            print(f"  Error {i}:")
            print(f"    Path: {list(error.absolute_path)}")
            print(f"    Validator: {error.validator}")
            print(f"    Message: {error.message[:150]}")
    else:
        print("  ✅ GraphType validates!")
