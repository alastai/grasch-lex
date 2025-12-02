#!/usr/bin/env python3
"""
Fix Location 1: Apply universal TI pattern to GraphSchemaContent.

The fix removes the oneOf constraint and ensures GraphSchemaContent uses
the same patternProperties pattern as GraphType, but wrapping graphType instead.
"""

import json

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'r') as f:
    schema = json.load(f)

# Get GraphSchemaContent
gsc = schema['$defs']['GraphSchemaContent']

print("BEFORE FIX:")
print(f"  Has oneOf: {'oneOf' in gsc}")
print(f"  additionalProperties: {gsc.get('additionalProperties')}")
print(f"  Has patternProperties: {'patternProperties' in gsc}")

# The patternProperties already exist and look correct!
# The problem is the oneOf constraint at the end that restricts which properties can exist

# Remove the oneOf constraint - it's incompatible with the universal TI pattern
if 'oneOf' in gsc:
    print("\nRemoving oneOf constraint...")
    del gsc['oneOf']

# The patternProperties are already there and correct
# additionalProperties: false is correct - only allows defined properties and pattern properties

print("\nAFTER FIX:")
print(f"  Has oneOf: {'oneOf' in gsc}")
print(f"  additionalProperties: {gsc.get('additionalProperties')}")
print(f"  Has patternProperties: {'patternProperties' in gsc}")

# Save fixed schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'w') as f:
    json.dump(schema, f, indent=2)

print("\n✓ Location 1 fix applied successfully!")
print("  GraphSchemaContent now uses universal TI pattern")
print("  Removed oneOf constraint that was incompatible with TI siblings")
