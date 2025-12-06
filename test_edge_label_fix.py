#!/usr/bin/env python3
"""Test validation of updated edge label files"""

import yaml
import jsonschema
import json

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'r') as f:
    schema = json.load(f)

# Files to test
test_files = [
    'src/grasch/examples/test-edge-directed-via.yaml',
    'src/grasch/examples/test-edge-directed-arc.yaml',
    'src/grasch/examples/test-edge-directed-typelabel.yaml',
    'src/grasch/examples/test-edge-undirected-via.yaml',
    'src/grasch/examples/test-edge-undirected-typelabel.yaml',
    'src/grasch/examples/test-edge-mixed-synonyms.yaml',
    'src/grasch/examples/test-edge-property-ordering.yaml',
    'src/grasch/examples/test-edge-extends-adding.yaml',
]

print("Testing edge label container fix...")
print("=" * 60)

passed = 0
failed = 0

for filepath in test_files:
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        # Validate against schema
        jsonschema.validate(instance=data, schema=schema)
        print(f"✅ PASS: {filepath.split('/')[-1]}")
        passed += 1
    except jsonschema.ValidationError as e:
        print(f"❌ FAIL: {filepath.split('/')[-1]}")
        print(f"   Error: {e.message[:100]}")
        failed += 1
    except Exception as e:
        print(f"❌ ERROR: {filepath.split('/')[-1]}")
        print(f"   Error: {str(e)[:100]}")
        failed += 1

print("=" * 60)
print(f"Results: {passed} passed, {failed} failed")
