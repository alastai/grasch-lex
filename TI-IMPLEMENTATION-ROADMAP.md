# Type Interpretation (TI) Implementation Roadmap

## Overview

This roadmap outlines the complete implementation and testing plan for Type Interpretation (TI) semantics, including sealed behavior, two-phase imports, and comprehensive validation.

**Reference Documents**:
- `TI-SEMANTICS-COMPLETE.md` - Complete TI semantics specification
- `TI-LOCATION-AUDIT.md` - All 47 TI-wrappable locations
- `TASK-2-REVISION-NEEDED.md` - Schema structure alignment
- `.kiro/specs/import-schema-consistency/` - Spec documents to update

---

## Phase 1: Update Spec Documents ✅ READY TO START

**Goal**: Incorporate TI-SEMANTICS-COMPLETE.md into import-schema-consistency spec

**Tasks**:
1. Update `requirements.md` with:
   - Sealed semantics correction (cannot seal abstract-only sets, makes non-abstract types final)
   - Valid TI combinations table
   - Complete glossary entries (sealed, final, extensible)
   - Edge endpoint exception clarification

2. Update `design.md` with:
   - Complete TI semantics from TI-SEMANTICS-COMPLETE.md
   - Sealed behavior examples
   - Two-phase import examples
   - Valid TI combinations documentation
   - Schema structure alignment

3. Add comprehensive examples showing:
   - Sealed with mixed abstract/concrete types
   - Phase 1 imports (import TI + content)
   - Phase 2 imports (import content only, strip TI)
   - Singleton vs array distinctions

**Deliverables**:
- Updated requirements.md
- Updated design.md
- User review and approval

---

## Phase 2: JSON Schema Updates

**Goal**: Apply TI patterns to lex-2026.0.3.2.schema.json

**Based on**: `.kiro/specs/import-schema-consistency/tasks.md`

### Task 2: Create Reusable Definitions
**Status**: Ready to execute after Phase 1 approval

**Deliverables**:
- `TIWrapperContentNode` - Content within node type TI wrappers
- `TIWrapperContentEdge` - Content within edge type TI wrappers  
- `PartitionBlockItemNode` - Items in nodeTypes arrays
- `PartitionBlockItemEdge` - Items in edgeTypes arrays

**Key Features**:
- anyOf pattern for singleton vs multi-element sets
- Phase 2 import support (import content only)
- Proper indentation-based set delimitation

### Tasks 3-6: Apply to All TI-Wrappable Locations
**Locations**: All 47 locations from TI-LOCATION-AUDIT.md

**Categories**:
- Task 3: Top-level xTypes properties (2 locations)
- Task 4: GraphType pattern properties (12 locations)
- Task 5: NodeTypeItem/EdgeTypeItem wrappers (10 locations)
- Task 6: Property-level TI wrappers (18 locations)

### Task 7: Validate Schema Structure
**Deliverables**:
- Schema validation passes
- All patterns correctly applied
- No regressions in existing functionality

---

## Phase 3: YAML Test Examples

**Goal**: Create comprehensive test suite showing PC→C equivalence

### Test Suite Structure

#### A. Without Imports (PC with abbreviations)
**Purpose**: Test single-level TI abbreviations

```yaml
# test-pc-abbreviations.yaml
graphType:
  nodeTypes:
    abstract:  # Shorthand for subtypesOf:abstract
      - nodeType: {typeLabel: Person}
    concrete:  # Shorthand for exactlyOf:concrete
      - nodeType: {typeLabel: Company}
```

#### B. With Phase 1 Imports (import TI + content)
**Purpose**: Test importing entire TI wrapper with types

```yaml
# test-pc-phase1-import.yaml
graphType:
  nodeTypes:
    - import: "person-types.yaml"  # Imports TI wrapper + types

# person-types.yaml:
subtypesOf:
  abstract:
    - nodeType: {typeLabel: Person}
```

#### C. With Phase 2 Imports (import content only)
**Purpose**: Test TI override (import content, reinterpret with outer TI)

```yaml
# test-pc-phase2-import.yaml
graphType:
  nodeTypes:
    - exactlyOf:
        concrete:
          import: "person-types.yaml"  # Strips subtypesOf:abstract, applies exactlyOf:concrete
```

#### D. Sealed Examples
**Purpose**: Test sealed semantics (makes non-abstract types final)

```yaml
# test-pc-sealed.yaml
graphType:
  nodeTypes:
    - sealed:
        nodeTypes:
          - subtypesOf:
              abstract:
                nodeType: {typeLabel: Place}
          - nodeType: {typeLabel: City, extends: Place}  # Made final by sealed
          - nodeType: {typeLabel: Country, extends: Place}  # Made final by sealed
```

