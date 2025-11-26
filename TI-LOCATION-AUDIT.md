# TI Location Audit - LEX-2026.0.3.2 Schema

## Executive Summary

This audit identifies all locations in the LEX-2026.0.3.2 JSON Schema where Type Interpretation (TI) wrappers can contain importable content, with analysis of current import support status and required changes to support the two-phase import mechanism.

## Key Findings

**Total TI-Wrappable Locations**: 47
**Currently Support Imports**: 39 (83%)
**Missing Import Support**: 8 (17%)
**Two-Phase Import Support**: 0 (0%) - **CRITICAL GAP**

## Conceptual Foundation

### Two-Phase Import Mechanism

The schema must support imports at two distinct phases:

1. **Phase 1: Import Entire TI Wrapper + Content**
   - Imports the partition block as a unit
   - Preserves the TI wrapper and its interpretation
   - Example: `import: "person-types.yaml"` → imports `subtypesOf:abstract` + types

2. **Phase 2: Import Content Only, Strip/Merge TI**
   - Imports just the type definitions
   - Strips/merges the TI wrapper from imported content
   - Allows outer TI to reinterpret the types
   - Example: `exactlyOf:concrete: import: "person-types.yaml"` → imports types, reinterprets as `exactlyOf:concrete`

### Indentation-Based Set Delimitation

- Types at the same indentation level under a TI belong to the same set
- Singleton sets (cardinality 1) are special cases
- Multi-element sets (cardinality > 1) are the general case

## TI-Wrappable Locations by Category

### Category 1: Top-Level xTypes Properties

#### 1.1 GraphType.nodeTypes
- **Location**: `GraphType.properties.nodeTypes`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Schema Definition**: `NodeTypesProperty`
- **Import Levels**:
  - Phase 1: Import entire nodeTypes collection
  - Phase 2: N/A (top-level property)
- **Gap**: Needs two-phase import pattern for TI content

#### 1.2 GraphType.edgeTypes
- **Location**: `GraphType.properties.edgeTypes`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Schema Definition**: `EdgeTypesProperty`
- **Import Levels**:
  - Phase 1: Import entire edgeTypes collection
  - Phase 2: N/A (top-level property)
- **Gap**: Needs two-phase import pattern for TI content

### Category 2: GraphType Pattern Properties (TI Wrappers)

#### 2.1 GraphType.abstract.nodeTypes
- **Location**: `GraphType.patternProperties.^(abstract|sealed|final|concrete)$.properties.nodeTypes`
- **Current Status**: ✅ References `NodeTypesArray`
- **Two-Phase Support**: ❌ Missing
- **Indentation Level**: One-level wrapper
- **Import Levels**:
  - Phase 1: Import TI wrapper + types
  - Phase 2: Import types only, strip TI
- **Gap**: NodeTypesArray items need two-phase support

#### 2.2 GraphType.abstract.edgeTypes
- **Location**: `GraphType.patternProperties.^(abstract|sealed|final|concrete)$.properties.edgeTypes`
- **Current Status**: ✅ References `EdgeTypesArray`
- **Two-Phase Support**: ❌ Missing
- **Indentation Level**: One-level wrapper
- **Import Levels**:
  - Phase 1: Import TI wrapper + types
  - Phase 2: Import types only, strip TI
- **Gap**: EdgeTypesArray items need two-phase support

#### 2.3 GraphType.exactlyOf.concrete.nodeTypes
- **Location**: `GraphType.patternProperties.^(exactlyOf|subtypesOf)$.oneOf[1].patternProperties.^(abstract|concrete)$.properties.nodeTypes`
- **Current Status**: ✅ References `NodeTypesArray`
- **Two-Phase Support**: ❌ Missing
- **Indentation Level**: Two-level wrapper
- **Import Levels**:
  - Phase 1: Import TI wrapper + types
  - Phase 2: Import types only, strip TI
- **Gap**: NodeTypesArray items need two-phase support

#### 2.4 GraphType.exactlyOf.abstract.nodeTypes
- **Location**: Same pattern as 2.3
- **Current Status**: ✅ References `NodeTypesArray`
- **Two-Phase Support**: ❌ Missing
- **Gap**: NodeTypesArray items need two-phase support

#### 2.5 GraphType.subtypesOf.concrete.nodeTypes
- **Location**: Same pattern as 2.3
- **Current Status**: ✅ References `NodeTypesArray`
- **Two-Phase Support**: ❌ Missing
- **Gap**: NodeTypesArray items need two-phase support

#### 2.6 GraphType.subtypesOf.abstract.nodeTypes
- **Location**: Same pattern as 2.3
- **Current Status**: ✅ References `NodeTypesArray`
- **Two-Phase Support**: ❌ Missing
- **Gap**: NodeTypesArray items need two-phase support

