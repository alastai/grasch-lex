#!/usr/bin/env python3
"""
Update GraphSchemaContent for Single-Level TI System

This script updates the GraphSchemaContent definition to use explicit properties
with the new single-level TI system, eliminating pattern properties.
"""

import json
from pathlib import Path

def load_schema():
    """Load the current schema"""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        return json.load(f)

def create_ti_wrapper_for_graphtype(ti_name, description):
    """Create a TI wrapper that contains a graphType"""
    return {
        "type": "object",
        "description": description,
        "required": ["graphType"],
        "properties": {
            "graphType": {
                "oneOf": [
                    {"$ref": "#/$defs/GraphType"},
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
        },
        "additionalProperties": False
    }

def transform_graphschema_content(schema):
    """Transform GraphSchemaContent to use single-level TI with explicit properties"""
    
    # Create new GraphSchemaContent with explicit properties for single-level TI
    new_graphschema_content = {
        "type": "object",
        "description": "Graph schema specification with single-level TI system using explicit properties",
        "required": ["pathName"],
        "oneOf": [
            # Bare graphType (0-level)
            {
                "properties": {
                    "pathName": {
                        "type": "string",
                        "description": "Path name for the graph schema"
                    },
                    "principal": {
                        "type": "string", 
                        "description": "The owner of the graph schema, an authorization identifier of a principal"
                    },
                    "graphType": {
                        "oneOf": [
                            {"$ref": "#/$defs/GraphType"},
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
                },
                "additionalProperties": False
            },
            # Primary TI forms (1-level)
            {
                "properties": {
                    "pathName": {
                        "type": "string",
                        "description": "Path name for the graph schema"
                    },
                    "principal": {
                        "type": "string",
                        "description": "The owner of the graph schema, an authorization identifier of a principal"
                    },
                    "exactlyOfConcrete": create_ti_wrapper_for_graphtype(
                        "exactlyOfConcrete",
                        "Primary TI form: exact type matching, concrete (instantiable) types"
                    )
                },
                "additionalProperties": False
            },
            {
                "properties": {
                    "pathName": {
                        "type": "string",
                        "description": "Path name for the graph schema"
                    },
                    "principal": {
                        "type": "string",
                        "description": "The owner of the graph schema, an authorization identifier of a principal"
                    },
                    "subtypeOfConcrete": create_ti_wrapper_for_graphtype(
                        "subtypeOfConcrete", 
                        "Primary TI form: subtype matching, concrete (instantiable) types"
                    )
                },
                "additionalProperties": False
            },
            {
                "properties": {
                    "pathName": {
                        "type": "string",
                        "description": "Path name for the graph schema"
                    },
                    "principal": {
                        "type": "string",
                        "description": "The owner of the graph schema, an authorization identifier of a principal"
                    },
                    "subtypeOfAbstract": create_ti_wrapper_for_graphtype(
                        "subtypeOfAbstract",
                        "Primary TI form: subtype matching, abstract (non-instantiable) types"
                    )
                },
                "additionalProperties": False
            },
            # Synonym TI forms (1-level)
            {
                "properties": {
                    "pathName": {
                        "type": "string",
                        "description": "Path name for the graph schema"
                    },
                    "principal": {
                        "type": "string",
                        "description": "The owner of the graph schema, an authorization identifier of a principal"
                    },
                    "concrete": create_ti_wrapper_for_graphtype(
                        "concrete",
                        "Synonym for exactlyOfConcrete: exact type matching, concrete types"
                    )
                },
                "additionalProperties": False
            },
            {
                "properties": {
                    "pathName": {
                        "type": "string",
                        "description": "Path name for the graph schema"
                    },
                    "principal": {
                        "type": "string",
                        "description": "The owner of the graph schema, an authorization identifier of a principal"
                    },
                    "exactlyOf": create_ti_wrapper_for_graphtype(
                        "exactlyOf",
                        "Synonym for exactlyOfConcrete: exact type matching, concrete types"
                    )
                },
                "additionalProperties": False
            },
            {
                "properties": {
                    "pathName": {
                        "type": "string",
                        "description": "Path name for the graph schema"
                    },
                    "principal": {
                        "type": "string",
                        "description": "The owner of the graph schema, an authorization identifier of a principal"
                    },
                    "subtypeOf": create_ti_wrapper_for_graphtype(
                        "subtypeOf",
                        "Synonym for subtypeOfConcrete: subtype matching, concrete types"
                    )
                },
                "additionalProperties": False
            },
            {
                "properties": {
                    "pathName": {
                        "type": "string",
                        "description": "Path name for the graph schema"
                    },
                    "principal": {
                        "type": "string",
                        "description": "The owner of the graph schema, an authorization identifier of a principal"
                    },
                    "properSubtypeOf": create_ti_wrapper_for_graphtype(
                        "properSubtypeOf",
                        "Synonym for subtypeOfAbstract: subtype matching, abstract types"
                    )
                },
                "additionalProperties": False
            }
        ]
    }
    
    return new_graphschema_content

def main():
    """Main transformation function"""
    print("Loading schema...")
    schema = load_schema()
    
    print("Transforming GraphSchemaContent to use explicit properties with single-level TI...")
    schema["$defs"]["GraphSchemaContent"] = transform_graphschema_content(schema)
    
    print("Saving transformed schema...")
    output_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("✅ GraphSchemaContent transformation complete!")
    print("✅ Eliminated pattern properties")
    print("✅ Implemented explicit properties for single-level TI system")
    print("✅ Added oneOf constraint for single graphType wrapper")

if __name__ == "__main__":
    main()