#!/usr/bin/env python3
"""
Apply type interpretation wrapper fix to ALL type definition locations:
- nodeTypes array items (already done)
- edgeTypes array items
- graphType itself
- Any other type sequences

The fix allows three patterns for subtypesOf:
1. subtypesOf: { [types]: [...] } (concrete by default)
2. subtypesOf: { abstract: { [types]: [...] } }
3. subtypesOf: { concrete: { [types]: [...] } }
"""
import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path, 'r') as f:
    schema = json.load(f)

def create_subtypesof_oneof(type_key, type_ref):
    """
    Create a oneOf structure for subtypesOf that supports:
    1. Direct types (concrete by default)
    2. abstract: { types }
    3. concrete: { types }
    """
    items_oneof = [
        {"$ref": type_ref},
        {
            "type": "object",
            "required": ["abstract"],
            "properties": {
                "abstract": {"$ref": type_ref}
            },
            "additionalProperties": False
        }
    ]
    
    return {
        "type": "object",
        "description": "Subtypes declaration",
        "required": ["subtypesOf"],
        "properties": {
            "subtypesOf": {
                "oneOf": [
                    {
                        "type": "object",
                        "description": f"Direct {type_key} (concrete by default)",
                        "required": [type_key],
                        "properties": {
                            type_key: {
                                "type": "array",
                                "items": {"oneOf": items_oneof}
                            }
                        },
                        "additionalProperties": False
                    },
                    {
                        "type": "object",
                        "description": f"Abstract {type_key}",
                        "required": ["abstract"],
                        "properties": {
                            "abstract": {
                                "type": "object",
                                "required": [type_key],
                                "properties": {
                                    type_key: {
                                        "type": "array",
                                        "items": {"oneOf": items_oneof}
                                    }
                                },
                                "additionalProperties": False
                            }
                        },
                        "additionalProperties": False
                    },
                    {
                        "type": "object",
                        "description": f"Concrete {type_key} (explicit)",
                        "required": ["concrete"],
                        "properties": {
                            "concrete": {
                                "type": "object",
                                "required": [type_key],
                                "properties": {
                                    type_key: {
                                        "type": "array",
                                        "items": {"oneOf": items_oneof}
                                    }
                                },
                                "additionalProperties": False
                            }
                        },
                        "additionalProperties": False
                    }
                ]
            }
        },
        "additionalProperties": False
    }

def add_or_update_subtypesof(oneof_list, type_key, type_ref):
    """
    Add or update subtypesOf pattern in a oneOf list.
    Returns True if added/updated, False if already exists correctly.
    """
    # Check if subtypesOf already exists
    subtypesof_index = None
    for i, item in enumerate(oneof_list):
        if isinstance(item, dict) and 'properties' in item and 'subtypesOf' in item['properties']:
            subtypesof_index = i
            break
    
    new_pattern = create_subtypesof_oneof(type_key, type_ref)
    
    if subtypesof_index is not None:
        # Update existing
        oneof_list[subtypesof_index] = new_pattern
        return True
    else:
        # Add new
        oneof_list.append(new_pattern)
        return True

# Get GraphType definition
graph_type = schema['$defs']['GraphType']

print("=" * 70)
print("Applying type interpretation fixes")
print("=" * 70)

# 1. Fix nodeTypes array items (verify/update)
print("\n1. Processing nodeTypes...")
if 'nodeTypes' in graph_type['properties']:
    node_types_prop = graph_type['properties']['nodeTypes']
    if 'oneOf' in node_types_prop:
        for nt_option in node_types_prop['oneOf']:
            if nt_option.get('type') == 'array' and 'items' in nt_option:
                if 'oneOf' in nt_option['items']:
                    if add_or_update_subtypesof(nt_option['items']['oneOf'], 'nodeTypes', '#/$defs/NodeType'):
                        print("   ✓ Updated nodeTypes subtypesOf pattern")

# 2. Fix edgeTypes array items
print("\n2. Processing edgeTypes...")
if 'edgeTypes' in graph_type['properties']:
    edge_types_prop = graph_type['properties']['edgeTypes']
    if 'oneOf' in edge_types_prop:
        for et_option in edge_types_prop['oneOf']:
            if et_option.get('type') == 'array' and 'items' in et_option:
                if 'oneOf' in et_option['items']:
                    if add_or_update_subtypesof(et_option['items']['oneOf'], 'edgeTypes', '#/$defs/EdgeType'):
                        print("   ✓ Added edgeTypes subtypesOf pattern")

# 3. Check if graphType itself needs interpretation wrappers
# (This would be at a higher level - in GraphSchemaContent)
print("\n3. Checking graphType-level interpretations...")
if 'GraphSchemaContent' in schema['$defs']:
    gsc = schema['$defs']['GraphSchemaContent']
    if 'properties' in gsc and 'graphType' in gsc['properties']:
        gt_prop = gsc['properties']['graphType']
        # GraphType is currently just a $ref, we'd need to wrap it in oneOf
        # to support interpretations at this level
        # For now, just note it
        print("   ℹ graphType is a direct $ref (no array, so interpretations apply differently)")

# 4. Look for any other type sequences that might need this pattern
print("\n4. Scanning for other type sequence patterns...")
# Check sealed nodeTypes/edgeTypes (nested arrays)
for nt_option in graph_type['properties']['nodeTypes']['oneOf']:
    if nt_option.get('type') == 'array' and 'items' in nt_option:
        if 'oneOf' in nt_option['items']:
            for item_pattern in nt_option['items']['oneOf']:
                if 'properties' in item_pattern and 'sealed' in item_pattern['properties']:
                    sealed_prop = item_pattern['properties']['sealed']
                    if 'properties' in sealed_prop and 'nodeTypes' in sealed_prop['properties']:
                        print("   ℹ Found sealed nodeTypes pattern (nested, already has abstract support)")

# Save the updated schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("\n" + "=" * 70)
print("Schema updated successfully!")
print("=" * 70)
print("\nChanges applied:")
print("  - nodeTypes array items: subtypesOf with abstract/concrete options")
print("  - edgeTypes array items: subtypesOf with abstract/concrete options")
print("\nRun: python validate_all_examples.py")