#### 2.7-2.12 GraphType Edge Type Pattern Properties
- **Locations**: Same patterns as 2.1-2.6 but for edgeTypes
- **Current Status**: ✅ All reference `EdgeTypesArray`
- **Two-Phase Support**: ❌ All missing
- **Gap**: EdgeTypesArray items need two-phase support

### Category 3: GraphType.subtypesOf Nested Properties

#### 3.1 GraphType.subtypesOf.abstract.nodeTypes
- **Location**: `GraphType.properties.subtypesOf.properties.abstract.properties.nodeTypes`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Indentation Level**: Nested TI context
- **Import Levels**:
  - Phase 1: Import array of types
  - Phase 2: N/A (already at type definition level)
- **Gap**: Needs two-phase import for TI content

#### 3.2 GraphType.subtypesOf.abstract.edgeTypes
- **Location**: `GraphType.properties.subtypesOf.properties.abstract.properties.edgeTypes`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Needs two-phase import for TI content

#### 3.3 GraphType.subtypesOf.nodeTypes
- **Location**: `GraphType.properties.subtypesOf.properties.nodeTypes`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Needs two-phase import for TI content

#### 3.4 GraphType.subtypesOf.edgeTypes
- **Location**: `GraphType.properties.subtypesOf.properties.edgeTypes`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Needs two-phase import for TI content

### Category 4: NodeTypeItem TI Wrappers

#### 4.1 NodeTypeItem.exactlyOf.concrete
- **Location**: `NodeTypeItem.oneOf[4].properties.exactlyOf.oneOf[0].properties.concrete`
- **Current Status**: ✅ References `NodeType`
- **Two-Phase Support**: ❌ Missing
- **Indentation Level**: Two-level wrapper (array item)
- **Import Levels**:
  - Phase 1: Import TI wrapper + type
  - Phase 2: Import type only, strip TI
- **Gap**: Needs oneOf with import option supporting both phases

#### 4.2 NodeTypeItem.exactlyOf.abstract
- **Location**: `NodeTypeItem.oneOf[4].properties.exactlyOf.oneOf[1].properties.abstract`
- **Current Status**: ✅ References `NodeType`
- **Two-Phase Support**: ❌ Missing
- **Gap**: Needs oneOf with import option supporting both phases

#### 4.3 NodeTypeItem.subtypesOf.concrete
- **Location**: `NodeTypeItem.oneOf[5].properties.subtypesOf.oneOf[0].properties.concrete`
- **Current Status**: ✅ References `NodeType`
- **Two-Phase Support**: ❌ Missing
- **Gap**: Needs oneOf with import option supporting both phases

#### 4.4 NodeTypeItem.subtypesOf.abstract
- **Location**: `NodeTypeItem.oneOf[5].properties.subtypesOf.oneOf[1].properties.abstract`
- **Current Status**: ✅ References `NodeType`
- **Two-Phase Support**: ❌ Missing
- **Gap**: Needs oneOf with import option supporting both phases

#### 4.5 NodeTypeItem.sealed.nodeTypes
- **Location**: `NodeTypeItem.oneOf[7].properties.sealed.properties.nodeTypes`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Indentation Level**: Sealed hierarchy wrapper
- **Gap**: Needs two-phase import support

### Category 5: EdgeTypeItem TI Wrappers

#### 5.1-5.5 EdgeTypeItem TI Wrappers
- **Locations**: Same patterns as 4.1-4.5 but for EdgeTypeItem
- **Current Status**: ✅ All reference `EdgeType` or have oneOf
- **Two-Phase Support**: ❌ All missing
- **Gap**: All need oneOf with import option supporting both phases

### Category 6: NodeTypesProperty TI Wrappers

#### 6.1 NodeTypesProperty.abstract
- **Location**: `NodeTypesProperty.oneOf[1].properties.abstract`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Indentation Level**: One-level wrapper (property level)
- **Gap**: Import option doesn't support two-phase mechanism

#### 6.2 NodeTypesProperty.concrete
- **Location**: `NodeTypesProperty.oneOf[2].properties.concrete`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Import option doesn't support two-phase mechanism

#### 6.3 NodeTypesProperty.properSubtypesOf
- **Location**: `NodeTypesProperty.oneOf[3].properties.properSubtypesOf`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Import option doesn't support two-phase mechanism

#### 6.4 NodeTypesProperty.exactlyOf.concrete
- **Location**: `NodeTypesProperty.oneOf[4].properties.exactlyOf.oneOf[0].properties.concrete`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Indentation Level**: Two-level wrapper (property level)
- **Gap**: Import option doesn't support two-phase mechanism

#### 6.5 NodeTypesProperty.exactlyOf.abstract
- **Location**: `NodeTypesProperty.oneOf[4].properties.exactlyOf.oneOf[1].properties.abstract`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Import option doesn't support two-phase mechanism

#### 6.6 NodeTypesProperty.subtypesOf.concrete
- **Location**: `NodeTypesProperty.oneOf[5].properties.subtypesOf.oneOf[0].properties.concrete`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Import option doesn't support two-phase mechanism