#### E. Expected Canonical Form
**Purpose**: All PC variants should produce this C form

```yaml
# expected-canonical.yaml
graphType:
  nodeTypes:
    - subtypesOf:
        abstract:
          - nodeType: {typeLabel: Person}
    - exactlyOf:
        concrete:
          - nodeType: {typeLabel: Company}
    - subtypesOf:
        abstract:
          - nodeType: {typeLabel: Place}
    - exactlyOf:
        final:
          - nodeType: {typeLabel: City, extends: Place}
          - nodeType: {typeLabel: Country, extends: Place}
```

### Test Files to Create

1. `test-pc-abbreviations.yaml` - Single-level TI abbreviations
2. `test-pc-phase1-import.yaml` - Phase 1 imports
3. `test-pc-phase2-import.yaml` - Phase 2 imports (TI override)
4. `test-pc-sealed.yaml` - Sealed hierarchies
5. `test-pc-mixed.yaml` - Combination of all patterns
6. `expected-canonical.yaml` - Expected C form for all variants
7. Import files:
   - `person-types.yaml`
   - `company-types.yaml`
   - `place-hierarchy.yaml`

---

## Phase 4: Canonicalizer Updates

**Goal**: Ensure canonicalizer handles all TI patterns correctly

### Required Updates to `src/grasch/canonicalizing_preprocessor.py`

#### 4.1 TI Abbreviation Expansion
**Current**: May not handle all abbreviations
**Required**:
- `abstract:` → `subtypesOf: abstract:`
- `concrete:` → `exactlyOf: concrete:`
- `final:` → `exactlyOf: final:`
- `properSubtypesOf:` → `subtypesOf: abstract:`

#### 4.2 Import Resolution
**Current**: Basic import support
**Required**:
- Phase 1: Import entire TI wrapper + content (preserve TI)
- Phase 2: Import content only (strip TI, allow outer TI to reinterpret)
- Handle nested imports
- Resolve import paths correctly

#### 4.3 TI Amalgamation
**Current**: May not consolidate duplicate TIs
**Required**:
- Merge multiple `exactlyOf:concrete` blocks into one
- Merge multiple `subtypesOf:abstract` blocks into one
- Preserve type order within merged blocks

#### 4.4 Sealed Expansion
**Current**: May not handle sealed semantics
**Required**:
- Identify sealed blocks
- Make all non-abstract types within sealed blocks final
- Preserve abstract types as abstract
- Add semantic marker for "no other subtypes allowed"

#### 4.5 Collection Consolidation
**Current**: May already work
**Verify**:
- All `nodeTypes` instances → ONE `nodeTypes` collection
- All `edgeTypes` instances → ONE `edgeTypes` collection

---

## Phase 5: Validation Pipeline

**Goal**: Comprehensive PC→C→Validate pipeline

### Test Script: `test_pc_c_equivalence.py`

```python
"""
Test PC to C canonicalization equivalence.

Validates that:
1. All PC forms validate against schema
2. PC forms canonicalize to C form
3. C forms validate against schema
4. All PC variants produce the same C form
"""

def test_pc_c_equivalence():
    """Test that all PC variants produce same C form."""
    
    # Load test files
    pc_abbreviations = load_yaml("test-pc-abbreviations.yaml")
    pc_phase1 = load_yaml("test-pc-phase1-import.yaml")
    pc_phase2 = load_yaml("test-pc-phase2-import.yaml")
    pc_sealed = load_yaml("test-pc-sealed.yaml")
    expected_c = load_yaml("expected-canonical.yaml")
    
    # Test each PC variant
    for name, pc_form in [
        ("abbreviations", pc_abbreviations),
        ("phase1-import", pc_phase1),
        ("phase2-import", pc_phase2),
        ("sealed", pc_sealed),
    ]:
        # 1. Validate PC form
        assert validate_against_schema(pc_form), f"{name}: PC form invalid"
        
        # 2. Canonicalize PC → C
        c_form = canonicalize(pc_form)
        
        # 3. Validate C form
        assert validate_against_schema(c_form), f"{name}: C form invalid"
        
        # 4. Verify C form matches expected
        assert c_form == expected_c, f"{name}: C form doesn't match expected"
        
        print(f"✅ {name}: PC→C equivalence verified")
```

### Validation Checks

1. **PC Form Validation**
   - Validates against lex-2026.0.3.2.schema.json
   - Accepts abbreviations
   - Accepts imports
   - Accepts sealed blocks

2. **Canonicalization**
   - Expands abbreviations
   - Resolves imports (Phase 1 and Phase 2)
   - Amalgamates duplicate TIs
   - Expands sealed to final
   - Consolidates collections

3. **C Form Validation**
   - Validates against same schema
   - No abbreviations
   - No imports
   - Two-level TI structure
   - Single nodeTypes/edgeTypes collections

