# Partition Model Clarification for TI Ordering Refactor

**Date**: 2024-12-06  
**Purpose**: Document the refined understanding of Locations 2, 4, and 6 using the partition model (NOT nesting)

## Critical Clarification: Partition Model vs Nesting Model

**WE ARE USING THE PARTITION MODEL, NOT THE NESTING MODEL**

### Three Distinct Concepts

1. **Location 2/3 - Types Collection** (`nodeTypesInterpretation` / `edgeTypesInterpretation`)
   - A TI wrapper around an ENTIRE collection property
   - Multiple collections can be siblings at the graphType level
   - Example: `graphType` can have `nodeTypes: [...]`, `edgeTypes: [...]`, `nodeTypes: [...]` as siblings

2. **Location 4/5 - Types Array/Subsequence** (`nodeTypeArrayInterpretation` / `edgeTypeArrayInterpretation`)
   - A TI wrapper around a PARTITION BLOCK (subsequence) within a collection
   - Partitions divide a collection into blocks, each with its own TI
   - This is NOT nesting - it's partitioning an array into segments

3. **Location 6/7 - Single Type** (`nodeTypeInterpretation` / `edgeTypeInterpretation`)
   - A TI wrapper around a SINGLE type definition
   - This is DISTINCT from a subsequence with cardinality 1
   - A single type is an atomic unit, not a partition block

### Key Distinction: Partition vs Nesting

**Partition Model** (CORRECT):
```yaml
nodeTypes:
  - typeLabel: Person          # Bare item (no TI)
  - abstract:                  # Partition block 1 (TI-wrapped subsequence)
      - typeLabel: Vehicle
      - typeLabel: Car
  - concrete:                  # Partition block 2 (TI-wrapped subsequence)
      - typeLabel: Company
```

