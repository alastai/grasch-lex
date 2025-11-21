# Canonicalization Process Clarification

## Two-Phase Canonicalization Process

The canonicalizing preprocessor performs **two distinct phases** in strict order:

### Phase 1: Import Resolution with Wrapper Stripping

**Purpose**: Merge all imported content inline

**Process**:
1. Find all `import:` directives
2. Load referenced files
3. **Strip duplicate wrapper keys** before merging:
   - If parent has `X: import: <file>`
   - And `<file>` starts with `X:`
   - Remove the second `X:` key before textual merge
4. Recursively process nested imports
5. Result: Single document with no `import:` directives

**Example**:
```yaml
# Parent file
nodeTypes:
  import: "types.yaml"

# types.yaml
nodeTypes:
  - nodeType: {...}

# After Phase 1 (wrapper stripped)
nodeTypes:
  - nodeType: {...}
```

### Phase 2: Syntax Canonicalization (PC → C)

**Purpose**: Normalize all convenience syntax to canonical form

**Critical Rule**: Type interpretation wrappers surround the **type identifier**, not the type definition structure.

**Type Identifier Forms**:
- `X` - single type label (string)
- `[X, Y]` - type labels set (array)
- `0` - type index for anonymous type (integer)

**Transformations**:

1. **Type interpretation wrappers** (surround identifier):
   ```yaml
   # PC form → C form
   abstract:
     nodeType:
       typeLabel: Message
   
   →
   
   subtypesOf:
     abstract:
       nodeType:
         typeLabel: Message
   ```

2. **Edge endpoint wrappers** (surround identifier, NOT structure):
   ```yaml
   # PC form → C form
   from: Person              → from: exactlyOf: concrete: Person
   to: Company               → to: exactlyOf: concrete: Company
   via: KNOWS                → via: exactlyOf: concrete: KNOWS
   
   # NOT this (WRONG):
   from: typeLabel: Person   → from: exactlyOf: concrete: typeLabel: Person
   
   # The wrapper surrounds the VALUE (Person), not the key-value pair
   ```

3. **Type identifier simplification**:
   ```yaml
   # PC form (verbose) → C form (simplified)
   from:
     typeLabel: Person       → from: exactlyOf: concrete: Person
   
   to:
     typeLabels: [X, Y]      → to: exactlyOf: concrete: [X, Y]
   
   via:
     typeLabel: KNOWS        → via: exactlyOf: concrete: KNOWS
   ```

4. **Default wrapper insertion**:
   ```yaml
   # PC form (omitted wrapper) → C form (explicit default)
   from: Person              → from: exactlyOf: concrete: Person
   nodeType: Person          → nodeType: exactlyOf: concrete: Person
   ```

**Result**: Canonical form with:
- Explicit type interpretation wrappers
- Simplified type identifiers (no `typeLabel:` keys)
- Normalized structure

## Critical Requirements

### Same Schema Validates Both Forms

**Key Principle**: The JSON Schema must validate **both** PC and C forms

- **PC form**: Convenience syntax (optional wrappers, imports, shorthands)
- **C form**: Canonical syntax (explicit wrappers, no imports, normalized)

The schema achieves this through:
- Optional properties (wrappers can be omitted in PC)
- `oneOf` patterns (accept multiple syntaxes)
- Flexible structure (both forms are valid)

### Document Type Preservation

After canonicalization, the document must still be:
- A valid `graph` (if it was a graph)
- A valid `graphSchema` (if it was a graphSchema)
- A valid `catalog` (if it was a catalog)

The root document type **never changes** during canonicalization.

### Validation Expectations

**PC Form Validation**:
```
PC document → JSON Schema → ✅ Valid
```

**C Form Validation**:
```
PC document → Canonicalize → C document → JSON Schema → ✅ Valid
```

**Current Issue**:
```
PC document → Canonicalize → C document → JSON Schema → ❌ Invalid (12/14 files)
```

## Root Cause Analysis

The validation failures indicate one or more of:

1. **Canonicalizer produces invalid syntax**
   - Wrappers not in correct form
   - Structure doesn't match schema expectations
   - Missing required properties

2. **Schema doesn't accept canonical syntax**
   - `oneOf` patterns too restrictive
   - Required properties not marked optional
   - Canonical forms not included in schema

3. **Wrapper stripping issues**
   - Duplicate keys not properly removed
   - Nested structure corrupted
   - Import resolution incomplete

## Debugging Strategy

### Step 1: Examine One Failing File

Pick a simple failing file (e.g., `minimal-import-example.yaml`):
1. Look at PC form (should validate ✅)
2. Look at C form (`CANON_*.yaml`)
3. Identify specific schema violation
4. Determine if issue is in canonicalizer or schema

### Step 2: Check Wrapper Canonicalization

Verify type interpretation wrappers surround identifiers correctly:
```yaml
# PC form (verbose)
nodeTypes:
  - abstract:
      nodeType:
        typeLabel: Message

# Expected C form (simplified identifier)
nodeTypes:
  - subtypesOf:
      abstract:
        nodeType: Message

# NOT this (WRONG - keeps verbose form):
nodeTypes:
  - subtypesOf:
      abstract:
        nodeType:
          typeLabel: Message

# Check: Are identifiers simplified to bare values?
```

```yaml
# PC form (edge endpoint)
edgeType:
  directed:
    from: Person
    via: KNOWS
    to: Person

# Expected C form
edgeType:
  directed:
    from:
      exactlyOf:
        concrete: Person
    via:
      exactlyOf:
        concrete: KNOWS
    to:
      exactlyOf:
        concrete: Person

# Check: Do wrappers surround the VALUE, not the structure?
```

### Step 3: Check Import Resolution

Verify imports are fully resolved:
```yaml
# PC form
nodeTypes:
  import: "types.yaml"

# Expected C form (no import:)
nodeTypes:
  - nodeType: {...}
  - nodeType: {...}

# Check: Are all import: directives gone?
```

### Step 4: Schema Validation

Check if schema accepts canonical forms:
```json
{
  "nodeTypes": {
    "type": "array",
    "items": {
      "oneOf": [
        {"$ref": "#/definitions/NodeType"},
        {"$ref": "#/definitions/SubtypesOfWrapper"},
        {"$ref": "#/definitions/SealedWrapper"},
        {"$ref": "#/definitions/FinalWrapper"}
      ]
    }
  }
}
```

Check: Does schema include all canonical wrapper patterns?

## Expected Fix

Once the issue is identified, the fix will be one of:

1. **Update canonicalizer** to produce schema-compliant output
2. **Update schema** to accept canonical forms
3. **Update both** to align properly

The goal: **All 14 files pass both PC and C validation** ✅

## Terminology Reference

- **PC (Pre-Canonical)**: All documents start in this form
- **C (Canonical)**: Normalized form after canonicalization
- **Importing file**: Contains `import:` directives
- **No-imports file**: No `import:` directives (but still in PC form)
- **JS Validation**: JSON Schema validation (structural only)
- **Canonicalizing preprocessor**: Performs both import resolution and syntax canonicalization
- **Wrapper stripping**: Removing duplicate keys during import merge

## Next Steps

1. Examine one failing C form in detail
2. Identify specific schema violation
3. Determine root cause (canonicalizer vs schema)
4. Implement fix
5. Re-run validation pipeline
6. Verify all 14 files pass ✅

---

**Status**: Analysis complete, ready for debugging
**Files**: 12/14 failing C form validation
**Root cause**: TBD (canonicalizer vs schema vs both)
