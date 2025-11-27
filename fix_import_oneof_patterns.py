#!/usr/bin/env python3
"""
Fix Import OneOf Patterns in JSON Schema

This script systematically fixes all locations where imports should be allowed
by ensuring they have the proper oneOf pattern:
  oneOf: [
    { actual content schema },
    { type: "object", required: ["import"], properties: { import: { type: "string" } }, additionalProperties: false }
  ]

The fix addresses the root cause: PC form validation should pass, and after canonicalization,
C form validation should also pass. The schema must accept both forms.
"""

import json
from pathlib import Path
from typing import Any, Dict
import copy

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Standard import option schema
IMPORT_OPTION = {
    "type": "object",
    "description": "Import content from file",
    "required": ["import"],
    "properties": {
        "import": {
            "type": "string",
            "description": "Import content from file"
        }
    },
    "additionalProperties": False
}

def create_import_oneof(content_schema: Dict) -> Dict:
    """
    Wrap a content schema in a oneOf with import option.
    
    Args:
        content_schema: The actual content schema
        
    Returns:
        A oneOf schema with content and import options
    """
    return {
        "oneOf": [
            content_schema,
            copy.deepcopy(IMPORT_OPTION)
        ]
    }

# Fix 1: GraphType definition - make it a oneOf at the root
print("Fixing GraphType definition...")
original_graph_type = copy.deepcopy(schema['$defs']['GraphType'])

# GraphType should be a oneOf: either inline definition or import
# But we need to preserve the patternProperties for wrappers
# So we keep the structure but ensure nested properties support imports

# Fix 2: GraphSchemaContent.graphType - should be oneOf
print("Fixing GraphSchemaContent.graphType...")
if 'graphType' in schema['$defs']['GraphSchemaContent']['properties']:
    current = schema['$defs']['GraphSchemaContent']['properties']['graphType']
    if 'oneOf' not in current:
        # Wrap in oneOf with import option
        schema['$defs']['GraphSchemaContent']['properties']['graphType'] = create_import_oneof(current)

# Fix 3: GraphContent.graphSchema.oneOf options - graphType should support imports
print("Fixing GraphContent.graphSchema graphType properties...")
if 'graphSchema' in schema['$defs']['GraphContent']['properties']:
    graph_schema_prop = schema['$defs']['GraphContent']['properties']['graphSchema']
    if 'oneOf' in graph_schema_prop:
        for option in graph_schema_prop['oneOf']:
            if isinstance(option, dict) and 'properties' in option:
                if 'graphType' in option['properties']:
                    current = option['properties']['graphType']
                    if 'oneOf' not in current:
                        option['properties']['graphType'] = create_import_oneof(current)

# Fix 4: GraphType.nodeTypes - should be oneOf (but it already references NodeTypesProperty which has oneOf)
# Actually, the issue is that GraphType has nodeTypes as a direct property without oneOf
print("Fixing GraphType.nodeTypes...")
if 'nodeTypes' in schema['$defs']['GraphType']['properties']:
    current = schema['$defs']['GraphType']['properties']['nodeTypes']
    # Check if it's already a $ref to NodeTypesProperty
    if '$ref' in current:
        print("  nodeTypes already references NodeTypesProperty - OK")
    else:
        # It should reference NodeTypesProperty
        schema['$defs']['GraphType']['properties']['nodeTypes'] = {
            "$ref": "#/$defs/NodeTypesProperty"
        }

# Fix 5: GraphType.edgeTypes - should reference EdgeTypesProperty
print("Fixing GraphType.edgeTypes...")
if 'edgeTypes' in schema['$defs']['GraphType']['properties']:
    current = schema['$defs']['GraphType']['properties']['edgeTypes']
    if '$ref' in current:
        print("  edgeTypes already references EdgeTypesProperty - OK")
    else:
        schema['$defs']['GraphType']['properties']['edgeTypes'] = {
            "$ref": "#/$defs/EdgeTypesProperty"
        }

