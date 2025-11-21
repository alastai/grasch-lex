#!/usr/bin/env python3
"""
Fix subtypesOf patterns in the schema using JSON manipulation.
"""
import json
from pathlib import Path
from copy import deepcopy

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path, 'r') as f:
    schema = json.load(f)

def create_concreteness_oneof(type_key, type_ref):
    """
    Create a oneOf structure that supports:
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

def fix_subtypesof_in_oneof(oneof_list, type_key, type_ref):
    """Find and fix subtypesOf patterns in a oneOf list."""
    fixed = False
    for i, item in enumerate(oneof_list):
        if isinstance(item, dict) and 'properties' in item and 'subtypesOf' in item['properties']:
            print(f"  Found subtypesOf pattern at index {i} for {type_key}")
            # Replace the subtypesOf property with the new structure
            item['properties']['subtypesOf'] = create_concreteness_oneof(type_key, type_ref)
            fixed = True
            print(f"  ✓ Fixed subtypesOf pattern for {type_key}")
    return fixed

# Navigate to nodeTypes items oneOf
print("=" * 70)
print("Fixing nodeTypes subtypesOf pattern")
print("=" * 70)

try:
    # The schema structure is: oneOf[1] -> properties -> graphSchema -> $ref
    # We need to find the definition in $defs
    for root_option in schema['oneOf']:
        if 'properties' in root_option and 'graphSchema' in root_option['properties']:
            # This references a $def, we need to look in $defs
            break
    
    # Look for GraphSchemaContent in $defs
    if '$defs' in schema:
        for def_name, def_content in schema['$defs'].items():
            if 'properties' in def_content and 'graphType' in def_content['properties']:
                graph_type = def_content['properties']['graphType']
                if 'properties' in graph_type and 'nodeTypes' in graph_type['properties']:
                    node_types_prop = graph_type['properties']['nodeTypes']
                    if 'oneOf' in node_types_prop:
                        for nt_option in node_types_prop['oneOf']:
                            if 'type' in nt_option and nt_option['type'] == 'array':
                                if 'items' in nt_option and 'oneOf' in nt_option['items']:
                                    if fix_subtypesof_in_oneof(nt_option['items']['oneOf'], 'nodeTypes', '#/$defs/NodeType'):
                                        print("✓ Fixed nodeTypes")
                
                # Also fix edgeTypes
                if 'properties' in graph_type and 'edgeTypes' in graph_type['properties']:
                    edge_types_prop = graph_type['properties']['edgeTypes']
                    if 'oneOf' in edge_types_prop:
                        for et_option in edge_types_prop['oneOf']:
                            if 'type' in et_option and et_option['type'] == 'array':
                                if 'items' in et_option and 'oneOf' in et_option['items']:
                                    if fix_subtypesof_in_oneof(et_option['items']['oneOf'], 'edgeTypes', '#/$defs/EdgeType'):
                                        print("✓ Fixed edgeTypes")

except Exception as e:
    print(f"Error navigating schema: {e}")
    import traceback
    traceback.print_exc()

# Save the updated schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("\n" + "=" * 70)
print("Schema updated successfully!")
print("=" * 70)
