#!/usr/bin/env python3
"""
Fix GraphSchemaContent (Location 1) in the schema - CORRECT VERSION:
1. Remove ALL patternProperties
2. Add explicit properties for all TI wrappers
   - 1-level: concrete, abstract, sealed, final (contain graphType directly)
   - 2-level: exactlyOf, subtypesOf, properSubtypesOf (MUST contain one finalization property)
3. Update oneOf to include all explicit properties
"""

import json

SCHEMA_PATH = "src/grasch/schemas/lex-2026.0.3.2.schema.json"

def fix_graphschema_content():
    """Fix GraphSchemaContent definition"""
    
    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)
    
    # Define the graphType reference that will be reused
    graphtype_ref = {
        "oneOf": [
            {
                "$ref": "#/$defs/GraphType"
            },
            {
                "type": "object",
                "description": "Import content from file",
                "required": ["import"],
                "properties": {
                    "import": {
                        "type": "string",
                        "description": "Import content from file"
                    }
                },
                "additionalProperties": False
            }
        ]
    }
    
    # Define one-level TI wrapper structure (for concrete, abstract, sealed, final)
    # These contain graphType directly
    one_level_wrapper = {
        "type": "object",
        "description": "One-level TI wrapper for graphType",
        "properties": {
            "graphType": graphtype_ref
        },
        "additionalProperties": False,
        "required": ["graphType"]
    }
    
    # Define two-level TI wrapper structure (for exactlyOf, subtypesOf, properSubtypesOf)
    # These MUST contain exactly one finalization property (concrete, abstract, sealed, final)
    two_level_wrapper = {
        "type": "object",
        "description": "Two-level TI wrapper - must contain exactly one finalization property",
        "properties": {
            "abstract": one_level_wrapper,
            "concrete": one_level_wrapper,
            "sealed": one_level_wrapper,
            "final": one_level_wrapper
        },
        "additionalProperties": False,
        "oneOf": [
            {"required": ["abstract"]},
            {"required": ["concrete"]},
            {"required": ["sealed"]},
            {"required": ["final"]}
        ]
    }
    
    # Build the new GraphSchemaContent definition
    new_graphschema_content = {
        "type": "object",
        "description": "Graph schema specification - structural graph type plus constraints",
        "required": ["pathName"],
        "properties": {
            "pathName": {
                "type": "string",
                "description": "Path name for the graph schema"
            },
            "principal": {
                "type": "string",
                "description": "The owner of the graph schema, an authorization identifier of a principal"
            },
            "graphType": graphtype_ref,
            "constraints": {
                "type": "object",
                "description": "A map of constraint names to constraint descriptors (optional)",
                "additionalProperties": {
                    "$ref": "#/$defs/Constraint"
                }
            },
            # Add explicit 1-level TI wrapper properties
            "concrete": one_level_wrapper,
            "abstract": one_level_wrapper,
            "sealed": one_level_wrapper,
            "final": one_level_wrapper,
            # Add explicit 2-level TI wrapper properties
            "exactlyOf": two_level_wrapper,
            "subtypesOf": two_level_wrapper,
            "properSubtypesOf": two_level_wrapper
        },
        "additionalProperties": False,
        "oneOf": [
            {"required": ["pathName", "graphType"]},
            {"required": ["pathName", "abstract"]},
            {"required": ["pathName", "concrete"]},
            {"required": ["pathName", "sealed"]},
            {"required": ["pathName", "final"]},
            {"required": ["pathName", "exactlyOf"]},
            {"required": ["pathName", "subtypesOf"]},
            {"required": ["pathName", "properSubtypesOf"]}
        ]
    }
    
    # Replace GraphSchemaContent in schema
    schema["$defs"]["GraphSchemaContent"] = new_graphschema_content
    
    # Write back to file
    with open(SCHEMA_PATH, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("✓ Fixed GraphSchemaContent (Location 1) - CORRECT VERSION")
    print("  - Removed ALL patternProperties")
    print("  - Added 1-level TI wrappers: concrete, abstract, sealed, final")
    print("    (these contain graphType directly)")
    print("  - Added 2-level TI wrappers: exactlyOf, subtypesOf, properSubtypesOf")
    print("    (these MUST contain exactly one finalization property)")
    print("  - Updated oneOf constraint to include all 8 options")

if __name__ == "__main__":
    fix_graphschema_content()
