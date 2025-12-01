# Phase E Implementation Plan: Array-Level Type Interpretations

**Date**: 2024-12-01  
**Status**: READY TO START  
**Goal**: Implement Locations 1-5 (array-level and graph-level TI support) with correct nesting semantics

## Context

We have successfully completed Phases A-D (Locations 6-9):
- ✅ Location 6: `nodeTypeInterpretation` - individual node types
- ✅ Location 7: `edgeTypeInterpretation` - individual edge types  
- ✅ Location 8: `edgeTypeEndpointNodeTypeInterpretation` - undirected endpoints
- ✅ Location 9: `edgeTypeEndpointNodeTypeInterpretation` - directed endpoints

Now we need to implement the remaining locations for array-level and graph-level TIs.

## Remaining Locations

1. **Location 1**: `graphTypeInterpretation` - for the graphType property
2. **Location 2**: `nodeTypesInterpretation` - for nodeTypes arrays (entire collection)
3. **Location 3**: `edgeTypesInterpretation` - for edgeTypes arrays (entire collection)
4. **Location 4**: `nodeTypeArrayInterpretation` - for subsequence within nodeTypes array
5. **Location 5**: `edgeTypeArrayInterpretation` - for subsequence within edgeTypes array

## Current Schema State

### What Exists (Locations 2-3)
The schema ALREADY supports wrapping the entire `nodeTypes` and `edgeTypes` properties:

```json
"NodeTypesProperty": {
  "oneOf": [
    { "$ref": "#/$defs/NodeTypesArray" },  // Bare array
    { "abstract": { ... } },                // Location 2: Wrap entire nodeTypes
    { "concrete": { ... } },
    { "exactlyOf": { "concrete": { ... } } },
    // ... etc
  ]
}
```

**This is Location 2 and 3 - they're ALREADY IMPLEMENTED!**

### What's Missing (Locations 4-5)
The schema has `PartitionBlockItemNode` and `PartitionBlockItemEdge` but these are **incorrectly named** and don't properly support the nesting model we've agreed upon.

Current issues:
1. **Wrong terminology**: "Partition blocks" should be "Array subsequence interpretations"
2. **No nesting support**: Can't have TI wrapping TI wrapping array
3. **Doesn't follow proximity-wins model**: No implementation of double-wrap exception

### What's Missing (Location 1)
No support for wrapping the entire `graphType` property with a TI.

## Agreed Nesting Principles (from TEMP-NESTING-IDEAS.md)

1. **Proximity Wins**: Closest TI to the element prevails
2. **Double-Wrap Exception**: When two TIs directly enclose the same element, outer overrides inner
3. **Canonicalization**: Strip inner TI, keep outer TI
4. **Import Context**: Double-wrapping typically occurs through importation

## Implementation Strategy

We'll implement Phase E in stages, stopping at each stage for review:

### Stage 1: Locations 4+5 (Array Subsequences) ✋ STOP FOR REVIEW
**Goal**: Support TI wrappers for subsequences within nodeTypes/edgeTypes arrays

**What to implement**:
- Rename `PartitionBlockItemNode` → `NodeTypeArrayInterpretation`
- Rename `PartitionBlockItemEdge` → `EdgeTypeArrayInterpretation`
- Support nesting: TI wrapping TI wrapping array
- Implement proximity-wins semantics
- Support both singleton and multi-element arrays

**YAML Examples**:
```yaml
# Location 4: nodeTypeArrayInterpretation
nodeTypes:
  - abstract:  # Subsequence with 1-level TI
      - nodeType: { typeLabel: Vehicle }
      - nodeType: { typeLabel: Car }
  - nodeType: { typeLabel: Person }  # Bare item
  - subtypesOf:  # Subsequence with 2-level TI
      abstract:
        - nodeType: { typeLabel: Message }
```

