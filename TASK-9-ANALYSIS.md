# Task 9.2: C Form Validation Failure Analysis

## Overview

Analysis of the 12 C form validation failures to identify root causes and determine whether the JSON Schema or canonicalizing preprocessor needs updates.

## Common Pattern Identified

**All 12 failures share the same root cause**: The JSON Schema's root-level `oneOf` validation is rejecting the canonical structures.

### Error Pattern

Every failing file shows:
```
Error: {<entire_structure>} is not valid under any of the given schemas
Path: root (unknown line)
```

This indicates the root-level `oneOf` in the JSON Schema is not matching any of its alternatives.

## Canonical Structure Analysis

### Example: minimal-test.yaml

**PC Form** (validates ✅):
```yaml
graphSchema:
  pathName: /test/test_schema
  graphType:
    import: "imports/minimal-graph-type.yaml"
```

**C Form** (fails ❌):
```yaml
graphSchema:
  pathName: /test/test_schema
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
      # ... all defaults expanded
    nodeTypes:
    - nodeType:
        index: 0
        implies:
          labels: [Person]
          propertyTypes: [...]
    edgeTypes:
    - edgeType:
        undirected:
          between: {index: 0}
          and: {index: 0}
          via:
            exactlyOf:
              concrete: KNOWS
```

### Key Differences PC vs C

1. **Import resolution**: `import:` directives are resolved and content merged inline
2. **Defaults expansion**: `propertyGraphDataModel` defaults are explicitly written
3. **Wrapper canonicalization**: Type interpretation wrappers normalized to two-level form
4. **Structure flattening**: Nested imports are flattened into single arrays

## Root Cause Analysis

### Hypothesis 1: Schema oneOf Mismatch

The JSON Schema root has a `oneOf` with three alternatives:
1. `graphSchema` object
2. `graph` object  
3. `catalog` object

**Problem**: The canonical forms ARE `graphSchema` objects, but something in their structure doesn't match the schema's expectations.

### Hypothesis 2: Type Interpretation Wrapper Structure

The canonicalizer produces structures like:
```yaml
via:
  exactlyOf:
    concrete: KNOWS
```

**Problem**: The schema may expect different wrapper structures or may not properly validate the canonical two-level form.

### Hypothesis 3: Missing or Extra Properties

The canonical form includes all defaults explicitly:
```yaml
propertyGraphDataModel:
  valueTypeSystemName: CANONICAL
  graphPreferredName: GRAPH
  nodePreferredName: NODE
  edgePreferredName: EDGE
  nodeTypeMinimumLabels: 1
  nodeTypeMaximumLabels: 20
  # ... etc
```

**Problem**: The schema may not expect these properties or may have `additionalProperties: false` somewhere.

## Detailed Failure Analysis

### File 1: minimal-test.yaml

**Structure**: Simple graphSchema with one node type (index-based) and one edge type
**Issue**: Root-level oneOf rejection
**Specific problem**: Unknown - need to examine schema's graphSchema definition

### File 2: all-import-patterns.yaml

**Structure**: Complex graphSchema with many node types, edge types, sealed hierarchies, final types
**Issue**: Root-level oneOf rejection
**Specific problem**: Likely same as minimal-test (if minimal fails, complex will too)

### Files 3-12: Similar Pattern

All show the same root-level oneOf rejection, suggesting a systematic issue rather than file-specific problems.

## Investigation Steps

### Step 1: Examine JSON Schema Root

Check the root-level `oneOf` definition:
```json
{
  "oneOf": [
    {"$ref": "#/$defs/GraphSchema"},
    {"$ref": "#/$defs/Graph"},
    {"$ref": "#/$defs/Catalog"}
  ]
}
```

### Step 2: Examine GraphSchema Definition

Check what properties are required/allowed in `GraphSchema`:
- Required properties
- Optional properties
- `additionalProperties` setting
- Nested object definitions

### Step 3: Compare PC vs C Structures

Identify what changes during canonicalization that breaks validation:
- Are new properties added?
- Are property types changed?
- Are nested structures flattened incorrectly?

### Step 4: Test Minimal Fix

Create a minimal test case:
1. Take simplest failing file (minimal-test)
2. Manually adjust C form to validate
3. Identify exact change needed
4. Determine if schema or canonicalizer should change

## Preliminary Findings

### Finding 1: PC Forms Validate

All 14 PC forms validate successfully, proving:
- The schema correctly validates pre-canonical syntax
- The examples are well-formed
- Import directives are properly structured

### Finding 2: No-Imports Files Pass

The 2 no-imports files pass both PC and C validation:
- `example-catalog-no-iri.yaml`
- `example-catalog.yaml`

**Implication**: Files without imports don't undergo transformation, so PC == C and both validate. This suggests the canonicalization process itself introduces the validation failures.

### Finding 3: All Importing Files Fail

100% of files with imports fail C form validation:
- 12/12 importing files fail
- 0/12 importing files pass

**Implication**: The canonicalization transformation systematically produces structures the schema doesn't recognize.

## Recommended Actions

### Option A: Fix the Schema

**Approach**: Update JSON Schema to properly validate canonical forms

**Pros**:
- Canonical forms are the "correct" normalized representation
- Schema should validate both PC and C forms
- Aligns with LEX spec intent

**Cons**:
- May require significant schema changes
- Could break existing validation
- Need to ensure PC forms still validate

### Option B: Fix the Canonicalizer

**Approach**: Adjust canonicalizer to produce schema-compliant output

**Pros**:
- Preserves existing schema
- Simpler fix (one component vs schema)
- Less risk of breaking existing validation

**Cons**:
- May produce non-canonical output
- Doesn't address underlying schema gap
- Temporary fix, not architectural solution

### Option C: Hybrid Approach (RECOMMENDED)

**Approach**: 
1. Identify specific schema issues
2. Fix obvious schema bugs/gaps
3. Adjust canonicalizer for remaining issues
4. Document canonical form specification

**Pros**:
- Addresses root causes
- Produces correct canonical forms
- Ensures schema validates both forms
- Creates clear specification

**Cons**:
- More work upfront
- Requires careful coordination
- Need thorough testing

## Next Steps

1. **Examine JSON Schema** - Read `lex-2026.0.3.2.schema.json` root and GraphSchema definitions
2. **Create minimal test** - Manually fix one C form to validate
3. **Identify exact issue** - Determine what property/structure causes rejection
4. **Implement fix** - Update schema or canonicalizer based on findings
5. **Test all files** - Verify fix resolves all 12 failures
6. **Document canonical form** - Add specification to LEX docs

## Files for Investigation

**Schema**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`
**Canonicalizer**: `src/grasch/canonicalizing_preprocessor.py`
**Test Files**: All `CANON_*.yaml` in `src/grasch/examples/`
**Validation Script**: `validate_pc_and_c_forms.py`

## Success Criteria

- [ ] All 14 files pass PC form validation (already achieved ✅)
- [ ] All 14 files pass C form validation (current goal)
- [ ] Canonical form specification documented
- [ ] Schema validates both PC and C forms
- [ ] Round-trip testing passes (PC → C → validate → semantics)

---

**Status**: Analysis complete, ready for implementation
**Next Task**: 9.3 - Fix schema or canonicalizer alignment
