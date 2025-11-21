#!/usr/bin/env python3
"""
Fix the subtypesOf pattern to support optional concreteness wrappers.

Current: subtypesOf REQUIRES abstract: { nodeTypes: [...] }
Fixed: subtypesOf supports oneOf:
  1. { nodeTypes: [...] } - concrete by default
  2. { abstract: { nodeTypes: [...] } } - explicit abstract
  3. { concrete: { nodeTypes: [...] } } - explicit concrete
"""
import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path, 'r') as f:
    schema = json.load(f)

def find_and_fix_subtypesof(items_oneof, type_name="nodeTypes"):
    """Find and fix subtypesOf pattern in a oneOf array."""
    for i, item in enumerate(items_oneof):
        if (isinstance(item, dict) and 
            item.get('required') == ['subtypesOf'] and
            'properties' in item and 
            'subtypesOf' in item['properties']):
            
            print(f"\n✓ Found subtypesOf pattern for {type_name} at index {i}")
            
            subtypes_prop = item['properties']['subtypesOf']
            
            # Check if it currently requires 'abstract'
            if (isinstance(subtypes_prop, dict) and 
                subtypes_prop.get('required') == ['abstract']):
                
                print(f"  Current: requires 'abstract' wrapper")
                
                # Get the nodeTypes/edgeTypes definition from inside abstract
                if 'properties' in subtypes_prop and 'abstract' in subtypes_prop['properties']:
                    abstract_obj = subtypes_prop['properties']['abstract']
                    if 'properties' in abstract_obj and type_name in abstract_obj['properties']:
                        types_array_def = abstract_obj['properties'][type_name]
                        
                        # Create the new oneOf structure
                        new_subtypes_def = {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "description": f"Direct {type_name} (concrete by default)",
                                    "required": [type_name],
                                    "properties": {
                                        type_name: types_array_def
                                    },
                                    "additionalProperties": False
                                },
                                {
                                    "type": "object",
                                    "description": f"Abstract {type_name}",
                                    "required": ["abstract"],
                                    "properties": {
                                        "abstract": {
                                            "type": "object",
                                            "required": [type_name],
                                            "properties": {
                                                type_name: types_array_def
                                            },
                                            "additionalProperties": False
                                        }
                                    },
                                    "additionalProperties": False
                                },
                                {
                                    "type": "object",
                                    "description": f"Concrete {type_name} (explicit)",
                                    "required": ["concrete"],
                                    "properties": {
                                        "concrete": {
                                            "type": "object",
                                            "required": [type_name],
                                            "properties": {
                                                type_name: types_array_def
                                            },
                                            "additionalProperties": False
                                        }
                                    },
                                    "additionalProperties": False
                                }
                            ]
                        }
                        
                        # Replace the subtypesOf definition
                        item['properties']['subtypesOf'] = new_subtypes_def
                        print(f"  ✓ Fixed: now supports concrete (default), abstract, and concrete (explicit)")
                        return True
    
    return False

# Navigate to GraphType definition in $defs
print("=" * 70)
print("Fixing subtypesOf patterns in schema")
print("=" * 70)

if '$defs' in schema and 'GraphType' in schema['$defs']:
    graph_type = schema['$defs']['GraphType']
    
    # Fix nodeTypes
    if 'properties' in graph_type and 'nodeTypes' in graph_type['properties']:
        node_types_prop = graph_type['properties']['nodeTypes']
        
        # nodeTypes can be oneOf with array or import
        if 'oneOf' in node_types_prop:
            for option in node_types_prop['oneOf']:
                if option.get('type') == 'array' and 'items' in option:
                    items = option['items']
                    if 'oneOf' in items:
                        if find_and_fix_subtypesof(items['oneOf'], 'nodeTypes'):
                            print("✓ Fixed nodeTypes subtypesOf pattern")
    
    # Fix edgeTypes
    if 'properties' in graph_type and 'edgeTypes' in graph_type['properties']:
        edge_types_prop = graph_type['properties']['edgeTypes']
        
        # edgeTypes can be oneOf with array or import
        if 'oneOf' in edge_types_prop:
            for option in edge_types_prop['oneOf']:
                if option.get('type') == 'array' and 'items' in option:
                    items = option['items']
                    if 'oneOf' in items:
                        if find_and_fix_subtypesof(items['oneOf'], 'edgeTypes'):
                            print("✓ Fixed edgeTypes subtypesOf pattern")

# Save the updated schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("\n" + "=" * 70)
print("Schema fix complete!")
print("=" * 70)
print("\nThe subtypesOf pattern now supports:")
print("  1. subtypesOf: { nodeTypes: [...] } - concrete by default")
print("  2. subtypesOf: { abstract: { nodeTypes: [...] } } - explicit abstract")
print("  3. subtypesOf: { concrete: { nodeTypes: [...] } } - explicit concrete")
