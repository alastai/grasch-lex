# PC→C Canonicalization and Schema Validation Analysis

## Problem Statement

The JSON Schema for LEX-2026.0.3.2 is inconsistent in how it handles the PC→C transformation. This causes:
1. **PC (Pre-Canonical) forms** to validate correctly
2. **C (Canonical) forms** (after full canonicalization) to FAIL validation

## Understanding PC and C Forms

### PC (Pre-Canonical) Form
Documents in PC form are **user-friendly** and may contain:
- **Import directives** (`import: "file.yaml"`) for modularity
- **Shorthands** (one-level type interpretation wrappers like `abstract:`, `concrete:`)
- **Synonyms** (multiple ways to express the same thing):
  - Edge endpoint keywords: `from`/`tail`/`src`/`source` (all mean the same)
  - Edge endpoint keywords: `to`/`head`/`dst`/`dest`/`destination` (all mean the same)
  - Edge label keywords: `via`/`arc` (both mean the same)
- **Future canonicalizations** (the system is extensible)

### C (Canonical) Form
Documents in C form are **normalized** and have:
- **No imports** - all imports resolved and merged
- **Canonical wrappers** - all shorthands expanded to two-level form (`exactlyOf: concrete:`)
- **Canonical synonyms** - one preferred term chosen:
  - `from` (not `tail`, `src`, or `source`)
  - `to` (not `head`, `dst`, `dest`, or `destination`)
  - `via` (not `arc`)
- **Fully expanded structure** - ready for validation and processing

### The Canonicalizing Preprocessor

The `canonicalizing_preprocessor.py` performs the PC→C transformation:
1. **Import resolution** - recursively loads and merges imported files
2. **Wrapper canonicalization** - expands shorthands to canonical two-level form
3. **Synonym normalization** - picks canonical terms from synonym sets
4. **Structure normalization** - produces consistent, predictable structure

This is a **permanent feature** of LEX-2026 and any library supporting it (like Grasch).

## Root Cause

The schema has import support in some places but not consistently everywhere imports should be allowed. More critically, the schema doesn't properly accept the canonical structures produced by the preprocessor after full PC→C transformation.

## Key Findings

### 1. Import Pattern Inconsistency

The schema needs a uniform pattern: **anywhere an `import:` directive is allowed, there should be a `oneOf` accepting either the import OR the actual content**.

Current state:
- ✅ `NodeTypesProperty` and `EdgeTypesProperty` have proper oneOf with import support
- ✅ `NodeTypeItem` and `EdgeTypeItem` have import options
- ❌ Many nested properties lack import support
- ❌ Some properties have `$ref` to definitions that themselves have `$ref` to other definitions with imports

### 2. Validation Flow

```
PC Form (user-friendly with imports, shorthands, synonyms) 
  → JSON Schema Validation ✅ PASSES
  → PC→C Canonicalization:
      - Resolve imports
      - Normalize wrappers (shorthands → canonical two-level)
      - Normalize synonyms (arc → via, tail → from, head → to)
      - Normalize structure
  → C Form (canonical, normalized, no imports)
  → JSON Schema Validation ❌ FAILS
```

**The C form MUST also validate** because it's the normalized version of a valid PC form. The schema should accept both forms.

### 3. Specific Issues Identified

From `analyze_import_patterns.py`:
- 13 high-severity issues where importable properties lack oneOf patterns
- Key problem areas:
  - `GraphType` properties (`nodeTypes`, `edgeTypes` within various contexts)
  - `subtypesOf` nested properties
  - `sealed` wrapper contents
  - `Directory.directories`

## Attempted Fixes

### Fix 1: Add oneOf Wrappers (`fix_import_oneof_patterns.py`)
- Added oneOf wrappers to 12 locations
- **Result**: Created new problem - root `graphSchema` property shouldn't have oneOf

### Fix 2: Remove Root oneOf (`fix_import_patterns_correctly.py`)
- Removed oneOf from root `graphSchema` property
- **Result**: Still failing - deeper structural issues remain

## Current Status

**PC Validation**: ✅ All test files pass  
**C Validation**: ❌ All test files fail with "is not valid under any of the given schemas"

The error suggests the entire `graphSchema` object doesn't match any oneOf option at the root level, which means there's a structural mismatch between what the canonicalizer produces and what the schema expects.

## Next Steps - Recommended Approach

### Option 1: Systematic Schema Redesign (Recommended)

Create a spec to systematically redesign the import patterns:

1. **Requirements Phase**:
   - Define clear rules for where imports are allowed
   - Specify the oneOf pattern to use consistently
   - Document the PC vs C validation requirements

2. **Design Phase**:
   - Design a consistent import pattern for all importable properties
   - Define how `$ref` chains should work with imports
   - Specify wrapper canonicalization rules

