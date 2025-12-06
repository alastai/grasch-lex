# Proposed Changes: Task 10 Subtask and Design Updates

**Date**: 2024-12-06  
**Context**: Adding clarification about pattern properties vs explicit properties approach

## Summary of Changes

1. **Add new subtask 10.1** under Task 10 in tasks.md
2. **Add shorthand semantics section** to design.md
3. **Update Architecture section** in design.md to clarify the approach

---

## Change 1: New Subtask 10.1 in tasks.md

**Location**: Under Task 10 (Fix Location 3 - edgeTypesInterpretation)

**New Subtask**:

```markdown
### - [ ] 10. Fix Location 3 (edgeTypesInterpretation)

**DEPENDS ON**: Task 4 (Edge Label Container Fix) must be complete first

Fix EdgeTypesProperty to support sibling TI-wrapped properties

- Locate EdgeTypesProperty definition in schema (lines 2535-2850)
- **Problem**: Currently uses `oneOf` pattern (only one option allowed)
- **Target**: Support inline arrays at GraphType level (GraphType already has correct `patternProperties`)
- Note: GraphType level already correct - use as reference
- Fix EdgeTypesProperty definition to work with GraphType's pattern
- Ensure edge label containers use correct object form (from Task 4)
- Validate JSON syntax
- _Requirements: 1.1, 2.3, 9.1_

**Sub-task**:
- [ ] 10.1 Abandon pattern properties for sibling TI behavior
  - Replace `patternProperties` with explicit properties (without oneOf) wherever we need sibling TI behavior
  - Use explicit properties: `concrete:`, `abstract:`, `sealed:`, `final:` as siblings to content properties
  - Where we want to permit a single TI wrapper, use oneOf:
    - **Location 1**: Around `graphType` in GraphSchemaContent (single graphType property)
    - **Location 6**: Around individual `nodeType` content (Phases A-D, already complete ✅)
    - **Location 7**: Around individual `edgeType` content (Phases A-D, already complete ✅)
    - **Location 8**: Around endpoint `nodeType` references in edgeTypes (Phases C-D, already complete ✅)
  - Support all TI levels:
    - **0-level**: Direct specification (e.g., bare `nodeTypes:` or `edgeTypes:`)
    - **1-level**: Concreteness facets (`abstract:`, `concrete:`, `sealed:`, `final:`)
    - **2-level**: Interpretation facets (`exactlyOf:`, `subtypesOf:`, `properSubtypesOf:`)
  - Apply this pattern to GraphType and all locations where sibling TI wrappers are needed
  - _Rationale: Explicit properties provide better IDE support, clearer semantics, and avoid JSON Schema pattern property conflicts_
```

---

## Change 2: Add Shorthand Semantics Section to design.md

**Location**: After the "Three-Level TI System" section in the Architecture

**New Section**:

```markdown
### Shorthand Semantics

The 1-level TI keywords are shorthands for 2-level combinations:

- **`abstract:`** is shorthand for **`properSubtypesOf: { abstract: ... }`**
  - Meaning: This type is abstract (cannot be instantiated) and defines a proper subtype relationship
  - Example: `abstract: { nodeTypes: [...] }` ≡ `properSubtypesOf: { abstract: { nodeTypes: [...] } }`

- **`concrete:`** is shorthand for **`exactlyOf: { concrete: ... }`**
  - Meaning: This type is concrete (can be instantiated) and requires exact type matching
  - Example: `concrete: { edgeTypes: [...] }` ≡ `exactlyOf: { concrete: { edgeTypes: [...] } }`

These shorthands provide a more concise syntax for the most common type interpretation patterns while maintaining semantic equivalence with the explicit 2-level form.
```

---

## Change 3: Update Architecture Section in design.md

**Location**: Replace the "Core Pattern (from Location 1 - GraphType)" section under "Design Solution"

**Updated Section**:

