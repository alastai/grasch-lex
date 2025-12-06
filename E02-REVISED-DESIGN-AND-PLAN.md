# E.0.2 - REVISED: Edge Type Syntax Correction

**Date**: 2024-12-06  
**Status**: Ready for Implementation  
**Critical Discovery**: Edge label containers always use object form with `typeLabel:` child

---

## Executive Summary

The edge type syntax model was fundamentally misunderstood. The correct model is:

1. **Edge label containers (`via:`, `arc:`) are ALWAYS objects** with `typeLabel:` as a required child
2. **`typeLabel:` is NOT a synonym** - it's a required child property that holds the label value
3. **Endpoints are polymorphic** - they can be string references OR inline `nodeType` objects
4. **Consistent with nodeType** - both use the same pattern: container with `typeLabel:` child

---

## Correct Syntax Model

### Pattern 1: Simple Edge (No Properties)

```yaml
edgeType:
  directed:
    from: Person  # Polymorphic: string reference
    to: Person
    via:
      typeLabel: KNOWS  # Required child
```

### Pattern 2: Edge with Properties via `implies:`

```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:
      typeLabel: KNOWS  # Required child
      implies:          # Sibling to typeLabel
        propertyTypes:
          - name: since
            valueType: INTEGER
```

### Pattern 3: Edge with Subtyping via `extends:`/`adding:`

```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:
      typeLabel: KNOWS
      extends: RELATIONSHIP  # Sibling to typeLabel
      adding:                # Sibling to extends
        propertyTypes:
          - name: since
            valueType: INTEGER
```

### Pattern 4: Inline Endpoint Definition (Polymorphic Endpoint)

```yaml
edgeType:
  directed:
    from: Person  # String reference
    to:           # Inline definition
      nodeType:
        typeLabel: Cat
        extends: DomesticAnimal
        adding:
          propertyTypes:
            - name: CatRegistryChipNumber
              valueType: STRING
    via:
      typeLabel: OWNER
      implies:
        propertyTypes:
          - name: since
            valueType: INTEGER
```

---

## Key Architectural Principles

### 1. Consistent Container Pattern

Both `nodeType` and edge label containers follow the same pattern:

```yaml
# NodeType pattern
nodeType:
  typeLabel: Person      # Required child
  extends: Entity        # Optional sibling
  adding: {...}          # Optional sibling

# Edge label pattern (via/arc)
via:
  typeLabel: KNOWS       # Required child
  extends: RELATIONSHIP  # Optional sibling
  adding: {...}          # Optional sibling
```

### 2. Polymorphism at Endpoint Level

Endpoints can be:
- **String reference**: `from: Person` (references existing nodeType)
- **Inline object**: `from: { nodeType: { typeLabel: Cat, ... } }` (defines inline)

### 3. Edge Label Containers are NOT Polymorphic

`via:` and `arc:` are ALWAYS objects with `typeLabel:` as a required child.
They are NEVER simple strings.

### 4. Synonym Groups (Revised)

**Edge label containers** (mutually exclusive):
- `via:`
- `arc:`

**NOT synonyms**:
- `typeLabel:` is a CHILD property, not a synonym

**Endpoint synonyms** (still valid):
- Source: `from:`, `src:`, `source:`, `tail:`
- Destination: `to:`, `dst:`, `dest:`, `destination:`, `head:`

---

## Implementation Plan

### Phase 1: JSON Schema Updates

**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`

#### 1.1 Redefine Edge Label Containers

```json
"via": {
  "type": "object",
  "description": "Edge label container (always an object)",
  "properties": {
    "typeLabel": {
      "type": "string",
      "description": "The edge label value (required)"
    },
    "implies": {
      "$ref": "#/$defs/ImpliesPattern"
    },
    "extends": {
      "type": "string"
    },
    "adding": {
      "$ref": "#/$defs/AddingPattern"
    }
  },
  "required": ["typeLabel"],
  "additionalProperties": false
}
```

Apply same pattern to `arc:`.

#### 1.2 Update Property Ordering

**Directed edges**:
```
from → to → (via|arc) → [other properties]
```

**Undirected edges**:
```
between → and → (via|arc) → [other properties]
```

#### 1.3 Define Polymorphic Endpoints

```json
"EndpointReference": {
  "oneOf": [
    {
      "type": "string",
      "description": "Reference to existing nodeType by label"
    },
    {
      "type": "object",
      "description": "Inline nodeType definition",
      "properties": {
        "nodeType": {
          "$ref": "#/$defs/NodeTypeContent"
        }
      },
      "required": ["nodeType"],
      "additionalProperties": false
    }
  ]
}
```

#### 1.4 Remove Old Patterns

- Remove `implies:` at `edgeType` level (it's now under edge label container)
- Remove `typeLabel:` as synonym of `via:`/`arc:`
- Remove polymorphic string/object pattern for edge label containers

---

### Phase 2: Example File Updates

#### Priority 1: Simple Test Files (6 files)

**Files**:
- `test-edge-directed-via.yaml`
- `test-edge-directed-arc.yaml`
- `test-edge-directed-typelabel.yaml` (needs renaming/restructuring)
- `test-edge-undirected-via.yaml`
- `test-edge-undirected-typelabel.yaml` (needs renaming/restructuring)
- `test-edge-mixed-synonyms.yaml`

**Changes**:
```yaml
# OLD (WRONG)
via: KNOWS

