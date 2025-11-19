#!/usr/bin/env python3
"""
Fix the subtypesOf pattern in the schema to support both abstract and concrete concreteness levels.

Current issue: subtypesOf requires 'abstract' as a required property
Fix: subtypesOf should support:
  - subtypesOf: { nodeTypes: [...] } (concrete by default)
  - subtypesOf: { abstract: { nodeTypes: [...] } }
  - subtypesOf: { concrete: { nodeTypes: [...] } }
"""
import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path, 'r') as f:
    schema = json.load(f)

def fix_subtypesof_pattern(oneof_list):
    """
    Find and fix the subtypesOf pattern in a oneOf list.
    The pattern should support both abstract and concrete wrappers, or direct nodeTypes/edgeTypes.
    """
    for i, pattern in enumerate(oneof_list):
        if isinstance(pattern, dict) and 'properties' in pattern:
            if 'subtypesOf' in pattern['properties']:
                print(f"Found subtypesOf pattern at index {i}")
                
                # The subtypesOf property should be a oneOf with three options:
                # 1. Direct nodeTypes/edgeTypes (concrete by default)
                # 2. abstract: { nodeTypes/edgeTypes }
                # 3. concrete: { nodeTypes/edgeTypes }
                
                subtypes_def = pattern['properties']['subtypesOf']
                print(f"Current subtypesOf definition: {json.dumps(subtypes_def, indent=2)[:200]}")
                
                # Create the new definition
                # We need to determine if this is for nodeTypes or edgeTypes
                # by checking what's in the current structure
                
                if 'properties' in subtypes_def and 'abstract' in subtypes_def['properties']:
                    abstract_def = subtypes_def['properties']['abstract']
                    if 'properties' in abstract_def and 'nodeTypes' in abstract_def['properties']:
                        type_key = 'nodeTypes'
                        type_def = abstract_def['properties']['nodeTypes']
                    elif 'properties' in abstract_def and 'edgeTypes' in abstract_def['properties']:
                        type_key = 'edgeTypes'
                        type_def = abstract_def['properties']['edgeTypes']
                    else:
                        print("Warning: Could not determine type key")
                        continue
                    
                    # Create the new oneOf structure
                    new_subtypes_def = {
                        "oneOf": [
                            {
                                "type": "object",
                                "description": f"Direct {type_key} (concrete by default)",
                                "required": [type_key],
                                "properties": {
                                    type_key: type_def
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
                                            type_key: type_def
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
                                            type_key: type_def
                                        },
                                        "additionalProperties": False
                                    }
                                },
                                "additionalProperties": False
                            }
                        ]
                    }
                    
                    pattern['properties']['subtypesOf'] = new_subtypes_def
                    print(f"✓ Fixed subtypesOf pattern for {type_key}")
                    return True
    
    return False

# Fix nodeTypes array items
print("=" * 70)
print("Fixing nodeTypes subtypesOf pattern")
print("=" * 70)

if 'properties' in schema and 'graphSchema' in schema['properties']:
    graph_schema = schema['properties']['graphSchema']
    if 'properties' in graph_schema and 'graphType' in graph_schema['properties']:
        graph_type = graph_schema['properties']['graphType']
        if 'properties' in graph_type and 'nodeTypes' in graph_type['properties']:
            node_types = graph_type['properties']['nodeTypes']
            if 'items' in node_types and 'oneOf' in node_types['items']:
                if fix_subtypesof_pattern(node_types['items']['oneOf']):
                    print("✓ Fixed nodeTypes subtypesOf pattern")

# Fix edgeTypes array items
print("\n" + "=" * 70)
print("Fixing edgeTypes subtypesOf pattern")
print("=" * 70)

if 'properties' in schema and 'graphSchema' in schema['properties']:
    graph_schema = schema['properties']['graphSchema']
    if 'properties' in graph_schema and 'graphType' in graph_schema['properties']:
        graph_type = graph_schema['properties']['graphType']
        if 'properties' in graph_type and 'edgeTypes' in graph_type['properties']:
            edge_types = graph_type['properties']['edgeTypes']
            if 'items' in edge_types and 'oneOf' in edge_types['items']:
                if fix_subtypesof_pattern(edge_types['items']['oneOf']):
                    print("✓ Fixed edgeTypes subtypesOf pattern")

# Save the updated schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("\n" + "=" * 70)
print("Schema updated successfully!")
print("=" * 70)