4. **Equivalence Check**
   - All PC variants → same C form
   - Structural equality
   - Semantic equivalence

---

## Phase 6: API Tests

**Goal**: Ensure API correctly interprets TI semantics

### Test Areas

#### 6.1 Type Interpretation Queries
**File**: `tests/test_type_interpretation_api.py`

```python
def test_is_abstract():
    """Test isAbstract() method."""
    # subtypesOf:abstract → True
    # exactlyOf:concrete → False
    # sealed:abstract → True

def test_is_final():
    """Test isFinal() method."""
    # exactlyOf:final → True
    # sealed:concrete → True (made final by sealed)
    # subtypesOf:concrete → False

def test_is_sealed():
    """Test isSealed() method."""
    # Types within sealed block → True
    # Types outside sealed block → False
```

#### 6.2 Subtype Relationships with Sealed
**File**: `tests/test_sealed_subtyping.py`

```python
def test_sealed_prevents_extension():
    """Test that sealed hierarchies cannot be extended."""
    # Define sealed hierarchy: Place, City, Country
    # Attempt to add new subtype of Place → should fail
    # Attempt to extend City → should fail (made final by sealed)

def test_sealed_abstract_allows_defined_subtypes():
    """Test that abstract types in sealed allow defined subtypes."""
    # Place is abstract in sealed block
    # City and Country are valid subtypes (defined in sealed block)
    # No other subtypes allowed
```

#### 6.3 Import Handling in API
**File**: `tests/test_api_imports.py`

```python
def test_api_loads_phase1_imports():
    """Test API correctly loads Phase 1 imports."""
    # Load schema with Phase 1 imports
    # Verify TI preserved
    # Verify types loaded correctly

def test_api_loads_phase2_imports():
    """Test API correctly loads Phase 2 imports (TI override)."""
    # Load schema with Phase 2 imports
    # Verify outer TI applied
    # Verify inner TI stripped
```

#### 6.4 Sealed Semantic Enforcement
**File**: `tests/test_sealed_semantics.py`

```python
def test_sealed_makes_concrete_final():
    """Test that sealed makes non-abstract types final."""
    # Load sealed hierarchy
    # Verify concrete types are final
    # Verify abstract types remain abstract

def test_sealed_closure():
    """Test that sealed closes the hierarchy."""
    # Load sealed hierarchy
    # Verify no additional subtypes can be added
    # Verify semantic marker present
```

---

## Success Criteria

### Phase 1: Spec Documents
- [ ] requirements.md updated with sealed semantics
- [ ] design.md updated with complete TI semantics
- [ ] Examples added for all patterns
- [ ] User review and approval

### Phase 2: JSON Schema
- [ ] Reusable definitions created (Task 2)
- [ ] All 47 locations updated (Tasks 3-6)
- [ ] Schema validation passes (Task 7)
- [ ] No regressions in existing functionality

### Phase 3: YAML Tests
- [ ] Test files created for all PC variants
- [ ] Import files created
- [ ] Expected canonical form defined
- [ ] All tests validate against schema

### Phase 4: Canonicalizer
- [ ] TI abbreviation expansion works
- [ ] Phase 1 imports resolve correctly
- [ ] Phase 2 imports resolve correctly (TI override)
- [ ] TI amalgamation works
- [ ] Sealed expansion works
- [ ] Collection consolidation works

### Phase 5: Validation Pipeline
- [ ] PC forms validate
- [ ] Canonicalization produces correct C forms
- [ ] C forms validate
- [ ] All PC variants produce same C form
- [ ] Test script passes

### Phase 6: API Tests
- [ ] Type interpretation queries work
- [ ] Sealed subtyping enforced
- [ ] Import handling works
- [ ] Sealed semantics enforced
- [ ] All API tests pass

---

## Timeline Estimate

- **Phase 1**: 1-2 hours (spec document updates)
- **Phase 2**: 4-6 hours (JSON Schema updates)
- **Phase 3**: 2-3 hours (YAML test examples)
- **Phase 4**: 3-4 hours (canonicalizer updates)
- **Phase 5**: 2-3 hours (validation pipeline)
- **Phase 6**: 3-4 hours (API tests)

**Total**: 15-22 hours

---

## Next Steps

1. ✅ Save this roadmap
2. ✅ Commit all changes to GitHub
3. ▶️ Start Phase 1: Update spec documents
4. Get user review and approval
5. Proceed with Phase 2: JSON Schema updates

---

## Notes

- This roadmap assumes the canonicalizer already has basic import support
- API tests may reveal additional requirements
- Sealed semantics are the most complex part - extra testing needed
- Two-phase imports require careful handling in both schema and canonicalizer
- All changes must maintain backward compatibility with existing examples
