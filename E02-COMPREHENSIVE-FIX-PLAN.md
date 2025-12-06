# E.0.2 - Comprehensive Fix Plan: Edge Label Structure (REVISED)

**Date**: 2024-12-06 (Updated)  
**Issue**: Edge label containers must always be objects with `typeLabel:` child  
**Status**: Ready to implement  
**Context**: Design iteration for clean, correct first implementation

## CRITICAL CORRECTION (2024-12-06)

**Previous understanding was incorrect**: Edge labels cannot be polymorphic (string OR object) due to YAML constraints.

**Correct understanding**: 
- Edge label containers (`via:`, `arc:`) are ALWAYS objects
- `typeLabel:` is a REQUIRED child property (not a synonym)
- Polymorphism is at the ENDPOINT level (string reference OR inline nodeType)
- This makes the pattern consistent with `nodeType`

## Confirmed Correct Structure

### Pattern 1: Simple Edge (No Properties)
```yaml
edgeType:
  directed:
    from: Person  # Polymorphic endpoint: string reference
    to: Person
    via:
      typeLabel: KNOWS  # Required child of via
```

### Pattern 2: Edge with Properties
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:
      typeLabel: KNOWS  # Required child
      implies:          # Sibling to typeLabel
        propertyTypes:  # Child of implies
        - name: since
          valueType: INTEGER
```

### Pattern 3: Edge with Subtyping
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

### Pattern 4: Polymorphic Endpoint (Inline NodeType)
```yaml
edgeType:
  directed:
    from: Person  # String reference
    to:           # Inline definition (polymorphic endpoint)
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

## Implementation Plan

### Phase 1: JSON Schema Updates (CRITICAL)

**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`

**Changes Required**:

1. **Redefine edge label containers** (`via:`, `arc:`) as ALWAYS objects:
   ```json
   "via": {
     "type": "object",
     "description": "Edge label container (always an object)",
     "properties": {
       "typeLabel": {
         "type": "string",
         "description": "The edge label value (REQUIRED)"
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

2. **Apply same pattern to `arc:`** (synonym of `via:`)

3. **Remove `typeLabel:` as a synonym** - it's now a CHILD property only

4. **Define polymorphic endpoints**:
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
         "required": ["nodeType"]
       }
     ]
   }
   ```

5. **Remove old `implies:` at `edgeType` level** (it's now under edge label container)

### Phase 2: Example File Updates

**Priority 1 - Simple Test Files** (6 files):
- `test-edge-directed-via.yaml`
- `test-edge-directed-arc.yaml`
- `test-edge-directed-typelabel.yaml` (needs restructuring)
- `test-edge-undirected-via.yaml`
- `test-edge-undirected-typelabel.yaml` (needs restructuring)
- `test-edge-mixed-synonyms.yaml`

**Changes**: 
```yaml
# INCORRECT FORM
via: KNOWS

# CORRECT FORM
via:
  typeLabel: KNOWS
```
- Update all edge labels to use object form
- Move any `implies:` blocks to be children of edge label container
- Adjust inline node types to type references where appropriate

**Priority 2 - Files with Properties**:
- `test-edge-property-ordering.yaml`
- `test-edge-extends-adding.yaml`
- Any files with `implies:` or `extends:`/`adding:`

**Changes**: 
```yaml
# INCORRECT FORM
via: KNOWS
implies:
  propertyTypes: [...]

# CORRECT FORM
via:
  typeLabel: KNOWS
  implies:
    propertyTypes: [...]
```

**Priority 3 - Complex Files**:
- `imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml` (~50+ edges)
- `lex-2026.0.3.2-snb-schema.yaml`
- `lex-2026.0.3.2-finbench-schema.yaml`
- `lex-2026.0.3.2-finbench-sf1-graph.yaml`

**Changes**: Systematic update to correct structure

### Phase 3: Phase E Location 3 Files

**Files**:
- `test-phase-e-location-3.yaml`
- `test-phase-e-location-3-two-level.yaml`

**Changes**:
- Correct document structure
- Update edge label structure (via: as object with implies:)
- Adjust inline node types to references

### Phase 4: Design Documentation

**File**: `.kiro/specs/property-graph-schema/design.md`

**Changes**:
- Update all edge type examples
- Show both patterns (string vs object)
- Clarify `implies:` is child of edge label
- Update property ordering rules

### Phase 5: Design Documentation Updates

**File**: `.kiro/specs/property-graph-schema/design.md`

**Changes**:
- Update all edge type examples to show object form
- Add section explaining polymorphism is at endpoint level
- Update synonym documentation (clarify `typeLabel:` is a child property)
- Add note on consistency with `nodeType` pattern
- Update property ordering rules with correct structure

---

## E.0.3 Scope (Validation & Testing)

The following activities are part of E.0.3, NOT E.0.2:

1. Run schema validation on all updated files
2. Verify Phases A-D still pass
3. Test Phase E Location 3 files
4. Document any issues found
5. Create validation scripts if needed

## Execution Order

1. **Schema first** - Must be correct before examples can validate
2. **Simple test files** - Quick wins, verify schema works
3. **Phase E Location 3** - Unblock these failing tests
4. **Design docs** - Document the correct patterns
5. **Complex files** - Systematic updates
6. **Final validation** - Ensure everything passes

## Key Architectural Principles

1. **Consistent Container Pattern**: Both `nodeType` and edge label containers (`via:`, `arc:`) follow the same pattern - always objects with `typeLabel:` as required child

2. **Polymorphism at Endpoint Level**: Endpoints can be string references OR inline `nodeType` objects

3. **Edge Label Containers are NOT Polymorphic**: `via:` and `arc:` are ALWAYS objects, NEVER strings

4. **Synonym Groups (Revised)**:
   - Edge label containers: `via:`, `arc:` (mutually exclusive)
   - `typeLabel:` is a CHILD property, NOT a synonym
   - Endpoint synonyms still valid: `from:`/`src:`/`source:`/`tail:` and `to:`/`dst:`/`dest:`/`destination:`/`head:`

## E.0.2 Success Criteria

- [ ] JSON Schema correctly defines edge label containers as objects with required `typeLabel:`
- [ ] JSON Schema defines polymorphic endpoints (string OR inline object)
- [ ] All simple test files updated to use object form
- [ ] All files with properties updated (`implies:`, `extends:`/`adding:`)
- [ ] Phase E Location 3 files updated
- [ ] Complex schema files updated
- [ ] Design documentation updated with correct examples
- [ ] All files use correct object form for edge labels

## E.0.3 Success Criteria (Validation Phase)

- [ ] All updated files validate against schema
- [ ] Phases A-D tests still pass
- [ ] Phase E Location 3 files validate successfully
- [ ] No validation errors in any example files

## Next Steps

1. **Review this plan** with user
2. **Implement Phase 1**: JSON Schema updates
3. **Implement Phase 2**: Example file updates (all priorities)
4. **Implement Phase 5**: Design documentation updates
5. **Move to E.0.3**: Validation and testing

