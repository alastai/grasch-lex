# Phase 2: Locations 2-3 Problem Identified

**Date**: 2024-12-02  
**Status**: Problem Confirmed - Locations 2-3 Need Fixing

## Summary

After analyzing the schema, I can confirm:

1. **Location 1 (GraphType)**: ✓ CORRECT - Uses `patternProperties` for sibling TI wrappers
2. **Locations 2-3 (NodeTypesProperty/EdgeTypesProperty)**: ✗ WRONG - Uses `oneOf` pattern that prevents siblings

## The Problem: oneOf vs patternProperties

### Location 1 (GraphType) - CORRECT Pattern

```json
"GraphType": {
  "properties": {
    "nodeTypes": { ... },     // Bare property
    "edgeTypes": { ... }      // Bare property
  },
  "patternProperties": {      // Allows MULTIPLE siblings!
    "^(exactlyOf|subtypesOf)$": { ... },
    "^(abstract|concrete)$": { ... }
  },
  "additionalProperties": true
}
```

**Result**: You CAN have multiple siblings:
```yaml
graphType:
  nodeTypes: [...]           # Bare
  exactlyOf:                 # Sibling 1
    concrete:
      nodeTypes: [...]
  subtypesOf:                # Sibling 2
    abstract:
      nodeTypes: [...]
```

### Locations 2-3 (NodeTypesProperty) - WRONG Pattern

```json
"NodeTypesProperty": {
  "oneOf": [                  // Only ONE option allowed!
    { "$ref": "#/$defs/NodeTypesArray" },  // Option 1: bare
    {                                       // Option 2: abstract wrapper
      "required": ["abstract"],
      "properties": { "abstract": { ... } }
    },
    {                                       // Option 3: concrete wrapper
      "required": ["concrete"],
      "properties": { "concrete": { ... } }
    },
    {                                       // Option 4: exactlyOf wrapper
      "required": ["exactlyOf"],
      "properties": { "exactlyOf": { ... } }
    }
    // ... more options
  ]
}
```

**Result**: You CANNOT have multiple siblings because `oneOf` means "exactly one of these options"

## What User Wants (and What's Correct)

The user correctly identified that within GraphType, we should be able to have:

```yaml
graphType:
  nodeTypes: [...]           # Bare nodeTypes (0-level)
  exactlyOf:                 # TI-wrapped nodeTypes (sibling)
    concrete:
      nodeTypes: [...]
  subtypesOf:                # Another TI-wrapped nodeTypes (sibling)
    abstract:
      nodeTypes: [...]
  edgeTypes: [...]           # Bare edgeTypes (0-level)
  exactlyOf:                 # TI-wrapped edgeTypes (sibling)
    concrete:
      edgeTypes: [...]
```

**This is EXACTLY what Location 1 (GraphType) supports with its `patternProperties` pattern!**

## The Fix for Locations 2-3

Locations 2-3 need to be restructured to match Location 1's pattern:

### Current (Wrong):
- NodeTypesProperty uses `oneOf` (only one option)
- EdgeTypesProperty uses `oneOf` (only one option)

### Target (Correct):
- NodeTypesProperty should use `patternProperties` (multiple siblings)
- EdgeTypesProperty should use `patternProperties` (multiple siblings)

## Why This Matters

The current `oneOf` pattern means:
- You can have EITHER bare `nodeTypes` OR `exactlyOf: { nodeTypes }` OR `subtypesOf: { nodeTypes }`
- But NOT multiple as siblings

The correct `patternProperties` pattern means:
- You can have bare `nodeTypes` AND `exactlyOf: { nodeTypes }` AND `subtypesOf: { nodeTypes }` as siblings
- Just like GraphType already does!

## Phase 2 Scope Confirmed

**Locations that need fixing**:
- Location 2: NodeTypesProperty (change from `oneOf` to `patternProperties`)
- Location 3: EdgeTypesProperty (change from `oneOf` to `patternProperties`)
- Locations 4-7: (still need to investigate)

**Location that's already correct**:
- Location 1: GraphType (use as reference pattern)

## Next Steps

1. Confirm this understanding with the user
2. Update design and tasks documents to reflect this specific problem
3. Proceed with Phase 2 implementation to fix Locations 2-3
