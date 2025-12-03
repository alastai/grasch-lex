# Edge Type Label Synonym Implementation Plan

**Date**: 2024-12-03  
**Status**: 🔵 PLANNING  
**Priority**: P1 - Important consistency improvement

## Executive Summary

Standardize edge type label syntax across all examples and schema to support `typeLabel`, `via`, `arc`, and `and` as synonyms, with proper placement inside `directed:` or `undirected:` blocks.

## IMPORTANT REVISION - Property Ordering Mandate

**Date**: 2024-12-03  
**Status**: REGISTERED - Awaiting next instruction before implementation

### Mandated Property Order

The following property orders are now **mandatory** for edge types:

**Directed Edge Type:**
```yaml
edgeType:
  directed:
    from:        # 1. Source endpoint
    to:          # 2. Target endpoint  
    via:         # 3. Edge label (or arc: or typeLabel:)
    implies:     # 4. Optional: Content specification
      labels:    #    - Optional: Label types
      propertyTypes:  # - Optional: Property types
```

**Undirected Edge Type:**
```yaml
edgeType:
  undirected:
    between:     # 1. Endpoints specification (array of 2 node types)
    and:         # 2. Edge label (synonym: via: or typeLabel:)
    via:         # 2. Edge label (synonym: and: or typeLabel:) - SAME LEVEL as and:
    implies:     # 3. Optional: Content specification
      labels:    #    - Optional: Label types
      propertyTypes:  # - Optional: Property types
```

**Note**: For undirected edges, `between:`, `and:`, and `via:` are **three sibling keys** at the same level. Only one of `and:`, `via:`, or `typeLabel:` should be used (they are synonyms).

### Key Points

1. **This is about ordering only** - not about which properties are required/optional
2. **`from:`/`to:` come before `via:`** in directed edges
3. **`between:`, `and:`, `via:` are three sibling keys** in undirected edges (only one of `and:`/`via:`/`typeLabel:` should be used)
4. **`implies:` always comes last** (when present)
5. **Within `implies:`**, `labels:` comes before `propertyTypes:` (when both present)

### Implementation Scope

This ordering requirement affects:
- JSON Schema validation (must enforce property order)
- All example YAML files (must follow order)
- All test YAML files (must follow order)
- Documentation and guides

**WAITING FOR NEXT INSTRUCTION BEFORE IMPLEMENTING THESE CHANGES**

## Current State Analysis

### Current Patterns in Use

**Directed edges** should use one of:
- `via:` (preferred for directed)
- `arc:` (synonym for via)
- `typeLabel:` (generic, should work everywhere)

**Undirected edges** should use one of:
- `and:` (preferred for undirected)
- `typeLabel:` (generic, should work everywhere)

### Problems to Fix

1. **Inconsistent placement**: Some examples may have `typeLabel` outside `directed:`/`undirected:` blocks
2. **Missing synonyms**: Schema may not treat all variants as equivalent
3. **Incomplete examples**: Need examples showing all valid syntax variants
4. **Test coverage**: Need tests validating all synonym combinations

## Required Changes

### 1. Schema Updates

**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`

**Changes needed**:

1. In `DirectedEdgeTypeEndpoints` definition:
   - Ensure `via`, `arc`, and `typeLabel` are all valid synonyms
   - Use `oneOf` pattern to allow any of the three
   - All must be mutually exclusive (only one can appear)

2. In `UndirectedEdgeTypeEndpoints` definition:
   - Ensure `and` and `typeLabel` are valid synonyms
   - Use `oneOf` pattern to allow either
   - Must be mutually exclusive

3. Validation rules:
   - `typeLabel`/`via`/`arc` must be inside `directed:` block
   - `typeLabel`/`and` must be inside `undirected:` block
   - Cannot have both directed and undirected in same edge type

### 2. Example File Audits and Fixes

**Files to audit**:
- `src/grasch/examples/lex-2026.0.3.2-example-catalog.yaml`
- `src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml`
- `src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml`
- `src/grasch/examples/lex-2026.0.3.2-finbench-sf1-graph.yaml`
- `src/grasch/examples/lex-2026.0.3.2-type-definition-syntax-examples.yaml`
- `src/grasch/examples/lex-2026.0.3.2-mixed-import-example.yaml`
- `src/grasch/examples/test-siblings-bare-only.yaml`
- All `test-*.yaml` files with edge types
- All files in `src/grasch/examples/imports/`

**For each file**:
1. Find all edge type definitions
2. Verify `typeLabel`/`via`/`arc`/`and` is inside `directed:` or `undirected:`
3. Choose appropriate keyword:
   - Directed: prefer `via:`, but `arc:` and `typeLabel:` are valid
   - Undirected: prefer `and:`, but `typeLabel:` is valid
4. Update if needed

### 3. New Test Files

Create comprehensive test files for edge type label synonyms:

#### `test-edge-directed-via.yaml`
```yaml
# Test: Directed edge using via: (preferred)
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          directed:
            via: KNOWS
            from:
              nodeType:
                typeLabel: Person
            to:
              nodeType:
                typeLabel: Person
```

#### `test-edge-directed-arc.yaml`
```yaml
# Test: Directed edge using arc: (synonym for via)
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          directed:
            arc: KNOWS
            from:
              nodeType:
                typeLabel: Person
            to:
              nodeType:
                typeLabel: Person
```

#### `test-edge-directed-typelabel.yaml`
```yaml
# Test: Directed edge using typeLabel: (generic)
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          directed:
            typeLabel: KNOWS
            from:
              nodeType:
                typeLabel: Person
            to:
              nodeType:
                typeLabel: Person
