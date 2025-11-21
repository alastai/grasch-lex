#!/usr/bin/env python3
"""
Analyze JSON Schema for Import Pattern Consistency

This script identifies all locations in the schema where imports should be allowed
and checks if they have the proper oneOf pattern:
  oneOf: [
    { actual content schema },
    { import: { type: "string" } }
  ]
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Set

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Properties that should support imports
IMPORTABLE_PROPERTIES = {
    'graphSchema',
    'graphType',
    'propertyGraphDataModel',
    'nodeTypes',
    'edgeTypes',
    'directories',
    'graphStorageSchema',
}

# Properties that are wrappers and should have imports inside them
WRAPPER_KEYWORDS = {
    'abstract', 'concrete', 'final', 'sealed',
    'exactlyOf', 'subtypesOf', 'properSubtypesOf'
}

def analyze_schema_node(node: Any, path: str = "root", issues: List[Dict] = None) -> List[Dict]:
    """
    Recursively analyze schema nodes for import pattern consistency.
    
    Returns list of issues found.
    """
    if issues is None:
        issues = []
    
    if not isinstance(node, dict):
        return issues
    
    # Check if this is a property definition
    if 'properties' in node:
        for prop_name, prop_schema in node['properties'].items():
            prop_path = f"{path}.properties.{prop_name}"
            
            # Check if this is an importable property
            if prop_name in IMPORTABLE_PROPERTIES:
                # Check if it has oneOf with import option
                has_oneof = 'oneOf' in prop_schema
                has_import_option = False
                
                if has_oneof:
                    for option in prop_schema['oneOf']:
                        if isinstance(option, dict):
                            # Check if this option is an import
                            if 'required' in option and 'import' in option['required']:
                                has_import_option = True
                                break
                            # Check if properties has import
                            if 'properties' in option and 'import' in option['properties']:
                                has_import_option = True
                                break
                
                if not has_oneof:
                    issues.append({
                        'path': prop_path,
                        'property': prop_name,
                        'issue': 'Missing oneOf for importable property',
                        'severity': 'HIGH'
                    })
                elif not has_import_option:
                    issues.append({
                        'path': prop_path,
                        'property': prop_name,
                        'issue': 'Has oneOf but missing import option',
                        'severity': 'HIGH'
                    })
            
            # Recursively analyze
            analyze_schema_node(prop_schema, prop_path, issues)
    
    # Check if this is a oneOf
    if 'oneOf' in node:
        for i, option in enumerate(node['oneOf']):
            option_path = f"{path}.oneOf[{i}]"
            analyze_schema_node(option, option_path, issues)
    
    # Check if this is a $ref
    if '$ref' in node:
        ref_path = node['$ref']
        # Don't follow refs to avoid infinite recursion
        pass
    
    # Check definitions
    if '$defs' in node:
        for def_name, def_schema in node['$defs'].items():
            def_path = f"{path}.$defs.{def_name}"
            analyze_schema_node(def_schema, def_path, issues)
    
    return issues

print("="*80)
print("JSON SCHEMA IMPORT PATTERN ANALYSIS")
print("="*80)
print()

issues = analyze_schema_node(schema)

# Group issues by severity
high_severity = [i for i in issues if i['severity'] == 'HIGH']
medium_severity = [i for i in issues if i['severity'] == 'MEDIUM']
low_severity = [i for i in issues if i['severity'] == 'LOW']

print(f"Total issues found: {len(issues)}")
print(f"  - High severity: {len(high_severity)}")
print(f"  - Medium severity: {len(medium_severity)}")
print(f"  - Low severity: {len(low_severity)}")
print()

if high_severity:
    print("HIGH SEVERITY ISSUES:")
    print("="*80)
    for issue in high_severity:
        print(f"\nPath: {issue['path']}")
        print(f"Property: {issue['property']}")
        print(f"Issue: {issue['issue']}")
        print()

# Now let's check the actual structure of key definitions
print("\n" + "="*80)
print("DETAILED ANALYSIS OF KEY DEFINITIONS")
print("="*80)

def check_definition(def_name: str):
    """Check a specific definition for import support."""
    if def_name not in schema['$defs']:
        print(f"\n❌ Definition '{def_name}' not found")
        return
    
    definition = schema['$defs'][def_name]
    print(f"\n{def_name}:")
    print("-" * 40)
    
    # Check if it's a oneOf
    if 'oneOf' in definition:
        print(f"✓ Has oneOf with {len(definition['oneOf'])} options")
        
        # Check each option
        for i, option in enumerate(definition['oneOf']):
            if isinstance(option, dict):
                if 'required' in option and 'import' in option['required']:
                    print(f"  Option {i}: ✓ Import option")
                elif 'properties' in option and 'import' in option['properties']:
                    print(f"  Option {i}: ✓ Import option (via properties)")
                elif '$ref' in option:
                    print(f"  Option {i}: Reference to {option['$ref']}")
                elif 'type' in option:
                    print(f"  Option {i}: Type {option['type']}")
                else:
                    print(f"  Option {i}: Other structure")
    else:
        print("✗ No oneOf found")
        
        # Check if it has properties
        if 'properties' in definition:
            print(f"  Has properties: {list(definition['properties'].keys())}")

# Check key definitions
check_definition('NodeTypesProperty')
check_definition('EdgeTypesProperty')
check_definition('NodeTypeItem')
check_definition('EdgeTypeItem')
check_definition('GraphType')

# Save report
with open("IMPORT-PATTERN-ANALYSIS.md", "w") as f:
    f.write("# JSON Schema Import Pattern Analysis\n\n")
    f.write("## Overview\n\n")
    f.write("This analysis checks for consistency in import patterns throughout the schema.\n\n")
    f.write(f"**Total issues found:** {len(issues)}\n\n")
    
    if high_severity:
        f.write("## High Severity Issues\n\n")
        for issue in high_severity:
            f.write(f"### {issue['property']}\n\n")
            f.write(f"- **Path:** `{issue['path']}`\n")
            f.write(f"- **Issue:** {issue['issue']}\n\n")
    
    f.write("## Recommendations\n\n")
    f.write("1. Every importable property should have a oneOf pattern\n")
    f.write("2. The oneOf should include both the actual content and an import option\n")
    f.write("3. Import options should be consistent across all definitions\n")

print("\n✅ Analysis complete. Report saved to IMPORT-PATTERN-ANALYSIS.md")
