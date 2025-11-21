# LEX-2026.0.3.2 Aesthetic Audit

## Summary

Audit of all YAML example files to identify verbose patterns that violate the minimal syntax aesthetic principles.

## Key Issues Found

### 1. Redundant typeLabel in implies/adding

**Files Affected:**
- `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-message-hierarchy.yaml`
- `src/grasch/examples/imports/lex-2026.0.3.2-node-type-syntax-examples.yaml`

**Pattern:**
```yaml
# VERBOSE (current)
nodeType:
  typeLabel: Message
  implies:
    labels:
      - Message  # Redundant!
```

**Should be:**
```yaml
# CLEAN
nodeType:
  typeLabel: Message
  implies:
    # labels omitted - inferred from typeLabel
```

**Occurrences:**
- Message hierarchy: Abstract Message type, Post subtype, Comment subtype
- Node type syntax examples: Pattern 9 (CEO with additional labels)

### 2. Verbose extends Syntax

**Files Affected:**
- `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-place-hierarchy.yaml`
- `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-message-hierarchy.yaml`
- `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-organisation-hierarchy.yaml` (FIXED)

**Pattern:**
```yaml
# VERBOSE (current)
nodeType:
  typeLabel: City
  implies:
    supertypes:
      - Place
    propertyTypes: []
```

**Should be:**
```yaml
# CLEAN
nodeType:
  typeLabel: City
  extends: Place
```

**Occurrences:**
- Place hierarchy: City, Country, Continent (all use `implies: supertypes:`)
- Message hierarchy: Post, Comment (use `extends: supertypes: adding:`)
- Organisation hierarchy: ALREADY FIXED to clean syntax

### 3. Unnecessary adding: labels

**Files Affected:**
- `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-message-hierarchy.yaml`

**Pattern:**
```yaml
# VERBOSE (current)
nodeType:
  typeLabel: Post
  extends:
    supertypes:
      - Message
    adding:
      labels:
        - Post  # Redundant!
```

**Should be:**
```yaml
# CLEAN
nodeType:
  typeLabel: Post
  extends: Message
  adding:
    propertyTypes: [...]  # Only if adding properties
```

**Occurrences:**
- Message hierarchy: Post (adds properties + redundant label), Comment (only redundant label)

### 4. Empty propertyTypes Arrays

**Files Affected:**
- `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-place-hierarchy.yaml`

**Pattern:**
```yaml
# VERBOSE (current)
nodeType:
  typeLabel: City
  implies:
    supertypes:
      - Place
    propertyTypes: []  # Empty!
```

**Should be:**
```yaml
# CLEAN
nodeType:
  typeLabel: City
  extends: Place
  # No adding: section needed
```

**Occurrences:**
- Place hierarchy: All three subtypes (City, Country, Continent)

### 5. Block-Style vs Flow-Style Arrays

**Status:** Need to check if label sets use flow-style `[A, B, C]` format

**Files to Review:**
- All files with multi-label types
- Edge type references in `to:` and `from:` fields

## Files Requiring Updates

### High Priority (SNB Hierarchies)
1. ✅ `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-organisation-hierarchy.yaml` - FIXED
2. ❌ `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-place-hierarchy.yaml` - NEEDS FIX
3. ❌ `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-message-hierarchy.yaml` - NEEDS FIX

### Medium Priority (Syntax Examples)
4. ❌ `src/grasch/examples/imports/lex-2026.0.3.2-node-type-syntax-examples.yaml` - NEEDS REVIEW
5. ❌ `src/grasch/examples/imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml` - NEEDS REVIEW

### Lower Priority (Main Schemas)
6. ❌ `src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml` - NEEDS REVIEW
7. ❌ `src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml` - NEEDS REVIEW

## Transformation Summary

### Place Hierarchy (3 types to fix)
- City: `implies: supertypes: + propertyTypes: []` → `extends: Place`
- Country: Same transformation
- Continent: Same transformation

### Message Hierarchy (2 types to fix)
- Post: Remove redundant `labels: [Post]`, simplify `extends:` syntax
- Comment: Remove redundant `labels: [Comment]`, simplify `extends:` syntax, remove empty `adding:`

### Node Type Syntax Examples
- Review all patterns for consistency with aesthetic principles
- Ensure examples demonstrate both verbose (for completeness) and clean (for best practice) forms

## Next Steps

1. Update SNB hierarchy files (Tasks 2.1, 2.2, 2.3)
2. Review and update syntax example files (Task 3.1)
3. Update main schema files (Tasks 3.2, 3.3)
4. Update JSON schema to accept minimal syntax (Task 4)
5. Validate all examples (Task 5)
