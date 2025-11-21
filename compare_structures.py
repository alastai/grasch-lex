#!/usr/bin/env python3
"""
Compare the actual structures to find the difference
"""
import json
import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from grasch.import_preprocessor import preprocess_yaml_with_imports

# Load both files
test1 = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")
test2 = Path("src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml")

data1 = preprocess_yaml_with_imports(test1)
data2 = preprocess_yaml_with_imports(test2)

# Save to JSON for easier inspection
with open("minimal-test-preprocessed.json", "w") as f:
    json.dump(data1, f, indent=2)

with open("all-import-patterns-preprocessed.json", "w") as f:
    json.dump(data2, f, indent=2)

print("Saved preprocessed data to JSON files")
print("\nminimal-test nodeTypes count:", len(data1['graphSchema']['graphType']['nodeTypes']))
print("all-import-patterns nodeTypes count:", len(data2['graphSchema']['graphType']['nodeTypes']))

print("\nminimal-test edgeTypes count:", len(data1['graphSchema']['graphType']['edgeTypes']))
print("all-import-patterns edgeTypes count:", len(data2['graphSchema']['graphType']['edgeTypes']))

# Check for any extra keys
def get_all_keys(d, prefix=""):
    keys = set()
    if isinstance(d, dict):
        for k, v in d.items():
            keys.add(f"{prefix}.{k}" if prefix else k)
            keys.update(get_all_keys(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(d, list):
        for i, item in enumerate(d):
            keys.update(get_all_keys(item, f"{prefix}[{i}]"))
    return keys

keys1 = get_all_keys(data1)
keys2 = get_all_keys(data2)

print("\nKeys only in all-import-patterns:")
for key in sorted(keys2 - keys1)[:20]:
    print(f"  {key}")
