#!/usr/bin/env python3
"""
Detailed test to understand why preprocessed files don't validate
"""
import sys
import json
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from jsonschema import Draft202012Validator
from grasch.import_preprocessor import preprocess_yaml_with_imports

def test_minimal_case():
    """Test with minimal-test.yaml to understand validation failure"""
    print("=" * 70)
    print("Testing Schema Validation with Preprocessed File")
    print("=" * 70)
    
    # Load schema
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    validator = Draft202012Validator(schema)
    
    # Test file
    test_file = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")
    
    # Preprocess
    print("\n1. Preprocessing file...")
    processed = preprocess_yaml_with_imports(test_file)
    
    # Extract the graphType
    graph_type = processed['graphSchema']['graphType']
    
    print("\n2. Structure after preprocessing:")
    print(f"   graphType keys: {list(graph_type.keys())}")
    print(f"   nodeTypes type: {type(graph_type.get('nodeTypes'))}")
    if isinstance(graph_type.get('nodeTypes'), list):
        print(f"   nodeTypes length: {len(graph_type['nodeTypes'])}")
        print(f"   First item: {graph_type['nodeTypes'][0]}")
    
    # Validate the whole document
    print("\n3. Validating full document...")
    errors = list(validator.iter_errors(processed))
    
    if errors:
        print(f"   ❌ {len(errors)} validation errors found")
        print("\n4. Detailed errors:")
        for i, error in enumerate(errors[:3], 1):  # Show first 3
            print(f"\n   Error {i}:")
            print(f"   Path: {'.'.join(str(p) for p in error.absolute_path)}")
            print(f"   Validator: {error.validator}")
            print(f"   Message: {error.message}")
            if error.validator == 'oneOf':
                print(f"   Schema path: {'.'.join(str(p) for p in error.absolute_schema_path)}")
                # Try to understand which oneOf branch failed
                if hasattr(error, 'context') and error.context:
                    print(f"   OneOf branches tested: {len(error.context)}")
                    for j, suberror in enumerate(error.context[:2], 1):
                        print(f"     Branch {j} failed: {suberror.validator} - {suberror.message}")
    else:
        print("   ✅ Document validates successfully!")
    
    # Now test just the nodeTypes array against the schema
    print("\n5. Testing nodeTypes array directly...")
    node_types_schema = schema['$defs']['GraphType']['properties']['nodeTypes']
    print(f"   nodeTypes schema has oneOf with {len(node_types_schema['oneOf'])} options")
    
    # Test against each oneOf option
    for i, option in enumerate(node_types_schema['oneOf'], 1):
        print(f"\n   Option {i}: {option.get('type', 'unknown type')}")
        if option.get('type') == 'array':
            print(f"     Description: {option.get('description', 'N/A')}")
            # Try to validate
            option_validator = Draft202012Validator(option)
            option_errors = list(option_validator.iter_errors(graph_type['nodeTypes']))
            if option_errors:
                print(f"     ❌ Fails: {option_errors[0].message}")
            else:
                print(f"     ✅ Matches!")
        elif option.get('type') == 'object':
            print(f"     Description: {option.get('description', 'N/A')}")
            print(f"     Required: {option.get('required', [])}")
            print(f"     ❌ Doesn't match (we have array, not object)")

if __name__ == "__main__":
    test_minimal_case()
