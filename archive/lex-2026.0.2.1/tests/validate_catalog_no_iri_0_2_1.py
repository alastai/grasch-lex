#!/usr/bin/env python3
"""
Validation script for LEX:2026.0.2.1 Catalog Example without IRI
Validates the example catalog without IRI against the LEX:2026.0.2.1 JSON Schema for LEX specifications
"""

import json
import yaml
import jsonschema
from pathlib import Path
import sys

# Import the analysis function from the main validation script
from validate_catalog_example_0_2_1 import load_json_schema, load_yaml_schema, validate_schema, analyze_catalog_structure

def main():
    """Main validation function"""
    print("LEX:2026.0.2.1 Catalog Example (No IRI) Validation")
    print("=" * 60)
    
    # File paths (work from both workspace root and tests directory)
    json_schema_path = "src/grasch/schemas/lex-2026.0.2.1.schema.json"
    if not Path(json_schema_path).exists():
        json_schema_path = "../src/grasch/schemas/lex-2026.0.2.1.schema.json"
    
    yaml_schema_path = "src/grasch/examples/example-catalog-no-iri-lex-2026.0.2.1.yaml"
    if not Path(yaml_schema_path).exists():
        yaml_schema_path = "../src/grasch/examples/example-catalog-no-iri-lex-2026.0.2.1.yaml"
    
    # Check if files exist
    if not Path(json_schema_path).exists():
        print(f"❌ JSON Schema file not found: {json_schema_path}")
        sys.exit(1)
    
    if not Path(yaml_schema_path).exists():
        print(f"❌ YAML Catalog file not found: {yaml_schema_path}")
        sys.exit(1)
    
    # Load schemas
    print(f"📖 Loading JSON Schema: {json_schema_path}")
    json_schema = load_json_schema(json_schema_path)
    
    print(f"📖 Loading YAML Catalog: {yaml_schema_path}")
    yaml_data = load_yaml_schema(yaml_schema_path)
    
    # Validate
    print("\n🔍 Validating catalog...")
    is_valid, errors = validate_schema(yaml_data, json_schema)
    
    if is_valid:
        print("✅ Catalog validation PASSED")
    else:
        print("❌ Catalog validation FAILED")
        print("\nValidation errors:")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)
    
    # Analyze structure
    print("\n📊 Catalog Analysis:")
    analysis = analyze_catalog_structure(yaml_data)
    
    print(f"  Has IRI: {analysis['has_iri']}")
    if analysis['has_iri']:
        print(f"  IRI: {analysis['iri_value']}")
    else:
        print("  IRI: None (LQON-only addressing)")
    print(f"  Total Directories: {analysis['total_directories']}")
    print(f"  Total Graph Schemas: {analysis['total_graph_schemas']}")
    print(f"  Total Graphs: {analysis['total_graphs']}")
    
    print("\n🗂️  Directory Structure:")
    for path, contents in analysis['directory_tree'].items():
        print(f"    {path}/")
        if contents['schemas']:
            print(f"      📋 Schemas: {', '.join(contents['schemas'])}")
        if contents['graphs']:
            print(f"      📊 Graphs: {', '.join(contents['graphs'])}")
    
    # Display Graph Schemas with LQONs and GQONs
    print(f"\n📋 Graph Schemas ({len(analysis['graph_schemas'])} total):")
    if analysis['graph_schemas']:
        for schema in analysis['graph_schemas']:
            print(f"    • {schema['name']}")
            print(f"      LQON: {schema['lqon']}")
            print(f"      GQON: {schema['gqon']}")
    else:
        print("    (No graph schemas found)")
    
    # Display Graphs with LQONs and GQONs
    print(f"\n📊 Graph Instances ({len(analysis['graphs'])} total):")
    if analysis['graphs']:
        for graph in analysis['graphs']:
            print(f"    • {graph['name']}")
            print(f"      LQON: {graph['lqon']}")
            print(f"      GQON: {graph['gqon']}")
    else:
        print("    (No graph instances found)")
    
    print(f"\n🎉 Catalog LEX:2026.0.2.1 validation completed successfully!")
    print(f"   Catalog contains {analysis['total_directories']} directories")
    print(f"   with {analysis['total_graph_schemas']} graph schemas and {analysis['total_graphs']} graph instances")
    print("   Note: Only LQON addressing available (no catalog IRI specified)")

if __name__ == "__main__":
    main()
