#!/usr/bin/env python3
"""
Test PC to C Canonicalization Equivalence

Validates that:
1. All PC forms validate against schema
2. PC forms canonicalize to C form
3. C forms validate against schema
4. All PC variants produce the same C form (or semantically equivalent)

Test Files:
- test-pc-abbreviations.yaml: Single-level TI abbreviations
- test-pc-phase1-import.yaml: Phase 1 imports (import TI + content)
- test-pc-phase2-import.yaml: Phase 2 imports (import content only, TI override)
- test-pc-sealed.yaml: Sealed hierarchies
- test-expected-canonical.yaml: Expected C form
"""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError

# Paths
EXAMPLES_DIR = Path("src/grasch/examples")
SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

# Test files
PC_TESTS = {
    "abbreviations": EXAMPLES_DIR / "test-pc-abbreviations.yaml",
    "phase1-import": EXAMPLES_DIR / "test-pc-phase1-import.yaml",
    "phase2-import": EXAMPLES_DIR / "test-pc-phase2-import.yaml",
    "sealed": EXAMPLES_DIR / "test-pc-sealed.yaml",
}

EXPECTED_C = EXAMPLES_DIR / "test-expected-canonical.yaml"


def load_yaml(path: Path) -> dict:
    """Load YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def load_schema() -> dict:
    """Load JSON Schema."""
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def validate_against_schema(data: dict, schema: dict) -> tuple[bool, str]:
    """
    Validate data against schema.
    
    Returns:
        (is_valid, error_message)
    """
    try:
        validate(instance=data, schema=schema)
        return True, ""
    except ValidationError as e:
        return False, str(e)


def canonicalize(pc_form: dict) -> dict:
    """
    Canonicalize PC form to C form.
    
    TODO: This needs to be implemented in the canonicalizing_preprocessor module.
    For now, this is a placeholder that returns the input unchanged.
    
    Required transformations:
    1. Expand TI abbreviations (abstract: → subtypesOf:abstract:)
    2. Resolve imports (Phase 1 and Phase 2)
    3. Amalgamate duplicate TIs
    4. Expand sealed to final
    5. Consolidate collections
    """
    # Placeholder - actual implementation needed
    print("⚠️  WARNING: Canonicalization not yet implemented")
    print("   This test will fail until canonicalizer is updated")
    return pc_form


def compare_canonical_forms(c1: dict, c2: dict) -> tuple[bool, str]:
    """
    Compare two canonical forms for equivalence.
    
    Returns:
        (are_equivalent, difference_message)
    """
    if c1 == c2:
        return True, ""
    
    # TODO: Implement semantic equivalence checking
    # For now, just do structural equality
    return False, "Canonical forms differ (structural comparison)"


def test_pc_form(name: str, pc_path: Path, schema: dict, expected_c: dict) -> bool:
    """
    Test a single PC form variant.
    
    Returns:
        True if all tests pass, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    # Load PC form
    try:
        pc_form = load_yaml(pc_path)
        print(f"✅ Loaded PC form: {pc_path}")
    except Exception as e:
        print(f"❌ Failed to load PC form: {e}")
        return False
    
    # 1. Validate PC form
    is_valid, error = validate_against_schema(pc_form, schema)
    if is_valid:
        print("✅ PC form validates against schema")
    else:
        print(f"❌ PC form validation failed:")
        print(f"   {error}")
        return False
    
    # 2. Canonicalize PC → C
    try:
        c_form = canonicalize(pc_form)
        print("✅ Canonicalized PC → C")
    except Exception as e:
        print(f"❌ Canonicalization failed: {e}")
        return False
    
    # 3. Validate C form
    is_valid, error = validate_against_schema(c_form, schema)
    if is_valid:
        print("✅ C form validates against schema")
    else:
        print(f"❌ C form validation failed:")
        print(f"   {error}")
        return False
    
    # 4. Compare with expected C form
    are_equivalent, diff = compare_canonical_forms(c_form, expected_c)
    if are_equivalent:
        print("✅ C form matches expected canonical form")
    else:
        print(f"❌ C form doesn't match expected:")
        print(f"   {diff}")
        return False
    
    print(f"\n✅ All tests passed for: {name}")
    return True


def main():
    """Run all PC→C equivalence tests."""
    print("="*60)
    print("PC → C Canonicalization Equivalence Tests")
    print("="*60)
    
    # Load schema
    try:
        schema = load_schema()
        print(f"✅ Loaded schema: {SCHEMA_PATH}")
    except Exception as e:
        print(f"❌ Failed to load schema: {e}")
        return 1
    
    # Load expected canonical form
    try:
        expected_c = load_yaml(EXPECTED_C)
        print(f"✅ Loaded expected C form: {EXPECTED_C}")
    except Exception as e:
        print(f"❌ Failed to load expected C form: {e}")
        return 1
    
    # Test each PC variant
    results = {}
    for name, pc_path in PC_TESTS.items():
        results[name] = test_pc_form(name, pc_path, schema, expected_c)
    
    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