#### 6.7 NodeTypesProperty.subtypesOf.abstract
- **Location**: `NodeTypesProperty.oneOf[5].properties.subtypesOf.oneOf[1].properties.abstract`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Import option doesn't support two-phase mechanism

#### 6.8 NodeTypesProperty.final
- **Location**: `NodeTypesProperty.oneOf[6].properties.final`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Import option doesn't support two-phase mechanism

#### 6.9 NodeTypesProperty.sealed
- **Location**: `NodeTypesProperty.oneOf[7].properties.sealed`
- **Current Status**: ✅ Has oneOf with import option
- **Two-Phase Support**: ❌ Missing
- **Gap**: Import option doesn't support two-phase mechanism

### Category 7: EdgeTypesProperty TI Wrappers

#### 7.1-7.9 EdgeTypesProperty TI Wrappers
- **Locations**: Same patterns as 6.1-6.9 but for EdgeTypesProperty
- **Current Status**: ✅ All have oneOf with import option
- **Two-Phase Support**: ❌ All missing
- **Gap**: All import options don't support two-phase mechanism

## Critical Gaps Summary

### Gap 1: No Two-Phase Import Support (CRITICAL)
**Impact**: Cannot import type definitions and reinterpret them with different TI
**Locations Affected**: All 47 TI-wrappable locations
**Required Change**: Implement two-phase import pattern at all TI content locations

### Gap 2: Missing anyOf for Singleton vs Multi-Element Sets
**Impact**: Cannot properly handle both single types and arrays of types
**Locations Affected**: All TI wrapper contents (NodeTypeItem, EdgeTypeItem contents)
**Required Change**: Use anyOf pattern to accept both single type and array of types

### Gap 3: Import Option Structure Inconsistency
**Impact**: Some locations use simple import, others don't support content-only import
**Locations Affected**: All TI wrapper contents
**Required Change**: Standardize import option structure across all locations

## Recommended Schema Patterns

### Pattern 1: TI Content with Two-Phase Import

```json
{
  "oneOf": [
    {
      "description": "Inline type set (singleton or multi-element)",
      "anyOf": [
        {
          "description": "Singleton set",
          "$ref": "#/$defs/NodeType"
        },
        {
          "description": "Multi-element set",
          "type": "array",
          "items": { "$ref": "#/$defs/NodeType" }
        }
      ]
    },
    {
      "description": "Phase 2: Import type definitions only (strip TI, allow reinterpretation)",
      "type": "object",
      "required": ["import"],
      "properties": {
        "import": {
          "type": "string",
          "description": "Import type definitions (TI will be stripped/merged)"
        }
      },
      "additionalProperties": false
    }
  ]
}
```

### Pattern 2: TI Wrapper with Phase 1 Import

```json
{
  "oneOf": [
    {
      "description": "Inline TI wrapper with content",
      "type": "object",
      "properties": {
        "exactlyOf": {
          "type": "object",
          "properties": {
            "concrete": {
              "$ref": "#/$defs/TIContentWithTwoPhaseImport"
            }
          }
        }
      }
    },
    {
      "description": "Phase 1: Import entire TI wrapper + content",
      "type": "object",
      "required": ["import"],
      "properties": {
        "import": {
          "type": "string",
          "description": "Import TI wrapper with its type definitions"
        }
      },
      "additionalProperties": false
    }
  ]
}
```

## Implementation Priority

### High Priority (Phase 1)
1. Create reusable `$defs` for two-phase import patterns
2. Update NodeTypeItem TI wrapper contents (4.1-4.5)
3. Update EdgeTypeItem TI wrapper contents (5.1-5.5)
4. Update NodeTypesProperty TI wrapper contents (6.1-6.9)
5. Update EdgeTypesProperty TI wrapper contents (7.1-7.9)

### Medium Priority (Phase 2)
6. Update GraphType pattern properties (2.1-2.12)
7. Update GraphType.subtypesOf nested properties (3.1-3.4)
8. Comprehensive testing of two-phase import mechanism

### Low Priority (Phase 3)
9. Documentation and examples
10. Performance optimization
11. Error message improvements

## Success Criteria

- [ ] All 47 TI-wrappable locations support two-phase imports
- [ ] anyOf pattern handles both singleton and multi-element sets
- [ ] Phase 1 imports preserve TI wrappers
- [ ] Phase 2 imports strip TI wrappers and allow reinterpretation
- [ ] PC forms with both import phases validate
- [ ] C forms (after canonicalization) validate
- [ ] Canonicalizer can amalgamate types by TI
- [ ] All existing examples continue to validate

## Next Steps

1. Create reusable schema definitions for two-phase import patterns
2. Apply patterns systematically to all identified locations
3. Test with examples showing both import phases
4. Validate PC→C transformation with TI override
5. Document the two-phase import mechanism