3. **Implementation Phase**:
   - Apply the pattern systematically to all definitions
   - Ensure `$ref` chains resolve correctly
   - Test PC and C validation for all examples

### Option 2: Debug Current Schema (Faster but less systematic)

1. Create a minimal failing example
2. Trace exactly why it fails validation
3. Fix that specific issue
4. Repeat until all examples pass

### Option 3: Two-Schema Approach (Alternative)

Maintain two schemas:
- `lex-2026.0.3.2-pre-import.schema.json` - validates PC forms (with imports)
- `lex-2026.0.3.2.schema.json` - validates C forms (canonical, no imports)

This separates concerns but requires maintaining two schemas.

## Recommendation

**Go with Option 1** - Create a spec for systematic schema redesign. This will:
- Document the requirements clearly
- Ensure consistency across all import points
- Provide a clear implementation plan
- Result in a maintainable schema

The spec should be named something like `import-schema-consistency` and follow the standard spec workflow:
1. Requirements (what should be importable, what patterns to use)
2. Design (how to implement consistently)
3. Tasks (systematic application to all definitions)

## Technical Details

### The OneOf Pattern for Imports

Every importable property should follow this pattern:

```json
"propertyName": {
  "oneOf": [
    {
      "description": "Inline content",
      "$ref": "#/$defs/ContentType"  // or inline schema
    },
    {
      "type": "object",
      "description": "Import content from file",
      "required": ["import"],
      "properties": {
        "import": {
          "type": "string",
          "description": "Import content from file"
        }
      },
      "additionalProperties": false
    }
  ]
}
```

### Properties That Should Support Imports (PC Form)

Based on analysis:
- `graphType` (in GraphSchemaContent and GraphContent contexts)
- `nodeTypes` (at all levels: GraphType, subtypesOf, sealed, etc.)
- `edgeTypes` (at all levels: GraphType, subtypesOf, sealed, etc.)
- `propertyGraphDataModel`
- `directories` (in Directory)
- `graphStorageSchema`
- Individual items in arrays (NodeTypeItem, EdgeTypeItem)

### Properties That Should NOT Support Imports

- Root document type selectors (`catalog`, `graphSchema`, `graph`) - these define document type
- Primitive values (strings, numbers, booleans)
- Constraint definitions
- Property type definitions

### Canonicalization Transformations

The preprocessor performs these transformations (PC→C):

1. **Import Resolution**:
   - `nodeTypes: {import: "types.yaml"}` → `nodeTypes: [<resolved content>]`
   - Recursive resolution with circular import detection

2. **Wrapper Canonicalization**:
   - `abstract: <content>` → `subtypesOf: abstract: <content>`
   - `concrete: <content>` → `exactlyOf: concrete: <content>`
   - `properSubtypesOf: <content>` → `subtypesOf: abstract: <content>`

3. **Synonym Normalization** (edge endpoints):
   - `tail:` → `from:`
   - `head:` → `to:`
   - `src:` → `from:`
   - `dst:` → `to:`
   - `dest:` → `to:`
   - `source:` → `from:`
   - `destination:` → `to:`
   - `arc:` → `via:`

4. **Edge Endpoint Wrapper Insertion**:
   - Bare references get wrapped: `from: Person` → `from: {exactlyOf: {concrete: Person}}`
   - Already-wrapped references are canonicalized to two-level form

## Files Created During Analysis

- `analyze_import_patterns.py` - Identifies missing import patterns
- `fix_import_oneof_patterns.py` - First attempt at fixes
- `fix_import_patterns_correctly.py` - Corrected root-level fix
- `diagnose_graphtype_issue.py` - Detailed validation diagnostics
- `IMPORT-PATTERN-ANALYSIS.md` - Detailed analysis report
- `validate_pc_and_c_forms.py` - Comprehensive PC→C validation pipeline

## Key Insight

The PC→C canonicalization is a **permanent architectural feature** of LEX-2026, not just an import resolver. It's analogous to:
- **Compilers**: Source code (PC) → Intermediate representation (C)
- **Parsers**: Concrete syntax (PC) → Abstract syntax tree (C)
- **Normalizers**: User input (PC) → Canonical form (C)

The schema must accept **both** forms because:
1. **PC forms** are what users write (ergonomic, flexible, modular)
2. **C forms** are what tools process (normalized, predictable, unambiguous)
3. **The preprocessor** is the bridge between them

## Conclusion

The PC→C canonicalization system is conceptually sound and architecturally necessary. The schema needs systematic updates to accept both PC and C forms. A spec-driven approach will ensure consistency and maintainability.

The canonicalizing preprocessor is not just an "import resolver" - it's a **normalization pipeline** that transforms user-friendly PC forms into tool-friendly C forms. Both must validate against the schema.
