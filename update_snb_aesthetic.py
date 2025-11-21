#!/usr/bin/env python3
"""Update SNB hierarchy files with clean aesthetic (remove notNull: true)."""

import re
import glob

def clean_aesthetic(content):
    """Apply aesthetic transformations to YAML content."""
    
    # Remove notNull: true (non-null is default)
    content = re.sub(r'\n\s+notNull: true', '', content)
    
    # Replace notNull: false with ? suffix
    content = re.sub(r'(\s+valueType: [A-Z\s]+)\n\s+notNull: false', r'\1?', content)
    
    return content

# Update all SNB hierarchy files
files = glob.glob('src/grasch/examples/imports/snb-types/*.yaml')

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    cleaned = clean_aesthetic(content)
    
    with open(filepath, 'w') as f:
        f.write(cleaned)
    
    print(f"✅ Updated {filepath}")

print("\n✅ All SNB hierarchy files updated with clean aesthetic")
