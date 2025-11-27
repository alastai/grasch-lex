#!/usr/bin/env python3
"""
Phase A: Fix schema to support TI wrappers for single nodeType

This script:
1. Adds reusable TI pattern definitions to $defs
2. Updates NodeType definition to support 0/1/2-level TI wrappers
3. Validates the schema is still valid JSON
"""

import json
from pathlib import Path

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

def load_schema():
    """Load the current schema"""
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)

def save_schema(schema):
    """Save the schema with proper formatting"""
    with open(SCHEMA_PATH, 'w') as f:
        json.dump(schema, f, indent=2)
    print(f"✓ Schema saved to {SCHEMA_PATH}")

def add_ti_definitions(schema):
    """Add reusable TI pattern definitions to $defs"""
    
    # Create the TI wrapper definitions
    ti_defs = {
        "TypeInterpretationContent": {
            "description": "Content that can appear inside a type interpretation wrapper",
            "oneOf": [
                {"$ref": "#/$defs/NodeType"},
                {"$ref": "#/$defs/EdgeType"}
            ]
        },
        
        "TypeInterpretationShorthand": {
            "description": "1-level shorthand TI wrappers: abstract, concrete, properSubtypesOf, final, sealed",
            "type": "object",
            "oneOf": [
                {
                    "required": ["abstract"],
                    "properties": {
                        "abstract": {"$ref": "#/$defs/TypeInterpretationContent"}
                    },
                    "additionalProperties": False
                },
                {
                    "required": ["concrete"],
                    "properties": {
                        "concrete": {"$ref": "#/$defs/TypeInterpretationContent"}
                    },
                    "additionalProperties": False
                },
                {
                    "required": ["properSubtypesOf"],
                    "properties": {
                        "properSubtypesOf": {"$ref": "#/$defs/TypeInterpretationContent"}
                    },
                    "additionalProperties": False
                },
                {
                    "required": ["final"],
                    "properties": {
                        "final": {"$ref": "#/$defs/TypeInterpretationContent"}
                    },
                    "additionalProperties": False
                },
                {
                    "required": ["sealed"],
                    "properties": {
                        "sealed": {"$ref": "#/$defs/TypeInterpretationContent"}
                    },
                    "additionalProperties": False
                }
            ]
        },
        
        "TypeInterpretationExplicit": {
            "description": "2-level explicit TI wrappers: exactlyOf, subtypesOf, properSubtypesOf",
            "type": "object",
            "oneOf": [
                {
                    "required": ["exactlyOf"],
                    "properties": {
                        "exactlyOf": {
                            "type": "object",
                            "oneOf": [
                                {
                                    "required": ["concrete"],
                                    "properties": {
                                        "concrete": {"$ref": "#/$defs/TypeInterpretationContent"}
                                    },
                                    "additionalProperties": False
                                },
                                {
                                    "required": ["abstract"],
                                    "properties": {
                                        "abstract": {"$ref": "#/$defs/TypeInterpretationContent"}
                                    },
                                    "additionalProperties": False
                                }
                            ]
                        }
                    },
                    "additionalProperties": False
                },
                {
                    "required": ["subtypesOf"],
                    "properties": {
                        "subtypesOf": {
                            "type": "object",
                            "oneOf": [
                                {
                                    "required": ["concrete"],
                                    "properties": {
                                        "concrete": {"$ref": "#/$defs/TypeInterpretationContent"}
                                    },
                                    "additionalProperties": False
                                },
                                {
                                    "required": ["abstract"],
                                    "properties": {
                                        "abstract": {"$ref": "#/$defs/TypeInterpretationContent"}
                                    },
                                    "additionalProperties": False
                                }
                            ]
                        }
                    },
                    "additionalProperties": False
                },
                {
                    "required": ["properSubtypesOf"],
                    "properties": {
                        "properSubtypesOf": {
                            "type": "object",
                            "oneOf": [
                                {
                                    "required": ["concrete"],
                                    "properties": {
                                        "concrete": {"$ref": "#/$defs/TypeInterpretationContent"}
                                    },
                                    "additionalProperties": False
                                },
                                {
                                    "required": ["abstract"],
                                    "properties": {
                                        "abstract": {"$ref": "#/$defs/TypeInterpretationContent"}
                                    },
                                    "additionalProperties": False
                                }
                            ]
                        }
                    },
                    "additionalProperties": False
                }
            ]
        }
    }
    
    # Add the definitions to $defs
    schema["$defs"].update(ti_defs)
    print("✓ Added TI definitions to $defs")
    return schema

def update_nodetype_definition(schema):
    """Update NodeType to support TI wrappers"""
    
    # The current NodeType is just the bare form
    # We need to create a new definition that supports all 3 levels
    
    # Save the current NodeType as BareNodeType
    schema["$defs"]["BareNodeType"] = schema["$defs"]["NodeType"]
    print("✓ Saved current NodeType as BareNodeType")
    
    # Create new NodeType that supports 0/1/2-level wrappers
    schema["$defs"]["NodeType"] = {
        "description": "Node type with optional type interpretation wrappers (0/1/2-level)",
        "oneOf": [
            {
                "description": "0-level: Bare nodeType (implicit exactlyOf: concrete:)",
                "$ref": "#/$defs/BareNodeType"
            },
            {
                "description": "1-level: Shorthand TI wrapper (abstract, concrete, etc.)",
                "$ref": "#/$defs/TypeInterpretationShorthand"
            },
            {
                "description": "2-level: Explicit TI wrapper (exactlyOf, subtypesOf, etc.)",
                "$ref": "#/$defs/TypeInterpretationExplicit"
            }
        ]
    }
    print("✓ Updated NodeType definition to support TI wrappers")
    return schema

def main():
    print("Phase A: Fixing schema for single nodeType with TI wrappers\n")
    
    # Load schema
    print("Loading schema...")
    schema = load_schema()
    print(f"✓ Loaded schema from {SCHEMA_PATH}\n")
    
    # Add TI definitions
    print("Step 1: Adding TI definitions...")
    schema = add_ti_definitions(schema)
    print()
    
    # Update NodeType
    print("Step 2: Updating NodeType definition...")
    schema = update_nodetype_definition(schema)
    print()
    
    # Save schema
    print("Step 3: Saving schema...")
    save_schema(schema)
    print()
    
    print("✅ Phase A schema fix complete!")
    print("\nNext: Create test YAML to validate the changes")

if __name__ == "__main__":
    main()
