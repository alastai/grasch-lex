#!/usr/bin/env python3
"""
Validation script for LDBC SNB LEX:2026.0.3 Graph Schema
Validates the SNB schema against the LEX:2026.0.3.1 JSON Schema for LEX specifications
"""

import json
import yaml
import jsonschema
from pathlib import Path
import sys

def load_json_schema(schema_path: str) -> dict:
    """Load and parse JSON Schema file"""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON Schema from {schema_path}: {e}")
        sys.exit(1)

def load_yaml_schema(yaml_path: str) -> dict:
    """Load and parse YAML schema file"""
    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML schema from {yaml_path}: {e}")
        sys.exit(1)

def validate_schema(yaml_data: dict, json_schema: dict) -> tuple[bool, list]:
    """Validate YAML data against JSON Schema"""
    try:
        jsonschema.validate(yaml_data, json_schema)
        return True, []
    except jsonschema.ValidationError as e:
        return False, [str(e)]
    except Exception as e:
        return False, [f"Validation error: {e}"]

def analyze_schema_structure(yaml_data: dict) -> dict:
    """Analyze the structure of the schema for reporting"""
    analysis = {
        'identifier_type': 'unknown',
        'value_type_system': yaml_data.get('valueTypeSystemName', 'CANONICAL (default)'),
        'node_types': 0,
        'edge_types': 0,
        'constraints': 0,
        'node_type_identifiers': {},
        'edge_type_identifiers': {},
        'total_properties': 0,
        'has_supertypes': False,
        'types_with_supertypes': []
    }
    
    # Determine identifier type
    identifier = yaml_data.get('identifier', {})
    if 'locallyQualifiedObjectName' in identifier:
        analysis['identifier_type'] = 'LQON'
        analysis['identifier_value'] = identifier['locallyQualifiedObjectName']
    elif 'globallyQualifiedObjectName' in identifier:
        analysis['identifier_type'] = 'GQON'
        analysis['identifier_value'] = identifier['globallyQualifiedObjectName']
    
    # Analyze graph type
    graph_type = yaml_data.get('graphType', {})
    node_types = graph_type.get('nodeTypes', [])
    edge_types = graph_type.get('edgeTypes', [])
    
    analysis['node_types'] = len(node_types)
    analysis['edge_types'] = len(edge_types)
    
    # Analyze node type identifiers
    for i, node_type in enumerate(node_types):
        node_type_obj = node_type.get('nodeType', {})
        if 'typeLabel' in node_type_obj:
            analysis['node_type_identifiers'][i] = f"typeLabel: {node_type_obj['typeLabel']}"
        elif 'typeIdentifyingLabels' in node_type_obj:
            analysis['node_type_identifiers'][i] = f"typeIdentifyingLabels: {node_type_obj['typeIdentifyingLabels']}"
        elif 'nodeTypeIndex' in node_type_obj:
            analysis['node_type_identifiers'][i] = f"nodeTypeIndex: {node_type_obj['nodeTypeIndex']}"
        
        # Check for supertypes (LEX:2026.0.3 feature)
        implies = node_type_obj.get('implies', {})
        if 'supertypes' in implies and implies['supertypes']:
            analysis['has_supertypes'] = True
            type_name = node_type_obj.get('typeLabel', f"NodeType[{i}]")
            analysis['types_with_supertypes'].append(f"{type_name} extends {implies['supertypes']}")
        
        # Count properties
        analysis['total_properties'] += len(node_type.get('implies', {}).get('propertyTypes', []))
    
    # Analyze edge type identifiers
    for i, edge_type in enumerate(edge_types):
        edge_type_obj = edge_type.get('edgeType', {})
        if 'typeLabel' in edge_type_obj:
            analysis['edge_type_identifiers'][i] = f"typeLabel: {edge_type_obj['typeLabel']}"
        elif 'typeIdentifyingLabels' in edge_type_obj:
            analysis['edge_type_identifiers'][i] = f"typeIdentifyingLabels: {edge_type_obj['typeIdentifyingLabels']}"
        elif 'edgeTypeIndex' in edge_type_obj:
            analysis['edge_type_identifiers'][i] = f"edgeTypeIndex: {edge_type_obj['edgeTypeIndex']}"
        
        # Check for supertypes
        implies = edge_type_obj.get('implies', {})
        if 'supertypes' in implies and implies['supertypes']:
            analysis['has_supertypes'] = True
            type_name = edge_type_obj.get('typeLabel', f"EdgeType[{i}]")
            analysis['types_with_supertypes'].append(f"{type_name} extends {implies['supertypes']}")
        
        # Count properties
        analysis['total_properties'] += len(edge_type.get('implies', {}).get('propertyTypes', []))
    
    # Count constraints
    constraints = yaml_data.get('constraints', {})
    analysis['constraints'] = len(constraints)
    
    return analysis

