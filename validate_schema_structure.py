#!/usr/bin/env python3
"""Validate the schema structure to ensure no recursion and proper oneOf patterns."""

import json
from pathlib import Path

def check_for_recursion(schema, path=""):
    """Check if NodeType contains nodeTypes or EdgeType contains edgeTypes."""
    issues = []
    
    if isinstance(schema, dict):
        # Check if this is a NodeType definition
        if "NodeType" in path and "nodeTypes" in schema:
            issues.append(f"RECURSION: NodeType contains nodeTypes at {path}")
        
        # Check if this is an EdgeType definition
        if "EdgeType" in path and "edgeTypes" in schema:
            issues.append(f"RECURSION: EdgeType contains edgeTypes at {path}")
        
        # Recurse into nested structures
        for key, value in schema.items():
            new_path = f"{path}/{key}" if path else key
            issues.extend(check_for_recursion(value, new_path))
    
    elif isinstance(schema, list):
        for i, item in enumerate(schema):
            new_path = f"{path}[{i}]"
            issues.extend(check_for_recursion(item, new_path))
    
    return issues

def check_oneof_patterns(schema, path=""):
    """Check that oneOf patterns are mutually exclusive."""
    issues = []
    
    if isinstance(schema, dict):
        if "oneOf" in schema:
            oneof_items = schema["oneOf"]
            # Check each oneOf option has unique required fields
            required_sets = []
            for i, option in enumerate(oneof_items):
                if isinstance(option, dict) and "required" in option:
                    required_sets.append((i, set(option["required"])))
            
            # Check for overlaps
            for i, (idx1, req1) in enumerate(required_sets):
                for idx2, req2 in required_sets[i+1:]:
                    if req1 == req2:
                        issues.append(f"OVERLAP: oneOf options {idx1} and {idx2} have same required fields at {path}")
        
        # Recurse
        for key, value in schema.items():
            new_path = f"{path}/{key}" if path else key
            issues.extend(check_oneof_patterns(value, new_path))
    
    elif isinstance(schema, list):
        for i, item in enumerate(schema):
            new_path = f"{path}[{i}]"
            issues.extend(check_oneof_patterns(item, new_path))
    
    return issues

def main():
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    
    print("Loading schema...")
    with open(schema_path) as f:
        schema = json.load(f)
    
    print("\n1. Checking for recursion...")
    recursion_issues = check_for_recursion(schema)
    if recursion_issues:
        print("  ❌ RECURSION ISSUES FOUND:")
        for issue in recursion_issues:
            print(f"    - {issue}")
    else:
        print("  ✓ No recursion detected")
    
    print("\n2. Checking oneOf patterns...")
    oneof_issues = check_oneof_patterns(schema)
    if oneof_issues:
        print("  ⚠️  POTENTIAL ONEOF ISSUES:")
        for issue in oneof_issues:
            print(f"    - {issue}")
    else:
        print("  ✓ oneOf patterns look good")
    
    print("\n3. Checking component definitions exist...")
    defs = schema.get("$defs", {})
    required_defs = [
        "NodeType", "NodeTypeItem", "NodeTypesArray", "NodeTypesProperty",
        "EdgeType", "EdgeTypeItem", "EdgeTypesArray", "EdgeTypesProperty"
    ]
    
    missing = []
    for def_name in required_defs:
        if def_name in defs:
            print(f"  ✓ {def_name} exists")
        else:
            print(f"  ❌ {def_name} MISSING")
            missing.append(def_name)
    
    print("\n4. Checking GraphType uses new definitions...")
    graph_type = defs.get("GraphType", {})
    props = graph_type.get("properties", {})
    
    if "nodeTypes" in props:
        node_types_def = props["nodeTypes"]
        if "$ref" in node_types_def and "NodeTypesProperty" in node_types_def["$ref"]:
            print("  ✓ nodeTypes uses NodeTypesProperty")
        else:
            print(f"  ❌ nodeTypes doesn't use NodeTypesProperty: {node_types_def}")
    
    if "edgeTypes" in props:
        edge_types_def = props["edgeTypes"]
        if "$ref" in edge_types_def and "EdgeTypesProperty" in edge_types_def["$ref"]:
            print("  ✓ edgeTypes uses EdgeTypesProperty")
        else:
            print(f"  ❌ edgeTypes doesn't use EdgeTypesProperty: {edge_types_def}")
    
    print("\n" + "="*60)
    if recursion_issues or missing:
        print("❌ VALIDATION FAILED")
        return 1
    else:
        print("✓ SCHEMA STRUCTURE VALIDATION PASSED")
        return 0

if __name__ == "__main__":
    exit(main())
