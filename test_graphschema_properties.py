#!/usr/bin/env python3
"""
Check what properties graphSchema has after preprocessing
"""
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from grasch.import_preprocessor import preprocess_yaml_with_imports

# Test file
test_file = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")

print("Checking graphSchema properties...")
print("=" * 60)

# Load raw
with open(test_file, 'r') as f:
    raw = yaml.safe_load(f)

print("\n1. RAW file graphSchema keys:")
print(f"   {list(raw['graphSchema'].keys())}")

# Preprocess
processed = preprocess_yaml_with_imports(test_file)

print("\n2. PREPROCESSED file graphSchema keys:")
print(f"   {list(processed['graphSchema'].keys())}")

print("\n3. Schema allows for GraphSchemaContent:")
allowed = ['pathName', 'principal', 'valueTypeSystemName', 'graphType', 'constraints']
print(f"   {allowed}")

actual = list(processed['graphSchema'].keys())
unexpected = [k for k in actual if k not in allowed]

if unexpected:
    print(f"\n❌ Unexpected properties: {unexpected}")
else:
    print(f"\n✅ All properties are allowed")
