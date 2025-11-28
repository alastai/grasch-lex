# Phase E: Array Subsequence TI Analysis

## Goal
Support TI wrappers for subsequences within nodeTypes/edgeTypes arrays (Locations 4+5).

## What Are Array Subsequence TIs?

Array subsequence TIs allow partitioning a nodeTypes or edgeTypes array into multiple blocks, each with its own TI semantics.

### Example Use Case:
```yaml
nodeTypes:
  # Partition 1: Abstract base types
  - abstract:
      - nodeType: { typeLabel: Entity }
      - nodeType: { typeLabel: Thing }
  
  # Partition 2: Concrete types  
  - concrete:
      - nodeType: { typeLabel: Person }
      - nodeType: { typeLabel: Company }
```

## Current Schema Structure

Currently, `nodeTypes` and `edgeTypes` are simple arrays:
- `nodeTypes`: array of `NodeTypeItem`
- `edgeTypes`: array of `EdgeTypeItem`

Each item can have TI wrappers (Location 6/7), but the array itself cannot be partitioned.

## Required Changes

### Location 4: nodeTypeArrayInterpretation
Allow nodeTypes array to contain partition blocks:

```yaml
nodeTypes:
  - abstract:  # Partition block with TI wrapper
      - nodeType: { typeLabel: Base }
  - nodeType: { typeLabel: Concrete }  # Individual item
```

### Location 5: edgeTypeArrayInterpretation  
Same for edgeTypes array.

## Design Decision

**Option 1: Partition blocks as special array items**
- nodeTypes array can contain either:
  - Individual NodeTypeItem (existing)
  - Partition block: TI wrapper containing array of NodeTypeItems (new)

**Option 2: Nested arrays**
- More complex, harder to validate

**Recommendation**: Option 1 - extend NodeTypeItem/EdgeTypeItem oneOf to include partition blocks.

## Next Steps

1. Design partition block schema structure
2. Update NodeTypeItem to support partition blocks
3. Update EdgeTypeItem to support partition blocks  
4. Create test YAML examples
5. Validate

## Status

Phase E not yet started - analysis complete, ready to implement.
