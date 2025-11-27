#!/usr/bin/env python3
"""
Add context-specific type interpretation definitions to the schema.

Instead of generic TIWrapperContentNode/Edge, create:
- graphTypeInterpretation: for GraphType-level TI wrappers
- nodeTypesInterpretation: for nodeTypes property TI wrappers  
- edgeTypesInterpretation: for edgeTypes property TI wrappers
- partitionBlockNodeInterpretation: for partition blocks in nodeTypes arrays
- partitionBlockEdgeInterpretation: for partition blocks in edgeTypes arrays

Each knows its context and what content types it expects.
"""

import json
from pathlib import Path

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

def create_context_specific_definitions():
    """Create context-specific TI wrapper definitions."""
    
    # GraphType-level interpretation (wraps entire graphType content)
    graphTypeInterpretation = {
        "description": "Type interpretation wrapper for GraphType-level content (nodeTypes, edgeTypes, etc.)",
        "type": "object",
        "patternProperties": {
            "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
                "oneOf": [
                    {
                        "description": "Two-level TI wrapper (interpretation + concreteness)",
                        "type": "object",
                        "patternProperties": {
                            "^(abstract|concrete|final|sealed|extensible)$": {
                                "type": "object",
                                "description": "GraphType content with nodeTypes and/or edgeTypes",
                                "properties": {
                                    "nodeTypes": {"$ref": "#/$defs/NodeTypesArray"},
                                    "edgeTypes": {"$ref": "#/$defs/EdgeTypesArray"}
                                },
                                "additionalProperties": False,
                                "minProperties": 1
                            }
                        },
                        "additionalProperties": False,
                        "minProperties": 1,
                        "maxProperties": 1
                    },
                    {
                        "description": "Phase 1 Import: Import entire TI wrapper with its content",
                        "type": "object",
                        "required": ["import"],
                        "properties": {
                            "import": {
                                "type": "string",
                                "description": "Path to file containing TI wrapper + content"
                            }
                        },
                        "additionalProperties": False
                    }
                ]
            }
        },
        "additionalProperties": False,
        "minProperties": 1,
        "maxProperties": 1
    }
    
    # NodeTypes property-level interpretation
    nodeTypesInterpretation = {
        "description": "Type interpretation wrapper for nodeTypes property content",
        "type": "object",
        "patternProperties": {
            "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
                "oneOf": [
                    {
                        "description": "Two-level TI wrapper (interpretation + concreteness)",
                        "type": "object",
                        "patternProperties": {
                            "^(abstract|concrete|final|sealed|extensible)$": {
                                "oneOf": [
                                    {
                                        "description": "Inline node type array",
                                        "$ref": "#/$defs/NodeTypesArray"
                                    },
                                    {
                                        "description": "Phase 2 Import: Import type definitions only (TI stripped)",
                                        "type": "object",
                                        "required": ["import"],
                                        "properties": {
                                            "import": {
                                                "type": "string",
                                                "description": "Path to file containing node type definitions"
                                            }
                                        },
                                        "additionalProperties": False
                                    }
                                ]
                            }
                        },
                        "additionalProperties": False,
                        "minProperties": 1,
                        "maxProperties": 1
                    },
                    {
                        "description": "Phase 1 Import: Import entire TI wrapper with its types",
                        "type": "object",
                        "required": ["import"],
                        "properties": {
                            "import": {
                                "type": "string",
                                "description": "Path to file containing TI wrapper + node types"
                            }
                        },
                        "additionalProperties": False
                    }
                ]
            }
        },
        "additionalProperties": False,
        "minProperties": 1,
        "maxProperties": 1
    }
    
    # EdgeTypes property-level interpretation
    edgeTypesInterpretation = {
        "description": "Type interpretation wrapper for edgeTypes property content",
        "type": "object",
        "patternProperties": {
            "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
                "oneOf": [
                    {
                        "description": "Two-level TI wrapper (interpretation + concreteness)",
                        "type": "object",
                        "patternProperties": {
                            "^(abstract|concrete|final|sealed|extensible)$": {
                                "oneOf": [
                                    {
                                        "description": "Inline edge type array",
                                        "$ref": "#/$defs/EdgeTypesArray"
                                    },
                                    {
                                        "description": "Phase 2 Import: Import type definitions only (TI stripped)",
                                        "type": "object",
                                        "required": ["import"],
                                        "properties": {
                                            "import": {
                                                "type": "string",
                                                "description": "Path to file containing edge type definitions"
                                            }
                                        },
                                        "additionalProperties": False
                                    }
                                ]
                            }
                        },
                        "additionalProperties": False,
                        "minProperties": 1,
                        "maxProperties": 1
                    },
                    {
                        "description": "Phase 1 Import: Import entire TI wrapper with its types",
                        "type": "object",
                        "required": ["import"],
                        "properties": {
                            "import": {
                                "type": "string",
                                "description": "Path to file containing TI wrapper + edge types"
                            }
                        },
                        "additionalProperties": False
                    }
                ]
            }
        },
        "additionalProperties": False,
        "minProperties": 1,
        "maxProperties": 1
    }
    
    # Partition block for nodeTypes array items
    partitionBlockNodeInterpretation = {
        "description": "Type interpretation wrapper for partition blocks in nodeTypes arrays",
        "type": "object",
        "patternProperties": {
            "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
                "oneOf": [
                    {
                        "description": "Two-level TI wrapper (interpretation + concreteness)",
                        "type": "object",
                        "patternProperties": {
                            "^(abstract|concrete|final|sealed|extensible)$": {
                                "oneOf": [
                                    {
                                        "description": "Singleton set (single node type)",
                                        "$ref": "#/$defs/NodeType"
                                    },
                                    {
                                        "description": "Multi-element set (array of node types)",
                                        "type": "array",
                                        "items": {"$ref": "#/$defs/NodeType"},
                                        "minItems": 1
                                    },
                                    {
                                        "description": "Phase 2 Import: Import type definitions only (TI stripped)",
                                        "type": "object",
                                        "required": ["import"],
                                        "properties": {
                                            "import": {
                                                "type": "string",
                                                "description": "Path to file containing node type definitions"
                                            }
                                        },
                                        "additionalProperties": False
                                    }
                                ]
                            }
                        },
                        "additionalProperties": False,
                        "minProperties": 1,
                        "maxProperties": 1
                    },
                    {
                        "description": "Phase 1 Import: Import entire TI wrapper with its types",
                        "type": "object",
                        "required": ["import"],
                        "properties": {
                            "import": {
                                "type": "string",
                                "description": "Path to file containing TI wrapper + node types"
                            }
                        },
                        "additionalProperties": False
                    }
                ]
            }
        },
        "additionalProperties": False,
        "minProperties": 1,
        "maxProperties": 1
    }
    
    # Partition block for edgeTypes array items
    partitionBlockEdgeInterpretation = {
        "description": "Type interpretation wrapper for partition blocks in edgeTypes arrays",
        "type": "object",
        "patternProperties": {
            "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
                "oneOf": [
                    {
                        "description": "Two-level TI wrapper (interpretation + concreteness)",
                        "type": "object",
                        "patternProperties": {
                            "^(abstract|concrete|final|sealed|extensible)$": {
                                "oneOf": [
                                    {
                                        "description": "Singleton set (single edge type)",
                                        "$ref": "#/$defs/EdgeType"
                                    },
                                    {
                                        "description": "Multi-element set (array of edge types)",
                                        "type": "array",
                                        "items": {"$ref": "#/$defs/EdgeType"},
                                        "minItems": 1
                                    },
                                    {
                                        "description": "Phase 2 Import: Import type definitions only (TI stripped)",
                                        "type": "object",
                                        "required": ["import"],
                                        "properties": {
                                            "import": {
                                                "type": "string",
                                                "description": "Path to file containing edge type definitions"
                                            }
                                        },
                                        "additionalProperties": False
                                    }
                                ]
                            }
                        },
                        "additionalProperties": False,
                        "minProperties": 1,
                        "maxProperties": 1
                    },
                    {
                        "description": "Phase 1 Import: Import entire TI wrapper with its types",
                        "type": "object",
                        "required": ["import"],
                        "properties": {
                            "import": {
                                "type": "string",
                                "description": "Path to file containing TI wrapper + edge types"
                            }
                        },
                        "additionalProperties": False
                    }
                ]
            }
        },
        "additionalProperties": False,
        "minProperties": 1,
        "maxProperties": 1
    }
    
    return {
        "graphTypeInterpretation": graphTypeInterpretation,
        "nodeTypesInterpretation": nodeTypesInterpretation,
        "edgeTypesInterpretation": edgeTypesInterpretation,
        "partitionBlockNodeInterpretation": partitionBlockNodeInterpretation,
        "partitionBlockEdgeInterpretation": partitionBlockEdgeInterpretation
    }


def main():
    """Add context-specific TI definitions to schema."""
    
    print("Loading schema...")
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)
    
    print("Creating context-specific TI definitions...")
    new_defs = create_context_specific_definitions()
    
    # Add new definitions to $defs
    for name, definition in new_defs.items():
        schema["$defs"][name] = definition
        print(f"  Added: {name}")
    
    print(f"\nWriting updated schema...")
    with open(SCHEMA_PATH, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("✓ Context-specific TI definitions added successfully!")
    print("\nNew definitions:")
    for name in new_defs.keys():
        print(f"  - {name}")


if __name__ == "__main__":
    main()
