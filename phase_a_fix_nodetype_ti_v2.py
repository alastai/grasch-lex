#!/usr/bin/env python3
"""
Phase A: Fix schema to support TI wrappers for single nodeType - Version 2

The issue: NodeTypeItem already has TI wrapper support, but it needs to reference
the bare NodeType structure, not a wrapped version.

Solution: Keep NodeType as the bare structure, and ensure NodeTypeItem properly
references it for TI wrappers.
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

def fix_nodetype_item(schema):
    """
    The NodeTypeItem already has the right structure for TI wrappers.
    We just need to ensure it's working correctly.
    
    The issue is that we changed NodeType to be wrapped, but NodeTypeItem
    expects to wrap a bare NodeType. Let's revert our changes and verify
    NodeTypeItem is correct.
    """
    
    # Check if we have BareNodeType (from our previous attempt)
    if "BareNodeType" in schema["$defs"]:
        print("Found BareNodeType from previous attempt")
        # Restore NodeType to be the bare version
        schema["$defs"]["NodeType"] = schema["$defs"]["BareNodeType"]
        del schema["$defs"]["BareNodeType"]
        print("✓ Restored NodeType to bare structure")
        
        # Remove the TI definitions we added
        if "TypeInterpretationContent" in schema["$defs"]:
            del schema["$defs"]["TypeInterpretationContent"]
        if "TypeInterpretationShorthand" in schema["$defs"]:
            del schema["$defs"]["TypeInterpretationShorthand"]
        if "TypeInterpretationExplicit" in schema["$defs"]:
            del schema["$defs"]["TypeInterpretationExplicit"]
        print("✓ Removed incorrect TI definitions")
    
    # Now verify NodeTypeItem has all the TI wrappers we need
    node_type_item = schema["$defs"]["NodeTypeItem"]
    
    # Check what wrappers are supported
    wrappers = []
    for option in node_type_item["oneOf"]:
        if "$ref" in option:
            wrappers.append("bare (0-level)")
        elif "properties" in option:
            wrapper_keys = list(option["properties"].keys())
            if wrapper_keys:
                wrappers.append(wrapper_keys[0])
    
    print(f"\n✓ NodeTypeItem currently supports: {', '.join(wrappers)}")
    
    # Check if we're missing properSubtypesOf at 2-level
    has_2level_properSubtypesOf = False
    for option in node_type_item["oneOf"]:
        if "properties" in option and "properSubtypesOf" in option["properties"]:
            # Check if it's 2-level (has oneOf inside)
            prop_value = option["properties"]["properSubtypesOf"]
            if isinstance(prop_value, dict) and "oneOf" in prop_value:
                has_2level_properSubtypesOf = True
    
    if not has_2level_properSubtypesOf:
        print("\n⚠ Missing 2-level properSubtypesOf wrapper")
        print("Adding 2-level properSubtypesOf wrapper...")
        
        # Find the properSubtypesOf 1-level wrapper and update it to 2-level
        for i, option in enumerate(node_type_item["oneOf"]):
            if ("properties" in option and 
                "properSubtypesOf" in option["properties"] and
                "$ref" in option["properties"]["properSubtypesOf"]):
                
                # This is the 1-level version, keep it but also add 2-level
                # Actually, let's add a new 2-level version
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
                                            "$ref": "#/$defs/NodeType"
                                        }
                                    },
                                    "additionalProperties": False
                                },
                                {
                                    "type": "object",
                                    "required": ["abstract"],
                                    "properties": {
                                        "abstract": {
                                            "$ref": "#/$defs/NodeType"
                                        }
                                    },
                                    "additionalProperties": False
                                }
                            ]
                        }
                    },
                    "additionalProperties": False
                }
                
                # Insert after the existing 2-level wrappers
                # Find where subtypesOf 2-level is
                insert_pos = i + 1
                for j in range(i, len(node_type_item["oneOf"])):
                    if ("properties" in node_type_item["oneOf"][j] and 
                        "subtypesOf" in node_type_item["oneOf"][j]["properties"]):
                        insert_pos = j + 1
                        break
                
                node_type_item["oneOf"].insert(insert_pos, new_option)
                print("✓ Added 2-level properSubtypesOf wrapper")
                break
    
    return schema

def main():
    print("Phase A: Fixing NodeTypeItem for TI wrappers (v2)\n")
    
    # Load schema
    print("Loading schema...")
    schema = load_schema()
    print(f"✓ Loaded schema from {SCHEMA_PATH}\n")
    
    # Fix NodeTypeItem
    print("Checking and fixing NodeTypeItem...")
    schema = fix_nodetype_item(schema)
    print()
    
    # Save schema
    print("Saving schema...")
    save_schema(schema)
    print()
    
    print("✅ Phase A schema fix complete!")
    print("\nThe schema now supports TI wrappers for single nodeType via NodeTypeItem")

if __name__ == "__main__":
    main()
