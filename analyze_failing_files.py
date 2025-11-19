#!/usr/bin/env python3
"""
Analyze each failing file to understand the specific validation issue
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

# Files that fail AFTER IMPORTS
failing_files = [
    "lex-2026.0.3.2-all-import-patterns.yaml",
    "lex-2026.0.3.2-complete-import-example.yaml",
    "lex-2026.0.3.2-finbench-sf1-graph.yaml",
    "lex-2026.0.3.2-minimal-import-example.yaml",
    "lex-2026.0.3.2-mixed-import-example.yaml",
    "lex-2026.0.3.2-snb-schema.yaml",
    "lex-2026.0.3.2-type-definition-syntax-examples.yaml",
]

for filename in failing_files:
    print("=" * 70)
    print(f"Analyzing: {filename}")
    print("=" * 70)
    
    file_path = Path(f"src/grasch/examples/{filename}")
    
    try:
        preprocessed = preprocess_yaml_with_imports(file_path)
        errors = list(validator.iter_errors(preprocessed))
        
        if errors:
            print(f"✗ {len(errors)} validation error(s)")
            
            for i, error in enumerate(errors[:2]):  # Show first 2 errors
                print(f"\nError {i+1}:")
                print(f"  Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
                print(f"  Validator: {error.validator}")
                
                # For oneOf errors, show which options failed
                if error.validator == 'oneOf' and hasattr(error, 'context'):
                    print(f"  oneOf has {len(error.context)} options, all failed:")
                    for j, sub_error in enumerate(error.context):
                        print(f"    Option {j+1}: {sub_error.validator}")
                        if sub_error.validator == 'required':
                            print(f"      Missing: {sub_error.message}")
                        elif sub_error.validator == 'additionalProperties':
                            print(f"      Extra: {sub_error.message}")
                        elif sub_error.validator == 'type':
                            print(f"      Type: {sub_error.message}")
                        else:
                            print(f"      {sub_error.message[:80]}")
        else:
            print("✓ No errors (should not happen for failing files)")
            
    except Exception as e:
        print(f"✗ Error during preprocessing: {e}")
    
    print()
