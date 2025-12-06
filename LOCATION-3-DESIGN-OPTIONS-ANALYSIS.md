# Location 3 Design Options Analysis

**Date**: 2024-12-06  
**Context**: Task 10 - Fix Location 3 (edgeTypesInterpretation)  
**Question**: What does using pattern properties gain, over using explicit properties?

## Current Situation

The test files use this syntax:
```yaml
graphType:
  nodeTypes: [...]      # Bare (0-level)
  concrete:             # TI wrapper (1-level)
    edgeTypes: [...]    # Wrapped content
```

But the schema does NOT support `concrete` as a top-level GraphType property. Currently:
- GraphType has explicit properties: `nodeTypes`, `edgeTypes`, `subtypesOf`, `exactlyOf`, `properSubtypesOf`
- `concrete` only exists NESTED inside `exactlyOf`, `subtypesOf`, `properSubtypesOf`

## Design Options

### Option 1: Pattern Properties

**Structure**:
```json
"GraphType": {
  "type": "object",
  "properties": {
    "nodeTypes": { ... },
    "edgeTypes": { ... },
    "subtypesOf": { ... },
    "exactlyOf": { ... },
    "properSubtypesOf": { ... }
  },
  "patternProperties": {
    "^(concrete|abstract|sealed|final)$": {
      "type": "object",
      "properties": {
        "nodeTypes": { ... },
        "edgeTypes": { ... }
      }
    }
  }
}
```

**Advantages**:
- **Dynamic matching**: Any TI keyword automatically gets the same structure
- **Less repetition**: Define the pattern once, applies to all keywords
- **Extensible**: Easy to add new TI keywords without schema changes
- **Compact**: Shorter schema definition

**Disadvantages**:
- **Less explicit**: Harder to see exactly what properties are allowed
- **Validation complexity**: Pattern matching can be harder to debug
- **Documentation**: Less clear in schema what specific keywords mean
- **IDE support**: Some IDEs may not autocomplete pattern properties as well

### Option 2: Explicit Properties in OneOf

**Structure**:
```json
"GraphType": {
  "type": "object",
  "oneOf": [
    {
      "properties": {
        "nodeTypes": { ... },
        "edgeTypes": { ... }
      }
    },
    {
      "properties": {
        "concrete": {
          "type": "object",
          "properties": {
            "nodeTypes": { ... },
            "edgeTypes": { ... }
          }
        }
      }
    },
    {
      "properties": {
        "abstract": {
          "type": "object",
          "properties": {
            "nodeTypes": { ... },
            "edgeTypes": { ... }
          }
        }
      }
    }
  ]
}
```

**Advantages**:
- **Explicit**: Every allowed combination is clearly defined
- **Mutually exclusive**: OneOf ensures only one pattern matches
- **Clear validation**: Easy to see which branch failed
- **Documentation**: Each option can have specific descriptions

**Disadvantages**:
- **No siblings**: OneOf means you can't have `concrete: { nodeTypes: [...] }` AND `abstract: { edgeTypes: [...] }` as siblings
- **Repetitive**: Must repeat structure for each keyword
- **Verbose**: Schema becomes very long
- **Maintenance**: Adding new keywords requires duplicating structure

### Option 3: Explicit Properties Without OneOf (Heterogeneous Siblings)

**Structure**:
```json
"GraphType": {
  "type": "object",
  "properties": {
    "nodeTypes": { ... },
    "edgeTypes": { ... },
    "subtypesOf": { ... },
    "exactlyOf": { ... },
    "properSubtypesOf": { ... },
    "concrete": {
      "type": "object",
      "properties": {
        "nodeTypes": { ... },
        "edgeTypes": { ... }
      }
    },
    "abstract": {
      "type": "object",
      "properties": {
        "nodeTypes": { ... },
        "edgeTypes": { ... }
      }
    },
    "sealed": {
      "type": "object",
      "properties": {
        "nodeTypes": { ... },
        "edgeTypes": { ... }
      }
    },
    "final": {
      "type": "object",
      "properties": {
        "nodeTypes": { ... },
        "edgeTypes": { ... }
      }
    }
  }
}
```

**Advantages**:
- **Siblings allowed**: Can have `concrete: { nodeTypes: [...] }` AND `abstract: { edgeTypes: [...] }` at same level
- **Explicit**: Every property is clearly defined
- **IDE support**: Full autocomplete and validation
- **Clear semantics**: Each property has its own description
- **Flexible**: Can mix and match TI wrappers

**Disadvantages**:
- **Repetitive**: Must define each keyword explicitly
- **Verbose**: More lines in schema
- **Maintenance**: Adding new keywords requires explicit definition
- **Potential conflicts**: Need to ensure sibling combinations are valid

## Comparison Table

| Feature | Pattern Properties | Explicit in OneOf | Explicit Without OneOf |
|---------|-------------------|-------------------|------------------------|
| **Siblings allowed** | ✅ Yes | ❌ No | ✅ Yes |
| **Compact schema** | ✅ Yes | ❌ No | ⚠️ Medium |
| **Explicit definitions** | ❌ No | ✅ Yes | ✅ Yes |
| **IDE autocomplete** | ⚠️ Limited | ✅ Good | ✅ Excellent |
| **Easy to extend** | ✅ Yes | ❌ No | ⚠️ Medium |
| **Clear validation errors** | ⚠️ Medium | ✅ Good | ✅ Good |
| **Documentation clarity** | ⚠️ Medium | ✅ Good | ✅ Excellent |

## Recommendation

**For Location 3 (and all TI locations), I recommend Option 3: Explicit Properties Without OneOf**

**Rationale**:
1. **Sibling support is critical**: The design requires supporting `concrete: { nodeTypes: [...] }` AND `abstract: { edgeTypes: [...] }` as siblings
2. **Clarity over brevity**: Explicit properties make the schema easier to understand and maintain
3. **Better tooling**: IDEs can provide better autocomplete and validation
4. **Semantic clarity**: Each TI keyword can have its own description explaining its meaning
5. **Validation errors**: When validation fails, it's clearer which property caused the issue

**Trade-off accepted**: The schema will be more verbose, but this is acceptable for the benefits gained.

## Implementation Plan

To implement Option 3 for Location 3:

1. Add explicit properties to GraphType:
   - `concrete: { properties: { nodeTypes, edgeTypes } }`
   - `abstract: { properties: { nodeTypes, edgeTypes } }`
   - `sealed: { properties: { nodeTypes, edgeTypes } }`
   - `final: { properties: { nodeTypes, edgeTypes } }`

2. These properties become siblings to existing properties:
   - `nodeTypes` (bare, 0-level)
   - `edgeTypes` (bare, 0-level)
   - `subtypesOf` (interpretation facet, 2-level)
   - `exactlyOf` (interpretation facet, 2-level)
   - `properSubtypesOf` (interpretation facet, 2-level)

3. This enables the desired syntax:
   ```yaml
   graphType:
     nodeTypes: [...]        # 0-level
     concrete:               # 1-level TI wrapper
       edgeTypes: [...]
   ```

4. And also enables:
   ```yaml
   graphType:
     concrete:               # 1-level TI wrapper
       nodeTypes: [...]
     abstract:               # 1-level TI wrapper (different facet)
       edgeTypes: [...]
   ```

## Next Steps

1. **Wait for user confirmation** that Option 3 is the correct approach
2. **Update GraphType schema** to add explicit properties for TI keywords
3. **Test the changes** with existing test files
4. **Validate** that all 4 Location 2-3 test files pass

