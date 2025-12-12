#!/usr/bin/env python3
"""
Validate Location 3 Test Files - GraphType Only

This script validates just the graphType portion of the test files
to isolate edge label validation from root-level schema issues.
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

def validate_graphtype(filepath, schema):
    """Validate just the graphType portion of a file"""
    print(f"\n{'='*70}")
    print(f"Validating GraphType in: {filepath}")
    print(f"{'='*70}")
    
    try:
        # Load YAML
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        # Extract graphType
        if 'graphSchema' not in data or 'graphType' not in data['graphSchema']:
            print("❌ ERROR: No graphType found in file")
            return False
        
        graphtype_data = data['graphSchema']['graphType']
        
        # Get GraphType definition from schema
        if '$defs' not in schema or 'GraphType' not in schema['$defs']:
            print("❌ ERROR: GraphType definition not found in schema")
            return False
        
        graphtype_schema = schema['$defs']['GraphType']
        
        # Validate
        validator = Draft202012Validator(graphtype_schema)
        validator.validate(graphtype_data)
        
        print("✅ VALID - GraphType validates successfully")
        
        # Show what we validated
        if 'concrete' in graphtype_data and 'edgeTypes' in graphtype_data['concrete']:
            edge_count = len(graphtype_data['concrete']['edgeTypes'])
            print(f"   - concrete.edgeTypes: {edge_count} edge types")
        
        if 'exactlyOf' in graphtype_data:
            if 'concrete' in graphtype_data['exactlyOf'] and 'edgeTypes' in graphtype_data['exactlyOf']['concrete']:
                edge_count = len(graphtype_data['exactlyOf']['concrete']['edgeTypes'])
                print(f"   - exactlyOf.concrete.edgeTypes: {edge_count} edge types")
        
        return True
        
    except ValidationError as e:
        print(f"❌ INVALID - Validation error:")
        print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
        print(f"   Message: {e.message}")
        if e.context:
            print(f"   Context errors:")
            for ctx_error in e.context[:3]:  # Show first 3 context errors
                print(f"     - {ctx_error.message}")
        return False
    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {e}")
        return False

def main():
    """Main validation function"""
    print("="*70)
    print("Location 3 GraphType Validation")
    print("Testing edge label format in TI-wrapped edgeTypes")
    print("="*70)
    
    # Load schema
    print("\nLoading schema...")
    schema = load_schema()
    print("✅ Schema loaded successfully")
    
    # Test files
    test_files = [
        "src/grasch/examples/test-phase-e-location-3.yaml",
        "src/grasch/examples/test-phase-e-location-3-two-level.yaml",
    ]
    
    # Validate each file
    results = {}
    for filepath in test_files:
        if Path(filepath).exists():
            results[filepath] = validate_graphtype(filepath, schema)
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
        print("\n🎉 All Location 3 GraphType tests PASSED!")
        print("\nFindings:")
        print("- Edge labels now use correct object format with typeLabel: child")
        print("- TI-wrapped edgeTypes validate successfully")
        print("- Both 1-level (concrete) and 2-level (exactlyOf.concrete) work")
        return 0
    else:
        print("\n❌ Some tests FAILED - review errors above")
        return 1

if __name__ == "__main__":
    exit(main())
