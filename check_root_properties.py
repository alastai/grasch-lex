#!/usr/bin/env python3
"""Check what properties exist at root level of C form."""

import yaml
from pathlib import Path

c_file = Path("src/grasch/examples/CANON_lex-2026.0.3.2-minimal-import-example.yaml")
with open(c_file, 'r') as f:
    c_data = yaml.safe_load(f)

print("Root level properties:")
print(list(c_data.keys()))
print()

# Check if it's ONLY graphSchema
if list(c_data.keys()) == ['graphSchema']:
    print("✅ Only has 'graphSchema' key - should match schema")
else:
    print("❌ Has additional keys beyond 'graphSchema'")
    
# Now validate just the structure
import json
from jsonschema import Draft202012Validator

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Check which oneOf branch it should match
print("\nChecking oneOf branches:")
for i, branch in enumerate(schema['oneOf'], 1):
    required = branch.get('required', [])
    print(f"  Branch {i}: requires {required}")
    if required[0] in c_data:
        print(f"    ✅ Matches (has '{required[0]}')")
        
        # Try validating against just this branch
        branch_validator = Draft202012Validator(branch)
        branch_errors = list(branch_validator.iter_errors(c_data))
        if branch_errors:
            print(f"    ❌ But has {len(branch_errors)} validation errors:")
            for error in branch_errors[:3]:
                print(f"       - {error.message[:100]}")
        else:
            print(f"    ✅ Validates against this branch!")
