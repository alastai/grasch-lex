#!/usr/bin/env python3
"""
Validation script for Phase E - Stage 1: Locations 4+5
Tests array subsequence type interpretations (nodeTypeArrayInterpretation and edgeTypeArrayInterpretation)
"""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

def load_schema():
    """Load the LEX-2026.0.3.2 JSON Schema"""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        return json.load(f)

def load_test_yaml():
    """Load the test YAML file"""
    yaml_path = Path("src/grasch/examples/test-phase-e-locations-4-5.yaml")
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    print("=" * 80)
    print("Phase E - Stage 1: Locations 4+5 Validation")
    print("Testing: nodeTypeArrayInterpretation and edgeTypeArrayInterpretation")
    print("=" * 80)
    print()
    
    # Load schema and test data
    print("Loading schema...")
    schema = load_schema()
    print("✓ Schema loaded successfully")
    print()
    
    print("Loading test YAML...")
    test_data = load_test_yaml()
    print("✓ Test YAML loaded successfully")
    print()
    
    # Validate
    print("Validating test data against schema...")
    try:
        validate(instance=test_data, schema=schema)
        print("✓ VALIDATION SUCCESSFUL!")
        print()
        
        # Print summary of what was tested
        print("Test Summary:")
        print("-" * 80)
        
        graph_type = test_data['graphSchema']['graphType']
        node_types = graph_type.get('nodeTypes', [])
        edge_types = graph_type.get('edgeTypes', [])
        
        print(f"Total nodeTypes items: {len(node_types)}")
        print(f"Total edgeTypes items: {len(edge_types)}")
        print()
        
        print("NodeTypes breakdown:")
        for i, item in enumerate(node_types, 1):
            if 'nodeType' in item:
                print(f"  {i}. Bare NodeType (Location 6)")
            elif 'abstract' in item:
                if isinstance(item['abstract'], list):
                    print(f"  {i}. Abstract array subsequence - {len(item['abstract'])} types (Location 4)")
                else:
                    print(f"  {i}. Abstract single type (Location 6)")
            elif 'concrete' in item:
                if isinstance(item['concrete'], list):
                    print(f"  {i}. Concrete array subsequence - {len(item['concrete'])} types (Location 4)")
                else:
                    print(f"  {i}. Concrete single type (Location 6)")
            elif 'subtypesOf' in item:
                print(f"  {i}. SubtypesOf 2-level wrapper (Location 4)")
        
        print()
        print("EdgeTypes breakdown:")
        for i, item in enumerate(edge_types, 1):
            if 'edgeType' in item:
                print(f"  {i}. Bare EdgeType (Location 7)")
            elif 'abstract' in item:
                if isinstance(item['abstract'], list):
                    print(f"  {i}. Abstract array subsequence - {len(item['abstract'])} types (Location 5)")
                else:
                    print(f"  {i}. Abstract single type (Location 7)")
            elif 'exactlyOf' in item:
                print(f"  {i}. ExactlyOf 2-level wrapper (Location 5)")
        
        print()
        print("=" * 80)
        print("✓ ALL TESTS PASSED - Stage 1 Complete!")
        print("=" * 80)
        return 0
        
    except ValidationError as e:
        print("✗ VALIDATION FAILED!")
        print()
        print("Error details:")
        print(f"  Message: {e.message}")
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        print(f"  Schema path: {' -> '.join(str(p) for p in e.schema_path)}")
        print()
        print("=" * 80)
        print("✗ TESTS FAILED")
        print("=" * 80)
        return 1
    except Exception as e:
        print(f"✗ UNEXPECTED ERROR: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
