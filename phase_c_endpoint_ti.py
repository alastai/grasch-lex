#!/usr/bin/env python3
"""Phase C: Fix EndpointReference for TI wrappers"""

import json
from pathlib import Path

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

def main():
    print("Phase C: Fixing EndpointReference\n")
    
    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)
    
    endpoint_ref = schema["$defs"]["EndpointReference"]
    
    # Check for 2-level properSubtypesOf
    has_it = False
    for option in endpoint_ref["oneOf"]:
        if ("required" in option and 
            "properSubtypesOf" in option.get("required", []) and
            "oneOf" in option.get("properties", {}).get("properSubtypesOf", {})):
            has_it = True
    
    if not has_it:
        print("Adding 2-level properSubtypesOf...")
        
        # Find subtypesOf 2-level
        for i, option in enumerate(endpoint_ref["oneOf"]):
            if ("required" in option and 
                "subtypesOf" in option.get("required", []) and
                "oneOf" in option.get("properties", {}).get("subtypesOf", {})):
                
                new_option = {
                    "type": "object",
                    "required": ["properSubtypesOf"],
                    "properties": {
                        "properSubtypesOf": {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "required": ["concrete"],
                                    "properties": {
                                        "concrete": {"$ref": "#/$defs/EndpointReferenceBase"}
                                    },
                                    "additionalProperties": False
                                },
                                {
                                    "type": "object",
                                    "required": ["abstract"],
                                    "properties": {
                                        "abstract": {"$ref": "#/$defs/EndpointReferenceBase"}
                                    },
                                    "additionalProperties": False
                                }
                            ]
                        }
                    },
                    "additionalProperties": False,
                    "description": "Proper subtypes with concreteness (two-level wrapper)"
                }
                
                endpoint_ref["oneOf"].insert(i + 1, new_option)
                print("✓ Added 2-level properSubtypesOf")
                break
        
        with open(SCHEMA_PATH, 'w') as f:
            json.dump(schema, f, indent=2)
        print("✓ Schema saved")
    else:
        print("✓ Already has 2-level properSubtypesOf")
    
    print("\n✅ Phase C complete!")

if __name__ == "__main__":
    main()
