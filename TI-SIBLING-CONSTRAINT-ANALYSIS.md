# Type Interpretation Sibling Constraint Analysis

## Executive Summary

**Confirmed:** The current schema implementation using `patternProperties` for TI wrappers **fundamentally prevents multiple sibling TI-wrapped elements** at the same level. This is a JSON Schema architectural constraint, not a bug.

**Impact:** 6 out of 8 TI locations have wrong-order patterns, AND the sibling limitation affects all locations where multiple element types might appear.

**CONSTRAINT REMOVED:** Backward compatibility is NOT required. All YAML documents can be rewritten to match the corrected design.

---

## The Sibling Problem: Detailed Assessment

### What We've Established

1. **Pattern Properties Limitation**: JSON Schema `patternProperties` can only match property names, not distinguish between multiple properties with the same pattern at the same level.

2. **Current Failures**:
   - Cannot have multiple `nodeTypes` siblings (e.g., `exactlyOf: {nodeTypes: [...]}` + `subtypesOf: {nodeTypes: [...]}`)
   - Cannot have multiple `edgeTypes` siblings with different TI wrappers
   - Cannot have multiple TI-wrapped arrays within `nodeTypes` or `edgeTypes` properties
   - Cannot have multiple solo element types each with its own TI wrapper

### Why This Happens

When using `patternProperties: {"^(abstract|concrete|exactlyOf|subtypesOf)$": {...}}`:

```json
{
  "exactlyOf": {
    "nodeTypes": [...]  // ✓ Works
  },
  "subtypesOf": {
    "nodeTypes": [...]  // ✗ CONFLICT - both match the same pattern
  }
}
```

JSON Schema cannot distinguish which `patternProperty` definition should apply to which sibling. The validator sees:
- Two properties matching the pattern `^(abstract|concrete|exactlyOf|subtypesOf)$`
- One schema definition for that pattern
- Confusion about which property gets which validation

---

## The Wrong-Order Problem: Detailed Assessment

### Current State (6 Locations WRONG)

**Location 1 (GraphType):** ✓ CORRECT
- Pattern: `patternProperty` → content
- Works because it's at the root level

**Location 2 (NodeTypesProperty):** ✗ WRONG
- Current: `nodeTypes` → `exactlyOf` → `concrete` → array
- Should be: `patternProperty` → `nodeTypes` → array
- Problem: TI wrapper comes AFTER the property name

**Location 3 (EdgeTypesProperty):** ✗ WRONG  
- Current: `edgeTypes` → `exactlyOf` → `concrete` → array
- Should be: `patternProperty` → `edgeTypes` → array
- Problem: TI wrapper comes AFTER the property name

**Location 4 (NodeTypeItem):** ✗ WRONG
- Current: array item → `abstract` → NodeType
- Should be: `patternProperty` → NodeType
- Problem: TI wrapper embedded in array item schema

**Location 5 (EdgeTypeItem):** ✗ WRONG
- Current: array item → `abstract` → EdgeType  
- Should be: `patternProperty` → EdgeType
- Problem: TI wrapper embedded in array item schema

**Location 6 (Individual NodeType):** ✗ WRONG
- Current: No TI support at all
- Should be: `patternProperty` → NodeType content
- Problem: Missing TI capability entirely

**Location 7 (EdgeType Content):** ✗ WRONG
- Current: No TI support at all
- Should be: `patternProperty` → EdgeType content
- Problem: Missing TI capability entirely

**Location 8 (EndpointReference):** ✓ CORRECT
- Pattern: `patternProperty` → NodeType content (within oneOf)
- Works correctly

---

## Strategic Options for Resolution

### Option 1: Explicit Property Names (RECOMMENDED)

**Approach:** Replace `patternProperties` with explicit property definitions for each TI wrapper.

**Structure:**
```json
{
  "properties": {
    "exactlyOf": {
      "type": "object",
      "properties": {
        "nodeTypes": {"type": "array", "items": {...}},
        "edgeTypes": {"type": "array", "items": {...}}
      }
    },
    "subtypesOf": {
      "type": "object",
      "properties": {
        "nodeTypes": {"type": "array", "items": {...}},
        "edgeTypes": {"type": "array", "items": {...}}
      }
    },
    "abstract": {...},
    "concrete": {...}
  }
}
```

**Advantages:**
- ✓ Allows multiple sibling TI wrappers
- ✓ Clear, explicit validation rules
- ✓ Better error messages
- ✓ Easier to understand and maintain
- ✓ Solves both wrong-order AND sibling problems

**Disadvantages:**
- More verbose schema
- Requires updating all 6 wrong locations
- Breaking change for existing YAML documents

**Feasibility:** HIGH - This is the standard JSON Schema approach

---

### Option 2: OneOf with Explicit Branches

**Approach:** Use `oneOf` to enumerate all valid TI wrapper combinations.

**Structure:**
```json
{
  "oneOf": [
    {
      "properties": {
        "exactlyOf": {
          "properties": {
            "nodeTypes": [...]
          }
        }
      },
      "required": ["exactlyOf"]
    },
    {
      "properties": {
        "subtypesOf": {
          "properties": {
            "nodeTypes": [...]
          }
        }
      },
      "required": ["subtypesOf"]
    },
    // ... more branches for combinations
  ]
}
```

**Advantages:**
- ✓ Allows multiple siblings (by enumerating valid combinations)
- ✓ Precise validation

