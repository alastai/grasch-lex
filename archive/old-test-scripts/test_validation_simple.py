#!/usr/bin/env python3
"""
Simple test to check if our GQL descriptors schema validation works.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    # Test basic imports
    from grasch.schemas import load_gql_descriptors_schema
    print("✓ Successfully imported schema loader")
    
    # Load the schema
    schema = load_gql_descriptors_schema()
    print("✓ Successfully loaded GQL descriptors schema")
    print(f"  Schema title: {schema.get('title')}")
    print(f"  Schema has {len(schema.get('$defs', {}))} definitions")
    
    # Test validation with minimal valid data
    try:
        from grasch.validation import SchemaValidator
        print("✓ Successfully imported validator")
        
        validator = SchemaValidator()
        print("✓ Successfully created validator")
        
        # Test with minimal valid graph type
        minimal_valid = {
            "graphType": {
                "declaredName": "GRAPH DATA",
                "preferredName": "PROPERTY GRAPH", 
                "nodeTypeDescriptors": [],
                "edgeTypeDescriptors": [],
                "nodeTypeKeyLabelSetDictionary": {},
                "edgeTypeKeyLabelSetDictionary": {},
                "constraintSetDictionary": {}
            }
        }
        
        result = validator.validate_dict(minimal_valid)
        print("✓ Minimal graph type validation passed")
        
        # Test with invalid data
        invalid_data = {
            "graphType": {
                "declaredName": "INVALID",  # Should be "GRAPH DATA"
                "preferredName": "PROPERTY GRAPH"
                # Missing required fields
            }
        }
        
        try:
            validator.validate_dict(invalid_data)
            print("✗ Invalid data validation should have failed")
        except Exception as e:
            print("✓ Invalid data correctly rejected")
            print(f"  Error: {str(e)[:100]}...")
        
    except ImportError as e:
        print(f"⚠ Validation dependencies not available: {e}")
        print("  Install with: pip install jsonschema pyyaml")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()