# Fix 6: GraphType.subtypesOf.abstract.nodeTypes - should support imports
print("Fixing GraphType.subtypesOf.abstract.nodeTypes...")
if 'subtypesOf' in schema['$defs']['GraphType']['properties']:
    subtypes_of = schema['$defs']['GraphType']['properties']['subtypesOf']
    if 'properties' in subtypes_of:
        # Fix abstract.nodeTypes
        if 'abstract' in subtypes_of['properties']:
            abstract_prop = subtypes_of['properties']['abstract']
            if 'properties' in abstract_prop:
                if 'nodeTypes' in abstract_prop['properties']:
                    current = abstract_prop['properties']['nodeTypes']
                    if 'oneOf' not in current:
                        # Should be array of NodeType with import support
                        abstract_prop['properties']['nodeTypes'] = create_import_oneof(current)
                
                if 'edgeTypes' in abstract_prop['properties']:
                    current = abstract_prop['properties']['edgeTypes']
                    if 'oneOf' not in current:
                        abstract_prop['properties']['edgeTypes'] = create_import_oneof(current)
        
        # Fix direct nodeTypes/edgeTypes
        if 'nodeTypes' in subtypes_of['properties']:
            current = subtypes_of['properties']['nodeTypes']
            if 'oneOf' not in current:
                subtypes_of['properties']['nodeTypes'] = create_import_oneof(current)
        
        if 'edgeTypes' in subtypes_of['properties']:
            current = subtypes_of['properties']['edgeTypes']
            if 'oneOf' not in current:
                subtypes_of['properties']['edgeTypes'] = create_import_oneof(current)

# Fix 7: NodeTypeItem sealed.nodeTypes - should support imports
print("Fixing NodeTypeItem sealed.nodeTypes...")
if 'NodeTypeItem' in schema['$defs'] and 'oneOf' in schema['$defs']['NodeTypeItem']:
    for option in schema['$defs']['NodeTypeItem']['oneOf']:
        if isinstance(option, dict) and 'properties' in option:
            if 'sealed' in option['properties']:
                sealed_prop = option['properties']['sealed']
                if 'properties' in sealed_prop:
                    if 'nodeTypes' in sealed_prop['properties']:
                        current = sealed_prop['properties']['nodeTypes']
                        if 'oneOf' not in current:
                            sealed_prop['properties']['nodeTypes'] = create_import_oneof(current)

# Fix 8: EdgeTypeItem sealed.edgeTypes - should support imports
print("Fixing EdgeTypeItem sealed.edgeTypes...")
if 'EdgeTypeItem' in schema['$defs'] and 'oneOf' in schema['$defs']['EdgeTypeItem']:
    for option in schema['$defs']['EdgeTypeItem']['oneOf']:
        if isinstance(option, dict) and 'properties' in option:
            if 'sealed' in option['properties']:
                sealed_prop = option['properties']['sealed']
                if 'properties' in sealed_prop:
                    if 'edgeTypes' in sealed_prop['properties']:
                        current = sealed_prop['properties']['edgeTypes']
                        if 'oneOf' not in current:
                            sealed_prop['properties']['edgeTypes'] = create_import_oneof(current)

# Fix 9: Directory.directories - should support imports
print("Fixing Directory.directories...")
if 'Directory' in schema['$defs'] and 'properties' in schema['$defs']['Directory']:
    if 'directories' in schema['$defs']['Directory']['properties']:
        current = schema['$defs']['Directory']['properties']['directories']
        if 'oneOf' not in current:
            schema['$defs']['Directory']['properties']['directories'] = create_import_oneof(current)

# Fix 10: Root graphSchema property - should support imports
print("Fixing root graphSchema property...")
if 'oneOf' in schema:
    for option in schema['oneOf']:
        if isinstance(option, dict) and 'properties' in option:
            if 'graphSchema' in option['properties']:
                current = option['properties']['graphSchema']
                if 'oneOf' not in current:
                    option['properties']['graphSchema'] = create_import_oneof(current)

# Write the fixed schema
output_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(output_path, 'w') as f:
    json.dump(schema, f, indent=2)

print(f"\n✅ Fixed schema written to {output_path}")
print("\nFixes applied:")
print("  1. GraphSchemaContent.graphType - added oneOf with import")
print("  2. GraphContent.graphSchema.*.graphType - added oneOf with import")
print("  3. GraphType.nodeTypes - ensured reference to NodeTypesProperty")
print("  4. GraphType.edgeTypes - ensured reference to EdgeTypesProperty")
print("  5. GraphType.subtypesOf.abstract.nodeTypes - added oneOf with import")
print("  6. GraphType.subtypesOf.abstract.edgeTypes - added oneOf with import")
print("  7. GraphType.subtypesOf.nodeTypes - added oneOf with import")
print("  8. GraphType.subtypesOf.edgeTypes - added oneOf with import")
print("  9. NodeTypeItem.sealed.nodeTypes - added oneOf with import")
print(" 10. EdgeTypeItem.sealed.edgeTypes - added oneOf with import")
print(" 11. Directory.directories - added oneOf with import")
print(" 12. Root graphSchema property - added oneOf with import")

print("\n✅ All import patterns should now be consistent!")
print("   Run validate_pc_and_c_forms.py to verify the fixes.")
