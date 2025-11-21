#!/usr/bin/env python3
"""
Check specifically the graphSchema validation
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from jsonschema import Draft202012Validator
from grasch.import_preprocessor import preprocess_yaml_with_imports

# Load schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Get the GraphSchemaContent definition
graph_schema_def = schema['$defs']['GraphSchemaContent']

# Create a validator for just GraphSchemaContent
validator = Draft202012Validator(graph_schema_def)

# Check one file
file_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml")
preprocessed = preprocess_yaml_with_imports(file_path)

# Extract just the graphSchema content
graph_schema_content = preprocessed['graphSchema']

print("=" * 70)
print("Validating graphSchema content directly")
print("=" * 70)

errors = list(validator.iter_errors(graph_schema_content))

if errors:
    print(f"\nFound {len(errors)} error(s):\n")
    for i, error in enumerate(errors[:5]):
        print(f"Error {i+1}:")
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path)}")
        print(f"  Validator: {error.validator}")
        print(f"  Message: {error.message[:300]}")
        
        if error.validator == 'oneOf' and error.context:
            print(f"  Sub-errors: {len(error.context)}")
            for j, ctx in enumerate(error.context[:2]):
                print(f"    {j+1}. {ctx.validator}: {ctx.message[:150]}")
        print()
else:
    print("✓ No errors - graphSchema content is valid!")
