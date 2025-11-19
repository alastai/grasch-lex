#!/usr/bin/env python3
"""Test import preprocessor behavior"""

import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from grasch.import_preprocessor import preprocess_yaml_with_imports

# Test with minimal-test.yaml
test_file = Path("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml")

print("Testing import preprocessor with minimal-test.yaml")
print("=" * 80)

# Load raw file
with open(test_file) as f:
    raw_data = yaml.safe_load(f)

print("\n1. RAW FILE (before preprocessing):")
print("-" * 80)
print(f"propertyGraphDataModel type: {type(raw_data['graphSchema']['graphType']['propertyGraphDataModel'])}")
print(f"propertyGraphDataModel content: {raw_data['graphSchema']['graphType']['propertyGraphDataModel']}")

# Preprocess
try:
    preprocessed = preprocess_yaml_with_imports(test_file)
    
    print("\n2. PREPROCESSED FILE (after import resolution):")
    print("-" * 80)
    print(f"propertyGraphDataModel type: {type(preprocessed['graphSchema']['graphType']['propertyGraphDataModel'])}")
    print(f"propertyGraphDataModel keys: {list(preprocessed['graphSchema']['graphType']['propertyGraphDataModel'].keys())[:5]}...")
    print(f"Has 'import' key: {'import' in preprocessed['graphSchema']['graphType']['propertyGraphDataModel']}")
    print(f"Has 'valueTypeSystemName' key: {'valueTypeSystemName' in preprocessed['graphSchema']['graphType']['propertyGraphDataModel']}")
    
    print("\n3. VERIFICATION:")
    print("-" * 80)
    if 'import' in preprocessed['graphSchema']['graphType']['propertyGraphDataModel']:
        print("❌ FAIL: 'import' key still present after preprocessing")
    else:
        print("✅ PASS: 'import' key removed")
    
    if 'valueTypeSystemName' in preprocessed['graphSchema']['graphType']['propertyGraphDataModel']:
        print("✅ PASS: Content from import file is present")
    else:
        print("❌ FAIL: Content from import file is missing")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
