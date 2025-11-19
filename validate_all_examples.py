#!/usr/bin/env python3
"""
Regression test script to validate all existing YAML examples against the updated LEX-2026.0.3.2 schema.
This script:
1. Validates raw YAML files (with imports) against the pre-import schema
2. Preprocesses imports to resolve all import: directives
3. Validates preprocessed files against the post-import schema (no imports allowed)
"""

import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    print("ERROR: jsonschema not available. Install with: pip install jsonschema")
    JSONSCHEMA_AVAILABLE = False
    exit(1)

try:
    from grasch.import_preprocessor import preprocess_yaml_with_imports
    PREPROCESSOR_AVAILABLE = True
except ImportError:
    print("WARNING: Import preprocessor not available. Will only validate raw files.")
    PREPROCESSOR_AVAILABLE = False


def load_schema() -> dict:
    """Load the LEX-2026.0.3.2 JSON Schema."""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_yaml_files() -> List[Path]:
    """Find all top-level YAML example files (excluding imports directory)."""
    examples_dir = Path("src/grasch/examples")
    yaml_files = list(examples_dir.glob("lex-2026.0.3.2-*.yaml"))
    # Exclude files in the imports subdirectory
    yaml_files = [f for f in yaml_files if 'imports' not in f.parts]
    return sorted(yaml_files)


def validate_file(file_path: Path, schema: dict, validator: Draft202012Validator, preprocess: bool = False) -> Tuple[bool, List[str], any]:
    """
    Validate a single YAML file against the schema.
    
    Args:
        file_path: Path to the YAML file
        schema: JSON Schema to validate against
        validator: JSON Schema validator
        preprocess: If True, preprocess imports before validation
    
    Returns:
        (is_valid, error_messages, data)
    """
    try:
        if preprocess and PREPROCESSOR_AVAILABLE:
            # Preprocess to resolve imports
            data = preprocess_yaml_with_imports(file_path)
        else:
            # Load raw YAML
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, [f"YAML parsing error: {e}"], None
    except Exception as e:
        return False, [f"File reading/preprocessing error: {e}"], None
    
    errors = list(validator.iter_errors(data))
    if errors:
        error_messages = []
        for error in errors:
            path = '.'.join(str(p) for p in error.absolute_path) if error.absolute_path else 'root'
            error_messages.append(f"  Path: {path}")
            error_messages.append(f"  Error: {error.message}")
            if error.validator:
                error_messages.append(f"  Validator: {error.validator}")
            error_messages.append("")
        return False, error_messages, data
    
    return True, [], data


def main():
    """Run validation on all example files."""
    print("=" * 80)
    print("LEX-2026.0.3.2 Schema Regression Test")
    print("=" * 80)
    print()
    
    # Load schema
    print("Loading schema...")
    try:
        schema = load_schema()
        validator = Draft202012Validator(schema)
        print(f"✓ Schema loaded: {schema.get('title', 'Unknown')}")
        print()
    except Exception as e:
        print(f"✗ Failed to load schema: {e}")
        return 1
    
    # Find YAML files
    yaml_files = find_yaml_files()
    print(f"Found {len(yaml_files)} YAML example files")
    print()
    
    # Validate each file (both raw and preprocessed)
    results = []
    for yaml_file in yaml_files:
        print(f"Validating: {yaml_file.name}")
        
        # Step 1: Validate raw file (with imports)
        print(f"  [1/2] Raw validation (with imports)...")
        is_valid_raw, errors_raw, data_raw = validate_file(yaml_file, schema, validator, preprocess=False)
        
        if is_valid_raw:
            print(f"      ✓ Raw file valid")
        else:
            print(f"      ✗ Raw file invalid ({len(errors_raw)} errors)")
        
        # Step 2: Validate preprocessed file (imports resolved)
        if PREPROCESSOR_AVAILABLE:
            print(f"  [2/2] Preprocessed validation (imports resolved)...")
            is_valid_preprocessed, errors_preprocessed, data_preprocessed = validate_file(yaml_file, schema, validator, preprocess=True)
            
            if is_valid_preprocessed:
                print(f"      ✓ Preprocessed file valid")
            else:
                print(f"      ✗ Preprocessed file invalid ({len(errors_preprocessed)} errors)")
            
            # Overall result: both must pass
            is_valid = is_valid_raw and is_valid_preprocessed
            errors = errors_raw + errors_preprocessed if not is_valid else []
        else:
            is_valid = is_valid_raw
            errors = errors_raw
        
        results.append((yaml_file, is_valid, errors))
        
        if is_valid:
            print(f"  ✓ OVERALL: VALID")
        else:
            print(f"  ✗ OVERALL: INVALID")
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    
    print(f"Total files: {len(results)}")
    print(f"Valid: {valid_count}")
    print(f"Invalid: {invalid_count}")
    print()
    
    if invalid_count > 0:
        print("=" * 80)
        print("DETAILED ERRORS")
        print("=" * 80)
        print()
        
        for yaml_file, is_valid, errors in results:
            if not is_valid:
                print(f"File: {yaml_file.name}")
                print("-" * 80)
                for error_line in errors:
                    print(error_line)
                print()
    
    # Categorize files by expected document type
    print("=" * 80)
    print("FILE CATEGORIZATION (by name pattern)")
    print("=" * 80)
    print()
    
    graph_schemas = [f for f in yaml_files if 'schema' in f.name.lower() and 'catalog' not in f.name.lower()]
    graphs = [f for f in yaml_files if 'graph' in f.name.lower() and 'schema' not in f.name.lower() and 'catalog' not in f.name.lower()]
    catalogs = [f for f in yaml_files if 'catalog' in f.name.lower()]
    other = [f for f in yaml_files if f not in graph_schemas and f not in graphs and f not in catalogs]
    
    print(f"GraphSchema documents ({len(graph_schemas)}):")
    for f in graph_schemas:
        status = "✓" if any(r[0] == f and r[1] for r in results) else "✗"
        print(f"  {status} {f.name}")
    print()
    
    print(f"Graph documents ({len(graphs)}):")
    for f in graphs:
        status = "✓" if any(r[0] == f and r[1] for r in results) else "✗"
        print(f"  {status} {f.name}")
    print()
    
    print(f"Catalog documents ({len(catalogs)}):")
    for f in catalogs:
        status = "✓" if any(r[0] == f and r[1] for r in results) else "✗"
        print(f"  {status} {f.name}")
    print()
    
    if other:
        print(f"Other/Fragment files ({len(other)}):")
        for f in other:
            status = "✓" if any(r[0] == f and r[1] for r in results) else "✗"
            print(f"  {status} {f.name}")
        print()
    
    return 0 if invalid_count == 0 else 1


if __name__ == "__main__":
    exit(main())
