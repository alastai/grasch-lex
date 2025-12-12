#!/usr/bin/env python3
"""
Implement Single-Level TI System

This script transforms the LEX-2026.0.3.2 schema from the complex two-level TI system
to the simplified single-level system with three primary forms:
- exactlyOfConcrete
- subtypeOfConcrete  
- subtypeOfAbstract

Plus synonyms:
- concrete -> exactlyOfConcrete
- exactlyOf -> exactlyOfConcrete
- subtypeOf -> subtypeOfConcrete
- properSubtypeOf -> subtypeOfAbstract
"""

import json
import sys
from pathlib import Path

def load_schema():
    """Load the current schema"""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        return json.load(f)

def create_single_level_ti_property(content_ref, description):
    """Create a single-level TI property that wraps content"""
    return {
        "type": "object",
        "description": description,
        "properties": {
            "nodeTypes": {
                "type": "array",
                "items": {"$ref": content_ref}
            },
            "edgeTypes": {
                "type": "array", 
                "items": {"$ref": "#/$defs/EdgeType"}
            }
        },
        "additionalProperties": False
    }

def transform_graphtype(schema):
    """Transform the GraphType definition to use single-level TI system"""
    
    # Get the current GraphType definition
    graph_type = schema["$defs"]["GraphType"]
    
    # Create new simplified GraphType with single-level TI
    new_graph_type = {
        "type": "object",
        "description": "Graph type descriptor with simplified single-level TI system",
        "required": ["propertyGraphDataModel"],
        "properties": {
            # Keep all the existing metadata properties
            "graphPreferredName": graph_type["properties"]["graphPreferredName"],
            "nodePreferredName": graph_type["properties"]["nodePreferredName"], 
            "edgePreferredName": graph_type["properties"]["edgePreferredName"],
            "nodeTypeMinimumLabels": graph_type["properties"]["nodeTypeMinimumLabels"],
            "nodeTypeMaximumLabels": graph_type["properties"]["nodeTypeMaximumLabels"],
            "nodeTypeMinimumPropertyTypes": graph_type["properties"]["nodeTypeMinimumPropertyTypes"],
            "nodeTypeMaximumPropertyTypes": graph_type["properties"]["nodeTypeMaximumPropertyTypes"],
            "edgeTypeMinimumLabels": graph_type["properties"]["edgeTypeMinimumLabels"],
            "edgeTypeMaximumLabels": graph_type["properties"]["edgeTypeMaximumLabels"],
            "edgeTypeMinimumPropertyTypes": graph_type["properties"]["edgeTypeMinimumPropertyTypes"],
            "edgeTypeMaximumPropertyTypes": graph_type["properties"]["edgeTypeMaximumPropertyTypes"],
            "propertyGraphDataModel": graph_type["properties"]["propertyGraphDataModel"],
            "import": graph_type["properties"]["import"],
            
            # 0-level (bare) arrays - implicit exactlyOfConcrete
            "nodeTypes": {
                "$ref": "#/$defs/NodeTypesArray",
                "description": "Bare nodeTypes array (implicit exactlyOfConcrete semantics)"
            },
            "edgeTypes": {
                "$ref": "#/$defs/EdgeTypesArray", 
                "description": "Bare edgeTypes array (implicit exactlyOfConcrete semantics)"
            },
            
            # 1-level primary TI forms
            "exactlyOfConcrete": create_single_level_ti_property(
                "#/$defs/NodeType",
                "Exact type matching, concrete (instantiable) types"
            ),
            "subtypeOfConcrete": create_single_level_ti_property(
                "#/$defs/NodeType", 
                "Subtype matching, concrete (instantiable) types"
            ),
            "subtypeOfAbstract": create_single_level_ti_property(
                "#/$defs/NodeType",
                "Subtype matching, abstract (non-instantiable) types"
            ),
            
            # 1-level synonym forms
            "concrete": create_single_level_ti_property(
                "#/$defs/NodeType",
                "Synonym for exactlyOfConcrete - exact matching, concrete types"
            ),
            "exactlyOf": create_single_level_ti_property(
                "#/$defs/NodeType",
                "Synonym for exactlyOfConcrete - exact matching, concrete types"  
            ),
            "subtypeOf": create_single_level_ti_property(
                "#/$defs/NodeType",
                "Synonym for subtypeOfConcrete - subtype matching, concrete types"
            ),
            "properSubtypeOf": create_single_level_ti_property(
                "#/$defs/NodeType",
                "Synonym for subtypeOfAbstract - subtype matching, abstract types"
            )
        },
        "additionalProperties": False
    }
    
    return new_graph_type

def main():
    """Main transformation function"""
    print("Loading schema...")
    schema = load_schema()
    
    print("Transforming GraphType to single-level TI system...")
    schema["$defs"]["GraphType"] = transform_graphtype(schema)
    
    print("Saving transformed schema...")
    output_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("✅ Schema transformation complete!")
    print("✅ Single-level TI system implemented with three primary forms:")
    print("   - exactlyOfConcrete")
    print("   - subtypeOfConcrete") 
    print("   - subtypeOfAbstract")
    print("✅ Synonyms implemented:")
    print("   - concrete -> exactlyOfConcrete")
    print("   - exactlyOf -> exactlyOfConcrete")
    print("   - subtypeOf -> subtypeOfConcrete")
    print("   - properSubtypeOf -> subtypeOfAbstract")

if __name__ == "__main__":
    main()