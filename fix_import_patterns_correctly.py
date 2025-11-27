#!/usr/bin/env python3
"""
Correctly Fix Import OneOf Patterns in JSON Schema

The key insight: imports should be allowed for NESTED content, not for root document type selectors.

Root level (catalog/graphSchema/graph) defines the DOCUMENT TYPE - no imports here.
Nested properties (graphType, nodeTypes, etc.) can have imports.
"""

import json
from pathlib import Path
import copy

# Load the ORIGINAL schema (before our incorrect fixes)
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

# First, let's restore from a backup or re-apply fixes correctly
# For now, let's just fix the specific issue: remove the oneOf from root graphSchema

with open(schema_path, 'r') as f:
    schema = json.load(f)

print("Fixing root-level graphSchema property...")
print("="*80)

# The root oneOf should have graphSchema directly reference GraphSchemaContent
# NOT wrapped in a oneOf
if 'oneOf' in schema:
    for option in schema['oneOf']:
        if isinstance(option, dict) and 'properties' in option:
            if 'graphSchema' in option['properties']:
                current = option['properties']['graphSchema']
                # Check if it's wrapped in a oneOf
                if 'oneOf' in current:
                    print("Found oneOf wrapper on root graphSchema - removing it")
                    # It should just be a $ref to GraphSchemaContent
                    option['properties']['graphSchema'] = {
                        "$ref": "#/$defs/GraphSchemaContent"
                    }
                    print("✓ Fixed: root graphSchema now directly references GraphSchemaContent")

# Write the fixed schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print(f"\n✅ Schema fixed and written to {schema_path}")
print("\nThe fix:")
print("  - Root graphSchema property now directly references GraphSchemaContent")
print("  - Import support remains in nested properties where it belongs")
print("\nRationale:")
print("  - Root level defines DOCUMENT TYPE (catalog/graphSchema/graph)")
print("  - Imports are for CONTENT, not document type selection")
print("  - GraphSchemaContent.graphType can have imports")
print("  - GraphType.nodeTypes/edgeTypes can have imports")
print("  - But root 'graphSchema:' key itself cannot be imported")
