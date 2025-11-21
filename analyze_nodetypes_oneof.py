#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from jsonschema import Draft202012Validator
from grasch.import_preprocessor import preprocess_yaml_with_imports

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))
validator = Draft202012Validator(schema)

file_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml")
preprocessed = preprocess_yaml_with_imports(file_path)

errors = list(validator.iter_errors(preprocessed))
root_error = errors[0]

# Find the nodeTypes oneOf error
nodetypes_error = root_error.context[2]

print(f"nodeTypes oneOf error has {len(nodetypes_error.context)} sub-errors\n")

for i, ctx_err in enumerate(nodetypes_error.context):
    print(f"Sub-error {i+1}:")
    print(f"  Validator: {ctx_err.validator}")
    print(f"  Schema path: {'.'.join(str(p) for p in ctx_err.schema_path)}")
    print(f"  Message: {ctx_err.message[:200]}")
    print()
