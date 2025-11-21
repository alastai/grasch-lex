#!/usr/bin/env python3
"""
Fix subtypesOf patterns in the schema - correct navigation path.
"""
import json
from pathlib import Path

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

# Navigate to the correct location
print("=" * 70)
print("Fixing type interpretation patterns")
print("=" * 70)

try:
    graph_type = schema['$defs']['GraphType']
    
    # Fix nodeTypes
    if 'nodeTypes' in graph_type['properties']:
        node_types_prop = graph_type['properties']['nodeTypes']
        if 'oneOf' in node_types_prop:
            # Find the array option
            for nt_option in node_types_prop['oneOf']:
                if nt_option.get('type') == 'array' and 'items' in nt_option:
                    if 'oneOf' in nt_option['items']:
                        print("\nProcessing nodeTypes...")
                        if fix_subtypesof_in_oneof(nt_option['items']['oneOf'], 'nodeTypes', '#/$defs/NodeType'):
                            print("✓ Fixed nodeTypes subtypesOf pattern")
    
    # Fix edgeTypes
    if 'edgeTypes' in graph_type['properties']:
        edge_types_prop = graph_type['properties']['edgeTypes']
        if 'oneOf' in edge_types_prop:
            # Find the array option
            for et_option in edge_types_prop['oneOf']:
                if et_option.get('type') == 'array' and 'items' in et_option:
                    if 'oneOf' in et_option['items']:
                        print("\nProcessing edgeTypes...")
                        if fix_subtypesof_in_oneof(et_option['items']['oneOf'], 'edgeTypes', '#/$defs/EdgeType'):
                            print("✓ Fixed edgeTypes subtypesOf pattern")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Save the updated schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("\n" + "=" * 70)
print("Schema updated successfully!")
print("=" * 70)
print("\nNow run: python validate_all_examples.py")
