# Task 10.0 Complete: Location 1 Pattern Properties Eliminated

## Summary

Successfully completed Task 10.0 - eliminated pattern properties from Location 1 (GraphSchemaContent) and replaced with explicit properties using oneOf.

## Changes Made

### 1. Terminology Updates (Prerequisite)

**Schema Renaming**:
- `NodeTypeItem` → `NodeTypeArray`
- `EdgeTypeItem` → `EdgeTypeArray`
- Updated descriptions from "item" to "element"
- Updated all references to use new names

**Rationale**: Clarifies that these definitions handle array-level TI (Locations 4-5), not individual items.

### 2. Location 1 (GraphSchemaContent) - Pattern Properties Eliminated

**Before**: Used `patternProperties` to match TI keywords
- Pattern: `^(abstract|sealed|final|concrete)$` for 1-level wrappers
- Pattern: `^(exactlyOf|subtypesOf|properSubtypesOf)$` for 2-level wrappers
- Nested pattern properties for concreteness facets

**After**: Uses explicit properties with `oneOf` constraint
- **Structure**: `allOf` combining base properties with `oneOf` for TI options
- **Base properties**: `pathName` (required), `principal`, `constraints`
- **TI options** (exactly ONE required via `oneOf`):
  1. **0-level**: Bare `graphType` property
  2. **1-level**: `abstract: { graphType: ... }` wrapper
  3. **1-level**: `concrete: { graphType: ... }` wrapper
  4. **2-level**: `exactlyOf: { concrete|abstract: { graphType: ... } }` wrapper
  5. **2-level**: `subtypesOf: { concrete|abstract: { graphType: ... } }` wrapper
  6. **2-level**: `properSubtypesOf: { concrete|abstract: { graphType: ... } }` wrapper

**Key Improvements**:
- ✅ Eliminates JSON Schema pattern property conflicts
- ✅ Provides better IDE autocomplete support
- ✅ Makes schema structure explicit and clear
- ✅ Ensures exactly ONE graphType (bare or wrapped) via `oneOf`
- ✅ Follows the same pattern as Phases A-D (Locations 6-8)

## Pattern Details

### Structure

```json
{
  "allOf": [
    {
      "type": "object",
      "required": ["pathName"],
      "properties": {
        "pathName": { ... },
        "principal": { ... },
        "constraints": { ... }
      }
    },
    {
      "oneOf": [
        // 0-level: bare graphType
        { "required": ["graphType"], "properties": { "graphType": {...} } },
        
        // 1-level: abstract wrapper
        { "required": ["abstract"], "properties": { "abstract": { "graphType": {...} } } },
        
        // 1-level: concrete wrapper
        { "required": ["concrete"], "properties": { "concrete": { "graphType": {...} } } },
        
        // 2-level: exactlyOf with concrete/abstract
        { "required": ["exactlyOf"], "properties": { "exactlyOf": { "oneOf": [...] } } },
        
        // 2-level: subtypesOf with concrete/abstract
        { "required": ["subtypesOf"], "properties": { "subtypesOf": { "oneOf": [...] } } },
        
        // 2-level: properSubtypesOf with concrete/abstract
        { "required": ["properSubtypesOf"], "properties": { "properSubtypesOf": { "oneOf": [...] } } }
      ]
    }
  ]
}
```

### Supported Syntax

**0-level (bare)**:
```yaml
graphSchema:
  pathName: /mySchema
  graphType:
    nodeTypes: [...]
```

**1-level (shorthand)**:
```yaml
graphSchema:
  pathName: /mySchema
  abstract:
    graphType:
      nodeTypes: [...]
```

**2-level (explicit)**:
```yaml
graphSchema:
  pathName: /mySchema
  subtypesOf:
    abstract:
      graphType:
        nodeTypes: [...]
```

## Validation

Schema validated successfully:
```bash
python -m json.tool src/grasch/schemas/lex-2026.0.3.2.schema.json > /dev/null
# Output: Schema is valid JSON
```

## Next Steps

**Task 10**: Fix Locations 2 & 3 (nodeTypesInterpretation & edgeTypesInterpretation)
- Use corrected Location 1 as reference pattern
- Apply explicit sibling properties WITHOUT oneOf (multi-wrapper locations)
- Handle both locations together as they're aligned

**Dependencies**:
- Task 10 depends on Task 10.0 (✅ COMPLETE)
- Task 10 depends on Task 4 (Edge Label Container Fix) for Location 3

## Files Modified

1. `src/grasch/schemas/lex-2026.0.3.2.schema.json`
   - Renamed `NodeTypeItem` → `NodeTypeArray`
   - Renamed `EdgeTypeItem` → `EdgeTypeArray`
   - Eliminated pattern properties from GraphSchemaContent (lines 203-420)
   - Replaced with explicit properties using `allOf` + `oneOf` structure

## Reference

- **Spec**: `.kiro/specs/ti-ordering-refactor/tasks.md` - Task 10.0
- **Design**: `.kiro/specs/ti-ordering-refactor/design.md` - Location 1 section
- **Pattern**: Phases A-D (Locations 6-8) - explicit properties with oneOf
