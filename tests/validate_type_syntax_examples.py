#!/usr/bin/env python3
"""
Validation script for Type Definition Syntax Examples
Tests all syntax patterns against LEX:2026.0.3.1 JSON Schema
"""

import json
import yaml
import jsonschema
from pathlib import Path
import sys

def load_json_schema(schema_path: str) -> dict:
    """Load and parse JSON Schema file"""
    with open(schema_path, 'r') as f:
        return json.load(f)

def load_yaml_schema(yaml_path: str) -> dict:
    """Load and parse YAML schema file"""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def validate_schema(yaml_data: dict, json_schema: dict) -> tuple[bool, list]:
    """Validate YAML data against JSON Schema"""
    try:
        jsonschema.validate(yaml_data, json_schema)
        return True, []
    except jsonschema.ValidationError as e:
        return False, [str(e)]
    except Exception as e:
        return False, [f"Validation error: {e}"]

def main():
    print("LEX:2026.0.3.1 Type Definition Syntax Validation")
    print("=" * 60)
    
    # File paths
    json_schema_path = "src/grasch/schemas/lex-2026.0.3.1.schema.json"
    if not Path(json_schema_path).exists():
        json_schema_path = "../src/grasch/schemas/lex-2026.0.3.1.schema.json"
    
    yaml_schema_path = "src/grasch/examples/lex-2026.0.3.1-type-definition-syntax-examples.yaml"
    if not Path(yaml_schema_path).exists():
        yaml_schema_path = "../src/grasch/examples/lex-2026.0.3.1-type-definition-syntax-examples.yaml"
    
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
    print("\n🔍 Validating all syntax patterns...")
    is_valid, errors = validate_schema(yaml_data, json_schema)
    
    if is_valid:
        print("✅ All syntax patterns validated successfully!")
        
        # Analyze patterns
        graph_type = yaml_data.get('graphType', {})
        node_types = graph_type.get('nodeTypes', [])
        allow_subtypes = graph_type.get('allowSubtypesOf', {})
        abstract_types = allow_subtypes.get('abstractSupertypes', {}).get('nodeTypes', [])
        
        print(f"\n📊 Syntax Patterns Validated:")
        print(f"  Regular node types: {len(node_types)}")
        print(f"  Abstract hierarchy types: {len(abstract_types)}")
        
        # Identify patterns
        patterns = {
            'base_with_implies': 0,
            'base_with_labels': 0,
            'extends_with_adding': 0,
            'extends_with_adding_labels': 0,
            'implies_with_supertypes': 0,
            'implies_with_supertypes_labels': 0
        }
        
        for nt in node_types:
            node_type = nt.get('nodeType', {})
            if 'extends' in node_type:
                if 'adding' in node_type:
                    adding = node_type['adding']
                    if 'labels' in adding:
                        patterns['extends_with_adding_labels'] += 1
                    else:
                        patterns['extends_with_adding'] += 1
            elif 'implies' in node_type:
                implies = node_type['implies']
                if 'supertypes' in implies:
                    if 'labels' in implies:
                        patterns['implies_with_supertypes_labels'] += 1
                    else:
                        patterns['implies_with_supertypes'] += 1
                elif 'labels' in implies:
                    patterns['base_with_labels'] += 1
                else:
                    patterns['base_with_implies'] += 1
        
        print(f"\n🎯 Pattern Distribution:")
        print(f"  Pattern A (base with implies): {patterns['base_with_implies']}")
        print(f"  Pattern B (base with labels): {patterns['base_with_labels']}")
        print(f"  Pattern C (extends + adding): {patterns['extends_with_adding']}")
        print(f"  Pattern D (extends + adding labels): {patterns['extends_with_adding_labels']}")
        print(f"  Pattern E (implies + supertypes): {patterns['implies_with_supertypes']}")
        print(f"  Pattern F (implies + supertypes + labels): {patterns['implies_with_supertypes_labels']}")
        
        print(f"\n🎉 Type definition syntax validation completed successfully!")
        return 0
    else:
        print("❌ Syntax validation FAILED")
        print("\nValidation errors:")
        for error in errors:
            print(f"  • {error}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
