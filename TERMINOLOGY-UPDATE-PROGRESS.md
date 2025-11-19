# Terminology Update Progress

## ✅ Completed Updates

### 1. "path name" → `pathName`
- ✅ Line 294: "path names" → "pathNames"
- ✅ Line 326: "path name" → "pathName"

### 2. "GQL-schema" → "types-graphs directory" (in catalog context)
- ✅ Line 296: "GQL-schema" → "types-graphs directory"
- ✅ Line 297: "GQL-schema" → "types-graphs directory"
- ✅ Line 322-325: Multiple "GQL-schemas" → "types-graphs directories"
- ✅ Line 326-329: Multiple "GQL-schemas" → "types-graphs directories"

### 3. Terminology Note Updated
- ✅ Added clarification about graphSchema (YAML) vs types-graphs directory (catalog concept)

---

## ⏳ Remaining Updates

### GQL-schema References (Contextual)

The following references to "GQL-schema" remain and need contextual review:

**Line 23**: Terminology clarification (keep as-is - explains the distinction)
**Line 34**: Terminology note (updated with clarification)
**Line 444**: Catalog structure description
**Line 475**: Visualization description
**Line 499-523**: Requirement 17 (LEX catalog DDL commands)
**Line 739-740**: IRI construction
**Line 768**: LEX schemas storage
**Line 777-781**: Data graphs storage

**Decision Needed**: These references are in contexts where:
1. Explaining GQL standard terminology (keep "GQL-schema")
2. Describing catalog structure (use "types-graphs directory")
3. DDL commands (may need "GQL SCHEMA" for DDL syntax)

---

## 📋 Additional Terminology to Check

### Type Identification Properties
- ✅ No instances of "type name label" found
- ✅ No instances of "type identifying labels" found  
- ✅ No instances of "node type index" found

### Edge Type Old Syntax
- ✅ Only one reference (Line 2001) - correctly marked as deprecated

---

## 🎯 Next Steps

### Option 1: Complete Remaining GQL-schema Updates
Review and update remaining GQL-schema references based on context:
- Catalog structure descriptions → "types-graphs directory"
- DDL command syntax → Keep "GQL SCHEMA" (DDL keyword)
- Explanatory text → Keep "GQL-schema" with clarification

### Option 2: Update Existing Requirements (1, 2, 4, 6, 7)
Move to updating the content of specific requirements identified in the analysis:
- Requirement 1: Use exact property names
- Requirement 2: Use pathName consistently
- Requirement 4: Rewrite edge type section
- Requirement 6: Update to reference-only pattern (DONE: terminology)
- Requirement 7: Mention required defaults block

### Option 3: Proceed to Design Phase
Consider terminology updates sufficient and move to design document updates.

---

## Summary Statistics

**Total Replacements Made**: 12
**Lines Modified**: ~15
**Terminology Standardized**:
- ✅ pathName (camelCase)
- ✅ types-graphs directory (catalog concept)
- ✅ graphSchema (YAML document type)

**Remaining GQL-schema References**: ~15 (contextual review needed)

---

**Status**: Core terminology updates complete
**Date**: November 19, 2024
**Next**: Review remaining GQL-schema references or proceed to requirement content updates
