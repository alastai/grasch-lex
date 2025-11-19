# Terminology Review Findings - GQL-schema Clarification

## Summary

Found **20+ occurrences** of deprecated terminology in requirements.md that need updating per the GQL-schema clarification.

## Terminology to Replace

### ❌ Deprecated Terms
1. "GQL-schema" (GQL spec term - not used in LEX)
2. "types-graphs directory" (previous LEX term - deprecated)
3. "type-graph" (should go away)

### ✅ Replacement Terms
**Standard replacement**: "data-schema (leaf) directory"

**Equivalence**:
- GQL-schema (from GQL spec) = Leaf directory (LEX approach)
- Optional term: Data-schema directory when differentiation is needed
- Deprecated: "types-graphs directory", "type-graph"
- Rule: Graphs and graph schemas can only exist in leaf node directories

## Specific Changes Needed

### Line 23: Introduction - Terminology Clarification Section
**Current**:
```
**Terminology Clarification**: Following LEX-99, Grasch uses "types-graphs directory" 
instead of "GQL-schema" to avoid confusion, as GQL-schema is merely a container, not a 
schema in the traditional computer science sense.
```

**Should be**:
```
**Terminology Clarification**: GQL-schema (from GQL spec) = Leaf directory (LEX approach). 
The GQL spec uses "GQL-schema" to refer to a leaf node directory that can contain graphs 
and graph schemas. LEX uses the simpler rule: graphs and graph schemas can only exist in 
leaf node directories. When differentiation is needed, we use "data-schema (leaf) directory". 
The deprecated term "types-graphs directory" should not be used. The term "schema" is 
reserved for graph types (descriptions of graph structure).
```

### Line 26: Introduction - Catalog Structure
**Current**: "types-graphs directories (leaf nodes)"
**Replace with**: "data-schema (leaf) directories"

### Line 34: Terminology Note
**Current**: "GQL-schemas / types-graphs directories"
**Replace with**: "Data-schema (leaf) directories (called GQL-schemas in GQL spec)"

### Requirement 6 (Lines 295-329): Catalog Requirements
**Multiple occurrences** of "types-graphs directory" should be replaced with "leaf directory"

Specific changes:
- Line 296: "root directory is also a types-graphs directory" → "root directory is also a leaf directory"
- Line 297: "within a types-graphs directory" → "within a leaf directory"
- Line 323: "within types-graphs directories (leaf nodes)" → "within leaf directories"
- Line 325: "reference any types-graphs directory" → "reference any leaf directory"
- Line 326: "directories or types-graphs directories" → "directories (non-leaf) or leaf directories"
- Line 326: "work with types-graphs directories" → "work with leaf directories"
- Line 328: "types-graphs directory's fully-qualified pathName" → "leaf directory's fully-qualified pathName"
- Line 329: "within types-graphs directories" → "within leaf directories"
- Line 329: "accessing types-graphs directories" → "accessing leaf directories"

### Requirement 17 (Lines 500-519): LEX Catalog DDL
**Current**: References "types-graphs directories" and "GQL SCHEMA" keyword
**Note**: DDL keyword "GQL SCHEMA" is from GQL spec, but documentation should clarify

Changes needed:
- Line 500: "types-graphs directories" → "leaf directories"
- Line 501: Update terminology note to clarify GQL SCHEMA keyword vs leaf directory concept
- Line 504: "types-graphs directories" → "leaf directories"
- Line 515: Keep "GQL SCHEMA" as DDL keyword but add note about leaf directories
- Line 516: Keep "GQL SCHEMA" as DDL keyword but add note about leaf directories

### Lines 741-742: IRI Requirements
**Current**: "types-graphs directory (leaf node)"
**Replace with**: "leaf directory"

### Line 783: Data Graph Storage
**Current**: "store a data graph in a types-graphs directory"
**Replace with**: "store a data graph in a leaf directory"

## Recommended Approach

1. **Global find/replace** for simple cases:
   - "types-graphs directories" → "data-schema (leaf) directories"
   - "types-graphs directory" → "data-schema (leaf) directory"

2. **Manual updates** for complex cases:
   - Line 23: Rewrite terminology clarification section
   - Line 34: Update terminology note
   - Line 501: Update DDL terminology note
   - Lines 515-516: Add clarifying notes about GQL SCHEMA keyword

3. **Add new terminology note** at beginning:
   - Explain GQL-schema ≡ leaf directory equivalence
   - Reference TERMINOLOGY-CLARIFICATION-GQL-SCHEMA.md

## Total Changes Required

- **Simple replacements**: ~15 occurrences
- **Section rewrites**: 3 sections
- **New content**: 1 terminology note

---

**CHECKPOINT**: Review complete. Ready to proceed with terminology updates.

**Next Step**: Apply these changes to requirements.md?
