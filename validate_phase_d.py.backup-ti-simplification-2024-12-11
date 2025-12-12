#!/usr/bin/env python3
import json, yaml
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
test_path = Path("test-phase-d.yaml")

with open(schema_path) as f:
    schema = json.load(f)
with open(test_path) as f:
    test_data = yaml.safe_load(f)

resolver = RefResolver.from_schema(schema)
validator = Draft202012Validator(schema, resolver=resolver)
errors = list(validator.iter_errors(test_data))

if errors:
    print(f"❌ FAILED ({len(errors)} errors)")
    for i, e in enumerate(errors[:3]):
        print(f"\n{i+1}. Path: {list(e.path)}")
        print(f"   {e.message[:150]}")
else:
    print("✅ PHASE D COMPLETE!")
    print("\nUndirected endpoint TI wrappers now supported:")
    print("  • 0-level (bare): Person")
    print("  • 1-level: abstract: Person")
    print("  • 2-level: properSubtypesOf: {concrete: Person} ← NEW!")
    print("\n" + "="*60)
    print("PHASES A-D ALL COMPLETE! ✅")
    print("="*60)
