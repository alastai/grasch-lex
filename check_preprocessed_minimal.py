#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from grasch.import_preprocessor import preprocess_yaml_with_imports

file_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml")
preprocessed = preprocess_yaml_with_imports(file_path)

print("Root keys:", list(preprocessed.keys()))
print("\nGraphSchema keys:", list(preprocessed['graphSchema'].keys()))
print("\nGraphType keys:", list(preprocessed['graphSchema']['graphType'].keys()))

# Check if propertyGraphDataModel exists
if 'propertyGraphDataModel' in preprocessed['graphSchema']['graphType']:
    print("\n✓ Has propertyGraphDataModel")
    pgdm = preprocessed['graphSchema']['graphType']['propertyGraphDataModel']
    print("  Keys:", list(pgdm.keys())[:5])
else:
    print("\n✗ Missing propertyGraphDataModel")

# Save for inspection
with open('preprocessed_minimal.json', 'w') as f:
    json.dump(preprocessed, f, indent=2)
print("\nSaved to preprocessed_minimal.json")
