#!/usr/bin/env python3
"""
Fix TI-content import pattern definitions - singleton sets are just arrays with 1 element.
Remove the incorrect anyOf pattern that treats singletons as special.
"""

import json
from pathlib import Path

def fix_ti_import_definitions():
    """Fix reusable definitions - singleton sets are just sets with cardinality 1."""
    
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    
    # Read the schema
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    # Remove the incorrect definitions
    defs_to_remove = [
        "NodeTypeOrImport",
        "NodeTypeSetOrImport", 
        "EdgeTypeOrImport",
        "EdgeTypeSetOrImport",
        "NodeTypesArrayOrImport",
        "EdgeTypesArrayOrImport"
    ]
    
    for def_name in defs_to_remove:
        if def_name in schema["$defs"]:
            del schema["$defs"][def_name]
    
    # Add correct definitions - arrays handle ALL sets (including singleton)
    correct_defs = {
        "NodeTypesArrayOrImport": {
            "description": "Array of NodeTypes or import - handles all set cardinalities (singleton sets are just arrays with 1 element)",
            "oneOf": [
                {
                    "description": "Inline array of node types (any cardinality)",
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
            "description": "Array of EdgeTypes or import - handles all set cardinalities (singleton sets are just arrays with 1 element)",
            "oneOf": [
                {
                    "description": "Inline array of edge types (any cardinality)",
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
    
    # Add the correct definitions
    schema["$defs"].update(correct_defs)
    
    # Write back the schema
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("✓ Fixed TI-content import pattern definitions")
    print(f"  - NodeTypesArrayOrImport: Array or import (handles ALL cardinalities)")
    print(f"  - EdgeTypesArrayOrImport: Array or import (handles ALL cardinalities)")
    print("\nKey insight:")
    print("  ✓ Singleton sets are just arrays with 1 element")
    print("  ✓ No special handling needed - arrays handle all cardinalities")
    print("  ✓ Indentation delimits sets in YAML, arrays represent sets in JSON Schema")

if __name__ == "__main__":
    fix_ti_import_definitions()