**Disadvantages:**
- ✗ Exponential explosion of combinations
- ✗ Extremely verbose
- ✗ Hard to maintain
- ✗ Poor error messages

**Feasibility:** LOW - Too complex for practical use

---

### Option 3: Nested Structure with Grouping

**Approach:** Group TI wrappers under a parent property.

**Structure:**
```json
{
  "properties": {
    "typeInterpretations": {
      "type": "object",
      "properties": {
        "exactlyOf": {
          "properties": {
            "nodeTypes": [...],
            "edgeTypes": [...]
          }
        },
        "subtypesOf": {
          "properties": {
            "nodeTypes": [...],
            "edgeTypes": [...]
          }
        }
      }
    }
  }
}
```

**Advantages:**
- ✓ Allows multiple siblings
- ✓ Logical grouping
- ✓ Clear namespace

**Disadvantages:**
- ✗ Adds extra nesting level
- ✗ Changes YAML structure significantly
- ✗ Breaking change

**Feasibility:** MEDIUM - Workable but requires significant restructuring

---

### Option 4: Array-Based Approach

**Approach:** Use arrays with discriminator properties.

**Structure:**
```json
{
  "properties": {
    "elementTypeGroups": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["interpretation"],
        "properties": {
          "interpretation": {
            "enum": ["exactlyOf", "subtypesOf", "abstract", "concrete"]
          },
          "nodeTypes": [...],
          "edgeTypes": [...]
        }
      }
    }
  }
}
```

**Advantages:**
- ✓ Allows unlimited siblings
- ✓ Extensible
- ✓ Clear structure

**Disadvantages:**
- ✗ Completely different YAML structure
- ✗ Less intuitive
- ✗ Major breaking change

**Feasibility:** LOW - Too disruptive

---

## Recommended Strategy

### Phase 1: Fix Wrong-Order Issues (Locations 2-7)

**Approach:** Use **Option 1 (Explicit Property Names)** to fix all 6 wrong-order locations.

**Changes Required:**

1. **Location 2 (NodeTypesProperty):**
   - Remove: `nodeTypes → exactlyOf → concrete → array`
   - Add: Explicit `exactlyOf`, `subtypesOf`, `abstract`, `concrete` properties at GraphType level
   - Each contains `nodeTypes` property with array

2. **Location 3 (EdgeTypesProperty):**
   - Remove: `edgeTypes → exactlyOf → concrete → array`
   - Add: Explicit TI properties at GraphType level
   - Each contains `edgeTypes` property with array

3. **Location 4 (NodeTypeItem):**
   - Remove: array item → `abstract` → NodeType
   - Add: Array items directly reference NodeType
   - TI wrapper moves to parent level

4. **Location 5 (EdgeTypeItem):**
   - Remove: array item → `abstract` → EdgeType
   - Add: Array items directly reference EdgeType
   - TI wrapper moves to parent level

5. **Location 6 (Individual NodeType):**
   - Add: TI wrapper capability at NodeType definition level
   - Use explicit properties or oneOf with TI options

6. **Location 7 (EdgeType Content):**
   - Add: TI wrapper capability at EdgeType definition level
   - Use explicit properties or oneOf with TI options

### Phase 2: Enable Sibling Support

**After Phase 1 is complete**, the explicit property approach naturally allows siblings:

```yaml
graphType:
  propertyGraphDataModel: true
  exactlyOf:
    nodeTypes:
      - typeLabel: Person
  subtypesOf:
    nodeTypes:
      - typeLabel: Entity
  abstract:
    nodeTypes:
      - typeLabel: Thing
```

This works because `exactlyOf`, `subtypesOf`, and `abstract` are now distinct properties, not pattern-matched.

---

## Implementation Considerations

### Backward Compatibility

**Breaking Changes:**
- YAML structure changes at 6 locations
- Existing documents will need migration
- Canonicalization logic must be updated

**Migration Path:**
1. Update schema (Phase 1)
2. Update canonicalizing preprocessor
3. Provide migration script for existing YAML files
4. Update all example files
5. Update documentation

### Testing Requirements

**Must Test:**
- Single TI wrapper at each location (baseline)
- Multiple sibling TI wrappers at each location
- Nested TI wrappers (where applicable)
- Import statements with TI wrappers
- Canonicalization of all patterns
- Validation of all 8 locations

### Estimated Effort

**Schema Updates:** 2-3 hours
- Rewrite 6 location definitions
- Add explicit properties
- Update references

**Preprocessor Updates:** 3-4 hours
- Update canonicalization logic
- Handle new explicit properties
- Maintain backward compatibility during transition

**Testing:** 4-5 hours
- Create test cases for all locations
- Test sibling scenarios
- Validate migration

**Documentation:** 2-3 hours
- Update examples
- Write migration guide
- Update spec documents

**Total:** 11-15 hours

---

## Conclusion

**The sibling constraint is real and fundamental** - it's a consequence of using `patternProperties` in JSON Schema.

**The solution is clear:** Replace `patternProperties` with explicit property definitions (Option 1). This simultaneously:
1. Fixes the wrong-order problem at 6 locations
2. Enables multiple sibling TI wrappers
3. Provides better validation and error messages
4. Creates a more maintainable schema

**Next Steps:**
1. Get approval for breaking changes
2. Implement Phase 1 (fix wrong-order issues)
3. Update preprocessor and tests
4. Migrate existing examples
5. Document the new structure

The work is substantial but straightforward, and the result will be a more consistent, flexible, and correct schema implementation.
