# Complete Phase 2 Analysis - Final Report

**Date**: 2024-12-02  
**Status**: Analysis Complete - Ready for Implementation

## User's Requirements (Definitive)

1. **Location 1**: TI wrappers (0/1/2-level) surrounding ONE graphType
2. **Locations 2-3**: TI wrappers (0/1/2-level) surrounding EACH nodeTypes/edgeTypes property (multiple siblings allowed, any order)

## Schema Analysis Results

### Location 1: GraphSchemaContent → graphType

**Current Schema**:
```json
"GraphSchemaContent": {
  "required": ["pathName", "graphType"],
  "properties": {
    "graphType": { "$ref": "#/$defs/GraphType" }
  },
  "additionalProperties": false
}
```

**Current Behavior**: 
- Only allows ONE bare `graphType` property
- Does NOT support TI wrappers at this level
- `additionalProperties: false` prevents any TI wrapper properties

**User Needs**:
```yaml
graphSchema:
  pathName: /mySchema
  # Option 1: Bare (0-level)
  graphType: { ... }
  
  # OR Option 2: 1-level TI
  abstract:
    graphType: { ... }
  
  # OR Option 3: 2-level TI
  subtypesOf:
    abstract:
      graphType: { ... }
```

**Status**: ✗ LOCATION 1 NEEDS FIXING
- Need to add `patternProperties` to GraphSchemaContent
- Need to change `additionalProperties` from `false` to `true` OR use pattern-based validation
- This is a NEW fix not previously identified!

### Locations 2-3: GraphType → nodeTypes/edgeTypes

**Current Schema (GraphType level)**:
```json
"GraphType": {
  "properties": {
    "nodeTypes": { "$ref": "#/$defs/NodeTypesProperty" }
  },
  "patternProperties": {
    "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
      "properties": { "nodeTypes": { ... } }
    }
  },
  "additionalProperties": true
}
```

**GraphType Level Status**: ✓ CORRECT - Already supports sibling TI wrappers

**BUT NodeTypesProperty Definition**:
```json
"NodeTypesProperty": {
  "oneOf": [
    { "bare array" },
    { "required": ["abstract"], "properties": { "abstract": {...} } },
    { "required": ["exactlyOf"], "properties": { "exactlyOf": {...} } }
  ]
}
```

**NodeTypesProperty Status**: ✗ WRONG - Uses `oneOf` (only one option allowed)

**User Needs**:
```yaml
graphType:
  nodeTypes: [...]           # Bare (0-level)
  abstract:                  # 1-level TI (sibling)
    nodeTypes: [...]
  exactlyOf:                 # 2-level TI (sibling)
    concrete:
      nodeTypes: [...]
  edgeTypes: [...]           # Bare (0-level)
  concrete:                  # 1-level TI (sibling)
    edgeTypes: [...]
```

**Status**: ✗ LOCATIONS 2-3 NEED FIXING
- NodeTypesProperty needs to change from `oneOf` to support inline arrays
- EdgeTypesProperty needs the same fix
- GraphType level already correct (has `patternProperties`)

## Summary: What Needs Fixing

### Location 1 (NEW DISCOVERY)
**Problem**: GraphSchemaContent doesn't support TI wrappers around graphType
**Fix**: Add `patternProperties` to GraphSchemaContent to allow TI wrappers as siblings to bare `graphType`

### Locations 2-3 (CONFIRMED)
**Problem**: NodeTypesProperty/EdgeTypesProperty use `oneOf` pattern
**Fix**: These definitions need restructuring, BUT GraphType level already has correct `patternProperties`

## The Confusion Resolved

The GraphType definition (Location 1 reference) ALREADY has the correct pattern for Locations 2-3!

The problem is:
1. **Location 1**: GraphSchemaContent needs the SAME pattern that GraphType has
2. **Locations 2-3**: NodeTypesProperty/EdgeTypesProperty are incorrectly defined with `oneOf`

## Phase 2 Scope - CORRECTED

**All 3 locations need fixing**:

1. **Location 1**: Add TI wrapper support to GraphSchemaContent (NEW)
2. **Location 2**: Fix NodeTypesProperty definition (CONFIRMED)
3. **Location 3**: Fix EdgeTypesProperty definition (CONFIRMED)

**Locations 4-7**: Still need investigation

**Location 8**: Already working

## Recommended Approach

1. Use GraphType's `patternProperties` pattern as the reference
2. Apply the SAME pattern to GraphSchemaContent for Location 1
3. Fix NodeTypesProperty and EdgeTypesProperty for Locations 2-3
4. All three should use the same sibling-supporting pattern

## Next Action

Update the design and tasks documents to reflect:
- Location 1 DOES need fixing (add TI wrapper support)
- Locations 2-3 need fixing (change from `oneOf` to sibling pattern)
- Use GraphType's existing pattern as the reference for all fixes
