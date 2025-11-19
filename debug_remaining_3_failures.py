#!/usr/bin/env python3
"""
Debug the remaining 3 failing files in detail
"""
import json
import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from jsonschema import Draft202012Validator
from grasch.import_preprocessor import preprocess_yaml_with_imports

# Load schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Check the 3 remaining failing files
failing_files = [
    "lex-2026.0.3.2-minimal-import-example.yaml",
    "lex-2026.0.3.2-mixed-import-example.yaml",
    "lex-2026.0.3.2-snb-schema.yaml"
]

for filename in failing_files:
    print("=" * 70)
    print(f"Analyzing: {filename}")
    print("=" * 70)
    
    file_path = Path(f"src/grasch/examples/{filename}")
    
    try:
        preprocessed = preprocess_yaml_with_imports(file_path)
        
        print(f"Root keys: {list(preprocessed.keys())}")
        
        # Get ALL validation errors
        errors = list(validator.iter_errors(preprocessed))
        
        if errors:
            print(f"\nFound {len(errors)} validation error(s):\n")
            
            for i, error in enumerate(errors[:3]):  # Show first 3 errors
                print(f"Error {i+1}:")
                print(f"  Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
                print(f"  Validator: {error.validator}")
                print(f"  Message: {error.message[:300]}")
                
                # Show the actual value that's failing
                if error.absolute_path:
                    try:
                        current = preprocessed
                        for key in error.absolute_path:
                            current = current[key]
                        print(f"  Failing value type: {type(current).__name__}")
                        if isinstance(current, (str, int, bool)):
                            print(f"  Failing value: {current}")
                        elif isinstance(current, dict):
                            print(f"  Failing value keys: {list(current.keys())[:5]}")
                        elif isinstance(current, list):
                            print(f"  Failing value length: {len(current)}")
                    except:
                        pass
                
                print()
        else:
            print("✓ No validation errors found")
            
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        import traceback
        traceback.print_exc()
    
    print()
