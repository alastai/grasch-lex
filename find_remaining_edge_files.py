#!/usr/bin/env python3
"""Find all YAML files with edgeTypes that still need updating."""

import yaml
import os
from pathlib import Path

def has_edgetypes(data):
    """Recursively check if data contains edgeTypes."""
    if isinstance(data, dict):
        if 'edgeTypes' in data:
            return True
        for value in data.values():
            if has_edgetypes(value):
                return True
    elif isinstance(data, list):
        for item in data:
            if has_edgetypes(item):
                return True
    return False

def check_edge_label_format(data, path=""):
    """Check if edge labels use old string format."""
    issues = []
    
    if isinstance(data, dict):
        # Check for edgeTypes array
        if 'edgeTypes' in data and isinstance(data['edgeTypes'], list):
            for i, edge in enumerate(data['edgeTypes']):
                if isinstance(edge, dict):
                    # Check for via/arc/typeLabel as strings (old format)
                    for label_key in ['via', 'arc', 'typeLabel']:
                        if label_key in edge:
                            if isinstance(edge[label_key], str):
                                issues.append(f"{path}.edgeTypes[{i}].{label_key} is string (should be object)")
                            elif isinstance(edge[label_key], dict):
                                # Check if it has typeLabel child
                                if 'typeLabel' not in edge[label_key]:
                                    issues.append(f"{path}.edgeTypes[{i}].{label_key} missing typeLabel child")
        
        # Recurse
        for key, value in data.items():
            new_issues = check_edge_label_format(value, f"{path}.{key}" if path else key)
            issues.extend(new_issues)
    
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_issues = check_edge_label_format(item, f"{path}[{i}]")
            issues.extend(new_issues)
    
    return issues

# Find all YAML files
yaml_files = []
for root, dirs, files in os.walk('src/grasch/examples'):
    # Skip archive directories
    if 'archive' in root or 'deprecated' in root:
        continue
    for file in files:
        if file.endswith('.yaml'):
            yaml_files.append(os.path.join(root, file))

print("Analyzing YAML files for edge label format...")
print("=" * 80)

files_needing_update = []

for filepath in sorted(yaml_files):
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        if has_edgetypes(data):
            issues = check_edge_label_format(data)
            if issues:
                files_needing_update.append((filepath, issues))
                print(f"\n❌ {filepath}")
                for issue in issues:
                    print(f"   - {issue}")
            else:
                print(f"✅ {filepath} - Already correct")
    except Exception as e:
        print(f"⚠️  {filepath} - Error: {e}")

print("\n" + "=" * 80)
print(f"\nSummary:")
print(f"  Files needing updates: {len(files_needing_update)}")
print(f"  Total files with edgeTypes: {len([f for f in yaml_files if has_edgetypes(yaml.safe_load(open(f)))])}")

if files_needing_update:
    print("\nFiles to update:")
    for filepath, _ in files_needing_update:
        print(f"  - {filepath}")
