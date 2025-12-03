# Edge Type Property Ordering - Corrected Design

**Date**: 2024-12-03  
**Status**: 🔵 AWAITING CONFIRMATION BEFORE IMPLEMENTATION

## Corrected Understanding

The three keys (`via:`, `arc:`, `typeLabel:`) are **synonyms** - only ONE of them appears in any given edge type definition. They are NOT all present simultaneously.

### Mandated Property Order for Directed Edges

**Three sibling properties at the same level:**

```yaml
edgeType:
  directed:
    from:        # Property 1: Source endpoint (required)
    to:          # Property 2: Target endpoint (required)
    via:         # Property 3: Edge label (required - use ONE of: via/arc/typeLabel)
    # OR arc:    # Property 3: Edge label (synonym for via)
    # OR typeLabel:  # Property 3: Edge label (synonym for via/arc)
    implies:     # Property 4: Content specification (optional)
      labels:    #   - Label types (optional)
      propertyTypes:  #   - Property types (optional)
```

**Key points:**
- `from:`, `to:`, and `via:` (or `arc:` or `typeLabel:`) are **three sibling properties**
- They appear at the same level inside `directed:`
- Only ONE of `via:`/`arc:`/`typeLabel:` appears (they are synonyms)
- Order: `from:` → `to:` → `via:`/`arc:`/`typeLabel:` → `implies:` (optional)

### Mandated Property Order for Undirected Edges

**Three sibling properties at the same level:**

```yaml
edgeType:
  undirected:
    between:     # Property 1: Endpoints specification (required)
    and:         # Property 2: Edge label (required - use ONE of: and/via/typeLabel)
    # OR via:    # Property 2: Edge label (synonym for and)
    # OR typeLabel:  # Property 2: Edge label (synonym for and/via)
    implies:     # Property 3: Content specification (optional)
      labels:    #   - Label types (optional)
      propertyTypes:  #   - Property types (optional)
```

**Key points:**
- `between:`, `and:` (or `via:` or `typeLabel:`), and `implies:` are **three sibling properties**
- They appear at the same level inside `undirected:`
- Only ONE of `and:`/`via:`/`typeLabel:` appears (they are synonyms)
- Order: `between:` → `and:`/`via:`/`typeLabel:` → `implies:` (optional)

## Synonym Rules

### For Directed Edges
- **Preferred**: `via:` 
- **Synonyms**: `arc:`, `typeLabel:`
- All three mean the same thing
- Only ONE appears in any given edge type

### For Undirected Edges
- **Preferred**: `and:`
- **Synonyms**: `via:`, `typeLabel:`
- All three mean the same thing
- Only ONE appears in any given edge type

## Examples

### Directed Edge with `via:` (preferred)
```yaml
edgeType:
  directed:
    from:
      nodeType:
        typeLabel: Person
    to:
      nodeType:
        typeLabel: Person
    via: KNOWS
    implies:
      propertyTypes:
        - name: since
          valueType: DATE
```

### Directed Edge with `arc:` (synonym)
```yaml
edgeType:
  directed:
    from:
      nodeType:
        typeLabel: Person
    to:
      nodeType:
        typeLabel: Person
    arc: KNOWS
```

### Directed Edge with `typeLabel:` (synonym)
```yaml
edgeType:
  directed:
    from:
      nodeType:
        typeLabel: Person
    to:
      nodeType:
        typeLabel: Person
    typeLabel: KNOWS
```

### Undirected Edge with `and:` (preferred)
```yaml
edgeType:
  undirected:
    between:
      - nodeType:
          typeLabel: Person
      - nodeType:
          typeLabel: Person
    and: FRIENDS_WITH
```

### Undirected Edge with `via:` (synonym)
```yaml
edgeType:
  undirected:
    between:
      - nodeType:
          typeLabel: Person
      - nodeType:
          typeLabel: Person
    via: FRIENDS_WITH
```

### Undirected Edge with `typeLabel:` (synonym)
```yaml
edgeType:
  undirected:
    between:
      - nodeType:
          typeLabel: Person
      - nodeType:
          typeLabel: Person
    typeLabel: FRIENDS_WITH
```

## What This Means for Implementation

1. **Schema Changes**:
   - `DirectedEdgeTypeEndpoints` must accept `via:`, `arc:`, OR `typeLabel:` (mutually exclusive)
   - `UndirectedEdgeTypeEndpoints` must accept `and:`, `via:`, OR `typeLabel:` (mutually exclusive)
   - Property order must be enforced in JSON Schema

2. **Example File Updates**:
   - Each directed edge uses ONE of: `via:`, `arc:`, or `typeLabel:`
   - Each undirected edge uses ONE of: `and:`, `via:`, or `typeLabel:`
   - Properties must appear in the mandated order

3. **Test File Updates**:
   - Create tests showing all three synonym variants for directed edges
   - Create tests showing all three synonym variants for undirected edges
   - Create negative tests showing multiple synonyms (should fail)

## Question for Confirmation

Is this understanding correct? Specifically:
- ✅ `via:`, `arc:`, and `typeLabel:` are synonyms (only ONE appears)
- ✅ For directed: three sibling properties are `from:`, `to:`, and `via:`/`arc:`/`typeLabel:`
- ✅ For undirected: three sibling properties are `between:`, `and:`/`via:`/`typeLabel:`, and `implies:`
- ✅ The ordering is about the sequence these properties appear in the YAML

**AWAITING CONFIRMATION BEFORE PROCEEDING WITH IMPLEMENTATION**
