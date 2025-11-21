#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))
full_data = json.load(open('preprocessed_minimal.json'))

# Get the items oneOf schema
gt = schema['$defs']['GraphType']
items_oneof_schema = gt['properties']['nodeTypes']['oneOf'][0]['items']['oneOf']

# Get the first nodeType item from the data
first_item = full_data['graphSchema']['graphType']['nodeTypes'][0]

print("First nodeType item:")
print(json.dumps(first_item, indent=2)[:300])
print("\n" + "=" * 70)

# Test against each oneOf option
for i, option_schema in enumerate(items_oneof_schema):
    validator = Draft202012Validator(option_schema)
    errors = list(validator.iter_errors(first_item))
    
    req = option_schema.get('required', [])
    desc = option_schema.get('description', 'no desc')[:40]
    
    if errors:
        print(f"{i}. ✗ required={req}, desc={desc}")
        print(f"   Errors: {len(errors)}")
        for err in errors[:2]:
            print(f"     - {err.validator}: {err.message[:60]}")
    else:
        print(f"{i}. ✓ MATCH! required={req}, desc={desc}")
