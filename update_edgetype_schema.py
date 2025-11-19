#!/usr/bin/env python3
"""
Update EdgeType schema to support new LEX-2026 directed/undirected syntax
"""
import json
from pathlib import Path

# Load current schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Define EndpointReference schema (supports all endpoint formats)
endpoint_reference = {
    "oneOf": [
        {
            "type": "string",
            "description": "Type label, or SAME/SELF for self-loops"
        },
        {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "description": "Type identifier (array of labels)"
        },
        {
            "type": "integer",
            "minimum": 0,
            "description": "Type index"
        },
        {
            "type": "object",
            "required": ["typeLabels"],
            "properties": {
                "typeLabels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1
                }
            },
            "additionalProperties": False
        },
        {
            "type": "object",
            "required": ["typeLabel"],
            "properties": {
                "typeLabel": {"type": "string"}
            },
            "additionalProperties": False
        },
        {
            "type": "object",
            "required": ["typeIdentifier"],
            "properties": {
                "typeIdentifier": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1
                }
            },
            "additionalProperties": False
        },
        {
            "type": "object",
            "required": ["index"],
            "properties": {
                "index": {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "additionalProperties": False
        },
        {
            "type": "object",
            "required": ["nodeType"],
            "properties": {
                "nodeType": {"$ref": "#/$defs/NodeType"}
            },
            "description": "Inline node type definition"
        },
        {
            "type": "object",
            "required": ["abstract"],
            "properties": {
                "abstract": {"type": "string"}
            },
            "additionalProperties": False,
            "description": "Abstract type reference"
        },
        {
            "type": "object",
            "required": ["abstractSupertype"],
            "properties": {
                "abstractSupertype": {"type": "string"}
            },
            "additionalProperties": False,
            "description": "Abstract supertype reference"
        }
    ]
}

# Add EndpointReference to $defs
schema['$defs']['EndpointReference'] = endpoint_reference

print("✓ Added EndpointReference definition")

# Define DirectedEdgeDescriptor (new syntax)
directed_edge = {
    "type": "object",
    "required": ["directed"],
    "properties": {
        "directed": {
            "type": "object",
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
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}}
            ]
        },
        "adding": {"$ref": "#/$defs/AddingDescriptor"}
    }
}

# Define UndirectedEdgeDescriptor (new syntax)
undirected_edge = {
    "type": "object",
    "required": ["undirected"],
    "properties": {
        "undirected": {
            "type": "object",
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
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}}
            ]
        },
        "adding": {"$ref": "#/$defs/AddingDescriptor"}
    }
}

# Add new patterns to EdgeType.edgeType oneOf
edge_type_def = schema['$defs']['EdgeType']
edge_type_inner = edge_type_def['properties']['edgeType']

# Add directed and undirected patterns to the beginning of oneOf
edge_type_inner['oneOf'].insert(0, directed_edge)
edge_type_inner['oneOf'].insert(1, undirected_edge)

print("✓ Added directed and undirected edge patterns to EdgeType")

# Save updated schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print(f"✓ Updated schema saved to {schema_path}")
print("\nNew patterns added:")
print("  - EndpointReference (supports all endpoint formats)")
print("  - DirectedEdgeDescriptor (directed: {from, via, to})")
print("  - UndirectedEdgeDescriptor (undirected: {between, via, and})")
