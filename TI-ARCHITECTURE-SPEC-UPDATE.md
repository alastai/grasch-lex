# Type Interpretation Architecture - Spec Update Complete

## Summary

Updated the type-interpretation-wrappers and import-schema-consistency specs with the corrected three-level TI architecture understanding.

## Key Corrections Made

### 1. Three-Level Architecture Clarified

**Level 1: TI Locations (Where TI Can Appear)**
- graphTypeInterpretation - for the graphType property
- nodeTypesInterpretation - for nodeTypes arrays
- edgeTypesInterpretation - for edgeTypes arrays
- nodeTypeArrayInterpretation - for a subsequence within a nodeTypes array
- edgeTypeArrayInterpretation - for a subsequence within an edgeTypes array
- nodeTypeInterpretation - for a single nodeType
- edgeTypeInterpretation - for a single edgeType
- edgeTypeEndpointNodeTypeInterpretation - for from:/to:/between:/and: (inline nodeType or reference)

**Level 2: TI Structure (How TI Is Expressed)**
- 2-level explicit: `subtypeOf: abstract:` or `exactlyOf: final:` (all valid combinations)
- 1-level shorthand: `concrete:` or `abstract:` (convenience shortcuts)
- 0-level bare: No wrapper (implicit default interpretation)

**Level 3: Type Definition**
- After TI wrappers comes the actual type definition with labels, properties, extensions, etc.

### 2. Key Architectural Principles Added

1. **TI Override**: When an outer TI immediately wraps an inner TI, the outer TI "knocks out" (overrides) the inner TI

2. **TI Default Cascade**: A TI at a higher level (e.g., on graphType or nodeTypes array) establishes a default that can be overridden by more specific TI at lower levels (individual element types)

3. **Facet Independence**: The subtype interpretation facet (`subtypeOf`, `properSubtypesOf`, `exactlyOf`) is a toggle/feature that ANY TI can contain - it is NOT part of the TI location name. Similarly for concreteness facet (`abstract`, `concrete`, `final`, `sealed`).

4. **Exception**: Edge type endpoints can have their own TI wrappers that override the edge type's TI at the endpoint level

### 3. Terminology Corrections

**Removed Incorrect Terms:**
- "Wrapper Nesting" (was described as invalid practice)
- "Usage-Level Interpretation Override" (confusing term)

**Added Correct Terms:**
- "TI Location" - The structural position where TI can be applied
- "TI Structure" - The wrapper syntax (0/1/2-level)
- "TI Override" - Outer TI knocking out inner TI
- "TI Default Cascade" - Higher-level TI establishing defaults
- "Subtype Interpretation Facet" - The toggle feature (subtypeOf/exactlyOf)
- "Concreteness Facet" - The toggle feature (abstract/concrete/final/sealed)

## Files Updated

### 1. `.kiro/specs/type-interpretation-wrappers/requirements.md`
- Updated Glossary with corrected terminology
- Added "Conceptual Foundation: Three-Level TI Architecture" section
- Clarified that facets are toggles, not part of location names
- Added TI Override and TI Default Cascade principles

### 2. `.kiro/specs/type-interpretation-wrappers/design.md`
- Updated Overview to explain three-level architecture
- Added comprehensive "Three-Level TI Architecture" section with tables
- Added "TI Facets (Not Part of Location Names)" section
- Added "TI Override and Default Cascade" section with examples
- Clarified valid combinations after canonicalization

### 3. `.kiro/specs/import-schema-consistency/requirements.md`
- Added "Three-Level TI Architecture" section to Conceptual Foundation
- Listed all 8 TI locations
- Explained TI structure levels
- Added key architectural principles

### 4. `.kiro/specs/import-schema-consistency/design.md`
- Added "0. Three-Level TI Architecture" to Architectural Principles
- Listed TI locations, structures, and type definition level
- Added key principles (override, cascade, facet independence, exception)

## Impact on Implementation

### What Changes in the Code

**No changes needed** - The implementation already handles these concepts correctly:

1. **TI Locations**: The canonicalizing_preprocessor already detects TI at different structural positions
2. **TI Structure**: Already handles 0/1/2-level wrappers and canonicalizes them
3. **TI Override**: Already implements override behavior when outer TI wraps inner TI
4. **Facets**: Already treats subtypeOf/exactlyOf and abstract/concrete as independent toggles

### What Changes in Understanding

**Conceptual clarity** - The specs now correctly explain:

1. **Three distinct levels** instead of confusing nested/non-nested terminology
2. **Facets as toggles** instead of being part of location names
3. **Override vs cascade** as two different mechanisms
4. **Edge endpoint exception** as a special case, not a general rule

## Examples Demonstrating Corrected Architecture

### Example 1: TI Override

```yaml
# Outer TI overrides inner TI
subtypesOf:
  abstract:
    exactlyOf:  # This inner TI is overridden
      concrete:
        nodeType: Person
# Result: Person is interpreted as subtypesOf:abstract
```

### Example 2: TI Default Cascade

```yaml
# Higher-level TI establishes default
graphType:
  subtypesOf:
    abstract:
      nodeTypes:
        - nodeType: Person  # Inherits subtypesOf:abstract from graphType
        - exactlyOf:
            concrete:
              nodeType: Company  # Overrides with exactlyOf:concrete
```

### Example 3: Edge Endpoint Exception

```yaml
# Edge type has TI, but endpoints can override
edgeTypes:
  - subtypesOf:
      abstract:
        edgeType:
          from:
            exactlyOf:  # Endpoint-specific TI overrides edge type's TI
              concrete:
                nodeType: Person
          via: KNOWS
          to: Person
```

### Example 4: Facets as Toggles

```yaml
# subtypeOf is a facet (toggle), not part of location name
# This is nodeTypeInterpretation with subtypeOf facet set to "subtypesOf"
# and concreteness facet set to "abstract"
subtypesOf:
  abstract:
    nodeType: Vehicle

# This is also nodeTypeInterpretation, but with different facet settings
exactlyOf:
  concrete:
    nodeType: Person
```

## Next Steps

With the specs now correctly documenting the three-level architecture:

1. **Continue with current implementation** - The code already handles this correctly
2. **Update documentation** - When writing user-facing docs, use the corrected terminology
3. **Review test examples** - Ensure test examples demonstrate the three levels clearly
4. **Schema validation** - Continue with Phase 2 (JSON Schema updates) using corrected understanding

## Conclusion

The specs now accurately reflect the three-level TI architecture:
- **Level 1**: TI Locations (where TI can appear)
- **Level 2**: TI Structure (how TI is expressed)
- **Level 3**: Type Definition (the actual type specification)

This clarification eliminates confusion about "nesting" and makes it clear that:
- Facets (subtypeOf/exactlyOf, abstract/concrete) are toggles, not location names
- TI Override and TI Default Cascade are two different mechanisms
- Edge endpoints are a special exception to the general rules

The implementation already handles these concepts correctly - this update just brings the documentation in line with the actual behavior.
