#!/usr/bin/env python3
"""Validate all updated wrapper files."""

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
    'src/grasch/examples/lex-2026.0.3.2-type-interpretation-wrappers-example.yaml',
]

print("Validating updated wrapper files...")
print("=" * 80)

all_passed = True

for filepath in files_to_validate:
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        validate(instance=data, schema=schema)
        print(f"✅ {filepath.split('/')[-1]}")
    except ValidationError as e:
        print(f"❌ {filepath.split('/')[-1]}")
        print(f"   Error: {e.message[:100]}")
        all_passed = False
    except Exception as e:
        print(f"⚠️  {filepath.split('/')[-1]}")
        print(f"   Error: {str(e)[:100]}")
        all_passed = False

print("=" * 80)
if all_passed:
    print("✅ All wrapper files validated successfully!")
    print("\nThese files have been updated with correct edge label structure:")
    print("  - Edge labels are now objects with typeLabel: as required child")
    print("  - implies:/extends:/adding: are children of edge label objects")
    print("  - All files use graphSchema wrapper with proper structure")
else:
    print("❌ Some files failed validation")
