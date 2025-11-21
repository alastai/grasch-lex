# Requirements Document

## Introduction

This specification addresses the aesthetic and syntactic consistency of LEX-2026.0.3.2 YAML examples and JSON schema validation. The goal is to enforce clean, minimal syntax that avoids redundancy while maintaining semantic precision.

## Glossary

- **LEX-2026**: LDBC Extended GQL Schema language version 2026.0.3.2
- **typeLabel**: The primary label identifier for a node or edge type
- **extends**: Keyword for declaring supertype relationships (synonym: supertypes)
- **implies**: Keyword for declaring inherited characteristics
- **adding**: Keyword for declaring additional characteristics beyond supertype
- **Type Interpretation Wrapper**: Structural patterns like `abstract:`, `sealed:`, `subtypesOf:`

## Requirements

### Requirement 1: Eliminate Redundant typeLabel Declarations

**User Story:** As a schema author, I want typeLabels to be declared once, so that schemas are concise and maintainable.

#### Acceptance Criteria

1. WHEN a nodeType or edgeType declares `typeLabel: X` THEN the system SHALL NOT require `X` to be repeated in `implies: labels:`
2. WHEN processing a type definition with `typeLabel: X` THEN the system SHALL automatically include `X` in the type's label set
3. WHEN a subtype declares `typeLabel: Y` and `extends: X` THEN the system SHALL NOT require `Y` to be restated in `adding: labels:`
4. WHEN validating schemas THEN the JSON schema SHALL permit `implies: labels:` to be omitted when only the typeLabel is needed

### Requirement 2: Simplify extends Syntax

**User Story:** As a schema author, I want to use clean extends syntax, so that subtype relationships are immediately clear.

#### Acceptance Criteria

1. WHEN declaring a subtype relationship THEN the system SHALL support `extends: SuperTypeName` as a scalar value
2. WHEN `extends:` is used THEN the system SHALL treat it as synonymous with `supertypes:`
3. WHEN a subtype only adds a new typeLabel THEN the system SHALL NOT require an `adding:` section
4. WHEN `extends:` and `adding:` are both present THEN they SHALL be adjacent keys at the same level (never nested)
5. WHEN validating schemas THEN the JSON schema SHALL accept both `extends: ScalarValue` and `extends: {supertypes: [...], adding: {...}}`

### Requirement 3: Use Bracketed Array Format for Label Sets

**User Story:** As a schema author, I want label sets represented as bracketed arrays, so that they can be reused as scalar values in edge type references.

#### Acceptance Criteria

1. WHEN a type has multiple labels THEN the system SHALL represent them as `[Label1, Label2, Label3]`
2. WHEN a type identifier is a label set THEN the system SHALL use bracketed array format for consistency
3. WHEN edge types reference node types by labels THEN the system SHALL accept bracketed array format in `to:` and `from:` fields
4. WHEN displaying or serializing label sets THEN the system SHALL use flow-style (bracketed) arrays, not block-style sequences

### Requirement 4: Enforce Minimal Syntax Principle

**User Story:** As a schema author, I want to write only what needs to be said, so that schemas are readable and maintainable.

#### Acceptance Criteria

1. WHEN a key would have no semantic content THEN the system SHALL allow it to be omitted
2. WHEN `adding:` would only contain a typeLabel already declared THEN the system SHALL allow `adding:` to be omitted
3. WHEN `implies:` would only contain the typeLabel THEN the system SHALL allow `implies:` to be omitted
4. WHEN validating schemas THEN the JSON schema SHALL make redundant keys optional
5. WHEN a property is nullable THEN the system SHALL use `?` suffix instead of `notNull: false`
6. WHEN a property is not nullable THEN the system SHALL omit `notNull: true` (non-null is default)

### Requirement 5: Update All Example Files

**User Story:** As a developer, I want all example files to follow consistent aesthetics, so that they serve as good references.

#### Acceptance Criteria

1. WHEN reviewing example files THEN all SHALL follow the minimal syntax principles
2. WHEN example files use `extends:` THEN they SHALL use the clean scalar or minimal nested format
3. WHEN example files declare typeLabels THEN they SHALL NOT redundantly repeat them in implies or adding
4. WHEN example files use label sets THEN they SHALL use bracketed array format
5. WHEN all examples are updated THEN validation tests SHALL pass

### Requirement 6: Update JSON Schema Validation

**User Story:** As a schema validator, I want the JSON schema to accept clean syntax, so that minimal examples validate correctly.

#### Acceptance Criteria

1. WHEN the JSON schema validates `extends:` THEN it SHALL accept both scalar strings and object forms
2. WHEN the JSON schema validates type definitions THEN it SHALL make `implies: labels:` optional
3. WHEN the JSON schema validates subtypes THEN it SHALL make `adding: labels:` optional
4. WHEN the JSON schema validates label sets THEN it SHALL accept both array formats (flow and block style)
5. WHEN schema changes are complete THEN all existing valid examples SHALL continue to validate

### Requirement 7: Refactor Nullability Syntax

**User Story:** As a schema author, I want nullability expressed through concise syntax, so that property definitions are more readable.

#### Acceptance Criteria

1. WHEN a property name is written as `name: identifier` (no `?`) THEN the system SHALL interpret it as NOT NULL
2. WHEN a property name is written as `name: identifier?` (with space-separated `?`) THEN the system SHALL interpret it as NULLABLE
3. WHEN the API is queried THEN it SHALL provide `isNullable()`, `isNotNull()`, and `isNotNullable()` methods
4. WHEN processing property definitions THEN the system SHALL NOT require or accept the `notNull:` key
5. WHEN validating schemas THEN the JSON schema SHALL reject `notNull:` key and require the `?` suffix syntax
6. WHEN all examples are updated THEN they SHALL use `name: identifier` or `name: identifier?` format
