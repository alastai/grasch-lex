#!/usr/bin/env python3
"""
Regression test script to validate all existing YAML examples against the updated LEX-2026.0.3.2 schema.
This helps identify what needs to be fixed in the examples after schema changes.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    print("ERROR: jsonschema not available. Install with: pip install jsonschema")
    JSONSCHEMA_AVAILABLE = False
    exit(1)


def load_schema() -> dict:
    """Load the LEX-2026.0.3.2 JSON Schema."""
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_yaml_files() -> List[Path]:
    """Find all YAML example files."""
    examples_dir = Path("src/grasch/examples")
    yaml_files = list(examples_dir.glob("lex-2026.0.3.2-*.yaml"))
    return sorted(yaml_files)


def validate_file(file_path: Path, schema: dict, validator: Draft202012Validator) -> Tuple[bool, List[str]]:
    """
    Validate a single YAML file against the schema.
    
    Returns:
        (is_valid, error_messages)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, [f"YAML parsing error: {e}"]
    except Exception as e:
        return False, [f"File reading error: {e}"]
    
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
        return False, error_messages
    
    return True, []


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
    
    # Validate each file
    results = []
    for yaml_file in yaml_files:
        print(f"Validating: {yaml_file.name}")
        is_valid, errors = validate_file(yaml_file, schema, validator)
        results.append((yaml_file, is_valid, errors))
        
        if is_valid:
            print(f"  ✓ VALID")
        else:
            print(f"  ✗ INVALID ({len(errors)} errors)")
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