**Nesting Model** (INCORRECT - NOT WHAT WE'RE DOING):
```yaml
nodeTypes:
  - abstract:
      nodeTypes:               # ❌ Nested array - NOT our model
        - abstract:
            nodeTypes:         # ❌ Recursive nesting - NOT our model
              - typeLabel: X
```

### What "Partition" Means

A partition divides a collection into non-overlapping blocks:
- Each block can have its own TI wrapper
- Blocks are siblings within the array
- No recursion or nesting of arrays
- A block can contain multiple items (cardinality ≥ 1)

### Sibling Collections at GraphType Level

Multiple collections can be siblings:

```yaml
graphType:
  nodeTypes:                   # Collection 1 (bare)
    - typeLabel: Person
  edgeTypes:                   # Collection 2 (bare)
    - typeLabel: KNOWS
  abstract:                    # Collection 3 (TI-wrapped nodeTypes)
    nodeTypes:
      - typeLabel: Entity
  concrete:                    # Collection 4 (TI-wrapped edgeTypes)
    edgeTypes:
      - typeLabel: RELATIONSHIP
```

## Changes Required to design.md

### 1. Update Location 4/5 Descriptions

**Current** (mentions "nesting"):
> #### Location 4: nodeTypeArrayInterpretation
> **Current**: Array items with TI inside item content  
> **Target**: `patternProperties` wrapping SUBSEQUENCES within `nodeTypes` array  
> **Change**: Restructure array item schema to support TI wrappers as partition blocks  
> **Semantics**: Wraps subsequences (partition blocks) within the nodeTypes array  

**Should Be** (clarifies partition, not nesting):
> #### Location 4: nodeTypeArrayInterpretation
> **Current**: Array items with TI inside item content  
> **Target**: Support TI wrappers as partition blocks within `nodeTypes` array  
> **Change**: Allow array items to be either bare types OR partition blocks (TI-wrapped subsequences)  
> **Semantics**: Partitions the nodeTypes array into blocks, each with its own TI  
> **Key Distinction**: A partition block (subsequence) is NOT the same as a single type (Location 6)

### 2. Remove "Nested TI" References

**Current** (in Integration Tests section):
> **Cross-Location Tests**:
> - Test TI at multiple locations simultaneously
> - Test nested TI (e.g., GraphType + NodeTypeItem)
> - Test mixed bare and wrapped syntax

**Should Be**:
> **Cross-Location Tests**:
> - Test TI at multiple locations simultaneously
> - Test partition blocks within collections (Locations 4-5)
> - Test mixed bare and wrapped syntax at all levels

### 3. Add Partition Model Explanation

Add a new section after "Three-Level TI System":

```markdown
### Partition Model for Array-Level TIs

**Locations 4-5** use a partition model to divide type collections into blocks:

**Partition Structure**:
- A collection (e.g., `nodeTypes`) can be divided into partition blocks
- Each partition block is a subsequence with its own TI wrapper
- Partition blocks are siblings within the array (not nested)
- A partition block can contain multiple types (cardinality ≥ 1)

**Example - Partitioned nodeTypes Array**:
```yaml
nodeTypes:
  - typeLabel: Person                    # Bare item (no partition)
  - abstract:                            # Partition block 1
      - typeLabel: Vehicle
      - typeLabel: Car
  - concrete:                            # Partition block 2
      - typeLabel: Company
      - typeLabel: Organization
```

**Key Distinctions**:
1. **Collection (Location 2)** vs **Partition Block (Location 4)** vs **Single Type (Location 6)**
   - Collection: Entire `nodeTypes:` property
   - Partition Block: Subsequence within the array
   - Single Type: Individual type definition (atomic unit)

2. **Partition Block** vs **Single Type with Cardinality 1**
   - Partition block with 1 item: `abstract: [{ typeLabel: X }]` (Location 4)
   - Single type: `abstract: { typeLabel: X }` (Location 6)
   - These are DIFFERENT structures with different semantics

3. **Partition** vs **Nesting**
   - Partition: Divides array into sibling blocks (our model)
   - Nesting: Recursive arrays within arrays (NOT our model)
```

### 4. Update Examples to Show Partition Model

Update the "Locations 4-5" example in "Sibling TI Wrapper Support":

**Current**:
```yaml
**Locations 4-5 (nodeTypeArrayInterpretation/edgeTypeArrayInterpretation) - Multiple Item Interpretations as Siblings**:
```yaml
nodeTypes:          # Array containing multiple interpretations as siblings
  - typeLabel: Person                    # Bare item
  - exactlyOf:                          # TI-wrapped item (sibling)
      concrete:
        typeLabel: Company
  - subtypesOf:                         # Another TI-wrapped item (sibling)
      abstract:
        typeLabel: Entity
```

**Should Be**:
```yaml
**Locations 4-5 (nodeTypeArrayInterpretation/edgeTypeArrayInterpretation) - Partition Blocks as Siblings**:
```yaml
nodeTypes:          # Array partitioned into blocks
  - typeLabel: Person                    # Bare item (no partition)
  - exactlyOf:                          # Partition block 1 (TI-wrapped subsequence)
      concrete:
        - typeLabel: Company
        - typeLabel: Organization
  - subtypesOf:                         # Partition block 2 (TI-wrapped subsequence)
      abstract:
        - typeLabel: Entity
        - typeLabel: Thing
```

## Changes Required to tasks.md

### Update Task 12 Description

**Current**:
> ### - [ ] 12. Fix Location 4 (nodeTypeArrayInterpretation)
> 
> Apply correct TI pattern to nodeTypeArrayInterpretation (wraps SUBSEQUENCES within nodeTypes array)
> 
> - Locate NodeTypeItem definition in schema (~line 2200)
> - Restructure to allow TI wrappers wrapping array subsequences (partition blocks)
> - Ensure TI wrappers can wrap individual array items as siblings
> - Add support for 0-level, 1-level, 2-level syntax
> - Validate JSON syntax
> - _Requirements: 1.1, 2.4, 9.1_

**Should Be**:
> ### - [ ] 12. Fix Location 4 (nodeTypeArrayInterpretation)
> 
> Apply partition model to nodeTypeArrayInterpretation (partition blocks within nodeTypes array)
> 
> - Locate NodeTypeItem definition in schema (~line 2200)
> - Allow array items to be EITHER bare types OR partition blocks (TI-wrapped subsequences)
> - Partition blocks are siblings within the array (not nested)
> - Each partition block contains an array of types (cardinality ≥ 1)
> - Distinguish partition blocks (Location 4) from single types (Location 6)
> - Add support for 0-level, 1-level, 2-level syntax
> - Validate JSON syntax
> - _Requirements: 1.1, 2.4, 9.1_
> - _Note: Partition model, not nesting model_

## Summary

**Key Changes**:
1. Replace "nesting" terminology with "partition" terminology
2. Clarify three distinct concepts: collection, partition block, single type
3. Emphasize that partition blocks are siblings (not nested)
4. Distinguish partition block from single type with cardinality 1
5. Update all examples to show partition structure clearly

**Files to Update**:
1. `.kiro/specs/ti-ordering-refactor/design.md` - Add partition model section, update Location 4/5 descriptions, remove nesting references
2. `.kiro/specs/ti-ordering-refactor/tasks.md` - Update Task 12 and 13 descriptions to clarify partition model

