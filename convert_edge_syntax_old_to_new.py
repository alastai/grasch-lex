#!/usr/bin/env python3
"""
Convert all edge types from old syntax to new LEX-2026 syntax
"""
import yaml
import re
from pathlib import Path

def convert_endpoint(endpoint_data):
    """Convert endpoint from old format to new format"""
    if isinstance(endpoint_data, dict):
        # Keep as-is (typeLabel, typeIdentifier, index, nodeType, etc.)
        return endpoint_data
    elif isinstance(endpoint_data, str):
        # String like "SAME" or type label
        return endpoint_data
    elif isinstance(endpoint_data, int):
        # Index
        return endpoint_data
    return endpoint_data

def convert_edge_type(edge_data):
    """Convert edge type from old syntax to new syntax"""
    if 'edgeType' not in edge_data:
        return edge_data
    
    edge = edge_data['edgeType']
    
    # Check if already using new syntax
    if 'directed' in edge or 'undirected' in edge:
        return edge_data  # Already new syntax
    
    # Check if using old syntax
    if 'direction' not in edge:
        return edge_data  # Not an edge type we recognize
    
    direction = edge.get('direction')
    type_label = edge.get('typeLabel')
    implies = edge.get('implies')
    extends = edge.get('extends')
    adding = edge.get('adding')
    first_endpoint = edge.get('firstEndpointNodeType')
    second_endpoint = edge.get('secondEndpointNodeType')
    
    # Build new syntax
    new_edge = {'edgeType': {}}
    
    if direction == 'DIRECTED':
        new_edge['edgeType']['directed'] = {
            'from': convert_endpoint(first_endpoint),
            'to': convert_endpoint(second_endpoint)
        }
        if type_label:
            new_edge['edgeType']['directed']['via'] = type_label
    elif direction == 'UNDIRECTED':
        new_edge['edgeType']['undirected'] = {
            'between': convert_endpoint(first_endpoint),
            'and': convert_endpoint(second_endpoint)
        }
        if type_label:
            new_edge['edgeType']['undirected']['via'] = type_label
    
    # Add implies, extends, adding at edgeType level
    if implies:
        new_edge['edgeType']['implies'] = implies
    if extends:
        new_edge['edgeType']['extends'] = extends
    if adding:
        new_edge['edgeType']['adding'] = adding
    
    return new_edge

def convert_file(file_path):
    """Convert a YAML file from old to new syntax"""
    print(f"\nProcessing: {file_path.name}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if file uses old syntax
    if 'direction: DIRECTED' not in content and 'direction: UNDIRECTED' not in content:
        print("  ⊘ No old syntax found")
        return False
    
    # Load YAML
    data = yaml.safe_load(content)
    
    # Find and convert edge types
    changes = 0
    
    def convert_recursive(obj):
        nonlocal changes
        if isinstance(obj, dict):
            # Check if this is an edge type
            if 'edgeType' in obj and isinstance(obj['edgeType'], dict):
                if 'direction' in obj['edgeType']:
                    new_obj = convert_edge_type(obj)
                    changes += 1
                    return new_obj
            # Recurse into dict values
            return {k: convert_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_recursive(item) for item in obj]
        return obj
    
    converted_data = convert_recursive(data)
    
    if changes > 0:
        # Save converted YAML
        with open(file_path, 'w') as f:
            yaml.dump(converted_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"  ✓ Converted {changes} edge type(s)")
        return True
    else:
        print("  ⊘ No conversions needed")
        return False

def main():
    print("=" * 70)
    print("Converting Edge Types: Old Syntax → New LEX-2026 Syntax")
    print("=" * 70)
    
    # Find all example YAML files
    examples_dir = Path("src/grasch/examples")
    yaml_files = list(examples_dir.glob("lex-2026.0.3.2-*.yaml"))
    
    converted_count = 0
    for yaml_file in sorted(yaml_files):
        if convert_file(yaml_file):
            converted_count += 1
    
    print("\n" + "=" * 70)
    print(f"Summary: {converted_count} file(s) converted")
    print("=" * 70)

if __name__ == '__main__':
    main()
