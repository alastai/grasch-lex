# LEX-2026.0.3.2 Schema Update Requirements

## Introduction

This specification defines the requirements for updating the LEX-2026.0.3.2 JSON Schema to properly support three distinct document types (graph, graphSchema, catalog) with correct root properties, import mechanisms, and structural organization. The update addresses critical issues identified in the gap analysis where the current schema incorrectly uses `pathName` at the top level instead of proper document type roots.

## Glossary

- **JSON_Schema**: The LEX-2026.0.3.2 JSON Schema file that validates YAML/JSON documents
- **Document_Type**: One of three root document types: graph, graphSchema, or catalog
- **Import_Pattern**: The oneOf pattern supporting inline definitions, import-only, and mixed mode
- **GraphSchema_Document**: Document with `graphSchema:` root containing pathName and graphType
- **Graph_Document**: Document with `graph:` root containing pathName and optional schema/storage references
- **Catalog_Document**: Document with `catalog:` root containing IRI and directory structure
- **pathName**: Mixed-case property name (NOT pathname) used for path identification

## Requirements

### Requirement 1: Top-Level Document Type Structure

**User Story:** As a schema validator, I want the JSON Schema to enforce correct document type roots so that all LEX documents have proper structure with graph:, graphSchema:, or catalog: at the top level.

#### Acceptance Criteria

1. WHEN the JSON_Schema validates a document THEN the system SHALL require exactly one of three root properties: graph, graphSchema, or catalog
2. WHEN a graphSchema document is validated THEN the system SHALL require the graphSchema root property with pathName and graphType as children
3. WHEN a graph document is validated THEN the system SHALL require the graph root property with pathName as a required child
4. WHEN a catalog document is validated THEN the system SHALL require the catalog root property with IRI as a required child
5. WHEN the top-level oneOf is evaluated THEN the system SHALL remove the old pathName + properties pattern that incorrectly placed pathName at the document root
6. IF a document has pathName at the top level THEN the system SHALL reject it as invalid (pathName must be inside the document type root)

### Requirement 2: GraphSchema Document Type Definition

**User Story:** As a schema author, I want to define graph schemas with the graphSchema: root so that my schema definitions are properly structured and validated.

#### Acceptance Criteria

1. WHEN I create a GraphSchema document THEN the system SHALL require graphSchema as the root property
2. WHEN graphSchema is defined THEN the system SHALL require pathName (mixed case) as a required property
3. WHEN graphSchema is defined THEN the system SHALL require graphType as a required property
4. WHEN graphType is specified THEN the system SHALL support the complete GraphType definition with optional pathName property
5. WHEN nodeTypes are defined in graphType THEN the system SHALL make them optional (not required)
6. WHEN edgeTypes are defined in graphType THEN the system SHALL make them optional (not required)
7. WHEN defaults are defined in graphType THEN the system SHALL keep them required with existing oneOf pattern
8. WHEN nodeTypes support imports THEN the system SHALL use the oneOf import pattern (inline, import-only, mixed)
9. WHEN edgeTypes support imports THEN the system SHALL use the oneOf import pattern (inline, import-only, mixed)
10. IF graphSchema validation fails THEN the system SHALL provide clear error messages indicating which required properties are missing

### Requirement 3: Graph Document Type Definition

**User Story:** As a graph instance author, I want to define graph instances with the graph: root so that my graph data references schemas correctly and includes storage information.

#### Acceptance Criteria

1. WHEN I create a Graph document THEN the system SHALL require graph as the root property
2. WHEN graph is defined THEN the system SHALL require pathName (mixed case) inside the graph object
3. WHEN graph references a schema THEN the system SHALL support graphSchema property with import oneOf pattern
4. WHEN graph specifies storage THEN the system SHALL support graphStorageSchema property (renamed from storageSchema) with import oneOf pattern
5. WHEN graph includes subtyping metadata THEN the system SHALL preserve subtypesOfSchemaType property for future use
6. WHEN the old pathName at document root exists THEN the system SHALL reject it (pathName must be inside graph object)
7. WHEN the old redundant graph.pathName exists THEN the system SHALL use only the pathName inside graph object
8. IF storageSchema property is used THEN the system SHALL reject it (must use graphStorageSchema)

### Requirement 4: Catalog Document Type Definition

**User Story:** As a catalog author, I want to define catalogs with the catalog: root so that my hierarchical directory structures are properly validated.

#### Acceptance Criteria