```markdown
### Core Pattern: Explicit Properties Without OneOf

**Design Decision**: Use explicit properties (not `patternProperties`) for sibling TI behavior.

**Rationale**:
- **Sibling support**: Allows multiple TI wrappers with different facets at the same level
- **IDE support**: Better autocomplete and validation in development tools
- **Clarity**: Each property is explicitly defined with its own description
- **Avoids conflicts**: No JSON Schema conflicts between pattern properties and regular properties

**Pattern for Sibling TI Wrappers** (e.g., at GraphType level):

```json
{
  "type": "object",
  "properties": {
    "nodeTypes": {
      "type": "array",
      "items": {"$ref": "#/$defs/NodeType"}
    },
    "edgeTypes": {
      "type": "array", 
      "items": {"$ref": "#/$defs/EdgeType"}
    },
    "concrete": {
      "type": "object",
      "properties": {
        "nodeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/NodeType"}
        },
        "edgeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/EdgeType"}
        }
      }
    },
    "abstract": {
      "type": "object",
      "properties": {
        "nodeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/NodeType"}
        },
        "edgeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/EdgeType"}
        }
      }
    },
    "exactlyOf": {
      "type": "object",
      "properties": {
        "concrete": {"$ref": "#/$defs/ConcretenessFacet"},
        "abstract": {"$ref": "#/$defs/ConcretenessFacet"}
      }
    },
    "subtypesOf": {
      "type": "object",
      "properties": {
        "concrete": {"$ref": "#/$defs/ConcretenessFacet"},
        "abstract": {"$ref": "#/$defs/ConcretenessFacet"}
      }
    },
    "properSubtypesOf": {
      "type": "object",
      "properties": {
        "concrete": {"$ref": "#/$defs/ConcretenessFacet"},
        "abstract": {"$ref": "#/$defs/ConcretenessFacet"}
      }
    }
  }
}
```

**Pattern for Single TI Wrapper** (e.g., around `graphType` in GraphSchemaContent):

Use `oneOf` to allow exactly one option:

```json
{
  "oneOf": [
    {
      "properties": {
        "graphType": {"$ref": "#/$defs/GraphType"}
      }
    },
    {
      "properties": {
        "concrete": {
          "type": "object",
          "properties": {
            "graphType": {"$ref": "#/$defs/GraphType"}
          }
        }
      }
    },
    {
      "properties": {
        "abstract": {
          "type": "object",
          "properties": {
            "graphType": {"$ref": "#/$defs/GraphType"}
          }
        }
      }
    }
  ]
}
```

**Supported TI Levels**:
- **0-level**: Bare properties (e.g., `nodeTypes:`, `edgeTypes:`)
- **1-level**: Concreteness facets (`concrete:`, `abstract:`, `sealed:`, `final:`)
- **2-level**: Interpretation facets (`exactlyOf:`, `subtypesOf:`, `properSubtypesOf:`)
```

---

## Location Number Verification

Based on the tasks.md file and Phase structure:

**Locations Using Single TI Wrapper (oneOf pattern)**:
- **Location 1**: GraphSchemaContent → `graphType` property (wraps the entire graphType object)
- **Location 6**: Individual NodeType content (Phase A ✅ Complete)
- **Location 7**: Individual EdgeType content (Phase B ✅ Complete)
- **Location 8**: Endpoint NodeType references in directed edges (Phase C ✅ Complete)
- **Location 9**: Endpoint NodeType references in undirected edges (Phase D ✅ Complete)

**Locations Using Sibling TI Wrappers (explicit properties without oneOf)**:
- **Location 2**: NodeTypesProperty at GraphType level (Phase E - this spec)
- **Location 3**: EdgeTypesProperty at GraphType level (Phase E - this spec)
- **Location 4**: NodeTypeItem within nodeTypes array (Phase E - this spec)
- **Location 5**: EdgeTypeItem within edgeTypes array (Phase E - this spec)

