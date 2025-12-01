# Phase E - Stage 2: Schema Bug Identified

**Date**: 2024-12-01  
**Status**: 🐛 BUG IDENTIFIED - NEEDS FIX

## Problem Statement

The current schema does NOT allow independent wrapping of `nodeTypes` and `edgeTypes` with different TI wrappers. This is a **schema bug**, not a design limitation.

### What Should Work (But Doesn't)

```yaml
graphType:
  concrete:
    nodeTypes:
      - nodeType: { typeLabel: Person, ... }
  abstract:
    edgeTypes:
      - edgeType: { typeLabel: KNOWS, ... }
```

This should be valid because:
1. Location 2 (nodeTypesInterpretation) should wrap nodeTypes independently
2. Location 3 (edgeTypesInterpretation) should wrap edgeTypes independently
3. They should be able to have DIFFERENT TI wrappers

### Current Schema Structure (Buggy)

The `GraphType` definition has:

```json
{
  "type": "object",
  "properties": {
    "nodeTypes": { "$ref": "#/$defs/NodeTypesProperty" },
    "edgeTypes": { "$ref": "#/$defs/EdgeTypesProperty" },
    // ... other properties
  },
  "additionalProperties": true,
  "patternProperties": {
    "^(abstract|concrete|...)$": {
      "type": "object",
      "properties": {
        "nodeTypes": { "$ref": "#/$defs/NodeTypesArray" },
        "edgeTypes": { "$ref": "#/$defs/EdgeTypesArray" }
      },
      "minProperties": 1
    }
  }
}
```

**The Problem**:
- The pattern properties define objects that contain BOTH `nodeTypes` AND `edgeTypes`
- When you use multiple pattern properties (e.g., `concrete:` and `abstract:`), the schema doesn't know how to validate them together
- The regular `nodeTypes` and `edgeTypes` properties use `NodeTypesProperty` and `EdgeTypesProperty` which ALREADY support TI wrappers
- The pattern properties are redundant and conflicting!

## Root Cause Analysis

The schema has TWO mechanisms for TI wrappers:

### Mechanism 1: Via NodeTypesProperty/EdgeTypesProperty (CORRECT)
```yaml
# This works because NodeTypesProperty supports wrappers
nodeTypes:
  abstract:
    - nodeType: { ... }
```

### Mechanism 2: Via Pattern Properties (BUGGY)
```yaml
# This tries to use pattern properties
abstract:
  nodeTypes:
    - nodeType: { ... }
```

**The bug**: Mechanism 2 (pattern properties) was added but it conflicts with Mechanism 1. When you try to use BOTH mechanisms (one for nodeTypes, one for edgeTypes), they conflict.

## The Correct Design

We should **REMOVE** the pattern properties from GraphType and rely ONLY on NodeTypesProperty and EdgeTypesProperty, which already support TI wrappers.

### Current (Buggy) Approach:
```
GraphType
├── properties
│   ├── nodeTypes → NodeTypesProperty (supports wrappers)
│   └── edgeTypes → EdgeTypesProperty (supports wrappers)
└── patternProperties (REDUNDANT AND BUGGY)
    └── ^(abstract|concrete|...)$ → Contains nodeTypes/edgeTypes
```

### Correct Approach:
```
GraphType
├── properties
│   ├── nodeTypes → NodeTypesProperty (supports wrappers) ✅
│   └── edgeTypes → EdgeTypesProperty (supports wrappers) ✅
└── NO pattern properties needed!
```

## Why Pattern Properties Were Added

Looking at the schema history, the pattern properties were likely added to support this shorthand:

```yaml
# Shorthand (what pattern properties enable)
graphType:
  abstract:
    nodeTypes: [...]
    edgeTypes: [...]

# vs. Full form (what NodeTypesProperty/EdgeTypesProperty enable)
graphType:
  nodeTypes:
    abstract: [...]
  edgeTypes:
    abstract: [...]
```

But this shorthand breaks independent wrapping!

## Solution

### Option 1: Remove Pattern Properties (RECOMMENDED)
- Remove all pattern properties from GraphType
- Rely solely on NodeTypesProperty and EdgeTypesProperty
- This allows independent wrapping
- Users write: `nodeTypes: abstract: [...]` instead of `abstract: nodeTypes: [...]`

### Option 2: Fix Pattern Properties (COMPLEX)
- Make pattern properties smarter to allow multiple instances
- Add logic to merge pattern properties
- Much more complex schema validation

### Option 3: Hybrid Approach
- Keep pattern properties for the common case (wrapping both together)
- Also allow regular properties for independent wrapping
- Need to add validation logic to prevent conflicts

## Recommended Fix: Option 1

**Remove the pattern properties** and update all examples to use the NodeTypesProperty/EdgeTypesProperty syntax.

### Changes Required:

1. **Schema Change**: Remove patternProperties from GraphType definition
2. **Example Updates**: Update all YAML examples that use pattern property syntax
3. **Documentation**: Update docs to show correct syntax

### Migration Path:

```yaml
# OLD (pattern property syntax - will break)
graphType:
  abstract:
    nodeTypes: [...]
    edgeTypes: [...]

# NEW (property syntax - works correctly)
graphType:
  nodeTypes:
    abstract: [...]
  edgeTypes:
    abstract: [...]
```

## Impact Assessment

### Breaking Change?
**YES** - Any YAML files using the pattern property syntax will need to be updated.

### Files Affected:
- Need to search codebase for pattern property usage
- Update all example files
- Update any test files

### Benefits:
- ✅ Enables independent wrapping of nodeTypes and edgeTypes
- ✅ Simpler schema (removes redundancy)
- ✅ More consistent with the rest of the design
- ✅ Fixes the Location 3 bug

## Next Steps

1. **User Approval**: Get approval to proceed with Option 1 (remove pattern properties)
2. **Schema Fix**: Remove pattern properties from GraphType
3. **Example Migration**: Update all YAML files to use property syntax
4. **Validation**: Re-run all tests
5. **Documentation**: Update design docs

## Status

⏸️ **PAUSED** - Waiting for user approval to proceed with schema fix

**Question for User**: Should we proceed with Option 1 (remove pattern properties) to fix this bug?
