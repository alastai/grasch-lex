#!/usr/bin/env python3
"""
Add type interpretation wrapper support to the pre-import JSON Schema.

This script updates lex-2026.0.3.2-pre-import.schema.json to support:
- Zero-level wrappers (bare type references)
- One-level wrappers (abstract, concrete, properSubtypesOf)
- Two-level wrappers (exactlyOf/subtypesOf with concrete/abstract)
- Wrappers around single properties and array items
- Validation to prevent wrapper nesting
"""

import json
import sys

def create_wrapper_definitions():
    """Create the wrapper pattern definitions."""
    
    # Base NodeType reference (what we're wrapping)
    node_type_ref = {"$ref": "#/$defs/NodeType"}
    edge_type_ref = {"$ref": "#/$defs/EdgeType"}
    
    # Create wrapper patterns for NodeType
    node_type_with_wrappers = {
        "oneOf": [
            # Zero-level: bare NodeType reference
            node_type_ref,
            
            # One-level: abstract wrapper
            {
                "type": "object",
                "properties": {
                    "abstract": node_type_ref
                },
                "required": ["abstract"],
                "additionalProperties": False,
                "description": "Abstract type wrapper (one-level) - maps to subtypesOf: abstract:"
            },
            
            # One-level: concrete wrapper
            {
                "type": "object",
                "properties": {
                    "concrete": node_type_ref
                },
                "required": ["concrete"],
                "additionalProperties": False,
                "description": "Concrete type wrapper (one-level) - maps to exactlyOf: concrete:"
            },
            
            # One-level: properSubtypesOf wrapper
            {
                "type": "object",
                "properties": {
                    "properSubtypesOf": node_type_ref
                },
                "required": ["properSubtypesOf"],
                "additionalProperties": False,
                "description": "Proper subtypes wrapper (one-level) - maps to subtypesOf: abstract:"
            },
            
            # Two-level: exactlyOf with concrete
            {
                "type": "object",
                "properties": {
                    "exactlyOf": {
                        "type": "object",
                        "properties": {
                            "concrete": node_type_ref
                        },
                        "required": ["concrete"],
                        "additionalProperties": False
                    }
                },
                "required": ["exactlyOf"],
                "additionalProperties": False,
                "description": "Exact match with concrete type (two-level)"
            },
            
            # Two-level: exactlyOf with abstract
            {
                "type": "object",
                "properties": {
                    "exactlyOf": {
                        "type": "object",
                        "properties": {
                            "abstract": node_type_ref
                        },
                        "required": ["abstract"],
                        "additionalProperties": False
                    }
                },
                "required": ["exactlyOf"],
                "additionalProperties": False,
                "description": "Exact match with abstract type (two-level)"
            },
            
            # Two-level: subtypesOf with concrete
            {
                "type": "object",
                "properties": {
                    "subtypesOf": {
                        "type": "object",
                        "properties": {
                            "concrete": node_type_ref
                        },
                        "required": ["concrete"],
                        "additionalProperties": False
                    }
                },
                "required": ["subtypesOf"],
                "additionalProperties": False,
                "description": "Subtype match with concrete type (two-level)"
            },
            
            # Two-level: subtypesOf with abstract
            {
                "type": "object",
                "properties": {
                    "subtypesOf": {
                        "type": "object",
                        "properties": {
                            "abstract": node_type_ref
                        },
                        "required": ["abstract"],
                        "additionalProperties": False
                    }
                },
                "required": ["subtypesOf"],
                "additionalProperties": False,
                "description": "Subtype match with abstract type (two-level)"
            }
        ]
    }
    
    # Create similar patterns for EdgeType
    edge_type_with_wrappers = {
        "oneOf": [
            # Zero-level: bare EdgeType reference
            edge_type_ref,
            
            # One-level: abstract wrapper
            {
                "type": "object",
                "properties": {
                    "abstract": edge_type_ref
                },
                "required": ["abstract"],
                "additionalProperties": False,
                "description": "Abstract type wrapper (one-level) - maps to subtypesOf: abstract:"
            },
            
            # One-level: concrete wrapper
            {
                "type": "object",
                "properties": {
                    "concrete": edge_type_ref
                },
                "required": ["concrete"],
                "additionalProperties": False,
                "description": "Concrete type wrapper (one-level) - maps to exactlyOf: concrete:"
            },
            
            # One-level: properSubtypesOf wrapper
            {
                "type": "object",
                "properties": {
                    "properSubtypesOf": edge_type_ref
                },
                "required": ["properSubtypesOf"],
                "additionalProperties": False,
                "description": "Proper subtypes wrapper (one-level) - maps to subtypesOf: abstract:"
            },
            
            # Two-level: exactlyOf with concrete
            {
                "type": "object",
                "properties": {
                    "exactlyOf": {
                        "type": "object",
                        "properties": {
                            "concrete": edge_type_ref
                        },
                        "required": ["concrete"],
                        "additionalProperties": False
                    }
                },
                "required": ["exactlyOf"],
                "additionalProperties": False,
                "description": "Exact match with concrete type (two-level)"
            },
            
            # Two-level: exactlyOf with abstract
            {
                "type": "object",
                "properties": {
                    "exactlyOf": {
                        "type": "object",
                        "properties": {
                            "abstract": edge_type_ref
                        },
                        "required": ["abstract"],
                        "additionalProperties": False
                    }
                },
                "required": ["exactlyOf"],
                "additionalProperties": False,
                "description": "Exact match with abstract type (two-level)"
            },
            
            # Two-level: subtypesOf with concrete
            {
                "type": "object",
                "properties": {
                    "subtypesOf": {
                        "type": "object",
                        "properties": {
                            "concrete": edge_type_ref
                        },
                        "required": ["concrete"],
                        "additionalProperties": False
                    }
                },
                "required": ["subtypesOf"],
                "additionalProperties": False,
                "description": "Subtype match with concrete type (two-level)"
            },
            
            # Two-level: subtypesOf with abstract
            {
                "type": "object",
                "properties": {
                    "subtypesOf": {
                        "type": "object",
                        "properties": {
                            "abstract": edge_type_ref
                        },
                        "required": ["abstract"],
                        "additionalProperties": False
                    }
                },
                "required": ["subtypesOf"],
                "additionalProperties": False,
                "description": "Subtype match with abstract type (two-level)"
            }
        ]
    }
    
    return node_type_with_wrappers, edge_type_with_wrappers


