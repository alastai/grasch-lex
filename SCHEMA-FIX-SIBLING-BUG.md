# Schema Fix: Sibling nodeTypes and edgeTypes Bug

## Problem

The GraphType definition prevents bare `nodeTypes` and `edgeTypes` arrays from coexisting as siblings. This violates Requirement 4.4.

## Root Cause

The `properties` section uses `NodeTypesProperty` and `EdgeTypesProperty` which are `oneOf` schemas expecting the ENTIRE property to match one pattern. This conflicts with having multiple sibling properties.

## Solution

Separate concerns:
1. **Bare arrays** → Define in `properties` as simple array references
2. **TI-wrapped objects** → Define in `patternProperties` only

## Implementation

### Change 1: Simplify properties section

**Current (lines ~680-690):**
```json
"properties": {
  ...
  "nodeTypes": {
    "$ref": "#/$defs/NodeTypesProperty"
  },
  ...
  "edgeTypes": {
    "$ref": "#/$defs/EdgeTypesProperty"
  },
  ...
}
```

**Fixed:**
```json
"properties": {
  ...
  "nodeTypes": {
    "$ref": "#/$defs/NodeTypesArray",
    "description": "Bare nodeTypes array (implicit exactlyOf:concrete for each item)"
  },
  ...
  "edgeTypes": {
    "$ref": "#/$defs/EdgeTypesArray",
    "description": "Bare edgeTypes array (implicit exactlyOf:concrete for each item)"
  },
  ...
}
```

### Change 2: Keep patternProperties for TI wrappers

The existing `patternProperties` section already handles TI-wrapped forms correctly:
- `^(abstract|sealed|final|concrete)$` - 1-level wrappers
- `^(properSubtypesOf)$` - 1-level or 2-level
- `^(exactlyOf|subtypesOf)$` - 1-level or 2-level

These should remain unchanged.

### Change 3: Update additionalProperties

Keep `"additionalProperties": true` to allow both `properties` and `patternProperties` to coexist.

## Result

After this fix:
- ✅ `nodeTypes: [...]` alone works (bare array)
- ✅ `edgeTypes: [...]` alone works (bare array)
- ✅ `nodeTypes: [...], edgeTypes: [...]` works (siblings)
- ✅ `abstract: { nodeTypes: [...] }` works (TI wrapper)
- ✅ `nodeTypes: [...], abstract: { nodeTypes: [...] }` works (mixed)
- ✅ `nodeTypes: [...], edgeTypes: [...], abstract: { nodeTypes: [...] }, concrete: { edgeTypes: [...] }` works (complex)

## Testing

All these test files should pass after the fix:
1. test-siblings-bare-only.yaml
2. test-siblings-mixed-0-1-level.yaml
3. test-siblings-mixed-0-2-level.yaml
4. test-siblings-all-1-level.yaml
5. test-siblings-all-2-level.yaml
6. test-siblings-interleaved.yaml
7. test-siblings-complex.yaml

## Notes

- `NodeTypesProperty` and `EdgeTypesProperty` definitions can remain in the schema for backward compatibility or be removed if not used elsewhere
- This fix aligns the schema with the design intent: bare arrays are the default, TI wrappers are optional extensions
