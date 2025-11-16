#!/usr/bin/env python3
"""
Validate the Jaguar Conservation LEX-2026.0.3.1 schema
Translated from RDFS/OWL ontology to property graph schema
"""

import json
import yaml
from pathlib import Path
import sys

def load_json_schema(schema_path: Path) -> dict:
    """Load the LEX-2026.0.3.1 JSON Schema"""
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_yaml_schema(yaml_path: Path) -> dict:
    """Load the Jaguar YAML schema"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_schema(yaml_data: dict, json_schema: dict) -> tuple[bool, list]:
    """Validate YAML data against JSON Schema"""
    try:
        from jsonschema import validate, ValidationError
        validate(instance=yaml_data, schema=json_schema)
        return True, []
    except ValidationError as e:
        return False, [str(e)]
    except Exception as e:
        return False, [f"Validation error: {str(e)}"]

def analyze_schema_features(yaml_data: dict) -> dict:
    """Analyze LEX-2026.0.3 features in the schema"""
    features = {
        'node_types': 0,
        'edge_types': 0,
        'with_supertypes': 0,
        'total_properties': 0,
        'hierarchies': []
    }
    
    graph_type = yaml_data.get('graphType', {})
    
    # Count node types
    node_types = graph_type.get('nodeTypes', [])
    features['node_types'] = len(node_types)
    
    # Analyze node types
    type_hierarchy = {}
    for nt in node_types:
        node_type = nt.get('nodeType', {})
        type_label = node_type.get('typeLabel', '')
        # Check for both 'supertypes' and 'extends' (LEX-2026.0.3 uses 'extends')
        supertypes = node_type.get('supertypes', []) or node_type.get('extends', [])
        
        if supertypes:
            features['with_supertypes'] += 1
            for supertype in supertypes:
                if supertype not in type_hierarchy:
                    type_hierarchy[supertype] = []
                type_hierarchy[supertype].append(type_label)
        
        # Count properties
        implies = node_type.get('implies', {})
        prop_types = implies.get('propertyTypes', [])
        features['total_properties'] += len(prop_types)
    
    # Count edge types
    edge_types = graph_type.get('edgeTypes', [])
    features['edge_types'] = len(edge_types)
    
    # Identify major hierarchies
    for base_type, subtypes in type_hierarchy.items():
        if len(subtypes) >= 2:
            features['hierarchies'].append({
                'base': base_type,
                'subtypes': subtypes,
                'count': len(subtypes)
            })
    
    return features

def main():
    print("=" * 60)
    print("LEX-2026.0.3.1 Jaguar Conservation Schema Validation")
    print("=" * 60)
    print()
    
    # Paths
    repo_root = Path(__file__).parent.parent
    json_schema_path = repo_root / "src" / "grasch" / "schemas" / "lex-2026.0.3.1.schema.json"
    yaml_schema_path = repo_root / "graph_RAG" / "jaguar-ontology-as-lex-2026.0.3.1-schema.yaml"
    
    # Check files exist
    if not json_schema_path.exists():
        print(f"❌ JSON Schema not found: {json_schema_path}")
        return 1
    
    if not yaml_schema_path.exists():
        print(f"❌ YAML Schema not found: {yaml_schema_path}")
        return 1
    
    print(f"📖 Loading JSON Schema: {json_schema_path.name}")
    json_schema = load_json_schema(json_schema_path)
    print(f"✅ JSON Schema loaded")
    print()
    
    print(f"📖 Loading Jaguar YAML Schema: {yaml_schema_path.name}")
    yaml_data = load_yaml_schema(yaml_schema_path)
    print(f"✅ YAML Schema loaded")
    print()
    
    # Validate
    print("🔍 Validating schema...")
    is_valid, errors = validate_schema(yaml_data, json_schema)
    
    if is_valid:
        print("✅ Validation successful!")
        print()
        
        # Analyze features
        print("📊 Schema Analysis:")
        print("-" * 60)
        features = analyze_schema_features(yaml_data)
        
        print(f"  Node Types: {features['node_types']}")
        print(f"  Edge Types: {features['edge_types']}")
        print(f"  Types with Supertypes: {features['with_supertypes']}")
        print(f"  Total Properties: {features['total_properties']}")
        print()
        
        if features['hierarchies']:
            print("  Major Type Hierarchies:")
            for hierarchy in sorted(features['hierarchies'], key=lambda x: x['count'], reverse=True):
                print(f"    • {hierarchy['base']} → {hierarchy['count']} subtypes")
                for subtype in hierarchy['subtypes']:
                    print(f"      - {subtype}")
        print()
        
        # Schema metadata
        print("📋 Schema Metadata:")
        print("-" * 60)
        print(f"  Path Name: {yaml_data.get('pathName', 'N/A')}")
        print(f"  Version: {yaml_data.get('version', 'N/A')}")
        print(f"  Description: {yaml_data.get('description', 'N/A')}")
        print()
        
        # LEX-2026.0.3 features
        graph_type = yaml_data.get('graphType', {})
        print("✨ LEX-2026.0.3 Features:")
        print("-" * 60)
        print(f"  Mandatory Labels: ✅ (min {graph_type.get('nodeTypeMinimumLabels', 1)})")
        print(f"  Subtyping Support: ✅ ({features['with_supertypes']} types use inheritance)")
        print(f"  Type Interpretation: {graph_type.get('typeInterpretation', 'exactlyOfThisType')}")
        print()
        
        print("🎉 Schema successfully translated from RDFS/OWL to LEX-2026!")
        return 0
    else:
        print("❌ Validation failed!")
        print()
        print("Errors:")
        for error in errors:
            print(f"  • {error}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
