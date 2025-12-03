#!/usr/bin/env python3
"""
Phase B: Fix schema to support TI wrappers for single edgeType

This script adds the missing 2-level properSubtypesOf wrapper to EdgeTypeItem
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

def fix_edgetype_item(schema):
    """Add 2-level properSubtypesOf wrapper to EdgeTypeItem"""
    
    edge_type_item = schema["$defs"]["EdgeTypeItem"]
    
    # Check what wrappers are supported
    wrappers = []
    for option in edge_type_item["oneOf"]:
        if "$ref" in option:
            wrappers.append("bare (0-level)")
        elif "properties" in option:
            wrapper_keys = list(option["properties"].keys())
            if wrapper_keys:
                wrappers.append(wrapper_keys[0])
    
    print(f"\n✓ EdgeTypeItem currently supports: {', '.join(wrappers)}")
    
    # Check if we're missing properSubtypesOf at 2-level
    has_2level_properSubtypesOf = False
    for option in edge_type_item["oneOf"]:
        if "properties" in option and "properSubtypesOf" in option["properties"]:
            # Check if it's 2-level (has oneOf inside)
            prop_value = option["properties"]["properSubtypesOf"]
            if isinstance(prop_value, dict) and "oneOf" in prop_value:
                has_2level_properSubtypesOf = True
    
    if not has_2level_properSubtypesOf:
        print("\n⚠ Missing 2-level properSubtypesOf wrapper")
        print("Adding 2-level properSubtypesOf wrapper...")
        
        # Find the properSubtypesOf 1-level wrapper and add 2-level after subtypesOf
        for i, option in enumerate(edge_type_item["oneOf"]):
            if ("properties" in option and 
                "subtypesOf" in option["properties"] and
                "oneOf" in option["properties"]["subtypesOf"]):
                
                # This is the 2-level subtypesOf, add properSubtypesOf after it
                new_option = {
                    "type": "object",
                    "description": "Two-level wrapper: properSubtypesOf with concreteness",
                    "required": ["properSubtypesOf"],
                    "properties": {
                        "properSubtypesOf": {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "required": ["concrete"],
                                    "properties": {
                                        "concrete": {
                                            "$ref": "#/$defs/EdgeType"
                                        }
                                    },
                                    "additionalProperties": False
                                },
                                {
                                    "type": "object",
                                    "required": ["abstract"],
                                    "properties": {
                                        "abstract": {
                                            "$ref": "#/$defs/EdgeType"
                                        }
                                    },
                                    "additionalProperties": False
                                }
                            ]
                        }
                    },
                    "additionalProperties": False
                }
                
                # Insert after the 2-level subtypesOf
                insert_pos = i + 1
                edge_type_item["oneOf"].insert(insert_pos, new_option)
                print("✓ Added 2-level properSubtypesOf wrapper to EdgeTypeItem")
                break
    else:
        print("\n✓ EdgeTypeItem already has 2-level properSubtypesOf wrapper")
    
    return schema

def main():
    print("Phase B: Fixing EdgeTypeItem for TI wrappers\n")
    
    # Load schema
    print("Loading schema...")
    schema = load_schema()
    print(f"✓ Loaded schema from {SCHEMA_PATH}\n")
    
    # Fix EdgeTypeItem
    print("Checking and fixing EdgeTypeItem...")
    schema = fix_edgetype_item(schema)
    print()
    
    # Save schema
    print("Saving schema...")
    save_schema(schema)
    print()
    
    print("✅ Phase B schema fix complete!")
    print("\nThe schema now supports TI wrappers for single edgeType via EdgeTypeItem")

if __name__ == "__main__":
    main()
