# TI Simplification Implementation - Backup Plan

**Date**: 2024-12-11  
**Purpose**: Document all files that will be modified during the unified TI simplification implementation and create comprehensive backups.

## Files to be Modified

### 1. JSON Schema Files
- `src/grasch/schemas/lex-2026.0.3.2.schema.json` - Main schema file requiring major updates for single-level TI system

### 2. Test Files (Phase A-E)
- `src/grasch/examples/test-phase-a-corrected.yaml` - Phase A test file
- `src/grasch/examples/test-phase-b-edgetype-ti.yaml` - Phase B test file  
- `src/grasch/examples/test-phase-c-endpoint-ti.yaml` - Phase C test file
- `test-phase-d.yaml` - Phase D test file
- `src/grasch/examples/test-phase-e-location-2.yaml` - Phase E Location 2 test
- `src/grasch/examples/test-phase-e-location-2-two-level.yaml` - Phase E Location 2 two-level test
- `src/grasch/examples/test-phase-e-location-3.yaml` - Phase E Location 3 test
- `src/grasch/examples/test-phase-e-location-3-two-level.yaml` - Phase E Location 3 two-level test
- `src/grasch/examples/test-phase-e-locations-2-3.yaml` - Phase E combined test
- `src/grasch/examples/test-phase-e-locations-2-3-advanced.yaml` - Phase E advanced test
- `src/grasch/examples/test-phase-e-locations-4-5.yaml` - Phase E array subsequence test
- `src/grasch/examples/test-phase-e-array-subsequence-ti.yaml` - Phase E array test

### 3. Sibling TI Test Files
- `src/grasch/examples/test-siblings-all-1-level.yaml`
- `src/grasch/examples/test-siblings-all-2-level.yaml`
- `src/grasch/examples/test-siblings-mixed-0-1-level.yaml`
- `src/grasch/examples/test-siblings-mixed-0-2-level.yaml`
- `src/grasch/examples/test-siblings-complex.yaml`
- `src/grasch/examples/test-siblings-interleaved.yaml`
- `src/grasch/examples/test-siblings-bare-only.yaml`

### 4. Complex Schema Files
- `src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml` - SNB schema
- `src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml` - FinBench schema
- `src/grasch/examples/lex-2026.0.3.2-finbench-sf1-graph.yaml` - FinBench graph
- `src/grasch/examples/imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml` - Edge syntax examples
- `src/grasch/examples/lex-2026.0.3.2-comprehensive-wrappers.yaml` - Comprehensive wrappers
- `src/grasch/examples/lex-2026.0.3.2-two-level-wrappers.yaml` - Two-level wrappers

### 5. Validation Scripts
- `validate_phase_a_corrected.py` - Phase A validation
- `validate_phase_b.py` - Phase B validation
- `validate_phase_c.py` - Phase C validation
- `validate_phase_d.py` - Phase D validation
- `validate_phase_e.py` - Phase E validation
- `validate_phase_e_locations_2_3.py` - Phase E locations 2-3 validation
- `validate_phase_e_locations_4_5.py` - Phase E locations 4-5 validation
- `validate_sibling_ti_wrappers.py` - Sibling TI validation

## Backup Strategy

### Backup Naming Convention
- Original file: `filename.ext`
- Backup file: `filename.ext.backup-ti-simplification-2024-12-11`

### Backup Locations
- Schema backups: Same directory as original
- Test file backups: Same directory as original  
- Validation script backups: Same directory as original

## Backup Status
- [x] JSON Schema files backed up (1 file)
- [x] Phase A-E test files backed up (12 files)
- [x] Sibling TI test files backed up (7 files)
- [x] Complex schema files backed up (6 files)
- [x] Validation scripts backed up (8 files)
- [x] Backup verification completed

**Total Files Backed Up**: 34 files
**Backup Verification**: All backups created successfully with naming convention `filename.ext.backup-ti-simplification-2024-12-11`

## Implementation Phases After Backup
1. **Phase 1**: Schema Simplification (Tasks 1-10)
2. **Phase 2**: Array-Only Organization (Tasks 11-15)  
3. **Phase 3**: TI Nesting Prevention (Tasks 16-20)
4. **Phase 4**: Test Updates and Validation (Tasks 21-30)

## Recovery Plan
If issues arise during implementation:
1. Stop implementation immediately
2. Restore files from backups using naming convention above
3. Analyze what went wrong
4. Adjust approach and retry with user approval

## Notes
- All backups will be created before any modifications begin
- Backup verification will ensure all files are properly saved
- Implementation will proceed only after successful backup completion