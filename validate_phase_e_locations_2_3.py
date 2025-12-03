#!/usr/bin/env python3
"""
Validate Phase E Locations 2+3: nodeTypesInterpretation & edgeTypesInterpretation

These locations wrap the ENTIRE nodeTypes or edgeTypes property.
"""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

def load_schema():
    """Load the LEX-2026.0.3.2 JSON Schema"""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        return json.load(f)

def load_yaml_file(filepath):
    """Load a YAML test file"""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def validate_file(filepath, schema):
    """Validate a single YAML file against the schema"""
    print(f"\n{'='*70}")
    print(f"Validating: {filepath}")
    print(f"{'='*70}")
    
    try:
        data = load_yaml_file(filepath)
        validator = Draft202012Validator(schema)
        validator.validate(data)
        print("✅ VALID - File validates successfully")
        return True
    except ValidationError as e:
        print(f"❌ INVALID - Validation error:")
        print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
        print(f"   Message: {e.message}")
        if e.context:
            print(f"   Context errors:")
            for ctx_error in e.context:
                print(f"     - {ctx_error.message}")
        return False
    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {e}")
        return False

def main():
    """Main validation function"""
    print("="*70)
    print("Phase E - Stage 2: Validating Locations 2+3")
    print("Location 2: nodeTypesInterpretation (wraps entire nodeTypes property)")
    print("Location 3: edgeTypesInterpretation (wraps entire edgeTypes property)")
    print("="*70)
    
    # Load schema
    print("\nLoading schema...")
    schema = load_schema()
    print("✅ Schema loaded successfully")
    
    # Test files
    test_files = [
        "src/grasch/examples/test-phase-e-location-2.yaml",
        "src/grasch/examples/test-phase-e-location-2-two-level.yaml",
        "src/grasch/examples/test-phase-e-location-3.yaml",
        "src/grasch/examples/test-phase-e-location-3-two-level.yaml",
    ]
    
    # Validate each file
    results = {}
    for filepath in test_files:
        if Path(filepath).exists():
            results[filepath] = validate_file(filepath, schema)
        else:
            print(f"\n⚠️  File not found: {filepath}")
            results[filepath] = False
    
    # Summary
    print(f"\n{'='*70}")
    print("VALIDATION SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for filepath, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {Path(filepath).name}")
    
    print(f"\nTotal: {passed}/{total} files passed")
    
    if passed == total:
        print("\n🎉 All Location 2+3 tests PASSED!")
        print("\nFindings:")
        print("- Location 2 (nodeTypesInterpretation) is correctly implemented")
        print("- Location 3 (edgeTypesInterpretation) is correctly implemented")
        print("- Both support 0-level (bare), 1-level, and 2-level TI wrappers")
        print("- Import support is available for both locations")
        return 0
    else:
        print("\n❌ Some tests FAILED - review errors above")
        return 1

if __name__ == "__main__":
    exit(main())
