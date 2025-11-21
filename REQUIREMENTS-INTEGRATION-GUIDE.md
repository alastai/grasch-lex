# Requirements Integration Guide

## New Requirements Created

**File**: `NEW-REQUIREMENTS-ADDITIONS.md` (168 lines, 17KB)

Contains 8 new requirements (LEX-9 through LEX-16) addressing critical gaps identified in the consistency analysis.

---

## New Requirements Summary

### LEX-9: Document Type Discrimination
- Three top-level document types: catalog, graphSchema, graph
- GraphType cannot be top-level (must be in graphSchema)
- 11 acceptance criteria

### LEX-10: Import Patterns and Modularization
- Comprehensive import mechanism
- Inline, import-only, and mixed modes
- Support for all IMPORTABLE elements
- 15 acceptance criteria

### LEX-11: Edge Type Syntax (0.3.2)
- New directed:/undirected: wrappers
- Semantic endpoint names (from/to, tail/head, src/dst)
- via:/arc: keywords for edge labels
- SAME/SELF for self-loops
- 20 acceptance criteria

### LEX-12: Abstract, Sealed, and Final Types
- abstract: and abstractSupertype: wrappers
- sealed: for closed hierarchies
- final: for non-extensible types
- Validation rules and equivalences
- 17 acceptance criteria

### LEX-13: Defaults Block
- Required defaults: block in every graphType
- Min/max labels and properties
- Preferred names configuration
- 17 acceptance criteria

### LEX-14: Edge Type Subtyping
- Covariant endpoint types
- Armstrong's Axioms (reflexive, transitive)
- Structural subtyping for properties
- 15 acceptance criteria

### LEX-15: NotNull Constraint
- notNull: boolean property on property types
- Validation enforcement
- Compatibility with GQL/SQL
- 11 acceptance criteria

### LEX-16: Catalog References
- Lightweight references vs embedded definitions
- graphReferences and graphSchemaReferences
- Leaf directory constraint
- 14 acceptance criteria

---

## Integration Steps

### Step 1: Backup Current Requirements
```bash
cp .kiro/specs/property-graph-schema/requirements.md \
   .kiro/specs/property-graph-schema/requirements-backup-$(date +%Y%m%d).md
```

### Step 2: Append New Requirements
```bash
cat NEW-REQUIREMENTS-ADDITIONS.md >> .kiro/specs/property-graph-schema/requirements.md
```

### Step 3: Update Existing Requirements

The following existing requirements need terminology updates:

**Requirement 1** (Attribute Types):
- Change "type name label" → "typeLabel"
- Update examples to use exact property names

**Requirement 2** (Content Record Types):
- Update to use "pathName" (camelCase) consistently

**Requirement 4** (Element Types):
- Rewrite edge type section to use 0.3.2 syntax
- Remove references to old firstEndpointNodeType/secondEndpointNodeType

**Requirement 6** (Catalog):
- Update to reference-only pattern
- Add leaf directory constraint
- Change "GQL-schema" → "graphSchema" or "types-graphs directory"

**Requirement 7** (Graph Types):
- Add mention of required defaults block
- Reference LEX-13 for details

---

## Terminology Updates Needed

Throughout the requirements document, replace:

| Old Term | New Term |
|----------|----------|
| "path name" (two words) | `pathName` (camelCase) |
| "type name label" | `typeLabel` |
| "type identifying labels" | `typeIdentifier` |
| "node type index" | `index` |
| "GQL-schema" | `graphSchema` or "types-graphs directory" |
| `firstEndpointNodeType` | `from:` or `to:` (new syntax) |
| `secondEndpointNodeType` | `to:` or `and:` (new syntax) |
| `direction:` property | `directed:` or `undirected:` wrapper |

---

## Validation After Integration

### Check Requirements Structure
```bash
# Verify all requirements are numbered correctly
grep -n "^### Requirement" .kiro/specs/property-graph-schema/requirements.md
```

### Check EARS Compliance
```bash
# Verify all acceptance criteria use SHALL
grep -c "SHALL" .kiro/specs/property-graph-schema/requirements.md
```

### Check Cross-References
```bash
# Find any broken references to old terminology
grep -i "firstEndpointNodeType\|secondEndpointNodeType\|type name label" \
  .kiro/specs/property-graph-schema/requirements.md
```

---

## Next Steps After Integration

1. **Update Design Document** - Reflect new requirements in design.md
2. **Update Tasks** - Add implementation tasks for new requirements
3. **Update Examples** - Ensure examples demonstrate all new features
4. **Update API Design** - Verify API Design doc aligns with new requirements
5. **Update Modernization Guide** - Incorporate findings from consistency analysis

---

## Files Created

1. `NEW-REQUIREMENTS-ADDITIONS.md` - 8 new requirements (168 lines)
2. `REQUIREMENTS-INTEGRATION-GUIDE.md` - This integration guide
3. `LEX-2026.0.3.2-COMPREHENSIVE-SPEC-CONSISTENCY-ANALYSIS.md` - Full analysis (1,349 lines)
4. `SPEC-CONSISTENCY-SUMMARY.md` - Executive summary

---

## Status

✅ New requirements written in EARS format
✅ All acceptance criteria use SHALL statements
✅ Requirements numbered LEX-9 through LEX-16
✅ Ready for integration into main requirements document

**Total New Acceptance Criteria**: 128 (across 8 requirements)
