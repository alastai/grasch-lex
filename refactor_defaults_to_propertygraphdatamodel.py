#!/usr/bin/env python3
"""
Refactor script to:
1. Rename 'defaults' to 'propertyGraphDataModel' 
2. Move 'valueTypeSystemName' from graphSchema level into propertyGraphDataModel
"""

import yaml
import json
from pathlib import Path
import re

def update_yaml_file(file_path):
    """Update a YAML file with the refactoring changes"""
    print(f"\nProcessing: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # Check if file has graphSchema
    if 'graphSchema:' not in content:
        print("  ⊘ No graphSchema found, skipping")
        return False
    
    # Step 1: Rename 'defaults:' to 'propertyGraphDataModel:'
    if re.search(r'^\s*defaults:', content, re.MULTILINE):
        content = re.sub(r'^(\s*)defaults:', r'\1propertyGraphDataModel:', content, flags=re.MULTILINE)
        changes_made.append("Renamed 'defaults:' to 'propertyGraphDataModel:'")
    
    # Step 2: Move valueTypeSystemName from graphSchema level into propertyGraphDataModel
    # Pattern: Find valueTypeSystemName at graphSchema level (before graphType)
    pattern = r'(graphSchema:\s*\n(?:\s*#[^\n]*\n)*\s*pathName:[^\n]*\n)(\s*valueTypeSystemName:\s*[^\n]*\n)(\s*(?:#[^\n]*\n)*\s*graphType:)'
    
    match = re.search(pattern, content)
    if match:
        # Extract the valueTypeSystemName line
        value_type_line = match.group(2).strip()
        
        # Remove it from graphSchema level
        content = content.replace(match.group(0), match.group(1) + match.group(3))
        
        # Now find propertyGraphDataModel and add valueTypeSystemName as first property
        # Pattern: propertyGraphDataModel: followed by either import or inline properties
        
        # Case 1: propertyGraphDataModel with import
        import_pattern = r'(propertyGraphDataModel:\s*\n)(\s*)(import:)'
        if re.search(import_pattern, content):
            # Add valueTypeSystemName before import (it will be in the imported file)
            # Actually, if there's an import, the imported file should have it
            # So we don't add it here - the import file will be updated separately
            changes_made.append(f"Removed valueTypeSystemName from graphSchema level (will be in import)")
        else:
            # Case 2: propertyGraphDataModel with inline properties
            inline_pattern = r'(propertyGraphDataModel:\s*\n)(\s+)([a-zA-Z])'
            inline_match = re.search(inline_pattern, content)
            if inline_match:
                indent = inline_match.group(2)
                # Add valueTypeSystemName as first property
                insertion = f"{inline_match.group(1)}{indent}{value_type_line}\n{indent}"
                content = content.replace(inline_match.group(0), insertion + inline_match.group(3))
                changes_made.append(f"Moved valueTypeSystemName into propertyGraphDataModel")
    
    if changes_made:
        with open(file_path, 'w') as f:
            f.write(content)
        for change in changes_made:
            print(f"  ✓ {change}")
        return True
    else:
        print("  ⊘ No changes needed")
        return False

def update_json_schema(file_path):
    """Update JSON schema file"""
    print(f"\nProcessing JSON Schema: {file_path}")
    
    with open(file_path, 'r') as f:
        schema = json.load(f)
    
    changes_made = []
    
    # Find and update GraphType definition
    if 'GraphType' in schema.get('$defs', {}):
        graph_type = schema['$defs']['GraphType']
        
        # Rename 'defaults' to 'propertyGraphDataModel' in required array
        if 'required' in graph_type and 'defaults' in graph_type['required']:
            graph_type['required'] = ['propertyGraphDataModel' if x == 'defaults' else x 
                                      for x in graph_type['required']]
            changes_made.append("Updated required array")
        
        # Rename in properties
        if 'properties' in graph_type and 'defaults' in graph_type['properties']:
            graph_type['properties']['propertyGraphDataModel'] = graph_type['properties'].pop('defaults')
            changes_made.append("Renamed 'defaults' to 'propertyGraphDataModel' in properties")
        
        # Update description
        if 'propertyGraphDataModel' in graph_type.get('properties', {}):
            prop = graph_type['properties']['propertyGraphDataModel']
            if 'oneOf' in prop:
                for option in prop['oneOf']:
                    if 'description' in option and 'defaults' in option['description']:
                        option['description'] = option['description'].replace('defaults', 'property graph data model')
                        changes_made.append("Updated description")
    
    # Move valueTypeSystemName from GraphSchemaContent to propertyGraphDataModel
    if 'GraphSchemaContent' in schema.get('$defs', {}):
        graph_schema = schema['$defs']['GraphSchemaContent']
        
        # Remove valueTypeSystemName from GraphSchemaContent properties
        if 'properties' in graph_schema and 'valueTypeSystemName' in graph_schema['properties']:
            value_type_def = graph_schema['properties'].pop('valueTypeSystemName')
            changes_made.append("Removed valueTypeSystemName from GraphSchemaContent")
            
            # Add it to propertyGraphDataModel definition
            # Find the inline propertyGraphDataModel definition and add valueTypeSystemName
            if 'GraphType' in schema.get('$defs', {}):
                graph_type = schema['$defs']['GraphType']
                if 'properties' in graph_type and 'propertyGraphDataModel' in graph_type['properties']:
                    pgdm = graph_type['properties']['propertyGraphDataModel']
                    if 'oneOf' in pgdm:
                        for option in pgdm['oneOf']:
                            if 'properties' in option and 'graphPreferredName' in option.get('properties', {}):
                                # Add valueTypeSystemName as first property
                                option['properties'] = {'valueTypeSystemName': value_type_def, **option['properties']}
                                changes_made.append("Added valueTypeSystemName to propertyGraphDataModel")
    
    if changes_made:
        with open(file_path, 'w') as f:
            json.dump(schema, f, indent=2)
        for change in changes_made:
            print(f"  ✓ {change}")
        return True
    else:
        print("  ⊘ No changes needed")
        return False

def main():
    print("=" * 60)
    print("Refactoring: defaults → propertyGraphDataModel")
    print("=" * 60)
    
    # Update YAML example files
    print("\n### YAML Example Files ###")
    yaml_files = list(Path('src/grasch/examples').glob('*.yaml'))
    yaml_updated = 0
    for yaml_file in sorted(yaml_files):
        if update_yaml_file(yaml_file):
            yaml_updated += 1
    
    # Update import files
    print("\n### Import Files ###")
    import_files = list(Path('src/grasch/examples/imports').glob('**/*.yaml'))
    for import_file in sorted(import_files):
        if update_yaml_file(import_file):
            yaml_updated += 1
    
    # Update JSON schemas
    print("\n### JSON Schema Files ###")
    schema_files = [
        Path('src/grasch/schemas/lex-2026.0.3.2.schema.json'),
        Path('src/grasch/schemas/lex-2026.0.3.2-pre-import.schema.json'),
    ]
    schema_updated = 0
    for schema_file in schema_files:
        if schema_file.exists():
            if update_json_schema(schema_file):
                schema_updated += 1
    
    print("\n" + "=" * 60)
    print(f"Summary: {yaml_updated} YAML files updated, {schema_updated} schema files updated")
    print("=" * 60)

if __name__ == '__main__':
    main()
