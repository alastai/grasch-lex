#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))
from grasch.import_preprocessor import preprocess_yaml_with_imports

file_path = Path('src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml')
preprocessed = preprocess_yaml_with_imports(file_path)

with open('preprocessed_minimal.json', 'w') as f:
    json.dump(preprocessed, f, indent=2)

print('Saved to preprocessed_minimal.json')
