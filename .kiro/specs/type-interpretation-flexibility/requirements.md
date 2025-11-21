# Requirements Document

## Introduction

This specification addresses the need for flexible type interpretation wrappers in LEX-2026.0.3.2 schema. The fundamental pattern is `graphType: nodeTypes: - nodeType:` where type interpretations (`abstract`, `final`, `sealed`, `subtypesOf`) can wrap either the entire `nodeTypes` array, or individual `- nodeType:` items, or subsequences of items. Type definitions can be imported, but there is no recursion - `nodeType` objects never contain `nodeTypes` arrays.

## Glossary

- **Type Interpretation Wrapper**: A YAML/JSON structure that modifies how types are interpreted (e.g., `abstract`, `final`, `sealed`, `subtypesOf`)
- **NodeType**: A node type definition with typeLabel, properties, and constraints (the `- nodeType:` item)
- **EdgeType**: An edge type definition with typeLabel, endpoints, properties, and constraints
- **nodeTypes Array**: The array property containing node type items (appears as `nodeTypes:` in YAML)
- **Type Interpretation**: A wrapper that can be applied at the nodeTypes array level or at individual array item level
- **Abstract Type**: A type that cannot be instantiated directly but serves as a supertype
- **Final Type**: A type that cannot be subtyped further
- **Concrete Type**: A type that can be instantiated (default behavior)

## Requirements

### Requirement 1

**User Story:** As a schema designer, I want type interpretations to wrap nodeTypes arrays or individual nodeType items flexibly, so that I can express complex type hierarchies clearly.

#### Acceptance Criteria

1. THE Schema SHALL support the basic pattern `graphType: nodeTypes: - nodeType:` where `- nodeType:` items appear only inside `nodeTypes:` arrays
2. THE Schema SHALL allow `abstract` to wrap an entire `nodeTypes:` array (e.g., `abstract: nodeTypes: [...]`)
3. THE Schema SHALL allow `abstract` to wrap individual `- nodeType:` items (e.g., `- abstract: nodeType: ...`)
4. THE Schema SHALL allow `abstract` to wrap a subsequence of `- nodeType:` items within a nodeTypes array
5. THE Schema SHALL apply the same wrapping flexibility to `final`, `sealed`, and `subtypesOf` interpretations

### Requirement 2

**User Story:** As a schema designer, I want to import type definitions within type interpretation wrappers, so that I can reuse type hierarchies across schemas.

#### Acceptance Criteria

1. WHEN a type interpretation wrapper contains type definitions, THE Schema SHALL allow those definitions to be imported from external files
2. THE Schema SHALL support `import` statements within type interpretation contexts
3. THE Schema SHALL validate that imported content matches the expected structure for the interpretation context

### Requirement 3

**User Story:** As a schema implementer, I want the schema to prevent recursive nesting, so that the structure remains simple and predictable.

#### Acceptance Criteria

1. THE Schema SHALL enforce that `nodeType` objects never contain `nodeTypes` arrays
2. THE Schema SHALL enforce that `edgeType` objects never contain `edgeTypes` arrays
3. THE Schema SHALL reject any structure attempting to nest type arrays within type definitions
4. THE Schema SHALL allow only one level of type interpretation wrapping (no interpretation wrappers inside interpretation wrappers)

### Requirement 4

**User Story:** As a schema designer, I want to define an abstract supertype with final subtypes in an importable fragment, so that I can create sealed type hierarchies.

#### Acceptance Criteria

1. THE Schema SHALL support a pattern where `abstract: nodeTypes:` contains a mix of abstract and final wrapped nodeType items
2. WHEN snb-place-hierarchy defines Place as abstract with City, Country, Continent as final subtypes, THE Schema SHALL validate this structure
3. THE Schema SHALL allow the pattern: `abstract: nodeTypes: [- abstract: nodeType: Place, - final: nodeType: City, - final: nodeType: Country]`
4. THE Schema SHALL support this pattern in importable fragments that can be referenced from graph schemas

### Requirement 5

**User Story:** As a schema validator, I want all 14 example files to validate successfully, so that I can confirm the schema correctly implements the type interpretation system.

#### Acceptance Criteria

1. THE snb-place-hierarchy.yaml file SHALL be corrected to use proper type interpretation wrapping
2. THE snb-organisation-hierarchy.yaml file SHALL be corrected to use proper type interpretation wrapping
3. ALL 14 example files SHALL validate successfully after schema and example corrections
4. THE Validator SHALL provide clear error messages when type interpretation patterns are incorrect
