#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from grasch.import_preprocessor import preprocess_yaml_with_imports

file_path = Path("src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml")
preprocessed = preprocess_yaml_with_imports(file_path)

node_types = preprocessed['graphSchema']['graphType']['nodeTypes']

print(f"nodeTypes array has {len(node_types)} items\n")

for i, item in enumerate(node_types):
    print(f"Item {i}: {list(item.keys())}")
    if 'subtypesOf' in item:
        print(f"  subtypesOf keys: {list(item['subtypesOf'].keys())}")
        if 'abstract' in item['subtypesOf']:
            print(f"    abstract keys: {list(item['subtypesOf']['abstract'].keys())}")
