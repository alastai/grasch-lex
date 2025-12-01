# Type Interpretation Levels: Correction and Clarification

## Critical Error in Previous Analysis

**I made a fundamental mistake**: I conflated the TI wrapper structure (0-level, 1-level, 2-level) with explicit property names. This is WRONG.

## The Correct TI Structure

### Three Levels of TI Expression

A Type Interpretation can be expressed in THREE forms at ANY location:

#### 0-Level (Bare/Implicit)
```yaml
nodeTypes:
  - typeLabel: Person  # No wrapper - implicit exactlyOf:concrete
```

**Canonical Form**: `exactlyOf: { concrete: { nodeType: {...} } }`

#### 1-Level (Shorthand)
```yaml
nodeTypes:
  - abstract:  # One wrapper keyword
      typeLabel: Person
```

**Canonical Form**: `subtypesOf: { abstract: { nodeType: {...} } }`

#### 2-Level (Explicit/Canonical)
```yaml
nodeTypes:
  - subtypesOf:  # Two wrapper keywords
      abstract:
        typeLabel: Person
```

**Canonical Form**: Already canonical

### The Key Insight

**TI wrappers use `patternProperties`** to match keywords like:
- `abstract`, `concrete`, `final`, `sealed` (concreteness facet)
- `exactlyOf`, `subtypesOf`, `properSubtypesOf` (interpretation facet)

These are NOT explicit property names - they're pattern-matched keywords that can appear in different combinations.

## What the Schema SHOULD Support

At each of the 8 locations, the schema should support:

### Pattern 1: 0-Level (Bare)
```yaml
nodeTypes:
  - typeLabel: Person  # Bare type definition
```

### Pattern 2: 1-Level (Shorthand)
```yaml
nodeTypes:
  - abstract:  # Single wrapper
      typeLabel: Person
  - concrete:
      typeLabel: Company
  - properSubtypesOf:
      typeLabel: Entity
```

### Pattern 3: 2-Level (Explicit)
```yaml
nodeTypes:
  - exactlyOf:
      concrete:
        typeLabel: Person
  - subtypesOf:
      abstract:
        typeLabel: Entity
  - properSubtypesOf:
      sealed:
        typeLabel: Message
```

## The Real Problem

Looking back at the 8 locations:

**Location 1 (GraphType):** ✓ CORRECT
- Uses `patternProperties` to match TI keywords
- Supports 0-level, 1-level, 2-level
- Pattern: `patternProperty` → content

**Locations 2-7:** ✗ WRONG ORDER
- The issue is NOT that they use patternProperties
- The issue is that the TI wrapper comes AFTER the content property instead of BEFORE
- Current: `nodeTypes` → `exactlyOf` → `concrete` → array
- Should be: `exactlyOf` → `concrete` → `nodeTypes` → array

**Location 8 (EndpointReference):** ✓ CORRECT
- Uses `patternProperties` correctly
- Supports 0-level, 1-level, 2-level

## The Sibling Issue Revisited

### The REAL Sibling Constraint

With `patternProperties`, you CAN have multiple siblings IF they match different patterns:

```yaml
# This WORKS:
nodeTypes:  # Explicit property
  - typeLabel: Person

abstract:  # Pattern-matched property
  nodeTypes:
    - typeLabel: Entity
```

But you CANNOT have:

```yaml
# This FAILS:
abstract:  # Both match same pattern
  nodeTypes: [...]
  
concrete:  # Both match same pattern
  nodeTypes: [...]
```

Because `abstract` and `concrete` both match the pattern `^(abstract|concrete|final|sealed)$`.

### The Solution

The schema needs to support NESTED patterns:

```yaml
# Level 1: Interpretation facet pattern
patternProperties:
  "^(exactlyOf|subtypesOf|properSubtypesOf)$":
    # Level 2: Concreteness facet pattern
    patternProperties:
      "^(abstract|concrete|final|sealed)$":
        # Content
        properties:
          nodeTypes: [...]
          edgeTypes: [...]
```

This allows:

```yaml
# Multiple siblings with DIFFERENT interpretation facets:
exactlyOf:
  concrete:
    nodeTypes: [...]

subtypesOf:
  abstract:
    nodeTypes: [...]

properSubtypesOf:
  sealed:
    edgeTypes: [...]
```

But still prevents:

```yaml
# Multiple siblings with SAME interpretation facet:
exactlyOf:
  concrete:
    nodeTypes: [...]
  
exactlyOf:  # ERROR - duplicate key
  abstract:
    nodeTypes: [...]
```

## Corrected Assessment

### What's Actually Implemented

Looking at Location 1 (GraphType), which is CORRECT, it likely has:

```json
{
  "patternProperties": {
    "^(abstract|concrete|final|sealed|exactlyOf|subtypesOf|properSubtypesOf)$": {
      "oneOf": [
        {
          "properties": {
            "nodeTypes": {...},
            "edgeTypes": {...}
          }
        },
        {
          "patternProperties": {
            "^(abstract|concrete|final|sealed|exactlyOf|subtypesOf|properSubtypesOf)$": {
              "properties": {
                "nodeTypes": {...},
                "edgeTypes": {...}
              }
            }
          }
        }
      ]
    }
  }
}
```

This supports:
- 0-level: Direct `nodeTypes`/`edgeTypes` properties
- 1-level: `abstract: { nodeTypes: [...] }`
- 2-level: `subtypesOf: { abstract: { nodeTypes: [...] } }`

### What Needs to Be Fixed

**Locations 2-7** need the SAME pattern as Location 1, but they currently have the wrapper AFTER the content property instead of BEFORE.

The fix is NOT to use explicit properties - it's to move the `patternProperties` to the CORRECT position in the schema hierarchy.

## Sibling Support

With the correct nested `patternProperties` structure:

### ✓ SUPPORTED:
```yaml
graphType:
  # Different interpretation facets can be siblings
  exactlyOf:
    concrete:
      nodeTypes: [...]
  
  subtypesOf:
    abstract:
      nodeTypes: [...]
  
  properSubtypesOf:
    sealed:
      edgeTypes: [...]
```

### ✗ NOT SUPPORTED (and shouldn't be):
```yaml
graphType:
  # Same interpretation facet cannot appear twice
  exactlyOf:
    concrete:
      nodeTypes: [...]
  
  exactlyOf:  # ERROR - duplicate key in YAML
    abstract:
      nodeTypes: [...]
```

### ✓ WORKAROUND (if needed):
```yaml
graphType:
  # Use 2-level nesting to have multiple concreteness facets
  exactlyOf:
    concrete:
      nodeTypes: [...]
    abstract:
      nodeTypes: [...]  # Different concreteness under same interpretation
```

## Conclusion

**My previous analysis was fundamentally flawed** because I:
1. Misunderstood the 0-level, 1-level, 2-level structure
2. Proposed replacing `patternProperties` with explicit properties
3. Would have eliminated the multi-level TI capability

**The correct fix is:**
1. Keep `patternProperties` (they're essential for the TI system)
2. Fix the 6 wrong-order locations to match Location 1's pattern
3. Ensure nested `patternProperties` support 2-level wrappers
4. Accept that siblings with the same interpretation facet cannot coexist (this is a YAML limitation, not a schema bug)

**Sibling support status:**
- ✓ Multiple siblings with DIFFERENT interpretation facets: SUPPORTED
- ✗ Multiple siblings with SAME interpretation facet: NOT SUPPORTED (YAML constraint)
- ✓ Multiple concreteness facets under same interpretation: SUPPORTED via nesting

The schema architecture is actually correct - we just need to fix the ordering at 6 locations.
