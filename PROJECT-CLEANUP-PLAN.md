# Project Structure Cleanup Plan

**Status**: Ready for execution  
**Priority**: High - Improves maintainability  
**Estimated Time**: 2-3 hours

## Current Problem

The project root directory contains ~150+ files with no clear organization:
- Ad-hoc test scripts mixed with validation scripts
- Analysis markdown files scattered everywhere
- Fix scripts and debug scripts in root
- No clear separation between temporary/permanent files

**CRITICAL UNRESOLVED ISSUE**: The distinction between "grasch" (the project) and "kiro" (the tool) and the proper placement of files in project root vs. tool-specific locations is completely unclear. This requires further analysis before any cleanup action begins. Specifically:

- Are files in the root directory grasch project files or kiro tool development files?
- Should development/debugging scripts be in the grasch project or are they kiro-specific tooling?
- What is the relationship between `.kiro/specs/` (tool specs) and project documentation?
- Are analysis documents about grasch development or kiro tool usage?
- Should test files for schema validation be considered grasch tests or kiro tool tests?

**This ambiguity must be resolved before executing any reorganization to avoid misplacing files or creating an incorrect structure.**

## Target Structure

```
grasch/
├── src/grasch/              # Source code (already correct)
├── tests/                   # All test files
│   ├── schema/             # Schema validation tests
│   ├── integration/        # Integration tests
│   └── unit/               # Unit tests (existing)
├── scripts/                # Utility scripts
│   ├── validation/         # Validation scripts
│   ├── fixes/              # One-time fix scripts
│   └── analysis/           # Analysis scripts
├── docs/                   # Documentation
│   ├── analysis/           # Analysis documents
│   ├── specs/              # Technical specifications
│   └── guides/             # Implementation guides
├── .kiro/                  # Kiro IDE (already correct)
├── archive/                # Historical/superseded (already exists)
├── ancillary docs/         # External docs (already correct)
├── [config files]          # Root config only
└── README.md               # Root readme only
```

## Categorization Rules

**CRITICAL DISTINCTION**: Many files currently in `src/grasch/examples/` are actually TEST FILES, not examples. These belong in the test directory structure, not with the source code examples.

### Misplaced Test Files in `src/grasch/examples/`

The following YAML files in `src/grasch/examples/` are tests and should be moved to `tests/schema/data/`:

**Test files with "test-" prefix:**
- `test-siblings-*.yaml` (all sibling test files)
- `test-phase-*.yaml` (all phase test files)
- `test-pc-*.yaml` (all PC form test files)
- `test-expected-canonical.yaml`
- Any other files starting with `test-`

**Test files with "-test" suffix:**
- `lex-2026.0.3.2-minimal-test.yaml`
- `lex-2026.0.3.2-subtype-abstract-test.yaml`
- `lex-2026.0.3.2-all-import-patterns.yaml` (comprehensive test file)
- Any other files ending with `-test.yaml`

**Test files in `src/grasch/examples/imports/`:**
- `imports/test-*.yaml` (e.g., `test-place-hierarchy.yaml`, `test-person-types.yaml`)

**True example files that should REMAIN in `src/grasch/examples/`:**
- `lex-2026.0.3.2-example-catalog.yaml`
- `lex-2026.0.3.2-example-catalog-no-iri.yaml`
- `lex-2026.0.3.2-snb-schema.yaml`
- `lex-2026.0.3.2-finbench-schema.yaml`
- `lex-2026.0.3.2-finbench-sf1-graph.yaml`
- `lex-2026.0.3.2-type-definition-syntax-examples.yaml`
- `lex-2026.0.3.2-type-interpretation-wrappers-example.yaml`
- `lex-2026.0.3.2-mixed-import-example.yaml`
- `imports/snb-types/*.yaml` (SNB type hierarchies)
- `imports/lex-2026.0.3.2-node-type-syntax-examples.yaml`

### Move to `tests/schema/`
All files matching: `test_*.py`, `validate_*.py`, `check_*.py`, `debug_*.py`
Examples: test_graphschema_validation.py, validate_phase_a.py, check_nodetypes_array.py

### Move to `scripts/fixes/`
All files matching: `fix_*.py`, `phase_*_fix_*.py`, `update_*.py`, `apply_*.py`
Examples: fix_schema_oneof_patterns.py, phase_a_fix_nodetype_ti.py, update_edgetype_schema.py

### Move to `scripts/analysis/`
All files matching: `analyze_*.py`, `diagnose_*.py`, `investigate_*.py`, `show_*.py`, `compare_*.py`
Examples: analyze_failing_files.py, diagnose_graphtype_issue.py, investigate_root_issue.py