def main():
    """Main validation function"""
    print("LEX:2026.0.3.1 SNB Schema Validation")
    print("=" * 50)
    
    # File paths (work from both workspace root and tests directory)
    json_schema_path = "src/grasch/schemas/lex-2026.0.3.1.schema.json"
    if not Path(json_schema_path).exists():
        json_schema_path = "../src/grasch/schemas/lex-2026.0.3.1.schema.json"
    
    yaml_schema_path = "src/grasch/examples/snb-lex-2026.0.3.1-schema.yaml"
    if not Path(yaml_schema_path).exists():
        yaml_schema_path = "../src/grasch/examples/snb-lex-2026.0.3.1-schema.yaml"
    
    # Check if files exist
    if not Path(json_schema_path).exists():
        print(f"❌ JSON Schema file not found: {json_schema_path}")
        sys.exit(1)
    
    if not Path(yaml_schema_path).exists():
        print(f"❌ YAML Schema file not found: {yaml_schema_path}")
        sys.exit(1)
    
    # Load schemas
    print(f"📖 Loading JSON Schema: {json_schema_path}")
    json_schema = load_json_schema(json_schema_path)
    
    print(f"📖 Loading YAML Schema: {yaml_schema_path}")
    yaml_data = load_yaml_schema(yaml_schema_path)
    
    # Validate
    print("\n🔍 Validating schema...")
    is_valid, errors = validate_schema(yaml_data, json_schema)
    
    if is_valid:
        print("✅ Schema validation PASSED")
    else:
        print("❌ Schema validation FAILED")
        print("\nValidation errors:")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)
    
    # Analyze structure
    print("\n📊 Schema Analysis:")
    analysis = analyze_schema_structure(yaml_data)
    
    print(f"  Identifier Type: {analysis['identifier_type']}")
    print(f"  Identifier Value: {analysis.get('identifier_value', 'N/A')}")
    print(f"  Value Type System: {analysis['value_type_system']}")
    print(f"  Node Types: {analysis['node_types']}")
    print(f"  Edge Types: {analysis['edge_types']}")
    print(f"  Total Properties: {analysis['total_properties']}")
    print(f"  Constraints: {analysis['constraints']}")
    
    # LEX:2026.0.3 features
    if analysis['has_supertypes']:
        print(f"\n🔗 Subtyping (LEX:2026.0.3):")
        for subtype_info in analysis['types_with_supertypes']:
            print(f"    • {subtype_info}")
    
    print("\n🏷️  Node Type Identifiers:")
    for i, identifier in analysis['node_type_identifiers'].items():
        print(f"    [{i}] {identifier}")
    
    print("\n🔗 Edge Type Identifiers:")
    for i, identifier in analysis['edge_type_identifiers'].items():
        print(f"    [{i}] {identifier}")
    
    print(f"\n🎉 SNB LEX:2026.0.3.1 schema validation completed successfully!")
    print(f"   Schema defines {analysis['node_types']} node types and {analysis['edge_types']} edge types")
    print(f"   with {analysis['total_properties']} total properties and {analysis['constraints']} constraints")
    print(f"   ✨ LEX:2026.0.3 - All types have mandatory labels (minimum 1)")

if __name__ == "__main__":
    main()
