# Phase E Location 3 - Detailed Error Analysis

**Date**: 2024-12-03  
**Status**: ANALYSIS ONLY - No actions taken

## Test Results Summary

**Passing**: 2/4 files
- ✅ `test-phase-e-location-2.yaml` (nodeTypes)
- ✅ `test-phase-e-location-2-two-level.yaml` (nodeTypes)

**Failing**: 2/4 files
- ❌ `test-phase-e-location-3.yaml` (edgeTypes)
- ❌ `test-phase-e-location-3-two-level.yaml` (edgeTypes)

## Error Messages Breakdown

### Primary Error
```
{'graphSchema': {...}} is not valid under any of the given schemas
```

### Context Errors (3 distinct issues)

#### Error 1: Missing 'catalog' property
```
'catalog' is a required property
```

#### Error 2: Unexpected 'graphSchema' property
```
Additional properties are not allowed ('graphSchema' was unexpected)
```

#### Error 3: Missing 'graph' property
```
'graph' is a required property
```

## Root Cause Analysis

### Issue 1: Document Type Mismatch

**What the files use**:
```yaml
graphSchema:
  pathName: /test/phase-e-location-3
  graphType:
    ...
```

**What the schema expects** (based on errors):
```yaml
catalog:
  ...
graph:
  ...
```

**Questions**:
1. Are Location 3 tests supposed to use a different document type than Location 2?
2. Why do Location 2 tests pass with `graphSchema:` but Location 3 tests fail?
3. Is this a schema validation issue or a test file issue?

### Issue 2: Edge Type Syntax Errors

Looking at the actual file content, there are **serious edge type syntax errors**:

**Current (WRONG)**:
```yaml
edgeTypes:
  - edgeType:
      typeLabel: KNOWS  # At edgeType level
      directed:
        from:
          nodeType:
            typeLabel: Person
        to:
          nodeType:
            typeLabel: Person
        via:  # WRONG: via is an object, not a string
          implies:
            propertyTypes:
              - name: since
                valueType: INTEGER
```

**Problems identified**:
1. `typeLabel: KNOWS` is at `edgeType` level (outside `directed:`)
2. `via:` is an object with `implies:` nested under it
3. `via:` should be a simple string: `via: KNOWS`
4. `implies:` should be at `edgeType` level, not nested under `via:`
5. Using inline node type definitions unnecessarily

**Should be (CORRECT)**:
```yaml
edgeTypes:
  - edgeType:
      directed:
        from: Person  # Type reference
        to: Person    # Type reference
        via: KNOWS    # String label
      implies:  # At edgeType level
        propertyTypes:
          - name: since
            valueType: INTEGER
```

### Issue 3: Redundant typeLabel

**Question**: If `typeLabel: KNOWS` is at the `edgeType` level, and `via: KNOWS` is inside `directed:`, which one is correct?

**Possibilities**:
1. Only `via:` inside `directed:` (most likely correct)
2. Only `typeLabel:` at `edgeType` level
3. Both are allowed but redundant
4. This is testing a specific pattern we don't understand yet

## Comparison: Why Location 2 Passes but Location 3 Fails

### Location 2 (Passing) - nodeTypes
```yaml
graphSchema:
  pathName: /test/phase-e-location-2
  graphType:
    propertyGraphDataModel:
      import: ...
    
    nodeTypes:
      - nodeType:
          typeLabel: Person
    
    # TI wrapper around nodeTypes property
    concrete:
      nodeTypes:
        - nodeType:
            typeLabel: Employee
```

**Why it passes**: 
- Uses `graphSchema:` document type
- NodeType syntax is correct
- No nested syntax errors

### Location 3 (Failing) - edgeTypes
```yaml
graphSchema:
  pathName: /test/phase-e-location-3
  graphType:
    propertyGraphDataModel:
      import: ...
    
    nodeTypes:
      - nodeType:
          typeLabel: Person
    
    # TI wrapper around edgeTypes property
    concrete:
      edgeTypes:
        - edgeType:
            typeLabel: KNOWS
            directed:
              from: {...}
              to: {...}
              via: {...}  # WRONG: Object instead of string
```

**Why it fails**:
- Uses same `graphSchema:` document type as Location 2
- BUT has edge type syntax errors
- The `via:` object syntax is invalid
- Schema validator may be rejecting the entire document

## Hypothesis

**Primary hypothesis**: The schema validator is rejecting the document because of the edge type syntax errors, and the error messages about `catalog`/`graph` are **misleading** or **secondary**.

**Why this hypothesis**:
1. Location 2 uses `graphSchema:` and passes
2. Location 3 uses `graphSchema:` and fails
3. The only difference is nodeTypes vs edgeTypes
4. Location 3 has clear edge type syntax errors
5. JSON Schema validators often give confusing error messages when deep validation fails

**Alternative hypothesis**: Location 3 tests are supposed to use a different document type (catalog/graph) but were incorrectly written with graphSchema.

## What We Need to Understand

### Question 1: Document Types
- What document types does the schema support?
- When should `graphSchema:` be used vs `catalog:`/`graph:`?
- Are Location 2 and Location 3 supposed to use the same document type?

### Question 2: Edge Type Syntax
- Is `typeLabel:` at `edgeType` level valid?
- Should `via:` be a string or can it be an object?
- Where should `implies:` be placed?

### Question 3: Test Intent
- What are Location 3 tests trying to demonstrate?
- Are they testing TI wrappers around edgeTypes?
- Are they testing a specific edge type pattern?

## Recommended Investigation Steps

1. **Check the schema** to see what document types are defined
2. **Look at other passing edge type examples** to see correct syntax
3. **Compare Location 2 and Location 3** test structure more carefully
4. **Check if there's documentation** about when to use different document types
5. **Fix the obvious edge syntax errors** and see if that resolves the issue

## Summary

The Phase E Location 3 failures have **multiple issues**:

1. **Document structure**: Error messages suggest wrong document type
2. **Edge type syntax**: Clear syntax errors with `via:` as object
3. **Inline node types**: Using inline form unnecessarily
4. **Redundant typeLabel**: Unclear if this is intentional

The errors were **incorrectly dismissed** as "pre-existing" and "unrelated to edge syntax" when they are actually **directly related** to edge type syntax problems.

**We cannot proceed** until we understand:
- What document type these tests should use
- What the correct edge type syntax is for these tests
- Why Location 2 passes but Location 3 fails with the same document type

## No Actions Taken

This is analysis only. No files have been modified. Awaiting instructions on how to proceed.
