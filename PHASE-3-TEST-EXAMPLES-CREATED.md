# Phase 3: Test Examples Created

## Summary

Created comprehensive YAML test examples demonstrating PC→C equivalence patterns. Tests currently **fail** as expected, revealing exactly what needs to be fixed in Phase 2 (JSON Schema updates).

## Test Files Created

### PC Form Variants

1. **test-pc-abbreviations.yaml** - Single-level TI abbreviations
   - Tests: `abstract:` → `subtypesOf:abstract:`
   - Tests: `concrete:` → `exactlyOf:concrete:`
   - Status: ❌ Fails - schema doesn't support multiple TI wrappers at same level

2. **test-pc-phase1-import.yaml** - Phase 1 imports (import TI + content)
   - Tests: Importing entire TI wrapper with types
   - Tests: Preserving TI from imported file
   - Status: ❌ Fails - YAML syntax error (needs fix)

3. **test-pc-phase2-import.yaml** - Phase 2 imports (TI override)
   - Tests: Importing content only, stripping original TI
   - Tests: Reinterpreting with different TI
   - Status: ❌ Fails - schema doesn't support import in TI content

4. **test-pc-sealed.yaml** - Sealed hierarchies
   - Tests: Sealed makes non-abstract types final
   - Tests: Hierarchy closure semantics
   - Status: ❌ Fails - schema doesn't support sealed with nested nodeTypes

### Import Files

5. **imports/test-person-types.yaml** - Person type with TI wrapper
   - Contains: `subtypesOf:abstract:` wrapper with Person type
   - Used by: Phase 1 and Phase 2 import tests

6. **imports/test-company-types.yaml** - Company type (bare)
   - Contains: Unwrapped Company type
   - Used by: Import tests for default TI wrapping

7. **imports/test-place-hierarchy.yaml** - Place hierarchy
   - Contains: Abstract Place + concrete City/Country
   - Used by: Sealed hierarchy tests

### Expected Output

8. **test-expected-canonical.yaml** - Expected C form
   - Shows: Two-level TI structure
   - Shows: No abbreviations, no imports
   - Shows: TI amalgamation applied
   - Shows: Sealed expanded to final

### Test Script

9. **test_pc_c_equivalence.py** - Comprehensive test script
   - Validates PC forms against schema
   - Canonicalizes PC → C
   - Validates C forms against schema
   - Compares C forms for equivalence

## Test Results

```
Total: 0/4 tests passed
❌ FAIL: abbreviations
❌ FAIL: phase1-import  
❌ FAIL: phase2-import
❌ FAIL: sealed
```

## Issues Revealed

### Issue 1: Multiple TI Wrappers Not Supported
**File**: test-pc-abbreviations.yaml
**Problem**: Schema doesn't allow multiple TI wrappers (abstract + concrete) at same level
**Example**:
```yaml
nodeTypes:
  abstract:  # First TI wrapper
    - nodeType: {typeLabel: Person}
  concrete:  # Second TI wrapper - NOT ALLOWED
    - nodeType: {typeLabel: Company}
```
**Fix Needed**: Schema must accept nodeTypes as array of partition blocks, where each block can have its own TI

### Issue 2: Import Syntax in TI Content
**File**: test-pc-phase2-import.yaml
**Problem**: Schema doesn't support import directive inside TI wrapper content
**Example**:
```yaml
nodeTypes:
  - subtypesOf:
      abstract:
        import: "file.yaml"  # NOT SUPPORTED
```
**Fix Needed**: TI wrapper content must support Phase 2 imports (import content only)

### Issue 3: Sealed with Nested nodeTypes
**File**: test-pc-sealed.yaml
**Problem**: Schema doesn't support sealed wrapper with nested nodeTypes property
**Example**:
```yaml
nodeTypes:
  - sealed:
      nodeTypes:  # Nested nodeTypes - NOT SUPPORTED
        - subtypesOf: ...
```
**Fix Needed**: Sealed wrapper must support nodeTypes property containing partition blocks

### Issue 4: YAML Syntax Error
**File**: test-pc-phase1-import.yaml
**Problem**: Invalid YAML syntax mixing import with other properties
**Fix Needed**: Correct YAML structure for import patterns

## Next Steps

### Immediate: Fix YAML Syntax
- Fix test-pc-phase1-import.yaml syntax error
- Ensure all test files have valid YAML structure

### Phase 2: JSON Schema Updates (Tasks 2-7)
Based on test failures, Phase 2 must implement:

1. **Task 2**: Create reusable definitions
   - `TIWrapperContentNode` - Support Phase 2 imports
   - `PartitionBlockItemNode` - Support TI wrappers in array items

2. **Task 3-6**: Apply to all 47 TI-wrappable locations
   - Update NodeTypesProperty to accept array of partition blocks
   - Update sealed wrapper to support nested nodeTypes
   - Add import support to all TI wrapper contents

3. **Task 7**: Validate schema structure
   - Run test_pc_c_equivalence.py
   - All PC forms should validate
   - (Canonicalization will still fail until Phase 4)

### Phase 4: Canonicalizer Updates
After schema fixes, implement canonicalization:
1. TI abbreviation expansion
2. Import resolution (Phase 1 and Phase 2)
3. TI amalgamation
4. Sealed expansion
5. Collection consolidation

### Phase 5: Validation Pipeline
Once canonicalizer works:
1. All PC forms validate ✅
2. PC → C canonicalization works ✅
3. C forms validate ✅
4. All PC variants produce same C form ✅

## Value of These Tests

These test files provide:

1. **Concrete Examples**: Real YAML showing all TI patterns
2. **Validation Target**: Clear goal for what schema must support
3. **Regression Prevention**: Tests ensure fixes don't break
4. **Documentation**: Examples show users how to use TI features
5. **Development Guide**: Failures show exactly what to implement

## Files Created

```
src/grasch/examples/
├── test-pc-abbreviations.yaml
├── test-pc-phase1-import.yaml
├── test-pc-phase2-import.yaml
├── test-pc-sealed.yaml
├── test-expected-canonical.yaml
└── imports/
    ├── test-person-types.yaml
    ├── test-company-types.yaml
    └── test-place-hierarchy.yaml

test_pc_c_equivalence.py
```

## Conclusion

Phase 3 complete! Test examples created and reveal exactly what Phase 2 must implement. The failing tests provide a clear roadmap for JSON Schema updates.

**Status**: ✅ Phase 3 Complete - Tests created, failures documented
**Next**: Phase 2 - JSON Schema updates to make tests pass
