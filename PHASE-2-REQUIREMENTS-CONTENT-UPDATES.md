# Phase 2: Requirements Content Updates

## Overview

This phase updates the **content** of existing requirements (not just terminology) to align with the JSON Schema and validated examples, which are the source of truth.

**Status**: Ready to begin
**Prerequisites**: ✅ Terminology updates completed, ✅ New requirements (LEX-9 through LEX-16) added

---

## Requirements to Update

Based on the comprehensive consistency analysis, these specific requirements need content updates:

### 1. Requirement LEX-1 (Abstract Syntax) - Use Exact Property Names ✅ COMPLETED

**Issue**: Requirements described abstract syntax but didn't explicitly document the concrete YAML property names

**Changes Made**:
- ✅ Updated acceptance criterion #7 to mention YAML concrete syntax: `index`, `typeLabel`, `typeIdentifier`/`typeLabels`
- ✅ Updated acceptance criterion #8 to reference LEX-11 for edge type YAML syntax
- ✅ Added new acceptance criterion #13 documenting all type identification properties
- ✅ Added new acceptance criterion #14 documenting `typeIdentifier`/`typeLabels` as synonyms

**Source of Truth**: 
- JSON Schema: `lex-2026.0.3.2.schema.json` (NodeType and EdgeType definitions)
- Examples: All 14 examples use these exact property names (`typeLabel`, `typeIdentifier`, `typeLabels`, `index`)

**Priority**: HIGH - Affects type identification throughout the system

**Status**: ✅ COMPLETED - LEX-1 now explicitly documents YAML concrete syntax property names

---

### 2. Requirement 2 (Content Record Types) - Use pathName Consistently

**Issue**: Requirements use "path name" (two words) or inconsistent casing

**Changes Needed**:
- Ensure all references use `pathName` (camelCase, one word)
- Update any "fully-qualified path name" → "fully-qualified pathName"
- Ensure consistency in all examples and descriptions

**Source of Truth**:
- JSON Schema: Uses `pathName` throughout
- Examples: All use `pathName` (camelCase)

**Priority**: HIGH - Core identifier property

---

### 3. Requirement 4 (Element Types) - Rewrite Edge Type Section for 0.3.2 Syntax

**Issue**: Requirements describe old 0.3.1 edge type syntax; 0.3.2 has complete redesign

**Old Syntax (0.3.1 - DEPRECATED)**:
```yaml
edgeType:
  typeLabel: KNOWS
  direction: UNDIRECTED
  firstEndpointNodeType: Person
  secondEndpointNodeType: Person
```

**New Syntax (0.3.2 - CURRENT)**:
```yaml
edgeType:
  undirected:
    between: Person
    via: KNOWS
    and: Person
```

**Changes Needed**:
1. Document `directed:` and `undirected:` wrappers (replaces `direction:` property)
2. Document `via:` and `arc:` keywords for edge labels (replaces `typeLabel:`)
3. Document semantic endpoint names:
   - Directed: `from:`/`to:` (primary), `tail:`/`head:`, `src:`/`dst:`/`dest:` (synonyms)
   - Undirected: `between:`/`and:` (primary)
4. Document `SAME` and `SELF` keywords for self-loops
5. Document inline node type definitions in edge endpoints
6. Mark old syntax as deprecated (but still validated by JSON Schema for backward compatibility)

**Source of Truth**:
- Examples: `lex-2026.0.3.2-edge-type-syntax-examples.yaml` (comprehensive)
- API Design: `LEX-2026.0.3.2-API-DESIGN.md` (documents all synonyms and accessor methods)
- JSON Schema: Validates both old and new syntax

**Priority**: HIGH - Core syntax change in 0.3.2

---

### 4. Requirement 6 (Catalog) - Update to Reference-Only Pattern

**Issue**: Requirements describe old pattern with embedded definitions; current pattern uses lightweight references