1. WHEN I create a Catalog document THEN the system SHALL require catalog as the root property
2. WHEN catalog is defined THEN the system SHALL require IRI as a required property with IRI format validation
3. WHEN catalog contains directories THEN the system SHALL support recursive Directory structure with import oneOf pattern
4. WHEN directories reference schemas THEN the system SHALL use graphSchemaReferences (not graphSchemas) with proper reference structure
5. WHEN directories reference graphs THEN the system SHALL use graphReferences (not graphs) with proper reference structure
6. WHEN references are defined THEN the system SHALL require name and qualifiedName properties
7. WHEN references include file paths THEN the system SHALL support optional filePath property
8. WHEN the old pathName at document root exists THEN the system SHALL reject it (catalogs don't have pathName)
9. IF old property names (graphSchemas, graphs) are used THEN the system SHALL reject them (must use graphSchemaReferences, graphReferences)

### Requirement 5: Directory and Reference Structure

**User Story:** As a catalog designer, I want recursive directory structures with proper reference types so that I can organize schemas and graphs hierarchically.

#### Acceptance Criteria

1. WHEN Directory is defined THEN the system SHALL require name as the only required property
2. WHEN Directory contains subdirectories THEN the system SHALL support recursive directories array referencing Directory definition
3. WHEN Directory references schemas THEN the system SHALL support graphSchemaReferences array with GraphSchemaReference items
4. WHEN Directory references graphs THEN the system SHALL support graphReferences array with GraphReference items
5. WHEN GraphReference is defined THEN the system SHALL require name and qualifiedName properties
6. WHEN GraphSchemaReference is defined THEN the system SHALL require name and qualifiedName properties
7. WHEN references include file locations THEN the system SHALL support optional filePath property
8. WHEN directories support imports THEN the system SHALL use the oneOf import pattern for the directories array
9. IF invalid reference structure is provided THEN the system SHALL reject with clear error messages

### Requirement 6: Import Support Pattern

**User Story:** As a schema modularization expert, I want consistent import patterns across all importable elements so that I can reuse definitions and override properties as needed.

#### Acceptance Criteria

1. WHEN an element supports imports THEN the system SHALL use the standard oneOf pattern with three alternatives
2. WHEN inline definition is used THEN the system SHALL validate all inline properties and ensure import property is NOT present
3. WHEN import-only is used THEN the system SHALL require import property and allow maxProperties of 1
4. WHEN mixed mode is used THEN the system SHALL require import property and allow inline property overrides with minProperties of 2
5. WHEN graphSchema property supports imports THEN the system SHALL apply the import oneOf pattern
6. WHEN graphStorageSchema property supports imports THEN the system SHALL apply the import oneOf pattern
7. WHEN graphType property supports imports THEN the system SHALL apply the import oneOf pattern
8. WHEN nodeTypes array supports imports THEN the system SHALL apply the import oneOf pattern
9. WHEN edgeTypes array supports imports THEN the system SHALL apply the import oneOf pattern
10. WHEN directories array supports imports THEN the system SHALL apply the import oneOf pattern with recursive structure support
11. IF import pattern validation fails THEN the system SHALL provide clear error messages indicating which import mode was attempted

### Requirement 7: Property Naming Consistency

**User Story:** As a schema maintainer, I want consistent property naming with pathName (mixed case) throughout so that there's no confusion between pathname and pathName.

#### Acceptance Criteria

1. WHEN any document uses path names THEN the system SHALL use pathName (mixed case) consistently
2. WHEN GraphSchema is defined THEN the system SHALL use pathName (not pathname)
3. WHEN Graph is defined THEN the system SHALL use pathName (not pathname)
4. WHEN GraphType optionally includes path THEN the system SHALL use pathName (not pathname)
5. IF pathname (lowercase) is used anywhere THEN the system SHALL reject it as invalid

### Requirement 8: Preservation of Future Features

**User Story:** As a forward-looking developer, I want abstract and subtyping properties preserved so that future LEX versions can build on this foundation.

#### Acceptance Criteria

1. WHEN graph documents include subtyping metadata THEN the system SHALL preserve subtypesOfSchemaType property
2. WHEN abstract supertypes are defined THEN the system SHALL preserve abstractSupertypes structure in allowSubtypesOf
3. WHEN future extension points exist THEN the system SHALL maintain them in the schema without removing them
4. IF these properties are used in current documents THEN the system SHALL validate them but not require implementation

### Requirement 9: Schema Self-Validation

**User Story:** As a schema developer, I want the JSON Schema itself to be valid so that it can be used with standard JSON Schema validators.

#### Acceptance Criteria

1. WHEN the JSON_Schema is parsed THEN the system SHALL validate it as a valid JSON Schema Draft 2020-12 document
2. WHEN $defs are referenced THEN the system SHALL ensure all $ref pointers resolve correctly
3. WHEN oneOf patterns are used THEN the system SHALL ensure they are mutually exclusive and complete
4. WHEN recursive structures are defined THEN the system SHALL ensure they don't create infinite loops in validation
5. IF the schema itself is invalid THEN the system SHALL report specific validation errors with line numbers

### Requirement 10: Example Document Updates

**User Story:** As a documentation maintainer, I want all example YAML files updated to match the new schema so that users have correct reference implementations.

#### Acceptance Criteria

1. WHEN GraphSchema examples are updated THEN the system SHALL wrap all content in graphSchema: root with proper indentation
2. WHEN Graph examples are updated THEN the system SHALL wrap all content in graph: root and rename storageSchema to graphStorageSchema
3. WHEN Catalog examples are updated THEN the system SHALL rename graphSchemas to graphSchemaReferences and graphs to graphReferences
4. WHEN examples are validated THEN the system SHALL ensure all examples pass validation against the updated schema
5. WHEN transformation is applied THEN the system SHALL preserve all abstract and subTypesOf properties
6. WHEN pathName is used THEN the system SHALL ensure it's inside the document type root, not at the top level
7. IF any example fails validation THEN the system SHALL report which example and which validation rule failed
