#!/usr/bin/env python3
"""
Comprehensive PC → C Validation Pipeline for LEX-2026.0.3.2

This script validates ALL example files through the complete pipeline:
1. Validate PC (pre-canonical) form against JSON Schema
2. Canonicalize PC → C using canonicalizing preprocessor
3. Write C form to disk with CANON_ prefix
4. Validate C (canonical) form against JSON Schema
5. Report line/column locations for all validation errors
6. Identify which files are true no-ops vs actual transformations

Terminology:
- PC (Pre-Canonical): All documents start in this form (may or may not have imports)
- C (Canonical): Normalized form after canonicalization (imports resolved, wrappers normalized)
- "Importing file": A file that contains import directives
- "No-imports file": A file without import directives (but still in PC form)
- JS Validation: JSON Schema validation (structural validation only)
"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError
from typing import Dict, List, Any, Tuple
import sys

# Import the canonicalizing preprocessor
sys.path.insert(0, str(Path(__file__).parent / "src"))
from grasch.canonicalizing_preprocessor import preprocess_yaml_with_imports

# Load the JSON Schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Example files to validate
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
    "pc_valid": [],
    "pc_invalid": [],
    "c_valid": [],
    "c_invalid": [],
    "pc_errors": {},
    "c_errors": {},
    "importing_files": [],
    "no_imports_files": [],
    "transformation_noop": [],
    "transformation_changed": [],
}


def has_imports(data: Any) -> bool:
    """Check if data contains import directives (importing file indicator)."""
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


def format_validation_error(error: ValidationError, yaml_content: str) -> str:
    """
    Format validation error with line/column information.
    
    Note: jsonschema doesn't provide line numbers directly, so we provide
    the JSON path and a snippet of the problematic content.
    """
    path = ".".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
    
    # Try to find approximate line number by searching for the path in YAML
    lines = yaml_content.split('\n')
    line_num = None
    
    # Search for the last component of the path
    if error.absolute_path:
        search_key = str(error.absolute_path[-1])
        for i, line in enumerate(lines, 1):
            if search_key in line:
                line_num = i
                break
    
    location = f"line ~{line_num}" if line_num else "unknown line"
    
    return f"  Path: {path} ({location})\n  Error: {error.message}"


def data_equal(data1: Any, data2: Any) -> bool:
    """Deep equality check for YAML data structures."""
    return data1 == data2


print("="*80)
print("LEX-2026.0.3.2 PC → C VALIDATION PIPELINE")
print("="*80)
print()

for file_path in example_files:
    path = Path(file_path)
    if not path.exists():
        print(f"⚠️  SKIP: {path.name} (file not found)")
        continue
    
    print(f"\n{'─'*80}")
    print(f"Processing: {path.name}")
    print(f"{'─'*80}")
    
    try:
        # Read PC form
        with open(path, 'r') as f:
            pc_yaml_content = f.read()
            pc_data = yaml.safe_load(pc_yaml_content)
        
        # Determine if this is an importing file
        is_importing = has_imports(pc_data)
        file_type = "importing file" if is_importing else "no-imports file"
        
        if is_importing:
            results["importing_files"].append(path.name)
        else:
            results["no_imports_files"].append(path.name)
        
        print(f"File type: {file_type}")
        
        # Step 1: JS Validation of PC form
        print(f"\n1️⃣  JS Validation of PC form...")
        pc_errors = list(validator.iter_errors(pc_data))
        
        if pc_errors:
            results["pc_invalid"].append(path.name)
            results["pc_errors"][path.name] = []
            print(f"   ❌ PC form INVALID")
            
            for error in pc_errors:
                error_msg = format_validation_error(error, pc_yaml_content)
                print(error_msg)
                results["pc_errors"][path.name].append(error_msg)
        else:
            results["pc_valid"].append(path.name)
            print(f"   ✅ PC form VALID")
        
        # Step 2: Canonicalization PC → C
        print(f"\n2️⃣  Canonicalizing PC → C...")
        try:
            c_data = preprocess_yaml_with_imports(path, canonicalize_wrappers=True)
            print(f"   ✅ Canonicalization successful")
            
            # Check if transformation was a no-op
            if data_equal(pc_data, c_data):
                results["transformation_noop"].append(path.name)
                print(f"   ℹ️  Transformation is NO-OP (PC == C)")
            else:
                results["transformation_changed"].append(path.name)
                print(f"   ℹ️  Transformation CHANGED data (PC ≠ C)")
            
        except Exception as e:
            print(f"   ❌ Canonicalization FAILED: {e}")
            results["c_invalid"].append(path.name)
            results["c_errors"][path.name] = [f"Canonicalization error: {e}"]
            continue
        
        # Step 3: Write C form to disk (in examples directory, overwrite if exists)
        print(f"\n3️⃣  Writing C form to disk...")
        c_path = path.parent / f"CANON_{path.name}"
        try:
            with open(c_path, 'w') as f:
                # Add header comment explaining this is a canonical form
                f.write("# CANONICAL FORM - AUTO-GENERATED\n")
                f.write("# This file is automatically generated from the PC (pre-canonical) form.\n")
                f.write("# DO NOT EDIT MANUALLY - Changes will be overwritten.\n")
                f.write(f"# Source: {path.name}\n")
                f.write("# Generated by: validate_pc_and_c_forms.py\n")
                f.write("#\n")
                f.write("# Transformations applied:\n")
                f.write("# - Import directives resolved and merged\n")
                f.write("# - Type interpretation wrappers canonicalized\n")
                f.write("# - Structure normalized to canonical form\n\n")
                yaml.dump(c_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"   ✅ Written to: {c_path}")
            print(f"   ℹ️  Canonical form persisted in examples directory")
        except Exception as e:
            print(f"   ❌ Failed to write C form: {e}")
        
        # Step 4: JS Validation of C form
        print(f"\n4️⃣  JS Validation of C form...")
        c_yaml_content = yaml.dump(c_data, default_flow_style=False, sort_keys=False)
        c_errors = list(validator.iter_errors(c_data))
        
        if c_errors:
            results["c_invalid"].append(path.name)
            results["c_errors"][path.name] = []
            print(f"   ❌ C form INVALID")
            
            for error in c_errors:
                error_msg = format_validation_error(error, c_yaml_content)
                print(error_msg)
                results["c_errors"][path.name].append(error_msg)
        else:
            results["c_valid"].append(path.name)
            print(f"   ✅ C form VALID")
        
        print(f"\n✓ Completed: {path.name}")
    
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        results["pc_invalid"].append(path.name)
        results["pc_errors"][path.name] = [f"YAML parsing error: {e}"]
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        results["pc_invalid"].append(path.name)
        results["pc_errors"][path.name] = [f"Unexpected error: {e}"]

# Summary Report
print("\n" + "="*80)
print("VALIDATION SUMMARY")
print("="*80)
print(f"\nTotal files processed: {len(example_files)}")
print(f"\nFile Classification:")
print(f"  - Importing files: {len(results['importing_files'])}")
print(f"  - No-imports files: {len(results['no_imports_files'])}")
print(f"\nPC Form JS Validation:")
print(f"  - Valid: {len(results['pc_valid'])}")
print(f"  - Invalid: {len(results['pc_invalid'])}")
print(f"\nC Form JS Validation:")
print(f"  - Valid: {len(results['c_valid'])}")
print(f"  - Invalid: {len(results['c_invalid'])}")
print(f"\nCanonicalization Analysis:")
print(f"  - No-op transformations (PC == C): {len(results['transformation_noop'])}")
print(f"  - Changed transformations (PC ≠ C): {len(results['transformation_changed'])}")

if results["pc_invalid"]:
    print(f"\n❌ PC Form Validation Failures:")
    for name in results["pc_invalid"]:
        print(f"  - {name}")

if results["c_invalid"]:
    print(f"\n❌ C Form Validation Failures:")
    for name in results["c_invalid"]:
        print(f"  - {name}")

if results["transformation_noop"]:
    print(f"\nℹ️  No-op Transformations (PC == C):")
    for name in results["transformation_noop"]:
        print(f"  - {name}")

# Save detailed results
with open("PC-C-VALIDATION-RESULTS.md", "w") as f:
    f.write("# LEX-2026.0.3.2 PC → C Validation Pipeline Results\n\n")
    f.write("## Overview\n\n")
    f.write("This validation tests the complete PC → C transformation pipeline:\n\n")
    f.write("1. **JS Validation of PC form**: Validate pre-canonical against JSON Schema\n")
    f.write("2. **Canonicalization**: Transform PC → C (resolve imports, normalize wrappers)\n")
    f.write("3. **Write C form**: Save canonical form with CANON_ prefix\n")
    f.write("4. **JS Validation of C form**: Validate canonical against JSON Schema\n\n")
    
    f.write("### Terminology\n\n")
    f.write("- **PC (Pre-Canonical)**: All documents start in this form\n")
    f.write("- **C (Canonical)**: Normalized form after canonicalization\n")
    f.write("- **Importing file**: Contains import directives\n")
    f.write("- **No-imports file**: No import directives (but still in PC form)\n")
    f.write("- **JS Validation**: JSON Schema validation (structural validation)\n\n")
    
    f.write("## Summary Statistics\n\n")
    f.write(f"**Total files processed:** {len(example_files)}\n\n")
    f.write(f"**File Classification:**\n")
    f.write(f"- Importing files: {len(results['importing_files'])}\n")
    f.write(f"- No-imports files: {len(results['no_imports_files'])}\n\n")
    f.write(f"**PC Form JS Validation:**\n")
    f.write(f"- Valid: {len(results['pc_valid'])}\n")
    f.write(f"- Invalid: {len(results['pc_invalid'])}\n\n")
    f.write(f"**C Form JS Validation:**\n")
    f.write(f"- Valid: {len(results['c_valid'])}\n")
    f.write(f"- Invalid: {len(results['c_invalid'])}\n\n")
    f.write(f"**Canonicalization Analysis:**\n")
    f.write(f"- No-op transformations (PC == C): {len(results['transformation_noop'])}\n")
    f.write(f"- Changed transformations (PC ≠ C): {len(results['transformation_changed'])}\n\n")
    
    if results["importing_files"]:
        f.write("## Importing Files\n\n")
        for name in results["importing_files"]:
            f.write(f"- {name}\n")
        f.write("\n")
    
    if results["no_imports_files"]:
        f.write("## No-Imports Files\n\n")
        for name in results["no_imports_files"]:
            f.write(f"- {name}\n")
        f.write("\n")
    
    if results["transformation_noop"]:
        f.write("## No-op Transformations (PC == C)\n\n")
        f.write("These files are unchanged by canonicalization:\n\n")
        for name in results["transformation_noop"]:
            f.write(f"- {name}\n")
        f.write("\n")
    
    if results["transformation_changed"]:
        f.write("## Changed Transformations (PC ≠ C)\n\n")
        f.write("These files are modified by canonicalization:\n\n")
        for name in results["transformation_changed"]:
            f.write(f"- {name}\n")
        f.write("\n")
    
    if results["pc_valid"]:
        f.write("## ✅ PC Form Valid Files\n\n")
        for name in results["pc_valid"]:
            f.write(f"- {name}\n")
        f.write("\n")
    
    if results["pc_invalid"]:
        f.write("## ❌ PC Form Invalid Files\n\n")
        for name in results["pc_invalid"]:
            f.write(f"### {name}\n\n")
            if name in results["pc_errors"]:
                for error in results["pc_errors"][name]:
                    f.write(f"{error}\n\n")
        f.write("\n")
    
    if results["c_valid"]:
        f.write("## ✅ C Form Valid Files\n\n")
        for name in results["c_valid"]:
            f.write(f"- {name}\n")
        f.write("\n")
    
    if results["c_invalid"]:
        f.write("## ❌ C Form Invalid Files\n\n")
        for name in results["c_invalid"]:
            f.write(f"### {name}\n\n")
            if name in results["c_errors"]:
                for error in results["c_errors"][name]:
                    f.write(f"{error}\n\n")
        f.write("\n")

print("\n✅ Detailed results saved to PC-C-VALIDATION-RESULTS.md")
print(f"✅ Canonical forms written to src/grasch/examples/CANON_*.yaml")
