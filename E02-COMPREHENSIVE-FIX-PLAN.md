# E.0.2 - Comprehensive Fix Plan: Edge Label Structure with `implies:`

**Date**: 2024-12-04  
**Issue**: Edge label properties must support both string and object forms  
**Status**: Ready to implement

## Confirmed Correct Structure

### Pattern 1: Simple Edge (No Properties)
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS  # String - simple label
```

### Pattern 2: Edge with Properties
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS  # Label value
      implies:  # Child of via:
        propertyTypes:  # Child of implies:
        - name: since
          valueType: INTEGER
```

## Implementation Plan

### Phase 1: JSON Schema Updates (CRITICAL)

**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`

**Changes Required**:

1. **Redefine edge label properties** (`via:`, `arc:`, `typeLabel:`):
   ```json
   "via": {
     "oneOf": [
       {
         "type": "string",
         "description": "Simple edge label"
       },
       {
         "type": "object",
         "description": "Edge label with properties",
         "properties": {
           "implies": {
             "type": "object",
             "properties": {
               "labels": {...},
               "propertyTypes": {...}
             }
           }
         },
         "required": ["implies"]
       }
     ]
   }
   ```

2. **Apply same pattern to synonyms**: `arc:`, `typeLabel:`

3. **Update `extends:`/`adding:` pattern** to work with this structure

4. **Remove old `implies:` at `edgeType` level** (it's now under edge label)

### Phase 2: Example File Updates

**Priority 1 - Simple Test Files** (6 files):
- `test-edge-directed-via.yaml`
- `test-edge-directed-arc.yaml`
- `test-edge-directed-typelabel.yaml`
- `test-edge-undirected-via.yaml`
- `test-edge-undirected-typelabel.yaml`
- `test-edge-mixed-synonyms.yaml`

**Changes**: 
- Keep simple edges as strings
- Move any `implies:` blocks to be children of edge label property
- Change inline node types to type references

**Priority 2 - New Test Files** (created in Phase 2):
- `test-edge-property-ordering.yaml`
- `test-edge-extends-adding.yaml`
- Others created recently

**Changes**: Update to new structure

**Priority 3 - Complex Files**:
- `imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml` (~50+ edges)
- `lex-2026.0.3.2-snb-schema.yaml`
- `lex-2026.0.3.2-finbench-schema.yaml`
- `lex-2026.0.3.2-finbench-sf1-graph.yaml`

**Changes**: Systematic review and update

### Phase 3: Phase E Location 3 Files

**Files**:
- `test-phase-e-location-3.yaml`
- `test-phase-e-location-3-two-level.yaml`

**Changes**:
- Fix document structure issues
- Fix edge label structure (via: as object with implies:)
- Change inline node types to references

### Phase 4: Design Documentation

**File**: `.kiro/specs/property-graph-schema/design.md`

**Changes**:
- Update all edge type examples
- Show both patterns (string vs object)
- Clarify `implies:` is child of edge label
- Update property ordering rules

### Phase 5: Validation & Testing

1. Run schema validation on all updated files
2. Verify Phases A-D still pass (regression test)
3. Test Phase E Location 3 files
4. Document any issues found

## Execution Order

1. **Schema first** - Must be correct before examples can validate
2. **Simple test files** - Quick wins, verify schema works
3. **Phase E Location 3** - Unblock these failing tests
4. **Design docs** - Document the correct patterns
5. **Complex files** - Systematic updates
6. **Final validation** - Ensure everything passes

## Key Points

- Edge label properties are **polymorphic**: string OR object
- When object form is used, `implies:` is **required** child
- `propertyTypes:` and `labels:` are children of `implies:`
- This is a **major structural change** from previous understanding
- ALL files with edge types need review

## Success Criteria

- [ ] JSON Schema correctly defines polymorphic edge label properties
- [ ] All simple test files validate successfully
- [ ] Phase E Location 3 files validate successfully
- [ ] Design documentation shows correct structure
- [ ] Phases A-D regression tests still pass
- [ ] Complex files updated and validated

## Next Step

**START WITH**: JSON Schema updates (Phase 1)

This is the foundation - nothing else can be fixed until the schema is correct.

