#!/usr/bin/env python3
"""
Fix the subtypesOf pattern in the JSON schema to support concrete/abstract/direct patterns.

The issue: subtypesOf currently requires 'abstract' as a mandatory property.
The fix: subtypesOf should be a oneOf supporting:
  1. Direct nodeTypes/edgeTypes (concrete by default)
  2. abstract: { nodeTypes/edgeTypes }
  3. concrete: { nodeTypes/edgeTypes }
"""
import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

print("Loading schema...")
with open(schema_path, 'r') as f:
    schema = json.load(f)

def create_subtypesof_oneof(type_key, items_oneof):
    """
    Create the oneOf structure for subtypesOf that supports:
    - Direct nodeTypes/edgeTypes (concrete by default)
    - abstract: { nodeTypes/edgeTypes }
    - concrete: { nodeTypes/edgeTypes }
    """
    return {
        "oneOf": [
            {
                "type": "object",
                "description": f"Direct {type_key} (concrete by default)",
                "required": [type_key],
                "properties": {
                    type_key: {
                        "type": "array",
                        "items": {
                            "oneOf": items_oneof
                        }
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
                                "items": {
                                    "oneOf": items_oneof
                                }
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
                                "items": {
                                    "oneOf": items_oneof
                                }
                            }
                        },
                        "additionalProperties": False
                    }
                },
                "additionalProperties": False
            }
        ]
    }

def fix_subtypesof_in_items(items_oneof, type_key):
    """
    Find and fix the subtypesOf pattern in a nodeTypes or edgeTypes items oneOf array.
    """
    fixed = False
    for i, pattern in enumerate(items_oneof):
        if isinstance(pattern, dict) and pattern.get('description') == 'Subtypes declaration':
            if 'properties' in pattern and 'subtypesOf' in pattern['properties']:
                print(f"  Found subtypesOf pattern at index {i} for {type_key}")
                
                # Get the items oneOf from the current structure
                current_subtypes = pattern['properties']['subtypesOf']
                if 'properties' in current_subtypes and 'abstract' in current_subtypes['properties']:
                    abstract_obj = current_subtypes['properties']['abstract']
                    if 'properties' in abstract_obj and type_key in abstract_obj['properties']:
                        type_array = abstract_obj['properties'][type_key]
                        if 'items' in type_array and 'oneOf' in type_array['items']:
                            items_oneof_inner = type_array['items']['oneOf']
                            
                            # Create the new subtypesOf structure
                            pattern['properties']['subtypesOf'] = create_subtypesof_oneof(type_key, items_oneof_inner)
                            print(f"  ✓ Fixed subtypesOf pattern for {type_key}")
                            fixed = True
    
    return fixed

# Navigate to GraphType definition in $defs
print("\n" + "=" * 70)
print("Fixing nodeTypes subtypesOf pattern")
print("=" * 70)

if '$defs' in schema and 'GraphType' in schema['$defs']:
    graph_type = schema['$defs']['GraphType']
    if 'properties' in graph_type and 'nodeTypes' in graph_type['properties']:
        node_types_def = graph_type['properties']['nodeTypes']
        if 'oneOf' in node_types_def:
            # Find the array pattern
            for option in node_types_def['oneOf']:
                if option.get('type') == 'array' and 'items' in option:
                    if 'oneOf' in option['items']:
                        if fix_subtypesof_in_items(option['items']['oneOf'], 'nodeTypes'):
                            print("✓ Successfully fixed nodeTypes subtypesOf pattern")

print("\n" + "=" * 70)
print("Fixing edgeTypes subtypesOf pattern")
print("=" * 70)

if '$defs' in schema and 'GraphType' in schema['$defs']:
    graph_type = schema['$defs']['GraphType']
    if 'properties' in graph_type and 'edgeTypes' in graph_type['properties']:
        edge_types_def = graph_type['properties']['edgeTypes']
        if 'oneOf' in edge_types_def:
            # Find the array pattern
            for option in edge_types_def['oneOf']:
                if option.get('type') == 'array' and 'items' in option:
                    if 'oneOf' in option['items']:
                        if fix_subtypesof_in_items(option['items']['oneOf'], 'edgeTypes'):
                            print("✓ Successfully fixed edgeTypes subtypesOf pattern")

# Save the updated schema
print("\n" + "=" * 70)
print("Saving updated schema...")
print("=" * 70)

with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("✓ Schema updated successfully!")
print("\nNow run: python debug_remaining_3_failures.py")
