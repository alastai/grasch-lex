# Type Interpretation Schema Fix - Action Plan

## Current State

- **0/4 PC tests passing** - All fail at schema validation
- **14/14 existing examples passing** - No regressions yet
- **Core Problem**: Schema treats nodeTypes as accepting ONE wrapper, needs to accept ARRAY of partition blocks

## Root Cause

Schema currently:
```yaml
nodeTypes:
  abstract:  # ONE wrapper only
    - nodeType: Person
```

Needs to accept:
```yaml
nodeTypes:
  - abstract:  # First partition block
      - nodeType: Person
  - concrete:  # Second partition block  
      - nodeType: Company
```

## Action Plan

### Phase 1: Check Test YAML Syntax
- Verify all test files are valid YAML
- Fix any syntax errors

### Phase 2: Document Current Schema
- Map NodeTypesProperty, NodeTypesArray, NodeTypeItem
- Identify where TI wrappers are defined
- Find all 47 TI-wrappable locations

### Phase 3: Design New Schema Structure
- Create PartitionBlockItem pattern
- Define reusable TI wrapper definitions (0/1/2-level)
- Plan updates to all TI-wrappable locations

### Phase 4: Implement Schema Changes
- Update NodeTypesProperty → array of partition blocks
- Add sealed wrapper support
- Apply pattern to all TI locations

### Phase 5: Test Schema
- Run test_pc_c_equivalence.py (should pass PC validation)
- Run validate_all_examples.py (no regressions)

### Phase 6: Update Canonicalizer
- TI abbreviation expansion
- Import resolution (Phase 1 and 2)
- TI amalgamation
- Sealed expansion

### Phase 7: Complete Pipeline
- All PC forms validate ✅
- PC → C canonicalization works ✅
- C forms validate ✅
- All PC variants produce same C form ✅

## Next Steps

1. Check test YAML files for syntax errors
2. Document current schema structure
3. Design new PartitionBlockItem pattern
4. Implement schema changes
5. Test and validate

**Timeline**: 12-20 hours total
**Current Focus**: Phases 1-5 (Fix schema to accept PC forms)