### Move to `scripts/utilities/`
All files matching: `add_*.py`, `allow_*.py`, `implement_*.py`, `rename_*.py`, `save_*.py`
Examples: add_ti_content_defs.py, allow_nested_type_interpretations.py

### Move to `docs/analysis/`
All uppercase markdown files in root (except README.md)
Examples: PHASE-E-STATUS-SUMMARY.md, TYPE-INTERPRETATION-ANALYSIS.md, SCHEMA-UPDATE-PROGRESS.md

### Move to `docs/specs/`
Technical specification documents
Examples: LEX-2026.0.3.2-GUIDE.md, TYPE-DEFINITION-CANONICALIZATION-RULES.md

### Keep in Root
- README.md
- Makefile
- pyproject.toml
- .gitignore
- .python-version
- requirements_test.txt
- run_tests.sh

### Archive or Delete
- Temporary test YAML files in root (test-phase-*.yaml)
- Duplicate/superseded scripts
- Empty or 0-byte files

## Execution Steps

1. **Create new directories**
   ```bash
   mkdir -p tests/schema scripts/{validation,fixes,analysis,utilities} docs/{analysis,specs,guides}
   ```

2. **Move test scripts** (~60 files)
   ```bash
   mv test_*.py check_*.py validate_*.py debug_*.py tests/schema/
   ```

3. **Move fix scripts** (~30 files)
   ```bash
   mv fix_*.py phase_*_fix_*.py update_*.py apply_*.py scripts/fixes/
   ```

4. **Move analysis scripts** (~20 files)
   ```bash
   mv analyze_*.py diagnose_*.py investigate_*.py show_*.py compare_*.py scripts/analysis/
   ```

5. **Move utility scripts** (~15 files)
   ```bash
   mv add_*.py allow_*.py implement_*.py rename_*.py save_*.py scripts/utilities/
   ```

6. **Move documentation** (~80 files)
   ```bash
   mv *-ANALYSIS.md *-STATUS.md *-COMPLETE.md *-SUMMARY.md docs/analysis/
   mv LEX-*.md TYPE-*.md docs/specs/
   ```

7. **Move test YAML files**
   ```bash
   # Create test data directory
   mkdir -p tests/schema/data/imports
   
   # Move test YAML files from src/grasch/examples/ to tests/schema/data/
   mv src/grasch/examples/test-*.yaml tests/schema/data/
   mv src/grasch/examples/*-test.yaml tests/schema/data/
   mv src/grasch/examples/imports/test-*.yaml tests/schema/data/imports/
   
   # Move any test YAML files in root to tests/schema/data/
   mv test-*.yaml tests/schema/data/ 2>/dev/null || true
   
   # Keep only true examples in src/grasch/examples/
   # (like lex-2026.0.3.2-example-catalog.yaml, lex-2026.0.3.2-snb-schema.yaml)
   ```

8. **Update imports and references**
   - Update test imports to reflect new paths
   - Update script references in documentation
   - Update Makefile if needed

9. **Create index files**
   - `docs/analysis/INDEX.md` - Catalog of analysis documents
   - `scripts/README.md` - Explain script organization
   - `tests/schema/README.md` - Explain test organization

10. **Verify nothing broke**
    ```bash
    make test
    python tests/schema/validate_phase_a.py
    ```

## Benefits

- Clear separation of concerns
- Easy to find relevant files
- Reduced root directory clutter
- Better for version control (can .gitignore temp files by directory)
- Easier onboarding for new contributors
- Follows Python project best practices
- **Separates test data from example data** - critical for understanding what's a test vs. what's a usage example
- Prevents confusion about which YAML files are meant for users vs. internal testing

## Risks

- May break some hardcoded paths in scripts
- Documentation references may need updating
- Takes time away from bug fixing

## Recommendation

**DO NOT EXECUTE** this cleanup until the grasch/kiro distinction is clarified. Once that fundamental question is resolved:

1. First, clarify the grasch vs. kiro file placement strategy
2. Then, execute this cleanup AFTER fixing the critical sibling TI wrapper bug
3. Finally, proceed BEFORE the next major feature work

Without understanding whether this is a grasch project repository or a kiro tool development repository (or both), any reorganization risks creating more confusion rather than less.

## Automation Script

A single script could automate most of this:

```python
# scripts/reorganize_project.py
# Categorizes and moves files based on patterns
# Generates a report of what was moved
# Can be run in dry-run mode first
```

## Estimated Time

- Planning and categorization: 30 min (done)
- Moving files: 30 min
- Updating references: 1 hour
- Testing and verification: 30 min
- Documentation: 30 min

**Total**: 2.5-3 hours
