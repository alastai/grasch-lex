#!/usr/bin/env python3
"""
Fix Location 3 Test Files - Update Edge Labels to New Format

Updates test-phase-e-location-3*.yaml files to use the new edge label format
where edge labels are ALWAYS objects with typeLabel: as required child.

Old format:
  via:
    implies:
      propertyTypes: [...]

New format:
  via:
    typeLabel: KNOWS
    implies:
      propertyTypes: [...]
"""

import yaml
from pathlib import Path

def fix_edge_label(edge_type_dict):
    """Fix edge label in an edgeType to use object format with typeLabel child"""
    
    # Get the typeLabel from the edgeType level
    type_label = edge_type_dict.get('typeLabel')
    if not type_label:
        print("  ⚠️  No typeLabel found at edgeType level")
        return edge_type_dict
    
    # Check if this is a directed edge
    if 'directed' in edge_type_dict:
        directed = edge_type_dict['directed']
        
        # Fix 'via' if it exists
        if 'via' in directed:
            via = directed['via']
            
            # Check if via is already in correct format (has typeLabel child)
            if isinstance(via, dict) and 'typeLabel' not in via:
                # Old format - via has implies/extends/adding directly
                # New format - via should have typeLabel child, with implies/extends/adding as siblings
                new_via = {'typeLabel': type_label}
                
                # Move implies, extends, adding to be siblings of typeLabel
                if 'implies' in via:
                    new_via['implies'] = via['implies']
                if 'extends' in via:
                    new_via['extends'] = via['extends']
                if 'adding' in via:
                    new_via['adding'] = via['adding']
                
                directed['via'] = new_via
                print(f"  ✅ Fixed 'via' for {type_label}")
        
        # Fix 'arc' if it exists (same pattern)
        if 'arc' in directed:
            arc = directed['arc']
            
            if isinstance(arc, dict) and 'typeLabel' not in arc:
                new_arc = {'typeLabel': type_label}
                
                if 'implies' in arc:
                    new_arc['implies'] = arc['implies']
                if 'extends' in arc:
                    new_arc['extends'] = arc['extends']
                if 'adding' in arc:
                    new_arc['adding'] = arc['adding']
                
                directed['arc'] = new_arc
                print(f"  ✅ Fixed 'arc' for {type_label}")
    
    # Check if this is an undirected edge
    if 'undirected' in edge_type_dict:
        undirected = edge_type_dict['undirected']
        
        # Fix 'via' if it exists
        if 'via' in undirected:
            via = undirected['via']
            
            if isinstance(via, dict) and 'typeLabel' not in via:
                new_via = {'typeLabel': type_label}
                
                if 'implies' in via:
                    new_via['implies'] = via['implies']
                if 'extends' in via:
                    new_via['extends'] = via['extends']
                if 'adding' in via:
                    new_via['adding'] = via['adding']
                
                undirected['via'] = new_via
                print(f"  ✅ Fixed 'via' for {type_label}")
    
    return edge_type_dict

def process_edge_types_array(edge_types):
    """Process an array of edge types"""
    if not isinstance(edge_types, list):
        return edge_types
    
    for item in edge_types:
        if isinstance(item, dict) and 'edgeType' in item:
            fix_edge_label(item['edgeType'])
    
    return edge_types

def fix_yaml_file(filepath):
    """Fix a single YAML file"""
    print(f"\n{'='*70}")
    print(f"Processing: {filepath}")
    print(f"{'='*70}")
    
    # Load YAML
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    
    # Navigate to graphType
    if 'graphSchema' not in data:
        print("❌ No graphSchema found")
        return False
    
    graph_schema = data['graphSchema']
    if 'graphType' not in graph_schema:
        print("❌ No graphType found")
        return False
    
    graph_type = graph_schema['graphType']
    
    # Process edgeTypes at different locations
    changes_made = False
    
    # Check bare edgeTypes
    if 'edgeTypes' in graph_type:
        print("\n📝 Processing bare edgeTypes...")
        process_edge_types_array(graph_type['edgeTypes'])
        changes_made = True
    
    # Check concrete.edgeTypes (1-level wrapper)
    if 'concrete' in graph_type and isinstance(graph_type['concrete'], dict):
        if 'edgeTypes' in graph_type['concrete']:
            print("\n📝 Processing concrete.edgeTypes...")
            process_edge_types_array(graph_type['concrete']['edgeTypes'])
            changes_made = True
    
    # Check exactlyOf.concrete.edgeTypes (2-level wrapper)
    if 'exactlyOf' in graph_type and isinstance(graph_type['exactlyOf'], dict):
        if 'concrete' in graph_type['exactlyOf'] and isinstance(graph_type['exactlyOf']['concrete'], dict):
            if 'edgeTypes' in graph_type['exactlyOf']['concrete']:
                print("\n📝 Processing exactlyOf.concrete.edgeTypes...")
                process_edge_types_array(graph_type['exactlyOf']['concrete']['edgeTypes'])
                changes_made = True
    
    # Check other TI wrapper combinations
    for interp_facet in ['subtypesOf', 'properSubtypesOf']:
        if interp_facet in graph_type and isinstance(graph_type[interp_facet], dict):
            for concrete_facet in ['concrete', 'abstract']:
                if concrete_facet in graph_type[interp_facet] and isinstance(graph_type[interp_facet][concrete_facet], dict):
                    if 'edgeTypes' in graph_type[interp_facet][concrete_facet]:
                        print(f"\n📝 Processing {interp_facet}.{concrete_facet}.edgeTypes...")
                        process_edge_types_array(graph_type[interp_facet][concrete_facet]['edgeTypes'])
                        changes_made = True
    
    if not changes_made:
        print("\n⚠️  No edgeTypes found to process")
        return False
    
    # Save updated YAML
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"\n✅ File updated: {filepath}")
    return True

def main():
    """Main function"""
    print("="*70)
    print("Fix Location 3 Test Files - Edge Label Format Update")
    print("="*70)
    
    files_to_fix = [
        "src/grasch/examples/test-phase-e-location-3.yaml",
        "src/grasch/examples/test-phase-e-location-3-two-level.yaml"
    ]
    
    results = {}
    for filepath in files_to_fix:
        path = Path(filepath)
        if path.exists():
            results[filepath] = fix_yaml_file(filepath)
        else:
            print(f"\n⚠️  File not found: {filepath}")
            results[filepath] = False
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for filepath, success in results.items():
        status = "✅ UPDATED" if success else "❌ FAILED"
        print(f"{status}: {Path(filepath).name}")
    
    print(f"\nTotal: {success_count}/{total_count} files updated")
    
    if success_count == total_count:
        print("\n✅ All files updated successfully!")
        print("\nNext step: Run validate_phase_e_locations_2_3.py to verify")
        return 0
    else:
        print("\n❌ Some files failed to update")
        return 1

if __name__ == "__main__":
    exit(main())
