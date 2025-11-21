#!/usr/bin/env python3
"""
Check what properties the preprocessed file has at root level
"""
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from grasch.import_preprocessor import preprocess_yaml_with_imports

# Test file
test_file = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")

print("Checking root properties...")
print("=" * 60)

# Load raw
with open(test_file, 'r') as f:
    raw = yaml.safe_load(f)

print("\n1. RAW file root keys:")
print(f"   {list(raw.keys())}")

# Preprocess
processed = preprocess_yaml_with_imports(test_file)

print("\n2. PREPROCESSED file root keys:")
print(f"   {list(processed.keys())}")

print("\n3. Schema expects for graphSchema document:")
print("   - required: ['graphSchema']")
print("   - additionalProperties: false")
print("   - So ONLY 'graphSchema' key allowed at root")

if list(processed.keys()) == ['graphSchema']:
    print("\n✅ Root structure matches schema expectation")
else:
    print(f"\n❌ Root has unexpected keys: {[k for k in processed.keys() if k != 'graphSchema']}")
