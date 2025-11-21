#!/usr/bin/env python3
"""Update node type syntax examples with clean aesthetic."""

import re

def clean_aesthetic(content):
    """Apply aesthetic transformations to YAML content."""
    
    # Remove notNull: true (non-null is default)
    content = re.sub(r'\n\s+notNull: true', '', content)
    
    # Replace notNull: false with ? suffix
    content = re.sub(r'(\s+valueType: \w+(?:\s+\w+)*)\n\s+notNull: false', r'\1?', content)
    
    # Convert block-style label arrays to flow-style
    # Match patterns like:
    #   labels:
    #   - Label1
    #   - Label2
    # And convert to: labels: [Label1, Label2]
    def convert_labels(match):
        indent = match.group(1)
        labels_text = match.group(2)
        labels = re.findall(r'- (\w+)', labels_text)
        if labels:
            return f"{indent}labels: [{', '.join(labels)}]"
        return match.group(0)
    
    content = re.sub(
        r'(\s+)labels:\n((?:\s+- \w+\n)+)',
        convert_labels,
        content
    )
    
    # Convert typeLabels arrays to flow-style
    def convert_typelabels(match):
        indent = match.group(1)
        labels_text = match.group(2)
        labels = re.findall(r'- (\w+)', labels_text)
        if labels:
            return f"{indent}typeLabels: [{', '.join(labels)}]"
        return match.group(0)
    
    content = re.sub(
        r'(\s+)typeLabels:\n((?:\s+- \w+\n)+)',
        convert_typelabels,
        content
    )
    
    return content

# Read the file
with open('src/grasch/examples/imports/lex-2026.0.3.2-node-type-syntax-examples.yaml', 'r') as f:
    content = f.read()

# Apply transformations
cleaned = clean_aesthetic(content)

# Write back
with open('src/grasch/examples/imports/lex-2026.0.3.2-node-type-syntax-examples.yaml', 'w') as f:
    f.write(cleaned)

print("✅ Updated node-type-syntax-examples.yaml with clean aesthetic")
