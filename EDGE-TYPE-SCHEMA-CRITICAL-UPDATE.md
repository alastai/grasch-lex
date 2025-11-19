# Edge Type Schema - Critical Update Needed

## Problem

The current JSON Schema only supports OLD edge type syntax, not the new LEX-2026.0.3.2 syntax with `directed:`/`undirected:` wrappers and semantic endpoint names.

### Current (OLD)
```json
"edgeType": {
  "typeLabel": "KNOWS",
  "direction": "DIRECTED",
  "firstEndpointNodeType": {...},
  "secondEndpointNodeType": {...}
}
```

### Required (NEW)
```yaml
edgeType:
  directed:
    from: Person
    via: KNOWS
    to: Person
```

## Impact

Files using new syntax fail validation:
- all-import-patterns.yaml
- type-definition-syntax-examples.yaml
- Others with comprehensive edge examples

## Solution

Update EdgeType schema to support BOTH old and new syntax.

---

**Status**: CRITICAL - Blocking Phase 3
**Priority**: HIGHEST