# NEW (CORRECT)
via:
  typeLabel: KNOWS
```

#### Priority 2: Files with Properties

**Files**:
- `test-edge-property-ordering.yaml`
- `test-edge-extends-adding.yaml`
- Any files with `implies:`

**Changes**:
```yaml
# OLD (WRONG)
via: KNOWS
implies:
  propertyTypes: [...]

# NEW (CORRECT)
via:
  typeLabel: KNOWS
  implies:
    propertyTypes: [...]
```

#### Priority 3: Phase E Location 3 Files

**Files**:
- `test-phase-e-location-3.yaml`
- `test-phase-e-location-3-two-level.yaml`

**Changes**:
- Fix document structure (graphSchema vs catalog/graph)
- Apply correct edge label syntax
- Change inline node types to references where appropriate

#### Priority 4: Complex Schema Files

**Files**:
- `imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml`
- `lex-2026.0.3.2-snb-schema.yaml`
- `lex-2026.0.3.2-finbench-schema.yaml`
- `lex-2026.0.3.2-finbench-sf1-graph.yaml`

**Approach**: Systematic review and update

---

### Phase 3: Design Documentation Updates

**File**: `.kiro/specs/property-graph-schema/design.md`

**Updates Required**:

1. **Correct all edge type examples** to show object form
2. **Add section on polymorphism** - clarify it's at endpoint level
3. **Update synonym documentation** - remove `typeLabel:` from synonyms
4. **Add consistency note** - explain parallel with `nodeType` pattern
5. **Update property ordering rules** with correct structure

---

### Phase 4: Validation & Testing

1. **Schema validation**: Ensure schema is valid JSON Schema
2. **Simple files**: Validate all 6 simple test files
3. **Phase E Location 3**: Unblock these failing tests
4. **Regression**: Verify Phases A-D still pass
5. **Complex files**: Validate updated complex schemas

---

## Migration Guide

### For Existing YAML Files

**Step 1**: Identify all edge label usages
```bash
grep -r "via:" examples/
grep -r "arc:" examples/
```

**Step 2**: Convert string form to object form
```yaml
# Before
via: KNOWS

# After
via:
  typeLabel: KNOWS
```

**Step 3**: Move `implies:` under edge label
```yaml
# Before
via: KNOWS
implies:
  propertyTypes: [...]

# After
via:
  typeLabel: KNOWS
  implies:
    propertyTypes: [...]
```

**Step 4**: Convert inline endpoints to references (where appropriate)
```yaml
# Before (unnecessary inline)
from:
  nodeType:
    typeLabel: Person

# After (simple reference)
from: Person
```

---

## Success Criteria

- [ ] JSON Schema correctly defines edge label containers as objects
- [ ] `typeLabel:` is required child of edge label containers
- [ ] Endpoints are polymorphic (string OR inline object)
- [ ] All simple test files validate successfully
- [ ] Phase E Location 3 files validate successfully
- [ ] Design documentation shows correct structure
- [ ] Phases A-D regression tests still pass
- [ ] Complex files updated and validated
- [ ] No files use old string form for edge labels

---

## Breaking Changes

This is a **breaking change** that affects:

1. **All edge type definitions** - must use object form for `via:`/`arc:`
2. **Property ordering** - `implies:` moves under edge label
3. **Synonym understanding** - `typeLabel:` is not a synonym
4. **Consistency model** - now parallel with `nodeType` pattern

---

## Next Steps

1. **Review this design** with user
2. **Update JSON Schema** (Phase 1)
3. **Update simple test files** (Phase 2, Priority 1)
4. **Validate changes** (Phase 4)
5. **Update remaining files** (Phase 2, Priorities 2-4)
6. **Update documentation** (Phase 3)
7. **Final validation** (Phase 4)

---

## Questions for Review

1. Is the object form for edge labels correct?
2. Should we support any shorthand syntax?
3. Are there any other files that need updating?
4. Should we create migration scripts?
5. Ready to proceed with implementation?
