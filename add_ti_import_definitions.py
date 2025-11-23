#!/usr/bin/env python3
"""
Add reusable TI-content import pattern definitions to the schema.
This script adds definitions that support both singleton and multi-element type sets.
"""

import json
from pathlib import Path

def add_ti_import_definitions():
    """Add reusable definitions for TI-content import patterns."""
    
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    
    # Read the schema
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    # Define reusable patterns for TI-content imports
    new_defs = {
        "NodeTypeOrImport": {
            "description": "A single NodeType or import directive",
            "oneOf": [
                {
                    "description": "Inline NodeType",
                    "$ref": "#/$defs/NodeType"
                },
                {
                    "description": "Import NodeType",
                    "type": "object",
                    "required": ["import"],
                    "properties": {
                        "import": {
                            "type": "string",
                            "description": "Import NodeType from file"
                        }
                    },
                    "additionalProperties": False
                }
            ]
        },
        
        "NodeTypeSetOrImport": {
            "description": "A set of NodeTypes (singleton or multi-element) or import directive - indentation delimits the set",
            "oneOf": [
                {
                    "description": "Inline type set (delimited by indentation)",
                    "anyOf": [
                        {
                            "description": "Singleton set (single type)",
                            "$ref": "#/$defs/NodeType"
                        },
                        {
                            "description": "Multi-element set (multiple types at same indentation level)",
                            "type": "array",
                            "items": {"$ref": "#/$defs/NodeType"}
                        }
                    ]
                },
                {
                    "description": "Import type set",
                    "type": "object",
                    "required": ["import"],
                    "properties": {
                        "import": {
                            "type": "string",
                            "description": "Import set of types for this TI"
                        }
                    },
                    "additionalProperties": False
                }
            ]
        },
        
        "EdgeTypeOrImport": {
            "description": "A single EdgeType or import directive",
            "oneOf": [
                {
                    "description": "Inline EdgeType",
                    "$ref": "#/$defs/EdgeType"
                },
                {
                    "description": "Import EdgeType",
                    "type": "object",
                    "required": ["import"],
                    "properties": {
                        "import": {
                            "type": "string",
                            "description": "Import EdgeType from file"
                        }
                    },
                    "additionalProperties": False
                }
            ]
        },
        
        "EdgeTypeSetOrImport": {
            "description": "A set of EdgeTypes (singleton or multi-element) or import directive - indentation delimits the set",
            "oneOf": [
                {
                    "description": "Inline type set (delimited by indentation)",
                    "anyOf": [
                        {
                            "description": "Singleton set (single type)",
                            "$ref": "#/$defs/EdgeType"
                        },
                        {
                            "description": "Multi-element set (multiple types at same indentation level)",
                            "type": "array",
                            "items": {"$ref": "#/$defs/EdgeType"}
                        }
                    ]
                },
                {
                    "description": "Import type set",
                    "type": "object",
                    "required": ["import"],
                    "properties": {
                        "import": {
                            "type": "string",
                            "description": "Import set of types for this TI"
                        }
                    },
                    "additionalProperties": False
                }
            ]
        },
        
        "NodeTypesArrayOrImport": {
            "description": "Array of NodeTypes or import directive",
            "oneOf": [
                {
                    "description": "Inline array of node types",
                    "$ref": "#/$defs/NodeTypesArray"
                },
                {
                    "description": "Import array of node types",
                    "type": "object",
                    "required": ["import"],
                    "properties": {
                        "import": {
                            "type": "string",
                            "description": "Import NodeTypesArray from file"
                        }
                    },
                    "additionalProperties": False
                }
            ]
        },
        
        "EdgeTypesArrayOrImport": {
            "description": "Array of EdgeTypes or import directive",
            "oneOf": [
                {
                    "description": "Inline array of edge types",
                    "$ref": "#/$defs/EdgeTypesArray"
                },
                {
                    "description": "Import array of edge types",
                    "type": "object",
                    "required": ["import"],
                    "properties": {
                        "import": {
                            "type": "string",
                            "description": "Import EdgeTypesArray from file"
                        }
                    },
                    "additionalProperties": False
                }
            ]
        }
    }
    
    # Add the new definitions to the schema
    schema["$defs"].update(new_defs)
    
    # Write back the schema
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("✓ Added reusable TI-content import pattern definitions")
    print(f"  - NodeTypeOrImport: Single NodeType or import")
    print(f"  - NodeTypeSetOrImport: Set of NodeTypes (singleton/multi-element) or import")
    print(f"  - EdgeTypeOrImport: Single EdgeType or import")
    print(f"  - EdgeTypeSetOrImport: Set of EdgeTypes (singleton/multi-element) or import")
    print(f"  - NodeTypesArrayOrImport: Array of NodeTypes or import")
    print(f"  - EdgeTypesArrayOrImport: Array of EdgeTypes or import")
    print("\nThese definitions support:")
    print("  ✓ Singleton sets (cardinality 1)")
    print("  ✓ Multi-element sets (cardinality > 1)")
    print("  ✓ Indentation-based set delimitation")
    print("  ✓ Import at TI level (atomic unit)")

if __name__ == "__main__":
    add_ti_import_definitions()
