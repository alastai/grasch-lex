#!/usr/bin/env python3
"""
Check what the preprocessed nodeTypes structure looks like in failing files
"""
import json
import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from grasch.import_preprocessor import preprocess_yaml_with_imports

# Check one failing file
filename = "lex-2026.0.3.2-minimal-import-example.yaml"
file_path = Path(f"src/grasch/examples/{filename}")

print(f"Checking preprocessed structure of: {filename}")
print("=" * 70)

preprocessed = preprocess_yaml_with_imports(file_path)

if 'graphSchema' in preprocessed:
    gs = preprocessed['graphSchema']
    if 'graphType' in gs:
        gt = gs['graphType']
        if 'nodeTypes' in gt:
            node_types = gt['nodeTypes']
            print(f"nodeTypes is a: {type(node_types)}")
            print(f"nodeTypes length: {len(node_types)}")
            print()
            
            for i, item in enumerate(node_types):
                print(f"Item {i}:")
                print(f"  Type: {type(item)}")
                if isinstance(item, dict):
                    print(f"  Keys: {list(item.keys())}")
                    
                    # Show first level structure
                    for key in item.keys():
                        val = item[key]
                        print(f"  {key}: {type(val).__name__}", end="")
                        if isinstance(val, dict):
                            print(f" with keys: {list(val.keys())[:3]}")
                        elif isinstance(val, list):
                            print(f" with {len(val)} items")
                        else:
                            print()
                print()
