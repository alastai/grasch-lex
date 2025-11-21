#!/usr/bin/env python3
"""
Replace EdgeType schema to support ONLY new LEX-2026 syntax
Remove all old syntax patterns
"""
import json
from pathlib import Path

# Load current schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

print("Replacing EdgeType definition with new syntax only...")

# Define the new EdgeType that ONLY supports new syntax
new_edge_type = {
    "type": "object",
    "description": "Edge type descriptor using LEX-2026 directed/undirected syntax",
    "properties": {
        "edgeType": {
            "type": "object",
            "description": "Edge type with directed or undirected specification",
            "oneOf": [
                {"$ref": "#/$defs/DirectedEdgeDescriptor"},
                {"$ref": "#/$defs/UndirectedEdgeDescriptor"}
            ]
        }
    },
    "required": ["edgeType"],
    "additionalProperties": False
}

# Define DirectedEdgeDescriptor
directed_edge_descriptor = {
    "type": "object",
    "description": "Directed edge type with from/to endpoints",
    "required": ["directed"],
    "properties": {
        "directed": {
            "type": "object",
            "description": "Directed edge specification with endpoint names",
            "properties": {
                "from": {"$ref": "#/$defs/EndpointReference"},
                "to": {"$ref": "#/$defs/EndpointReference"},
                "tail": {"$ref": "#/$defs/EndpointReference"},
                "head": {"$ref": "#/$defs/EndpointReference"},
                "src": {"$ref": "#/$defs/EndpointReference"},
                "dst": {"$ref": "#/$defs/EndpointReference"},
                "dest": {"$ref": "#/$defs/EndpointReference"},
                "via": {"type": "string", "description": "Edge label"},
                "arc": {"type": "string", "description": "Edge label (synonym for via)"}
            },
            "oneOf": [
                {"required": ["from", "to"]},
                {"required": ["tail", "head"]},
                {"required": ["src", "dst"]},
                {"required": ["src", "dest"]}
            ]
        },
        "implies": {"$ref": "#/$defs/ImpliesDescriptor"},
        "extends": {
            "oneOf": [
                {"type": "string", "description": "Single supertype"},
                {"type": "array", "items": {"type": "string"}, "description": "Multiple supertypes"}
            ]
        },
        "adding": {"$ref": "#/$defs/AddingDescriptor"}
    },
    "additionalProperties": False
}

# Define UndirectedEdgeDescriptor
undirected_edge_descriptor = {
    "type": "object",
    "description": "Undirected edge type with between/and endpoints",
    "required": ["undirected"],
    "properties": {
        "undirected": {
            "type": "object",
            "description": "Undirected edge specification",
            "required": ["between", "and"],
            "properties": {
                "between": {"$ref": "#/$defs/EndpointReference"},
                "and": {"$ref": "#/$defs/EndpointReference"},
                "via": {"type": "string", "description": "Edge label"},
                "arc": {"type": "string", "description": "Edge label (synonym for via)"}
            }
        },
        "implies": {"$ref": "#/$defs/ImpliesDescriptor"},
        "extends": {
            "oneOf": [
                {"type": "string", "description": "Single supertype"},
                {"type": "array", "items": {"type": "string"}, "description": "Multiple supertypes"}
            ]
        },
        "adding": {"$ref": "#/$defs/AddingDescriptor"}
    },
    "additionalProperties": False
}

# Replace EdgeType in schema
schema['$defs']['EdgeType'] = new_edge_type
schema['$defs']['DirectedEdgeDescriptor'] = directed_edge_descriptor
schema['$defs']['UndirectedEdgeDescriptor'] = undirected_edge_descriptor

print("✓ Replaced EdgeType with new syntax only")
print("✓ Added DirectedEdgeDescriptor")
print("✓ Added UndirectedEdgeDescriptor")

# Save updated schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print(f"✓ Schema saved to {schema_path}")
print("\nOld syntax REMOVED:")
print("  ✗ direction: DIRECTED/UNDIRECTED")
print("  ✗ firstEndpointNodeType")
print("  ✗ secondEndpointNodeType")
print("\nNew syntax ONLY:")
print("  ✓ directed: {from, via, to}")
print("  ✓ undirected: {between, via, and}")
print("  ✓ All endpoint name synonyms supported")