def create_array_wrapper_for_node_types():
    """Create wrapper patterns that can wrap entire nodeTypes arrays or subsequences."""
    
    node_type_ref = {"$ref": "#/$defs/NodeTypeWithWrappers"}
    
    # Pattern for wrapping a nodeTypes array or subsequence
    wrapped_node_types_array = {
        "oneOf": [
            # One-level: abstract wrapper around nodeTypes array
            {
                "type": "object",
                "properties": {
                    "abstract": {
                        "type": "object",
                        "properties": {
                            "nodeTypes": {
                                "type": "array",
                                "items": node_type_ref
                            }
                        },
                        "required": ["nodeTypes"],
                        "additionalProperties": False
                    }
                },
                "required": ["abstract"],
                "additionalProperties": False,
                "description": "Abstract wrapper around nodeTypes array"
            },
            
            # One-level: concrete wrapper around nodeTypes array
            {
                "type": "object",
                "properties": {
                    "concrete": {
                        "type": "object",
                        "properties": {
                            "nodeTypes": {
                                "type": "array",
                                "items": node_type_ref
                            }
                        },
                        "required": ["nodeTypes"],
                        "additionalProperties": False
                    }
                },
                "required": ["concrete"],
                "additionalProperties": False,
                "description": "Concrete wrapper around nodeTypes array"
            },
            
            # One-level: properSubtypesOf wrapper around nodeTypes array
            {
                "type": "object",
                "properties": {
                    "properSubtypesOf": {
                        "type": "object",
                        "properties": {
                            "nodeTypes": {
                                "type": "array",
                                "items": node_type_ref
                            }
                        },
                        "required": ["nodeTypes"],
                        "additionalProperties": False
                    }
                },
                "required": ["properSubtypesOf"],
                "additionalProperties": False,
                "description": "ProperSubtypesOf wrapper around nodeTypes array"
            },
            
            # Two-level wrappers for arrays...
            {
                "type": "object",
                "properties": {
                    "exactlyOf": {
                        "type": "object",
                        "properties": {
                            "concrete": {
                                "type": "object",
                                "properties": {
                                    "nodeTypes": {
                                        "type": "array",
                                        "items": node_type_ref
                                    }
                                },
                                "required": ["nodeTypes"],
                                "additionalProperties": False
                            }
                        },
                        "required": ["concrete"],
                        "additionalProperties": False
                    }
                },
                "required": ["exactlyOf"],
                "additionalProperties": False,
                "description": "ExactlyOf-concrete wrapper around nodeTypes array"
            },
            
            {
                "type": "object",
                "properties": {
                    "subtypesOf": {
                        "type": "object",
                        "properties": {
                            "abstract": {
                                "type": "object",
                                "properties": {
                                    "nodeTypes": {
                                        "type": "array",
                                        "items": node_type_ref
                                    }
                                },
                                "required": ["nodeTypes"],
                                "additionalProperties": False
                            }
                        },
                        "required": ["abstract"],
                        "additionalProperties": False
                    }
                },
                "required": ["subtypesOf"],
                "additionalProperties": False,
                "description": "SubtypesOf-abstract wrapper around nodeTypes array"
            }
        ]
    }
    
    return wrapped_node_types_array


