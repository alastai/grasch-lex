#!/usr/bin/env python3
"""
Fix Location 2 (nodeTypesInterpretation) in LEX-2026.0.3.2 Schema

This script adds exactlyOf and properSubtypesOf properties to GraphType definition
to enable sibling TI-wrapped nodeTypes/edgeTypes properties.

The fix follows the existing pattern used for subtypesOf in GraphType.
"""

import json
from pathlib import Path

def load_schema():
    """Load the schema file"""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        return json.load(f)

def save_schema(schema):
    """Save the schema file with proper formatting"""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
    print(f"✅ Schema saved to {schema_path}")

def add_exactlyof_property(graphtype_def):
    """Add exactlyOf property to GraphType definition"""
    
    # Create the exactlyOf property structure (similar to subtypesOf)
    exactlyof_property = {
        "type": "object",
        "description": "Exact type matching (invariant matching)",
        "properties": {
            "concrete": {
                "type": "object",
                "description": "Concrete types that can be instantiated",
                "properties": {
                    "nodeTypes": {
                        "oneOf": [
                            {
                                "type": "array",
                                "items": {"$ref": "#/$defs/NodeType"}
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
                    },
                    "edgeTypes": {
                        "oneOf": [
                            {
                                "type": "array",
                                "items": {"$ref": "#/$defs/EdgeType"}
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
                },
                "additionalProperties": False
            },
            "abstract": {
                "type": "object",
                "description": "Abstract types that cannot be instantiated directly",
                "properties": {
                    "nodeTypes": {
                        "oneOf": [
                            {
                                "type": "array",
                                "items": {"$ref": "#/$defs/NodeType"}
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
                    },
                    "edgeTypes": {
                        "oneOf": [
                            {
                                "type": "array",
                                "items": {"$ref": "#/$defs/EdgeType"}
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
                },
                "additionalProperties": False
            },
            "nodeTypes": {
                "oneOf": [
                    {
                        "type": "array",
                        "description": "Node types with exact matching (default concrete)",
                        "items": {"$ref": "#/$defs/NodeType"}
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
            },
            "edgeTypes": {
                "oneOf": [
                    {
                        "type": "array",
                        "description": "Edge types with exact matching (default concrete)",
                        "items": {"$ref": "#/$defs/EdgeType"}
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
        },
        "additionalProperties": False
    }
    
    # Add exactlyOf to properties
    graphtype_def["properties"]["exactlyOf"] = exactlyof_property
    print("✅ Added exactlyOf property to GraphType")

def add_propersubtypesof_property(graphtype_def):
    """Add properSubtypesOf property to GraphType definition"""
    
    # Create the properSubtypesOf property structure (similar to subtypesOf)
    propersubtypesof_property = {
        "type": "object",
        "description": "Proper subtype matching (covariant matching, excluding supertype)",
        "properties": {
            "concrete": {
                "type": "object",
                "description": "Concrete types that can be instantiated",
                "properties": {
                    "nodeTypes": {
                        "oneOf": [
                            {
                                "type": "array",
                                "items": {"$ref": "#/$defs/NodeType"}
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
                    },
                    "edgeTypes": {
                        "oneOf": [
                            {
                                "type": "array",
                                "items": {"$ref": "#/$defs/EdgeType"}
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
                },
                "additionalProperties": False
            },
            "abstract": {
                "type": "object",
                "description": "Abstract types that cannot be instantiated directly",
                "properties": {
                    "nodeTypes": {
                        "oneOf": [
                            {
                                "type": "array",
                                "items": {"$ref": "#/$defs/NodeType"}
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
                    },
                    "edgeTypes": {
                        "oneOf": [
                            {
                                "type": "array",
                                "items": {"$ref": "#/$defs/EdgeType"}
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
                },
                "additionalProperties": False
            },
            "nodeTypes": {
                "oneOf": [
                    {
                        "type": "array",
                        "description": "Node types with proper subtype matching (default abstract)",
                        "items": {"$ref": "#/$defs/NodeType"}
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
            },
            "edgeTypes": {
                "oneOf": [
                    {
                        "type": "array",
                        "description": "Edge types with proper subtype matching (default abstract)",
                        "items": {"$ref": "#/$defs/EdgeType"}
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
        },
        "additionalProperties": False
    }
    
    # Add properSubtypesOf to properties
    graphtype_def["properties"]["properSubtypesOf"] = propersubtypesof_property
    print("✅ Added properSubtypesOf property to GraphType")

def main():
    """Main function to apply the fix"""
    print("="*70)
    print("Task 8: Fix Location 2 (nodeTypesInterpretation)")
    print("="*70)
    
    # Load schema
    print("\n📖 Loading schema...")
    schema = load_schema()
    print("✅ Schema loaded")
    
    # Find GraphType definition
    print("\n🔍 Locating GraphType definition...")
    if "GraphType" not in schema["$defs"]:
        print("❌ ERROR: GraphType definition not found in schema")
        return 1
    
    graphtype_def = schema["$defs"]["GraphType"]
    print("✅ GraphType definition found")
    
    # Check if properties already exist
    if "exactlyOf" in graphtype_def["properties"]:
        print("⚠️  exactlyOf property already exists - skipping")
    else:
        print("\n➕ Adding exactlyOf property...")
        add_exactlyof_property(graphtype_def)
    
    if "properSubtypesOf" in graphtype_def["properties"]:
        print("⚠️  properSubtypesOf property already exists - skipping")
    else:
        print("\n➕ Adding properSubtypesOf property...")
        add_propersubtypesof_property(graphtype_def)
    
    # Save schema
    print("\n💾 Saving schema...")
    save_schema(schema)
    
    print("\n" + "="*70)
    print("✅ Location 2 Fix Complete!")
    print("="*70)
    print("\nChanges made:")
    print("- Added 'exactlyOf' property to GraphType definition")
    print("- Added 'properSubtypesOf' property to GraphType definition")
    print("\nThis enables sibling TI-wrapped nodeTypes/edgeTypes properties:")
    print("  graphType:")
    print("    nodeTypes: [...]              # Bare (0-level)")
    print("    exactlyOf:                    # 2-level TI (sibling)")
    print("      concrete:")
    print("        nodeTypes: [...]")
    print("    properSubtypesOf:             # 2-level TI (sibling)")
    print("      abstract:")
    print("        nodeTypes: [...]")
    print("\nNext step: Run validate_phase_e_locations_2_3.py to test the fix")
    
    return 0

if __name__ == "__main__":
    exit(main())
