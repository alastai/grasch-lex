#!/usr/bin/env python3
"""
Test wrapper stripping in import preprocessor
"""
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from grasch.import_preprocessor import preprocess_yaml_with_imports

def test_wrapper_stripping():
    """Test that wrapper keys are stripped correctly"""
    print("Testing Wrapper Stripping")
    print("=" * 60)
    
    # Test with all-import-patterns which imports nodeTypes
    test_file = Path("src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml")
    
    print("\n1. Processing file with nodeTypes import...")
    result = preprocess_yaml_with_imports(test_file)
    
    # Check the structure
    graph_type = result['graphSchema']['graphType']
    node_types = graph_type.get('nodeTypes')
    
    print(f"\n2. Checking nodeTypes structure...")
    print(f"   Type: {type(node_types)}")
    
    if isinstance(node_types, dict):
        print(f"   Keys: {list(node_types.keys())}")
        if 'nodeTypes' in node_types:
            print("   ❌ FAIL: Double nesting detected (nodeTypes.nodeTypes)")
            print("   The wrapper was NOT stripped correctly")
            return False
        else:
            print("   ✅ Unexpected dict structure (should be array)")
            return False
    elif isinstance(node_types, list):
        print(f"   Length: {len(node_types)}")
        print(f"   First item keys: {list(node_types[0].keys()) if node_types else 'empty'}")
        print("   ✅ PASS: nodeTypes is an array (wrapper was stripped)")
        return True
    else:
        print(f"   ❌ Unexpected type: {type(node_types)}")
        return False

if __name__ == "__main__":
    success = test_wrapper_stripping()
    print("\n" + "=" * 60)
    if success:
        print("✅ Wrapper stripping test PASSED")
        sys.exit(0)
    else:
        print("❌ Wrapper stripping test FAILED")
        sys.exit(1)
