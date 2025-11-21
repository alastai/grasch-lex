#!/usr/bin/env python3
"""
Rename type interpretation terms from old to new names in all example files
"""
import re
from pathlib import Path

# Define the renaming mappings
RENAMINGS = {
    'allowSubtypesOf': 'subtypesOf',
    'allowsProperSubtypesOf': 'properSubtypesOf',
    'exactlyOfThisType': 'exactlyOf',
    'abstractSupertype': 'abstract',
    'abstractSupertypes': 'abstract',  # Also rename the plural form
}

def rename_in_file(file_path):
    """Rename terms in a single file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    for old_term, new_term in RENAMINGS.items():
        # Count occurrences
        count = content.count(old_term)
        if count > 0:
            content = content.replace(old_term, new_term)
            changes_made.append(f"  {old_term} → {new_term} ({count} times)")
    
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        return changes_made
    return None

def main():
    # Find all YAML example files
    examples_dir = Path('src/grasch/examples')
    yaml_files = list(examples_dir.glob('**/*.yaml'))
    
    print(f"Found {len(yaml_files)} YAML files to process\n")
    
    total_files_changed = 0
    
    for yaml_file in sorted(yaml_files):
        changes = rename_in_file(yaml_file)
        if changes:
            total_files_changed += 1
            print(f"✓ {yaml_file.relative_to('src/grasch/examples')}:")
            for change in changes:
                print(change)
            print()
    
    print(f"\nSummary: Updated {total_files_changed} files")

if __name__ == '__main__':
    main()
