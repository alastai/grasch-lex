#!/usr/bin/env python3
"""
Update all references from graph-type-defaults.yaml to property-graph-data-model.yaml
"""

from pathlib import Path
import re

def update_file(file_path):
    """Update import references in a file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    
    # Replace the old filename with the new one
    content = content.replace(
        'lex-2026.0.3.2-graph-type-defaults.yaml',
        'lex-2026.0.3.2-property-graph-data-model.yaml'
    )
    
    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✓ Updated: {file_path}")
        return True
    else:
        print(f"⊘ No changes: {file_path}")
        return False

def main():
    print("=" * 60)
    print("Updating import filename references")
    print("=" * 60)
    
    # Update all YAML files in examples
    yaml_files = list(Path('src/grasch/examples').glob('*.yaml'))
    
    updated = 0
    for yaml_file in sorted(yaml_files):
        if update_file(yaml_file):
            updated += 1
    
    print("\n" + "=" * 60)
    print(f"Updated {updated} files")
    print("=" * 60)

if __name__ == '__main__':
    main()
