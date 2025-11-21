#!/usr/bin/env python3
"""
Validate all LEX-2026.0.3.2 example YAML files against the JSON Schema.

This script validates files in both pre-canonical and canonical forms:
- Pre-canonical: Files with convenience syntax (wrappers, imports, etc.)
- Canonical: Files after canonicalization (normalized, imports resolved)

The single schema validates both forms.
"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

# Load the schema (single schema validates both pre-canonical and canonical forms)
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Files to validate
example_files = [
    "src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml",
    "src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml",
    "src/grasch/examples/lex-2026.0.3.2-complete-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-comprehensive-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-example-catalog-no-iri.yaml",
    "src/grasch/examples/lex-2026.0.3.2-example-catalog.yaml",
    "src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml",
    "src/grasch/examples/lex-2026.0.3.2-finbench-sf1-graph.yaml",
    "src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-mixed-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml",
    "src/grasch/examples/lex-2026.0.3.2-snb-special-identification-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-subtype-abstract-test.yaml",
    "src/grasch/examples/lex-2026.0.3.2-type-definition-syntax-examples.yaml",
]

results = {
    "valid": [],
    "invalid": [],
    "errors": {},
    "pre_canonical": {},
    "canonical": {}
}

def has_imports(data):
    """Check if data contains import statements (pre-canonical indicator)."""
    if isinstance(data, dict):
        if 'import' in data:
            return True
        for value in data.values():
            if has_imports(value):
                return True
    elif isinstance(data, list):
        for item in data:
            if has_imports(item):
                return True
    return False

for file_path in example_files:
    path = Path(file_path)
    if not path.exists():
        print(f"⚠️  SKIP: {path.name} (file not found)")
        continue
    
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Determine if this is pre-canonical or canonical form
        is_pre_canonical = has_imports(data)
        form_label = "pre-canonical" if is_pre_canonical else "canonical"
        
        # Validate (single schema validates both forms)
        errors = list(validator.iter_errors(data))
        
        if errors:
            results["invalid"].append(path.name)
            results["errors"][path.name] = []
            if is_pre_canonical:
                results["pre_canonical"][path.name] = "failed"
                print(f"❌ INVALID ({form_label}): {path.name}")
            else:
                results["canonical"][path.name] = "failed"
                print(f"❌ INVALID ({form_label}): {path.name}")
            
            for error in errors:
                error_path = ".".join(str(p) for p in error.absolute_path)
                error_msg = f"  Path: {error_path} - {error.message}"
                print(error_msg)
                results["errors"][path.name].append(error_msg)
        else:
            results["valid"].append(path.name)
            if is_pre_canonical:
                results["pre_canonical"][path.name] = "passed"
                print(f"✅ VALID ({form_label}): {path.name}")
                print(f"   Pre-canonical validation: passed")
            else:
                results["canonical"][path.name] = "passed"
                print(f"✅ VALID ({form_label}): {path.name}")
                print(f"   Canonical validation: passed")
    
    except yaml.YAMLError as e:
        results["invalid"].append(path.name)
        results["errors"][path.name] = [f"YAML parsing error: {e}"]
        print(f"❌ YAML ERROR: {path.name} - {e}")
    except Exception as e:
        results["invalid"].append(path.name)
        results["errors"][path.name] = [f"Unexpected error: {e}"]
        print(f"❌ ERROR: {path.name} - {e}")

# Summary
print("\n" + "="*60)
print("VALIDATION SUMMARY")
print("="*60)
print(f"Total files: {len(example_files)}")
print(f"Valid: {len(results['valid'])}")
print(f"Invalid: {len(results['invalid'])}")
print(f"Pre-canonical files: {len(results['pre_canonical'])}")
print(f"Canonical files: {len(results['canonical'])}")

if results["valid"]:
    print("\n✅ Valid files:")
    for name in results["valid"]:
        if name in results["pre_canonical"]:
            print(f"  - {name} (pre-canonical validation: {results['pre_canonical'][name]})")
        elif name in results["canonical"]:
            print(f"  - {name} (canonical validation: {results['canonical'][name]})")

if results["invalid"]:
    print("\n❌ Invalid files:")
    for name in results["invalid"]:
        print(f"  - {name}")

# Save detailed results
with open("SCHEMA-VALIDATION-RESULTS.md", "w") as f:
    f.write("# LEX-2026.0.3.2 Schema Validation Results\n\n")
    f.write("## Overview\n\n")
    f.write("This validation uses the single LEX-2026.0.3.2 schema which validates both:\n")
    f.write("- **Pre-canonical form**: Files with convenience syntax (wrappers, imports, etc.)\n")
    f.write("- **Canonical form**: Files after canonicalization (normalized, imports resolved)\n\n")
    f.write(f"**Total files tested:** {len(example_files)}\n\n")
    f.write(f"**Valid:** {len(results['valid'])}\n\n")
    f.write(f"**Invalid:** {len(results['invalid'])}\n\n")
    f.write(f"**Pre-canonical files:** {len(results['pre_canonical'])}\n\n")
    f.write(f"**Canonical files:** {len(results['canonical'])}\n\n")
    
    if results["valid"]:
        f.write("## ✅ Valid Files\n\n")
        for name in results["valid"]:
            if name in results["pre_canonical"]:
                status = results["pre_canonical"][name]
                f.write(f"- {name}\n")
                f.write(f"  - Pre-canonical validation: **{status}**\n")
            elif name in results["canonical"]:
                status = results["canonical"][name]
                f.write(f"- {name}\n")
                f.write(f"  - Canonical validation: **{status}**\n")
        f.write("\n")
    
    if results["invalid"]:
        f.write("## ❌ Invalid Files\n\n")
        for name in results["invalid"]:
            f.write(f"### {name}\n\n")
            if name in results["errors"]:
                for error in results["errors"][name]:
                    f.write(f"{error}\n")
            f.write("\n")

print("\nDetailed results saved to SCHEMA-VALIDATION-RESULTS.md")
