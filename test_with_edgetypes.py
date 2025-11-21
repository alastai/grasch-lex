#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))
validator = Draft202012Validator(schema)

# Load the actual preprocessed data
full_data = json.load(open('preprocessed_minimal.json'))

# Test the full data
print("Testing full preprocessed data:")
errors = list(validator.iter_errors(full_data))

if errors:
    print(f"✗ FAILED with {len(errors)} error(s)\n")
    
    # Get the root error
    root_err = errors[0]
    print(f"Root error: {root_err.validator}")
    print(f"Context errors: {len(root_err.context)}\n")
    
    # Find which oneOf option is the graphSchema option
    for i, ctx in enumerate(root_err.context):
        schema_path = '.'.join(str(p) for p in ctx.schema_path)
        if 'graphSchema' in schema_path:
            print(f"GraphSchema option (index {i}):")
            print(f"  Validator: {ctx.validator}")
            print(f"  Path: {'.'.join(str(p) for p in ctx.absolute_path) or 'root'}")
            print(f"  Message: {ctx.message[:200]}")
            
            if ctx.context:
                print(f"  Sub-errors: {len(ctx.context)}")
                for j, sub_ctx in enumerate(ctx.context[:3]):
                    print(f"    {j+1}. {sub_ctx.validator}: {sub_ctx.message[:100]}")
else:
    print("✓ PASSED")
