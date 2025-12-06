#!/usr/bin/env python3
"""Analyze YAML files to determine if they're additive or duplicative"""

import yaml
from pathlib import Path

# Files to analyze
FILES_TO_ANALYZE = [
    ("src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml", "Main schema example"),
    ("src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml", "FinBench benchmark schema"),
    ("src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml", "SNB benchmark schema"),
    ("src/grasch/examples/lex-2026.0.3.2-subtype-abstract-test.yaml", "Subtype/abstract testing"),
    ("src/grasch/examples/test-phase-b-edgetype-ti.yaml", "Phase B: EdgeType TI wrappers"),
    ("src/grasch/examples/test-siblings-bare-only.yaml", "Sibling TI: bare only"),
    ("src/grasch/examples/test-siblings-complex.yaml", "Sibling TI: complex patterns"),
    ("src/grasch/examples/test-edge-invalid-adding-without-extends-INVALID.yaml", "Negative test"),
    ("src/grasch/examples/test-edge-inline-nodetype.yaml", "Edge with inline nodeType"),
    ("test-edge-label-structure.yaml", "Edge label structure test"),
]

print("ADDITIVE FILES (need updates):")
for filepath, desc in FILES_TO_ANALYZE:
    if Path(filepath).exists():
        print(f"  ✓ {Path(filepath).name}")
    else:
        print(f"  ✗ {Path(filepath).name} (missing)")
