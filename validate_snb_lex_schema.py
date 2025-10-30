#!/usr/bin/env python3
"""
Validate the SNB LEX:2026.0.0 Graph Schema YAML against the JSON Schema
Version: LEX:2026.0.0
"""

import json
import yaml
import jsonschema
from pathlib import Path

def load_json_schema(schema_path: str) -> dict:
    """Load the JSON Schema from file"""
    with open(schema_path, 'r') as f:
        return json.load(f)

def load_yaml_data(yaml_path: str) -> dict:
    """Load the YAML data to validate"""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def validate_schema(data: dict, schema: dict) -> tuple[bool, list]:
    """Validate data against schema and return results"""
    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    return len(errors) == 0, errors

def main():
    # File paths
    schema_path = "lex-2026.0.0-graph-schema.schema.json"
    yaml_path = "snb-lex-2026.0.0-schema.yaml"
    
    try:
        # Load schema and data
        print(f"Loading JSON Schema from: {schema_path}")
        schema = load_json_schema(schema_path)
        
        print(f"Loading YAML data from: {yaml_path}")
        data = load_yaml_data(yaml_path)
        
        # Validate
        print("\nValidating YAML against JSON Schema...")
        is_valid, errors = validate_schema(data, schema)
        
        if is_valid:
            print("✅ VALIDATION SUCCESSFUL!")
            print("The SNB LEX:2026 Graph Schema YAML is valid according to the JSON Schema.")
            
            # Print some statistics
            node_count = len(data['graphType']['nodeTypes'])
            edge_count = len(data['graphType']['edgeTypes'])
            constraint_count = len(data.get('constraints', {}))
            
            print(f"\nSchema Statistics:")
            print(f"  - Node Types: {node_count}")
            print(f"  - Edge Types: {edge_count}")
            print(f"  - Constraints: {constraint_count}")
            print(f"  - Value Type System: {data['valueTypeSystemName']}")
            print(f"  - Schema Name: {data['identifier']['name']}")
            
        else:
            print("❌ VALIDATION FAILED!")
            print(f"Found {len(errors)} validation errors:")
            
            for i, error in enumerate(errors, 1):
                print(f"\nError {i}:")
                print(f"  Path: {' -> '.join(str(p) for p in error.absolute_path)}")
                print(f"  Message: {error.message}")
                if error.validator_value:
                    print(f"  Expected: {error.validator_value}")
                if hasattr(error, 'instance') and error.instance is not None:
                    print(f"  Found: {error.instance}")
    
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()