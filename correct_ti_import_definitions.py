#!/usr/bin/env python3
"""
Correct TI-content import pattern definitions:
1. Use singular names (NodeTypeArray not NodeTypesArray)
2. Add definitions that support wrapper duplication/stripping (nodeTypes:/edgeTypes:)
"""

import json
from pathlib import Path

def correct_ti_import_definitions():
    """Create correct reusable definitions with proper naming and wrapper support."""
    
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    
    # Read the schema
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    # Remove incorrect definitions
    if "NodeTypesArrayOrImport" in schema["$defs"]:
        del schema["$defs"]["NodeTypesArrayOrImport"]
    if "EdgeTypesArrayOrImport" in schema["$defs"]:
        del schema["$defs"]["EdgeTypesArrayOrImport"]
    
    # Add correct definitions
    correct_defs = {
        "NodeTypeArrayOrImport": {
            "description": "Array of NodeTypes or import - handles all set cardinalities",
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
        
        "EdgeTypeArrayOrImport": {
            "description": "Array of EdgeTypes or import - handles all set cardinalities",
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
        },
        
        "NodeTypeSetOrImport": {
            "description": "Set of node types with optional nodeTypes: wrapper (allows duplication/stripping)",
            "oneOf": [
                {
                    "description": "Inline array (no wrapper)",
                    "$ref": "#/$defs/NodeTypesArray"
                },
                {
                    "description": "With nodeTypes: wrapper (can be stripped during canonicalization)",
                    "type": "object",
                    "required": ["nodeTypes"],
                    "properties": {
                        "nodeTypes": {
                            "$ref": "#/$defs/NodeTypeArrayOrImport"
                        }
                    },
                    "additionalProperties": False
                },
                {
                    "description": "Import node type set",
                    "type": "object",
                    "required": ["import"],
                    "properties": {
                        "import": {
                            "type": "string",
                            "description": "Import node type set from file"
                        }
                    },
                    "additionalProperties": False
                }
            ]
        },
        
        "EdgeTypeSetOrImport": {
            "description": "Set of edge types with optional edgeTypes: wrapper (allows duplication/stripping)",
            "oneOf": [
                {
                    "description": "Inline array (no wrapper)",
                    "$ref": "#/$defs/EdgeTypesArray"
                },
                {
                    "description": "With edgeTypes: wrapper (can be stripped during canonicalization)",
                    "type": "object",
                    "required": ["edgeTypes"],
                    "properties": {
                        "edgeTypes": {
                            "$ref": "#/$defs/EdgeTypeArrayOrImport"
                        }
                    },
                    "additionalProperties": False
                },
                {
                    "description": "Import edge type set",
                    "type": "object",
                    "required": ["import"],
                    "properties": {
                        "import": {
                            "type": "string",
                            "description": "Import edge type set from file"
                        }
                    },
                    "additionalProperties": False
                }
            ]
        }
    }
    
    # Add the correct definitions
    schema["$defs"].update(correct_defs)
    
    # Write back the schema
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("✓ Corrected TI-content import pattern definitions")
    print("\nLower-level (array) definitions:")
    print("  - NodeTypeArrayOrImport: Array or import (singular)")
    print("  - EdgeTypeArrayOrImport: Array or import (singular)")
    print("\nHigher-level (set) definitions:")
    print("  - NodeTypeSetOrImport: Supports nodeTypes: wrapper duplication/stripping")
    print("  - EdgeTypeSetOrImport: Supports edgeTypes: wrapper duplication/stripping")
    print("\nKey features:")
    print("  ✓ Singular naming (NodeType not NodeTypes)")
    print("  ✓ Wrapper duplication allowed in PC form")
    print("  ✓ Wrapper stripping during canonicalization to C form")

if __name__ == "__main__":
    correct_ti_import_definitions()
