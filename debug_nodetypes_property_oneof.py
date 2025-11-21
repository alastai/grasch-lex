#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))
validator = Draft202012Validator(schema)

full_data = json.load(open('preprocessed_minimal.json'))

errors = list(validator.iter_errors(full_data))
root_err = errors[0]

# Navigate to the nodeTypes oneOf error
graphschema_err = root_err.context[2]  # The graphSchema option
nodetypes_err = graphschema_err  # This IS the nodeTypes error

print(f"nodeTypes oneOf error has {len(nodetypes_err.context)} sub-errors:\n")

for i, ctx in enumerate(nodetypes_err.context):
    print(f"Sub-error {i+1}:")
    print(f"  Validator: {ctx.validator}")
    print(f"  Schema path: {'.'.join(str(p) for p in ctx.schema_path)}")
    print(f"  Message: {ctx.message[:150]}")
    
    if ctx.context:
        print(f"  Has {len(ctx.context)} nested errors")
        for j, nested in enumerate(ctx.context[:2]):
            print(f"    {j+1}. {nested.validator}: {nested.message[:80]}")
    print()
