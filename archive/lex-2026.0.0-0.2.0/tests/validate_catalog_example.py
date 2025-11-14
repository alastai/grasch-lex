#!/usr/bin/env python3
"""
Validation script for LEX:2026.0.2 Catalog Example
Validates the example catalog against the LEX:2026.0.2 JSON Schema for LEX specifications
"""

import json
import yaml
import jsonschema
from pathlib import Path
import sys

def load_json_schema(schema_path: str) -> dict:
    """Load and parse JSON Schema file"""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON Schema from {schema_path}: {e}")
        sys.exit(1)

def load_yaml_schema(yaml_path: str) -> dict:
    """Load and parse YAML schema file"""
    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML schema from {yaml_path}: {e}")
        sys.exit(1)

def validate_schema(yaml_data: dict, json_schema: dict) -> tuple[bool, list]:
    """Validate YAML data against JSON Schema"""
    try:
        jsonschema.validate(yaml_data, json_schema)
        return True, []
    except jsonschema.ValidationError as e:
        return False, [str(e)]
    except Exception as e:
        return False, [f"Validation error: {e}"]

def analyze_catalog_structure(yaml_data: dict) -> dict:
    """Analyze the structure of the catalog for reporting"""
    analysis = {
        'has_iri': False,
        'iri_value': None,
        'total_directories': 0,
        'total_graph_schemas': 0,
        'total_graphs': 0,
        'directory_tree': {},
        'graph_schemas': [],  # List of {name, lqon, gqon}
        'graphs': []          # List of {name, lqon, gqon}
    }
    
    catalog = yaml_data.get('catalog', {})
    
    # Check for IRI
    if 'IRI' in catalog:
        analysis['has_iri'] = True
        analysis['iri_value'] = catalog['IRI']
    
    def generate_lqon(path: str, name: str) -> str:
        """Generate LQON for an object"""
        if path:
            return f"/{path}/{name}"
        else:
            return f"/{name}"
    
    def generate_gqon(lqon: str, iri: str = None) -> str:
        """Generate GQON for an object if IRI is available"""
        if iri:
            return f"{iri}|{lqon}"
        else:
            return "N/A (no catalog IRI)"
    
    def collect_objects(directories, path=""):
        """Recursively collect objects and generate LQONs/GQONs"""
        for directory in directories:
            dir_name = directory.get('name', 'unnamed')
            current_path = f"{path}/{dir_name}" if path else dir_name
            
            analysis['total_directories'] += 1
            
            # Process schemas and graphs in this directory
            schemas = directory.get('graphSchemas', [])
            graphs = directory.get('graphs', [])
            
            analysis['total_graph_schemas'] += len(schemas)
            analysis['total_graphs'] += len(graphs)
            
            # Store in tree structure
            analysis['directory_tree'][current_path] = {
                'schemas': [s.get('name', 'unnamed') for s in schemas],
                'graphs': [g.get('name', 'unnamed') for g in graphs]
            }
            
            # Generate LQONs and GQONs for graph schemas
            for schema in schemas:
                schema_name = schema.get('name', 'unnamed')
                lqon = generate_lqon(current_path, schema_name)
                gqon = generate_gqon(lqon, analysis['iri_value'])
                analysis['graph_schemas'].append({
                    'name': schema_name,
                    'lqon': lqon,
                    'gqon': gqon
                })
            
            # Generate LQONs and GQONs for graphs
            for graph in graphs:
                graph_name = graph.get('name', 'unnamed')
                lqon = generate_lqon(current_path, graph_name)
                gqon = generate_gqon(lqon, analysis['iri_value'])
                analysis['graphs'].append({
                    'name': graph_name,
                    'lqon': lqon,
                    'gqon': gqon
                })
            
            # Recurse into subdirectories
            subdirs = directory.get('directories', [])
            if subdirs:
                collect_objects(subdirs, current_path)
    
    # Start collecting from root directories
    root_directories = catalog.get('directories', [])
    if root_directories:
        collect_objects(root_directories)
    
    # Also check for root-level schemas and graphs
    root_schemas = catalog.get('graphSchemas', [])
    root_graphs = catalog.get('graphs', [])
    
    analysis['total_graph_schemas'] += len(root_schemas)
    analysis['total_graphs'] += len(root_graphs)
    
    # Generate LQONs and GQONs for root-level objects
    for schema in root_schemas:
        schema_name = schema.get('name', 'unnamed')
        lqon = f"/{schema_name}"
        gqon = generate_gqon(lqon, analysis['iri_value'])
        analysis['graph_schemas'].append({
            'name': schema_name,
            'lqon': lqon,
            'gqon': gqon
        })
    
    for graph in root_graphs:
        graph_name = graph.get('name', 'unnamed')
        lqon = f"/{graph_name}"
        gqon = generate_gqon(lqon, analysis['iri_value'])
        analysis['graphs'].append({
            'name': graph_name,
            'lqon': lqon,
            'gqon': gqon
        })
    
    return analysis

def main():
    """Main validation function"""
    print("LEX:2026.0.2 Catalog Example Validation")
    print("=" * 50)
    
    # File paths
    json_schema_path = "lex-2026.0.2.schema.json"
    yaml_schema_path = "example-catalog-lex-2026.0.2.yaml"
    
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
    
    print(f"\n🎉 Catalog LEX:2026.0.2 validation completed successfully!")
    print(f"   Catalog contains {analysis['total_directories']} directories")
    print(f"   with {analysis['total_graph_schemas']} graph schemas and {analysis['total_graphs']} graph instances")

if __name__ == "__main__":
    main()