**Deliverables**:
1. Update schema definitions for `NodeTypeArrayInterpretation` and `EdgeTypeArrayInterpretation`
2. Create test YAML file: `test-phase-e-locations-4-5.yaml`
3. Create validation script: `validate_phase_e_locations_4_5.py`
4. Document changes in: `PHASE-E-STAGE-1-COMPLETE.md`

### Stage 2: Locations 2+3 Review ✋ STOP FOR REVIEW
**Goal**: Verify that existing Location 2+3 support is correct and document it

**What to verify**:
- `NodeTypesProperty` correctly supports wrapping entire nodeTypes array
- `EdgeTypesProperty` correctly supports wrapping entire edgeTypes array
- Import support works correctly
- Nesting semantics are correct

**YAML Examples**:
```yaml
# Location 2: nodeTypesInterpretation (wraps WHOLE nodeTypes property)
abstract:
  nodeTypes:
    - nodeType: { typeLabel: Person }
    - nodeType: { typeLabel: Company }
```

**Deliverables**:
1. Create test YAML file: `test-phase-e-locations-2-3.yaml`
2. Create validation script: `validate_phase_e_locations_2_3.py`
3. Document findings in: `PHASE-E-STAGE-2-COMPLETE.md`

### Stage 3: Location 1 (Graph Type Interpretation) ✋ STOP FOR REVIEW
**Goal**: Support TI wrapper for the entire graphType property

**What to implement**:
- Add TI wrapper support to `GraphType` definition
- Support 0/1/2-level wrappers
- Ensure nesting semantics work correctly

**YAML Examples**:
```yaml
# Location 1: graphTypeInterpretation
graphSchema:
  pathName: /my/schema
  graphType:
    abstract:  # Wrap entire graphType
      nodeTypes:
        - nodeType: { typeLabel: Entity }
      edgeTypes:
        - edgeType: { ... }
```

**Deliverables**:
1. Update schema to support graphType TI wrappers
2. Create test YAML file: `test-phase-e-location-1.yaml`
3. Create validation script: `validate_phase_e_location_1.py`
4. Document changes in: `PHASE-E-STAGE-3-COMPLETE.md`

### Stage 4: Nesting Semantics & Canonicalization ✋ STOP FOR REVIEW
**Goal**: Implement and test the agreed nesting principles

**What to implement**:
- Proximity-wins algorithm
- Double-wrap detection and resolution
- Canonicalization rules (strip inner, keep outer)
- Integration with import processing

**Test Cases**:
```yaml
# Test double-wrapping
nodeTypes:
  - subtypesOf:  # Outer TI
      abstract:  # Inner TI (should be stripped)
        nodeType: { typeLabel: Person }
# After canonicalization: subtypesOf: abstract: Person
```

**Deliverables**:
1. Update `canonicalizing_preprocessor.py` with nesting logic
2. Create comprehensive test suite: `test_ti_nesting_semantics.py`
3. Create test YAML files for all nesting scenarios
4. Document in: `PHASE-E-STAGE-4-COMPLETE.md`

### Stage 5: Integration & Final Validation ✋ STOP FOR REVIEW
**Goal**: Ensure all locations work together correctly

**What to test**:
- All 9 locations working together
- Nesting across different location levels
- Import interactions
- Canonicalization end-to-end

**Deliverables**:
1. Comprehensive integration test: `test_all_ti_locations.py`
2. Update all example YAML files to use correct patterns
3. Final documentation: `PHASE-E-COMPLETE.md`
4. Update TEMP-NESTING-IDEAS.md status

## Success Criteria

Phase E is complete when:
1. ✅ All 9 TI locations are implemented and tested
2. ✅ Nesting semantics (proximity-wins + double-wrap exception) work correctly
3. ✅ Canonicalization properly strips inner TIs
4. ✅ Import processing handles TI conflicts correctly
5. ✅ All test files validate successfully
6. ✅ Documentation is complete and accurate

## Next Steps

**READY TO START STAGE 1**: Implement Locations 4+5 (Array Subsequences)

Shall we proceed with Stage 1?
