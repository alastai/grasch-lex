# Type Interpretation Sibling Constraint Analysis

## Executive Summary

**Confirmed:** The current schema implementation using `patternProperties` for TI wrappers **fundamentally prevents multiple sibling TI-wrapped elements** at the same level. This is a JSON Schema architectural constraint, not a bug.

**Impact:** 6 out of 8 TI locations have wrong-order patterns, AND the sibling limitation affects all locations where multiple element types might appear.

**CONSTRAINT REMOVED:** Backward compatibility is NOT required. All YAML documents can be rewritten to match the corrected design.

---

## Key Clarification: What Does "Explicit Properties" Mean?

**Question:** Are we replacing the regex with `anyOf`?

**Answer:** **NO.** We are replacing `patternProperties` with explicit named properties.

### Current Approach (WRONG):
```json
{
  "patternProperties": {
    "^(abstract|concrete|exactlyOf|subtypesOf)$": {
      "type": "object",
      "properties": {
        "nodeTypes": {...}
      }
    }
  }
}
```

This uses a **regex pattern** to match property names. The problem: JSON Schema can't distinguish between multiple properties that match the same pattern.

### Proposed Approach (CORRECT):
```json
{
  "properties": {
    "abstract": {
      "type": "object",
      "properties": {
        "nodeTypes": {...}
      }
    },
    "concrete": {
      "type": "object",
      "properties": {
        "nodeTypes": {...}
      }
    },
    "exactlyOf": {
      "type": "object",
      "properties": {
        "nodeTypes": {...}
      }
    },
    "subtypesOf": {
      "type": "object",
      "properties": {
        "nodeTypes": {...}
      }
    }
  }
}
```

This defines **four separate, named properties**. No regex, no `anyOf`, no `oneOf`. Just explicit property definitions.

**Result:** Multiple siblings work naturally because `abstract`, `concrete`, `exactlyOf`, and `subtypesOf` are distinct properties.

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

**Clarification on "Explicit Properties":**
- **NOT using `anyOf`** - we define each TI wrapper as a distinct named property
- The regex pattern `^(abstract|concrete|exactlyOf|subtypesOf)$` is REPLACED with four separate property definitions
- Each property (`exactlyOf`, `subtypesOf`, `abstract`, `concrete`) is explicitly defined in the schema
- Multiple siblings are allowed because they are different properties, not pattern-matched

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
    "abstract": {
      "type": "object",
      "properties": {
        "nodeTypes": {"type": "array", "items": {...}},
        "edgeTypes": {"type": "array", "items": {...}}
      }
    },
    "concrete": {
      "type": "object",
      "properties": {
        "nodeTypes": {"type": "array", "items": {...}},
        "edgeTypes": {"type": "array", "items": {...}}
      }
    }
  }
}
```

**Advantages:**
- ✓ Allows multiple sibling TI wrappers naturally
- ✓ Clear, explicit validation rules
- ✓ Better error messages
- ✓ Easier to understand and maintain
- ✓ Solves both wrong-order AND sibling problems
- ✓ No backward compatibility concerns - rewrite all YAML as needed

**Disadvantages:**
- More verbose schema (but clearer)
- Requires updating all 6 wrong locations

**Feasibility:** HIGH - This is the standard JSON Schema approach

---

### Option 2: OneOf with Explicit Branches (NOT RECOMMENDED)

**Approach:** Use `oneOf` to enumerate all valid TI wrapper combinations.

**Important Note:** This is **NOT** what Option 1 proposes. Option 1 uses explicit properties WITHOUT `oneOf` or `anyOf`.

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
    {
      "properties": {
        "exactlyOf": {...},
        "subtypesOf": {...}
      },
      "required": ["exactlyOf", "subtypesOf"]
    }
    // ... exponential explosion of all possible combinations
  ]
}
```

**Advantages:**
- ✓ Allows multiple siblings (by enumerating valid combinations)
- ✓ Precise validation

**Disadvantages:**
- ✗ Exponential explosion of combinations (2^4 = 16 branches for 4 TI wrappers)
- ✗ Extremely verbose
- ✗ Hard to maintain
- ✗ Poor error messages
- ✗ Unnecessary complexity

**Feasibility:** LOW - Too complex for practical use

**Why Option 1 is Better:** Option 1 achieves the same goal (multiple siblings) without `oneOf`/`anyOf` by simply defining each TI wrapper as its own property.

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

**NO BACKWARD COMPATIBILITY REQUIRED:**
- All YAML documents will be rewritten to match the corrected design
- No migration scripts needed
- Clean slate approach

**Implementation Path:**
1. Update schema with explicit properties (all 6 wrong locations)
2. Update canonicalizing preprocessor to handle new structure
3. Rewrite all example YAML files to match new schema
4. Update documentation to reflect correct patterns

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
- Rewrite 6 location definitions with explicit properties
- Remove all `patternProperties` for TI wrappers
- Update references throughout schema

**Preprocessor Updates:** 2-3 hours
- Update canonicalization logic for new structure
- Handle explicit TI wrapper properties
- No backward compatibility needed - simpler!

**YAML Rewriting:** 3-4 hours
- Rewrite all example files to match new schema
- Update test fixtures
- Ensure consistency across all documents

**Testing:** 3-4 hours
- Create test cases for all 8 locations
- Test sibling scenarios at each location
- Validate all patterns work correctly

**Documentation:** 1-2 hours
- Update examples in documentation
- Update spec documents
- No migration guide needed!

**Total:** 11-16 hours (similar effort, but cleaner result)

---

## Conclusion

**The sibling constraint is real and fundamental** - it's a consequence of using `patternProperties` in JSON Schema.

**The solution is clear:** Replace `patternProperties` with explicit property definitions (Option 1). This simultaneously:
1. Fixes the wrong-order problem at 6 locations
2. Enables multiple sibling TI wrappers
3. Provides better validation and error messages
4. Creates a more maintainable schema
5. No backward compatibility concerns - clean implementation

**Clarification on Implementation:**
- **NOT using `anyOf` or `oneOf`** to replace the regex
- **Using explicit named properties** instead: `exactlyOf`, `subtypesOf`, `abstract`, `concrete`
- Each TI wrapper becomes its own distinct property in the schema
- Multiple siblings work naturally because they are different properties

**Next Steps:**
1. ✓ Approval received - no backward compatibility needed
2. Implement explicit properties at all 6 wrong locations
3. Update preprocessor for new structure
4. Rewrite all YAML examples to match corrected schema
5. Update documentation

The work is substantial but straightforward, and the result will be a more consistent, flexible, and correct schema implementation. The lack of backward compatibility constraints makes this cleaner and faster to implement.