**Status Confirmation**:
- ✅ Locations 6, 7, 8, 9 are already complete from Phases A-D
- 🔄 Locations 1, 2, 3, 4, 5 are part of Phase E (current spec)
- ✅ Location 1 was verified as already working correctly (no changes needed)
- 🔄 Locations 2-5 need fixes (this spec's focus)

## Summary of Approach

### For Sibling TI Behavior (Locations 2-7 at GraphType level):
- **Use explicit properties WITHOUT oneOf**
- Add properties: `concrete:`, `abstract:`, `sealed:`, `final:`, `exactlyOf:`, `subtypesOf:`, `properSubtypesOf:`
- These can coexist as siblings with bare properties (`nodeTypes:`, `edgeTypes:`)
- Example: `graphType: { nodeTypes: [...], concrete: { edgeTypes: [...] } }`

### For Single TI Wrapper (Locations 1, 6, 7, 8):
- **Use oneOf to allow exactly one option**
- **Location 1** (GraphSchemaContent): Around `graphType` property
  - Options: bare `graphType:` OR `concrete: { graphType: ... }` OR `abstract: { graphType: ... }` etc.
  - Only ONE can be present at a time
  - Example: `graphSchema: { pathName: /x, concrete: { graphType: {...} } }`
- **Location 6** (Individual NodeType): Around single nodeType content (✅ Already complete - Phases A-D)
  - Options: bare `nodeType:` OR `concrete: { nodeType: ... }` OR `abstract: { nodeType: ... }` etc.
  - Example: `nodeTypes: [{ concrete: { nodeType: { typeLabel: Person, ... } } }]`
- **Location 7** (Individual EdgeType): Around single edgeType content (✅ Already complete - Phases A-D)
  - Options: bare `edgeType:` OR `concrete: { edgeType: ... }` OR `abstract: { edgeType: ... }` etc.
  - Example: `edgeTypes: [{ concrete: { edgeType: { directed: {...}, ... } } }]`
- **Location 8** (Endpoint NodeType): Around endpoint nodeType references (✅ Already complete - Phases C-D)
  - Options: bare `nodeType:` OR `concrete: { nodeType: ... }` OR `abstract: { nodeType: ... }` etc.
  - Example: `from: { concrete: { nodeType: { typeLabel: Person } } }`

### Shorthand Semantics:
- `abstract:` = `properSubtypesOf: { abstract: ... }`
- `concrete:` = `exactlyOf: { concrete: ... }`

---

## Design Note: Double Wrapping and TI Override (Future - Canonicalization Phase)

**Context**: At every location where TI wrappers are permitted, the schema will allow "double wrapping" where TI wrappers can be nested.

**Example of Double Wrapping**:
```yaml
subtypesOf:
  abstract:
    exactlyOf:
      concrete:
        nodeType:
          typeLabel: Person
```

**Semantics**:
- When double wrapping occurs, the **outer TI wrapper overrides the inner TI wrapper**
- In the example above, `subtypesOf: abstract:` overrides `exactlyOf: concrete:`
- The effective interpretation is `subtypesOf` with `abstract` concreteness

**Purpose**:
- This supports **importation of definitions that include TI wrappers**
- When importing a type definition that already has a TI wrapper, you can wrap it with a different TI to override the imported interpretation
- Example: Import a `concrete` type but use it as `abstract` in your schema

**Canonicalization**:
- This is **not normal behavior** and would never appear in a canonicalized YAML document
- During canonicalization, the inner TI wrapper would be removed, leaving only the outer (effective) wrapper
- Canonical form: `subtypesOf: { abstract: { nodeType: { typeLabel: Person } } }`

**Implementation Status**:
- ⏸️ **Deferred to Phase H (Canonicalization)**
- No implementation required at this stage (Phase E)
- The schema will naturally permit this structure (it won't explicitly prevent nested TI wrappers)
- Canonicalization logic will handle the override semantics and simplification

**Applies To**:
- All locations where TI wrappers are permitted (Locations 1-9)
- Both single TI wrapper locations (1, 6, 7, 8, 9) and sibling TI wrapper locations (2, 3, 4, 5)

---

## Files to Update

1. `.kiro/specs/ti-ordering-refactor/tasks.md` - Add subtask 10.1
2. `.kiro/specs/ti-ordering-refactor/design.md` - Add shorthand semantics section, update architecture section, and add double wrapping design note