def update_schema():
    """Update the pre-import schema with wrapper support."""
    
    schema_path = 'src/grasch/schemas/lex-2026.0.3.2-pre-import.schema.json'
    
    print(f"Loading schema from {schema_path}...")
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    # Create wrapper definitions
    node_type_with_wrappers, edge_type_with_wrappers = create_wrapper_definitions()
    
    # Add new definitions to schema
    schema['$defs']['NodeTypeWithWrappers'] = node_type_with_wrappers
    schema['$defs']['EdgeTypeWithWrappers'] = edge_type_with_wrappers
    
    # Update GraphType's nodeTypes property to use wrappers
    graph_type = schema['$defs']['GraphType']
    if 'properties' in graph_type and 'nodeTypes' in graph_type['properties']:
        # Update the items in the nodeTypes array to allow wrappers
        node_types_prop = graph_type['properties']['nodeTypes']
        if 'oneOf' in node_types_prop:
            for option in node_types_prop['oneOf']:
                if 'type' in option and option['type'] == 'array':
                    # Update items to use NodeTypeWithWrappers
                    if 'items' in option and 'oneOf' in option['items']:
                        # Find the NodeType reference and replace with NodeTypeWithWrappers
                        for i, item_option in enumerate(option['items']['oneOf']):
                            if '$ref' in item_option and item_option['$ref'] == '#/$defs/NodeType':
                                option['items']['oneOf'][i] = {'$ref': '#/$defs/NodeTypeWithWrappers'}
    
    # Update GraphType's edgeTypes property to use wrappers
    if 'properties' in graph_type and 'edgeTypes' in graph_type['properties']:
        edge_types_prop = graph_type['properties']['edgeTypes']
        if 'oneOf' in edge_types_prop:
            for option in edge_types_prop['oneOf']:
                if 'type' in option and option['type'] == 'array':
                    if 'items' in option and 'oneOf' in option['items']:
                        for i, item_option in enumerate(option['items']['oneOf']):
                            if '$ref' in item_option and item_option['$ref'] == '#/$defs/EdgeType':
                                option['items']['oneOf'][i] = {'$ref': '#/$defs/EdgeTypeWithWrappers'}
    
    # Save updated schema
    print(f"Saving updated schema to {schema_path}...")
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("Schema updated successfully!")
    print("\nAdded definitions:")
    print("  - NodeTypeWithWrappers: Supports zero-level, one-level, and two-level wrappers")
    print("  - EdgeTypeWithWrappers: Supports zero-level, one-level, and two-level wrappers")
    print("\nUpdated properties:")
    print("  - GraphType.nodeTypes: Now accepts wrapped node types")
    print("  - GraphType.edgeTypes: Now accepts wrapped edge types")


if __name__ == '__main__':
    try:
        update_schema()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