**Old Pattern (DEPRECATED)**:
```yaml
directories:
- name: ldbc
  graphSchemas:
  - name: snb
    graphType: {...}  # Full definition embedded
```

**New Pattern (CURRENT)**:
```yaml
directories:
- name: ldbc
  graphSchemaReferences:
  - name: snb
    qualifiedName: /benchmarks/ldbc/snb
    filePath: schemas/snb-schema.yaml  # Optional
```

**Changes Needed**:
1. Update to reference-only pattern (no embedded definitions)
2. Document `graphReferences` and `graphSchemaReferences` (not `graphs` and `graphSchemas`)
3. Document required properties: `name`, `qualifiedName`
4. Document optional property: `filePath`
5. Emphasize data-schema (leaf) directory constraint (references only in leaf directories)
6. Update examples to show reference pattern

**Source of Truth**:
- Examples: `lex-2026.0.3.2-example-catalog.yaml`, `lex-2026.0.3.2-example-catalog-no-iri.yaml`
- Document Types: `LEX-2026.0.3.2-DOCUMENT-TYPES-AND-IMPORTS.md`
- JSON Schema: Validates reference structure

**Priority**: MEDIUM - Catalog structure change

**Note**: Terminology already updated (✅ "data-schema (leaf) directory" terminology in place)

---

### 5. Requirement 7 (Graph Types) - Add Mention of Required Defaults Block

**Issue**: Requirements don't mention that `defaults:` block is required in every graphType

**Current Reality**:
```yaml
graphType:
  defaults:  # REQUIRED
    import: lex-2026.0.3.2-graph-type-defaults.yaml
  nodeTypes: [...]
  edgeTypes: [...]
```

**Changes Needed**:
1. Add statement that `defaults:` block is required in every graphType
2. Document that defaults can be inline or imported
3. Reference LEX-13 (new requirement) for full defaults block specification
4. Note that defaults specify cardinality constraints (min/max labels and properties)

**Source of Truth**:
- JSON Schema: `defaults` is in required array for GraphType
- Examples: ALL examples have defaults block (most import from shared file)
- New Requirement: LEX-13 provides full specification

**Priority**: MEDIUM - Required property not documented

---

## Implementation Approach

### Step 1: Review Current Requirement Text
For each requirement, read the current text to understand what needs to change

### Step 2: Draft Updated Text
Write updated requirement text that:
- Uses exact property names from JSON Schema
- Describes current implementation (not deprecated patterns)
- Includes examples from validated YAML files
- Maintains EARS format (WHEN/THEN/SHALL structure)
- Preserves existing acceptance criteria that are still valid
- Adds new acceptance criteria for new features

### Step 3: Validate Against Source of Truth
Cross-check updated text against:
- JSON Schema definitions
- Validated example files
- API Design document (for edge types)
- Document Types specification (for catalog)

### Step 4: Update Requirements Document
Apply changes to `.kiro/specs/property-graph-schema/requirements.md`

### Step 5: Document Changes
Record what was changed and why in this tracking document

---

## Success Criteria

- [ ] All 5 requirements updated with current implementation details
- [ ] All property names match JSON Schema exactly
- [ ] Edge type section describes 0.3.2 syntax as primary
- [ ] Catalog section describes reference-only pattern
- [ ] Defaults block documented as required
- [ ] All examples in requirements match validated YAML files
- [ ] EARS format maintained throughout
- [ ] Cross-references to new requirements (LEX-9 through LEX-16) added where appropriate

---

## Next Steps After Phase 2

Once requirements content is updated:

**Phase 3**: Update design documents to align with updated requirements
- design.md
- LEX-2026.0.3.2-API-DESIGN.md  
- LEX-100r3 modernization.md

**Phase 4**: Update tasks.md with implementation tasks for new requirements

---

**Date**: November 19, 2024
**Version**: LEX-2026.0.3.2
**Status**: Ready to begin - awaiting user confirmation to proceed