```

#### `test-edge-undirected-and.yaml`
```yaml
# Test: Undirected edge using and: (preferred)
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          undirected:
            and: FRIENDS_WITH
            endpoints:
              - nodeType:
                  typeLabel: Person
              - nodeType:
                  typeLabel: Person
```

#### `test-edge-undirected-typelabel.yaml`
```yaml
# Test: Undirected edge using typeLabel: (generic)
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          undirected:
            typeLabel: FRIENDS_WITH
            endpoints:
              - nodeType:
                  typeLabel: Person
              - nodeType:
                  typeLabel: Person
```

#### `test-edge-mixed-synonyms.yaml`
```yaml
# Test: Multiple edges using different synonyms
graphSchema:
  graphType:
    nodeTypes:
      - nodeType:
          typeLabel: Person
    edgeTypes:
      - edgeType:
          directed:
            via: KNOWS  # Using via
            from:
              nodeType:
                typeLabel: Person
            to:
              nodeType:
                typeLabel: Person
      - edgeType:
          directed:
            arc: FOLLOWS  # Using arc
            from:
              nodeType:
                typeLabel: Person
            to:
              nodeType:
                typeLabel: Person
      - edgeType:
          directed:
            typeLabel: LIKES  # Using typeLabel
            from:
              nodeType:
                typeLabel: Person
            to:
              nodeType:
                typeLabel: Person
      - edgeType:
          undirected:
            and: FRIENDS_WITH  # Using and
            endpoints:
              - nodeType:
                  typeLabel: Person
              - nodeType:
                  typeLabel: Person
      - edgeType:
          undirected:
            typeLabel: COLLEAGUES_WITH  # Using typeLabel
            endpoints:
              - nodeType:
                  typeLabel: Person
              - nodeType:
                  typeLabel: Person
```

#### `test-edge-invalid-outside-INVALID.yaml`
```yaml
# Test: INVALID - typeLabel outside directed/undirected
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          typeLabel: KNOWS  # ERROR: Must be inside directed: or undirected:
          directed:
            from:
              nodeType:
                typeLabel: Person
            to:
              nodeType:
                typeLabel: Person
```

#### `test-edge-invalid-multiple-synonyms-INVALID.yaml`
```yaml
# Test: INVALID - Multiple synonyms in same edge
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          directed:
            via: KNOWS
            arc: KNOWS  # ERROR: Cannot have both via and arc
            from:
              nodeType:
                typeLabel: Person
            to:
              nodeType:
                typeLabel: Person
```

### 4. Validation Script

Create `validate_edge_label_synonyms.py`:

```python
#!/usr/bin/env python3
"""Validate edge type label synonym support."""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

def main():
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    positive_tests = [
        "src/grasch/examples/test-edge-directed-via.yaml",
        "src/grasch/examples/test-edge-directed-arc.yaml",
        "src/grasch/examples/test-edge-directed-typelabel.yaml",
        "src/grasch/examples/test-edge-undirected-and.yaml",
        "src/grasch/examples/test-edge-undirected-typelabel.yaml",
        "src/grasch/examples/test-edge-mixed-synonyms.yaml",
    ]
    
    negative_tests = [
        "src/grasch/examples/test-edge-invalid-outside-INVALID.yaml",
        "src/grasch/examples/test-edge-invalid-multiple-synonyms-INVALID.yaml",
    ]
    
    # Test logic here...
```

## Implementation Steps

### Phase 1: Analysis (30 min)
1. ✅ Create this plan document
2. ⏳ Audit all example files for current edge type patterns
3. ⏳ Document which files need changes
4. ⏳ Identify current schema structure for edge type labels

### Phase 2: Schema Updates (1-2 hours)
1. ⏳ Update `DirectedEdgeTypeEndpoints` to support via/arc/typeLabel synonyms
2. ⏳ Update `UndirectedEdgeTypeEndpoints` to support and/typeLabel synonyms
3. ⏳ Add validation rules for proper placement
4. ⏳ Test schema changes with simple examples

### Phase 3: Example File Updates (1-2 hours)
1. ⏳ Fix `test-siblings-bare-only.yaml` (use `via:` inside `directed:`)
2. ⏳ Audit and fix all other test files
3. ⏳ Audit and fix all example files
4. ⏳ Audit and fix all import files

### Phase 4: New Test Files (1 hour)
1. ⏳ Create positive test files (6 files)
2. ⏳ Create negative test files (2 files)
3. ⏳ Create validation script
4. ⏳ Run validation to ensure all tests pass/fail correctly

### Phase 5: Documentation (30 min)
1. ⏳ Update LEX-2026.0.3.2 documentation
2. ⏳ Create summary document
3. ⏳ Update any relevant guides

## Success Criteria

1. ✅ Schema accepts `via`, `arc`, and `typeLabel` as synonyms in directed edges
2. ✅ Schema accepts `and` and `typeLabel` as synonyms in undirected edges
3. ✅ Schema rejects labels outside `directed:`/`undirected:` blocks
4. ✅ Schema rejects multiple synonyms in same edge type
5. ✅ All existing examples validate correctly
6. ✅ All new test files validate correctly (positive pass, negative fail)
7. ✅ Documentation is updated

## Estimated Time

- Phase 1: 30 minutes
- Phase 2: 1-2 hours
- Phase 3: 1-2 hours
- Phase 4: 1 hour
- Phase 5: 30 minutes

**Total**: 4-6 hours

## Notes

- This work is independent of the sibling TI wrapper bug fix
- Can be done in parallel or sequentially
- Improves consistency and user experience
- Provides better test coverage for edge type syntax

