#!/usr/bin/env python3
"""
Fix type interpretation wrappers in the schema.

The subtypesOf pattern currently requires 'abstract' but should support:
1. subtypesOf: { nodeTypes/edgeTypes: [...] } (concrete by default)
2. subtypesOf: { abstract: { nodeTypes/edgeTypes: [...] } }
3. subtypesOf: { concrete: { nodeTypes/edgeTypes: [...] } }
"""
import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path, 'r') as f:
    content = f.read()

# The current pattern that needs to be replaced (for nodeTypes)
old_nodetype_pattern = '''                  {
                    "type": "object",
                    "description": "Subtypes declaration",
                    "required": [
                      "subtypesOf"
                    ],
                    "properties": {
                      "subtypesOf": {
                        "type": "object",
                        "required": [
                          "abstract"
                        ],
                        "properties": {
                          "abstract": {
                            "type": "object",
                            "required": [
                              "nodeTypes"
                            ],
                            "properties": {
                              "nodeTypes": {
                                "type": "array",
                                "items": {
                                  "oneOf": [
                                    {
                                      "$ref": "#/$defs/NodeType"
                                    },
                                    {
                                      "type": "object",
                                      "required": [
                                        "abstract"
                                      ],
                                      "properties": {
                                        "abstract": {
                                          "$ref": "#/$defs/NodeType"
                                        }
                                      }
                                    }
                                  ]
                                }
                              }
                            }
                          }
                        }
                      }
                    },
                    "additionalProperties": false
                  }'''

# New pattern that supports all three forms
new_nodetype_pattern = '''                  {
                    "type": "object",
                    "description": "Subtypes declaration",
                    "required": [
                      "subtypesOf"
                    ],
                    "properties": {
                      "subtypesOf": {
                        "oneOf": [
                          {
                            "type": "object",
                            "description": "Direct nodeTypes (concrete by default)",
                            "required": [
                              "nodeTypes"
                            ],
                            "properties": {
                              "nodeTypes": {
                                "type": "array",
                                "items": {
                                  "oneOf": [
                                    {
                                      "$ref": "#/$defs/NodeType"
                                    },
                                    {
                                      "type": "object",
                                      "required": [
                                        "abstract"
                                      ],
                                      "properties": {
                                        "abstract": {
                                          "$ref": "#/$defs/NodeType"
                                        }
                                      },
                                      "additionalProperties": false
                                    }
                                  ]
                                }
                              }
                            },
                            "additionalProperties": false
                          },
                          {
                            "type": "object",
                            "description": "Abstract nodeTypes",
                            "required": [
                              "abstract"
                            ],
                            "properties": {
                              "abstract": {
                                "type": "object",
                                "required": [
                                  "nodeTypes"
                                ],
                                "properties": {
                                  "nodeTypes": {
                                    "type": "array",
                                    "items": {
                                      "oneOf": [
                                        {
                                          "$ref": "#/$defs/NodeType"
                                        },
                                        {
                                          "type": "object",
                                          "required": [
                                            "abstract"
                                          ],
                                          "properties": {
                                            "abstract": {
                                              "$ref": "#/$defs/NodeType"
                                            }
                                          },
                                          "additionalProperties": false
                                        }
                                      ]
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            },
                            "additionalProperties": false
                          },
                          {
                            "type": "object",
                            "description": "Concrete nodeTypes (explicit)",
                            "required": [
                              "concrete"
                            ],
                            "properties": {
                              "concrete": {
                                "type": "object",
                                "required": [
                                  "nodeTypes"
                                ],
                                "properties": {
                                  "nodeTypes": {
                                    "type": "array",
                                    "items": {
                                      "oneOf": [
                                        {
                                          "$ref": "#/$defs/NodeType"
                                        },
                                        {
                                          "type": "object",
                                          "required": [
                                            "abstract"
                                          ],
                                          "properties": {
                                            "abstract": {
                                              "$ref": "#/$defs/NodeType"
                                            }
                                          },
                                          "additionalProperties": false
                                        }
                                      ]
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            },
                            "additionalProperties": false
                          }
                        ]
                      }
                    },
                    "additionalProperties": false
                  }'''

# Check if the old pattern exists
if old_nodetype_pattern in content:
    print("✓ Found nodeTypes subtypesOf pattern to fix")
    content = content.replace(old_nodetype_pattern, new_nodetype_pattern)
    print("✓ Replaced nodeTypes subtypesOf pattern")
else:
    print("✗ Could not find exact nodeTypes subtypesOf pattern")
    print("  Searching for similar pattern...")

# Now do the same for edgeTypes
old_edgetype_pattern = old_nodetype_pattern.replace('nodeTypes', 'edgeTypes').replace('NodeType', 'EdgeType')
new_edgetype_pattern = new_nodetype_pattern.replace('nodeTypes', 'edgeTypes').replace('NodeType', 'EdgeType')

if old_edgetype_pattern in content:
    print("✓ Found edgeTypes subtypesOf pattern to fix")
    content = content.replace(old_edgetype_pattern, new_edgetype_pattern)
    print("✓ Replaced edgeTypes subtypesOf pattern")
else:
    print("✗ Could not find exact edgeTypes subtypesOf pattern")

# Save the updated schema
with open(schema_path, 'w') as f:
    f.write(content)

print("\n" + "=" * 70)
print("Schema update complete!")
print("=" * 70)
