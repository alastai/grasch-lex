#!/usr/bin/env python3
"""Test import preprocessing to understand how it works"""

import sys
sys.path.insert(0, 'src/grasch')

from import_preprocessor import preprocess_yaml_with_imports
from pathlib import Path
import yaml
import json

# Test with minimal-test.yaml
print("=" * 80)
print("Testing: lex-2026.0.3.2-minimal-test.yaml")
print("=" * 80)
print()

file_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")

# Load raw YAML (what validation sees without preprocessing)
print("RAW YAML (without preprocessing):")
print("-" * 80)
with open(file_path) as f:
    raw_data = yaml.safe_load(f)
print(yaml.dump(raw_data, default_flow_style=False)[:500])
print()

# Load preprocessed YAML (with imports resolved)
print("PREPROCESSED YAML (with imports resolved):")
print("-" * 80)
try:
    processed_data = preprocess_yaml_with_imports(file_path)
    print(yaml.dump(processed_data, default_flow_style=False)[:500])
except Exception as e:
    print(f"ERROR: {e}")
print()

# Check if defaults were imported
print("ANALYSIS:")
print("-" * 80)
if 'graphSchema' in raw_data:
    if 'graphType' in raw_data['graphSchema']:
        if 'defaults' in raw_data['graphSchema']['graphType']:
            defaults = raw_data['graphSchema']['graphType']['defaults']
            if isinstance(defaults, dict) and 'import' in defaults:
                print(f"✓ Raw YAML has import directive: {defaults}")
                print("  This means validation sees the import directive, not the resolved content")
            else:
                print(f"✗ Raw YAML has inline defaults: {defaults}")
