#!/usr/bin/env python3
"""Analyze YAML files to find those with edgeTypes"""

import yaml
import sys
from pathlib import Path

def has_edgetypes(filepath):
    """Check if a YAML file contains edgeTypes"""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check various locations where edgeTypes might appear
        if not data:
            return False
            
        # Check in graphSchema -> graphType -> edgeTypes
        if isinstance(data, dict):
            if 'graphSchema' in data:
                gt = data['graphSchema'].get('graphType', {})
                if 'edgeTypes' in gt:
                    return True
                # Check in subtypesOf
                if 'subtypesOf' in gt:
                    st = gt['subtypesOf']
                    if isinstance(st, dict):
                        if 'edgeTypes' in st:
                            return True
                        if 'abstract' in st and isinstance(st['abstract'], dict):
                            if 'edgeTypes' in st['abstract']:
                                return True
            
            # Check in graph -> graphSchema -> graphType -> edgeTypes
            if 'graph' in data:
                gs = data['graph'].get('graphSchema', {})
                if isinstance(gs, dict):
                    gt = gs.get('graphType', {})
                    if isinstance(gt, dict) and 'edgeTypes' in gt:
                        return True
        
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return False

# Files to check
yaml_files = [
    # Main examples
    "src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml",
    "src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml",
    "src/grasch/examples/lex-2026.0.3.2-comprehensive-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml",
    "src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-mixed-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml",
    "src/grasch/examples/lex-2026.0.3.2-snb-special-identification-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-subtype-abstract-test.yaml",
    "src/grasch/examples/lex-2026.0.3.2-type-definition-syntax-examples.yaml",
    
    # Test phase files
    "src/grasch/examples/test-phase-b-edgetype-ti.yaml",
    "src/grasch/examples/test-phase-c-endpoint-ti.yaml",
    "src/grasch/examples/test-phase-e-location-2.yaml",
    "src/grasch/examples/test-phase-e-location-2-two-level.yaml",
    "src/grasch/examples/test-phase-e-location-3.yaml",
    "src/grasch/examples/test-phase-e-location-3-two-level.yaml",
    "src/grasch/examples/test-phase-e-locations-2-3.yaml",
    "src/grasch/examples/test-phase-e-locations-2-3-advanced.yaml",
    "src/grasch/examples/test-phase-e-locations-4-5.yaml",
    
    # Test siblings files
    "src/grasch/examples/test-siblings-bare-only.yaml",
    "src/grasch/examples/test-siblings-all-1-level.yaml",
    "src/grasch/examples/test-siblings-all-2-level.yaml",
    "src/grasch/examples/test-siblings-complex.yaml",
    "src/grasch/examples/test-siblings-interleaved.yaml",
    "src/grasch/examples/test-siblings-mixed-0-1-level.yaml",
    "src/grasch/examples/test-siblings-mixed-0-2-level.yaml",
    
    # Test edge invalid files
    "src/grasch/examples/test-edge-invalid-adding-without-extends-INVALID.yaml",
    "src/grasch/examples/test-edge-invalid-implies-with-extends-INVALID.yaml",
    "src/grasch/examples/test-edge-invalid-ordering-INVALID.yaml",
    "src/grasch/examples/test-edge-invalid-multiple-synonyms-INVALID.yaml",
    "src/grasch/examples/test-edge-invalid-outside-INVALID.yaml",
    
    # Other test edge files
    "src/grasch/examples/test-edge-inline-nodetype.yaml",
    
    # Root level test files
    "test-edge-label-structure.yaml",
    "test-phase-c.yaml",
    "test-phase-d.yaml",
    "test_edgetypes_only.yaml",
]

print("Files with edgeTypes:")
print("=" * 80)

files_with_edges = []
for filepath in yaml_files:
    if Path(filepath).exists() and has_edgetypes(filepath):
        files_with_edges.append(filepath)
        print(f"✓ {filepath}")

print("\n" + "=" * 80)
print(f"Total: {len(files_with_edges)} files with edgeTypes")
