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
  - Where we want to permit a single TI wrapper (e.g., around `graphType` in GraphSchemaContent), use oneOf
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

## Summary of Approach

### For Sibling TI Behavior (Locations 2-7 at GraphType level):
- **Use explicit properties WITHOUT oneOf**
- Add properties: `concrete:`, `abstract:`, `sealed:`, `final:`, `exactlyOf:`, `subtypesOf:`, `properSubtypesOf:`
- These can coexist as siblings with bare properties (`nodeTypes:`, `edgeTypes:`)
- Example: `graphType: { nodeTypes: [...], concrete: { edgeTypes: [...] } }`

### For Single TI Wrapper (Location 1 - GraphSchemaContent):
- **Use oneOf to allow exactly one option**
- Options: bare `graphType:` OR `concrete: { graphType: ... }` OR `abstract: { graphType: ... }` etc.
- Only ONE can be present at a time
- Example: `graphSchema: { pathName: /x, concrete: { graphType: {...} } }`

### Shorthand Semantics:
- `abstract:` = `properSubtypesOf: { abstract: ... }`
- `concrete:` = `exactlyOf: { concrete: ... }`

---

## Files to Update

1. `.kiro/specs/ti-ordering-refactor/tasks.md` - Add subtask 10.1
2. `.kiro/specs/ti-ordering-refactor/design.md` - Add shorthand semantics section and update architecture section

