#!/usr/bin/env python3
"""Test what the validation script actually sees"""

import yaml
from pathlib import Path

# Test with minimal-test.yaml
print("=" * 80)
print("What validation sees (RAW YAML without preprocessing)")
print("=" * 80)
print()

file_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")

with open(file_path) as f:
    raw_data = yaml.safe_load(f)

print("Full structure:")
print(yaml.dump(raw_data, default_flow_style=False))
print()

print("=" * 80)
print("ANALYSIS")
print("=" * 80)
print()

if 'graphSchema' in raw_data:
    print("✓ Has graphSchema root")
    gs = raw_data['graphSchema']
    
    if 'pathName' in gs:
        print(f"✓ graphSchema has pathName: {gs['pathName']}")
    
    if 'graphType' in gs:
        print("✓ Has graphType")
        gt = gs['graphType']
        
        if 'pathName' in gt:
            print(f"✗ ERROR: graphType has pathName: {gt['pathName']}")
            print("  This should NOT be there!")
        else:
            print("✓ graphType does NOT have pathName (correct)")
        
        if 'defaults' in gt:
            defaults = gt['defaults']
            print(f"\nDefaults structure: {type(defaults)}")
            if isinstance(defaults, dict):
                if 'import' in defaults:
                    print(f"  Has import directive: {defaults['import']}")
                    print("  → Validation sees the import directive, NOT the resolved content")
                    print("  → JSON Schema must validate the import directive structure")
                else:
                    print(f"  Inline defaults: {list(defaults.keys())[:5]}...")
