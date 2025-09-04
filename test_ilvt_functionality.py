#!/usr/bin/env python3
"""
Test script to verify ILVT functionality works correctly.
"""

import sys
sys.path.insert(0, 'src')

from grasch.value_types import inferPreciseType, translateType, isTypeCompatible
from grasch.core import LanguageLevel, LanguageTypes

def test_precise_inference():
    """Test precise type inference"""
    print("=== Testing Precise Type Inference ===")
    
    # Test integer value 128
    gql_type = inferPreciseType(128, LanguageTypes.GQL)
    cypher_type = inferPreciseType(128, LanguageTypes.CYPHER)
    
    print(f"Value 128:")
    print(f"  GQL type system: {gql_type}")
    print(f"  Cypher type system: {cypher_type}")
    
    # Test negative integer -100
    gql_neg = inferPreciseType(-100, LanguageTypes.GQL)
    cypher_neg = inferPreciseType(-100, LanguageTypes.CYPHER)
    
    print(f"Value -100:")
    print(f"  GQL type system: {gql_neg}")
    print(f"  Cypher type system: {cypher_neg}")
    
    # Test larger value 70000
    gql_large = inferPreciseType(70000, LanguageTypes.GQL)
    cypher_large = inferPreciseType(70000, LanguageTypes.CYPHER)
    
    print(f"Value 70000:")
    print(f"  GQL type system: {gql_large}")
    print(f"  Cypher type system: {cypher_large}")

def test_type_translation():
    """Test type translation between language levels"""
    print("\n=== Testing Type Translation ===")
    
    # Translate Cypher INTEGER to GQL
    gql_equivalents = translateType("INTEGER", LanguageTypes.CYPHER, LanguageTypes.GQL)
    print(f"Cypher INTEGER -> GQL: {gql_equivalents}")
    
    # Translate GQL UINT8 to Cypher
    cypher_equivalents = translateType("UINT8", LanguageTypes.GQL, LanguageTypes.CYPHER)
    print(f"GQL UINT8 -> Cypher: {cypher_equivalents}")

def test_type_compatibility():
    """Test type compatibility"""
    print("\n=== Testing Type Compatibility ===")
    
    # Test Cypher INTEGER with GQL BIGINT
    compat1 = isTypeCompatible("INTEGER", LanguageTypes.CYPHER, "BIGINT", LanguageTypes.GQL)
    print(f"Cypher INTEGER compatible with GQL BIGINT: {compat1}")
    
    # Test GQL UINT8 with Cypher INTEGER
    compat2 = isTypeCompatible("UINT8", LanguageTypes.GQL, "INTEGER", LanguageTypes.CYPHER)
    print(f"GQL UINT8 compatible with Cypher INTEGER: {compat2}")

if __name__ == "__main__":
    try:
        test_precise_inference()
        test_type_translation()
        test_type_compatibility()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()