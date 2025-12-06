#!/usr/bin/env python3
"""Validate the three updated wrapper files."""

import json
import yaml
from jsonschema import validate, ValidationError

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'r') as f:
    schema = json.load(f)

files_to_validate = [
    'src/grasch/examples/lex-2026.0.3.2-comprehensive-wrappers.yaml',
    'src/grasch/examples/lex-2026.0.3.2-two-level-wrappers.yaml',
    'src/grasch/examples/lex-2026.0.3.2-zero-level-wrappers.yaml',
]

print("Validating updated files...")
print("=" * 80)

all_passed = True

for filepath in files_to_validate:
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        validate(instance=data, schema=schema)
        print(f"✅ {filepath}")
    except ValidationError as e:
        print(f"❌ {filepath}")
        print(f"   Error: {e.message}")
        print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
        all_passed = False
    except Exception as e:
        print(f"⚠️  {filepath}")
        print(f"   Error: {e}")
        all_passed = False

print("=" * 80)
if all_passed:
    print("✅ All files validated successfully!")
else:
    print("❌ Some files failed validation")
