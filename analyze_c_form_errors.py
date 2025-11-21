#!/usr/bin/env python3
"""
Analyze C form validation errors to identify root causes.

This script examines one failing C form in detail to understand
what the schema expects vs what the canonicalizer produces.
"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator

# Load schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Load a simple failing C form
c_file = Path("src/grasch/examples/CANON_lex-2026.0.3.2-minimal-import-example.yaml")
with open(c_file, 'r') as f:
    c_data = yaml.safe_load(f)

print("="*80)
print("ANALYZING C FORM VALIDATION FAILURE")
print("="*80)
print(f"\nFile: {c_file.name}\n")

# Get validation errors
errors = list(validator.iter_errors(c_data))

print(f"Total errors: {len(errors)}\n")

for i, error in enumerate(errors, 1):
    print(f"Error {i}:")
    print(f"  Path: {'.'.join(str(p) for p in error.absolute_path)}")
    print(f"  Message: {error.message}")
    print(f"  Validator: {error.validator}")
    print(f"  Schema path: {'.'.join(str(p) for p in error.schema_path)}")
    
    # Show the failing value
    if error.instance:
        print(f"  Failing value type: {type(error.instance).__name__}")
        if isinstance(error.instance, dict):
            print(f"  Failing value keys: {list(error.instance.keys())[:5]}")
        elif isinstance(error.instance, list):
            print(f"  Failing value length: {len(error.instance)}")
            if error.instance:
                print(f"  First item type: {type(error.instance[0]).__name__}")
                if isinstance(error.instance[0], dict):
                    print(f"  First item keys: {list(error.instance[0].keys())}")
    print()

# Examine the nodeTypes structure
print("="*80)
print("EXAMINING NODETYPES STRUCTURE")
print("="*80)

if 'graphSchema' in c_data and 'graphType' in c_data['graphSchema']:
    graph_type = c_data['graphSchema']['graphType']
    if 'nodeTypes' in graph_type:
        node_types = graph_type['nodeTypes']
        print(f"\nnodeTypes is a: {type(node_types).__name__}")
        print(f"nodeTypes length: {len(node_types)}")
        
        for i, item in enumerate(node_types[:3], 1):
            print(f"\nItem {i}:")
            print(f"  Type: {type(item).__name__}")
            if isinstance(item, dict):
                print(f"  Keys: {list(item.keys())}")
                
                # Check for wrapper patterns
                if 'subtypesOf' in item:
                    print(f"  Has subtypesOf wrapper")
                    subtypes_of = item['subtypesOf']
                    print(f"    subtypesOf type: {type(subtypes_of).__name__}")
                    if isinstance(subtypes_of, dict):
                        print(f"    subtypesOf keys: {list(subtypes_of.keys())}")
                        if 'abstract' in subtypes_of:
                            print(f"    Has abstract wrapper")
                            abstract = subtypes_of['abstract']
                            print(f"      abstract type: {type(abstract).__name__}")
                            if isinstance(abstract, dict):
                                print(f"      abstract keys: {list(abstract.keys())}")
                
                if 'nodeType' in item:
                    print(f"  Has nodeType")
                    node_type = item['nodeType']
                    if isinstance(node_type, dict) and 'typeLabel' in node_type:
                        print(f"    typeLabel: {node_type['typeLabel']}")

# Check what schema expects for nodeTypes
print("\n" + "="*80)
print("SCHEMA EXPECTATIONS FOR NODETYPES")
print("="*80)

# Navigate to nodeTypes definition in schema
if 'definitions' in schema:
    if 'GraphType' in schema['definitions']:
        graph_type_def = schema['definitions']['GraphType']
        if 'properties' in graph_type_def and 'nodeTypes' in graph_type_def['properties']:
            node_types_def = graph_type_def['properties']['nodeTypes']
            print("\nnodeTypes schema definition:")
            print(json.dumps(node_types_def, indent=2)[:500])
            
            if 'items' in node_types_def:
                items_def = node_types_def['items']
                print("\n\nnodeTypes items schema:")
                print(json.dumps(items_def, indent=2)[:500])

print("\n" + "="*80)
print("RECOMMENDATION")
print("="*80)
print("""
The issue appears to be that the canonicalizer is producing wrapper structures
that don't match what the schema expects for the nodeTypes array items.

Next steps:
1. Check if schema has definitions for SubtypesOfWrapper, SealedWrapper, etc.
2. Verify canonicalizer produces structures matching those definitions
3. Update either schema or canonicalizer to align
""")
