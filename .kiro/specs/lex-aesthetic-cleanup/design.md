# Design Document

## Overview

This design addresses aesthetic and syntactic cleanup of LEX-2026.0.3.2 to enforce minimal, clean syntax across all YAML examples and JSON schema validation rules. The core principle is: **say what needs to be said, nothing more**.

## Architecture

The cleanup involves three layers:

1. **Example Files**: Update all YAML examples to follow clean syntax
2. **JSON Schema**: Modify validation rules to accept minimal syntax
3. **Documentation**: Update any guides or references to reflect clean patterns

## Components and Interfaces

### Example File Updates

**Affected Files:**
- `src/grasch/examples/imports/snb-types/*.yaml` (SNB hierarchy files)
- `src/grasch/examples/lex-2026.0.3.2-*.yaml` (main example files)
- Any other YAML files using verbose syntax

**Transformation Patterns:**

```yaml
# BEFORE (verbose)
- nodeType:
    typeLabel: Company
    extends:
      supertypes:
        - Organisation
      adding:
        labels:
          - Company

# AFTER (clean)
- nodeType:
    typeLabel: Company
    extends: Organisation
```

### JSON Schema Updates

**Schema File:** `src/grasch/schemas/lex-2026.0.3.2.schema.json`

**Key Changes:**

1. Make `extends` accept both scalar and object forms
2. Make `implies.labels` optional (can be inferred from typeLabel)
3. Make `adding.labels` optional (can be inferred from typeLabel)
4. Accept both flow-style `[A, B]` and block-style arrays

## Data Models

### Type Definition Structure (Minimal Form)

```yaml
nodeType:
  typeLabel: TypeName          # Required
  extends: SuperType           # Optional, scalar or object
  implies:                     # Optional
    propertyTypes: [...]       # Only if adding properties
  # labels omitted - inferred from typeLabel
```

### Type Definition Structure (With Extensions)

```yaml
nodeType:
  typeLabel: SubType
  extends: SuperType
  adding:                      # Only when adding beyond typeLabel
    propertyTypes: [...]
    # labels omitted - inferred from typeLabel
```

### Abstract Type Pattern

```yaml
- abstract:
    nodeType:
      typeLabel: AbstractType
      implies:
        propertyTypes: [...]
        # labels omitted - inferred from typeLabel
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: typeLabel Inference
*For any* type definition with `typeLabel: X`, the processed type should include `X` in its label set even if `implies: labels:` is omitted
**Validates: Requirements 1.2**

### Property 2: extends Scalar Equivalence
*For any* type definition, `extends: X` should be semantically equivalent to `extends: {supertypes: [X]}`
**Validates: Requirements 2.1**

### Property 3: Minimal Syntax Validation
*For any* valid minimal-syntax example, validation against the JSON schema should succeed
**Validates: Requirements 4.1, 6.2**

### Property 4: Backward Compatibility
*For any* example that validated before changes, it should continue to validate after changes
**Validates: Requirements 6.5**

### Property 5: Label Set Format Consistency
*For any* label set in examples, it should use bracketed array format `[A, B, C]`
**Validates: Requirements 3.1**

### Property 6: Nullability Syntax Round-Trip
*For any* property with `name: identifier`, parsing should yield `isNotNull() == true` and `isNullable() == false`
**Validates: Requirements 7.1, 7.3**

### Property 7: Nullable Syntax Round-Trip
*For any* property with `name: identifier?`, parsing should yield `isNullable() == true` and `isNotNull() == false`
**Validates: Requirements 7.2, 7.3**

### Property 8: notNull Key Rejection
*For any* property definition containing `notNull:` key, validation should fail
**Validates: Requirements 7.4, 7.5**

## Error Handling

- Schema validation errors should clearly indicate when optional fields are incorrectly required
- Preprocessor should handle both verbose and minimal syntax transparently
- Migration errors should be logged with file paths and line numbers

## Testing Strategy

### Unit Tests

- Test JSON schema accepts minimal syntax
- Test JSON schema accepts verbose syntax (backward compatibility)
- Test preprocessor handles both forms correctly
- Test label inference from typeLabel

### Property-Based Tests

- Property 1: Generate random type definitions, verify label inference
- Property 2: Generate random extends patterns, verify semantic equivalence
- Property 3: Generate minimal examples, verify validation succeeds
- Property 4: Use existing examples, verify continued validation

### Integration Tests

- Validate all updated example files
- Run full validation suite after changes
- Test import resolution with minimal syntax
