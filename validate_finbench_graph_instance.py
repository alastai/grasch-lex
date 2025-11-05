#!/usr/bin/env python3
"""
Validation script for LDBC FinBench SF1 Graph Instance LEX:2026.0.2
Validates the FinBench graph instance against the LEX:2026.0.2 JSON Schema for LEX specifications
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

def analyze_graph_instance_structure(yaml_data: dict) -> dict:
    """Analyze the structure of the graph instance for reporting"""
    analysis = {
        'identifier_type': 'unknown',
        'identifier_value': 'unknown',
        'value_type_system': yaml_data.get('valueTypeSystemName', 'CANONICAL (default)'),
        'has_graph_schema_ref': False,
        'graph_schema_ref': None,
        'constraints': 0,
        'has_storage_schema': False,
        'storage_type': None,
        'principal': yaml_data.get('principal', None)
    }
    
    # Determine identifier type
    identifier = yaml_data.get('identifier', {})
    if 'locallyQualifiedObjectName' in identifier:
        analysis['identifier_type'] = 'LQON'
        analysis['identifier_value'] = identifier['locallyQualifiedObjectName']
    elif 'globallyQualifiedObjectName' in identifier:
        analysis['identifier_type'] = 'GQON'
        analysis['identifier_value'] = identifier['globallyQualifiedObjectName']
    
    # Check for graph schema reference
    graph_schema = yaml_data.get('graphSchema', {})
    if graph_schema:
        analysis['has_graph_schema_ref'] = True
        if 'locallyQualifiedObjectName' in graph_schema:
            analysis['graph_schema_ref'] = f"LQON: {graph_schema['locallyQualifiedObjectName']}"
        elif 'globallyQualifiedObjectName' in graph_schema:
            analysis['graph_schema_ref'] = f"GQON: {graph_schema['globallyQualifiedObjectName']}"
    
    # Count constraints
    constraints = yaml_data.get('constraints', {})
    analysis['constraints'] = len(constraints)
    
    # Check for storage schema
    storage_schema = yaml_data.get('storageSchema', {})
    if storage_schema:
        analysis['has_storage_schema'] = True
        analysis['storage_type'] = storage_schema.get('storageType', 'unknown')
    
    return analysis

def main():
    """Main validation function"""
    print("LEX:2026.0.2 FinBench SF1 Graph Instance Validation")
    print("=" * 60)
    
    # File paths
    json_schema_path = "lex-2026.0.2.schema.json"
    yaml_schema_path = "finbench-sf1-graph-lex-2026.0.2.yaml"
    
    # Check if files exist
    if not Path(json_schema_path).exists():
        print(f"❌ JSON Schema file not found: {json_schema_path}")
        sys.exit(1)
    
    if not Path(yaml_schema_path).exists():
        print(f"❌ YAML Graph Instance file not found: {yaml_schema_path}")
        sys.exit(1)
    
    # Load schemas
    print(f"📖 Loading JSON Schema: {json_schema_path}")
    json_schema = load_json_schema(json_schema_path)
    
    print(f"📖 Loading YAML Graph Instance: {yaml_schema_path}")
    yaml_data = load_yaml_schema(yaml_schema_path)
    
    # Validate
    print("\n🔍 Validating graph instance...")
    is_valid, errors = validate_schema(yaml_data, json_schema)
    
    if is_valid:
        print("✅ Graph instance validation PASSED")
    else:
        print("❌ Graph instance validation FAILED")
        print("\nValidation errors:")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)
    
    # Analyze structure
    print("\n📊 Graph Instance Analysis:")
    analysis = analyze_graph_instance_structure(yaml_data)
    
    print(f"  Specification Type: Graph Instance")
    print(f"  Identifier Type: {analysis['identifier_type']}")
    print(f"  Identifier Value: {analysis['identifier_value']}")
    print(f"  Value Type System: {analysis['value_type_system']}")
    
    print(f"\n🔗 Schema Reference:")
    if analysis['has_graph_schema_ref']:
        print(f"  Graph Schema Reference: {analysis['graph_schema_ref']}")
    else:
        print("  Graph Schema Reference: None")
    
    print(f"\n👤 Principal:")
    if analysis['principal']:
        print(f"  Owner: {analysis['principal']}")
    else:
        print("  Owner: None")
    
    print(f"\n🔒 Constraints:")
    print(f"  Constraint Count: {analysis['constraints']}")
    
    print(f"\n💾 Storage Schema:")
    if analysis['has_storage_schema']:
        print(f"  Has Storage Schema: Yes")
        print(f"  Storage Type: {analysis['storage_type']}")
    else:
        print("  Has Storage Schema: No")
    
    print(f"\n🎉 FinBench SF1 graph instance LEX:2026.0.2 validation completed successfully!")
    print(f"   Graph instance '{analysis['identifier_value']}' references schema '{analysis['graph_schema_ref']}'")
    print(f"   with {analysis['constraints']} instance-specific constraints")
    if analysis['has_storage_schema']:
        print(f"   Storage schema type: {analysis['storage_type']}")
    else:
        print("   No storage schema specified")

if __name__ == "__main__":
    main()