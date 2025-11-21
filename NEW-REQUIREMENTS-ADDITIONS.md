### Requirement LEX-9

**User Story:** As a developer working with LEX:2026.0.3.2, I want to work with three distinct top-level document types (catalog, graphSchema, graph), so that I can clearly distinguish between catalog definitions, schema definitions, and graph instance definitions.

#### Acceptance Criteria

1. WHEN I create a LEX document THEN the system SHALL support exactly three top-level document types: catalog, graphSchema, and graph
2. WHEN I create a catalog document THEN the system SHALL require the root element to be `catalog:` with IRI and optional directories
3. WHEN I create a graphSchema document THEN the system SHALL require the root element to be `graphSchema:` with pathName and graphType
4. WHEN I create a graph instance document THEN the system SHALL require the root element to be `graph:` with pathName and optional graphSchema
5. WHEN I attempt to create a graphType as a top-level document THEN the system SHALL reject it as invalid (graphType must be contained within graphSchema)
6. WHEN I validate a LEX document THEN the system SHALL use JSON Schema oneOf to discriminate between the three document types
7. WHEN I serialize a catalog THEN the system SHALL use `catalog:` as the root element
8. WHEN I serialize a graphSchema THEN the system SHALL use `graphSchema:` as the root element
9. WHEN I serialize a graph instance THEN the system SHALL use `graph:` as the root element
10. WHEN I work with graphType THEN the system SHALL ensure it only appears nested within graphSchema documents
11. WHEN I reference document types in APIs THEN the system SHALL use consistent terminology: Catalog, GraphSchema, Graph (not GraphType as top-level)
### Requirement LEX-10

**User Story:** As a developer working with complex schemas, I want comprehensive import and modularization capabilities, so that I can organize schemas into reusable components and maintain them separately.

#### Acceptance Criteria

1. WHEN I work with IMPORTABLE elements THEN the system SHALL support three import modes: inline-only, import-only, and mixed (import with inline overrides)
2. WHEN I import an element THEN the system SHALL use the syntax `import: "filepath"` to reference external files
3. WHEN I import graphType defaults THEN the system SHALL support `defaults: import: "file.yaml"` syntax
4. WHEN I import nodeTypes THEN the system SHALL support importing the entire nodeTypes array with `nodeTypes: import: "file.yaml"`
5. WHEN I import edgeTypes THEN the system SHALL support importing the entire edgeTypes array with `edgeTypes: import: "file.yaml"`
6. WHEN I use mixed mode for nodeTypes THEN the system SHALL allow arrays containing both inline definitions and import references
7. WHEN I use mixed mode for edgeTypes THEN the system SHALL allow arrays containing both inline definitions and import references
8. WHEN I import a file THEN the system SHALL support two file formats: with root element (e.g., `nodeTypes: [...]`) or without root element (just the array contents)
9. WHEN I import directories in catalogs THEN the system SHALL support `directories: import: "file.yaml"` syntax
10. WHEN I import graphSchema in a graph document THEN the system SHALL support `graphSchema: import: "file.yaml"` syntax
11. WHEN I import graphStorageSchema THEN the system SHALL support `graphStorageSchema: import: "file.yaml"` syntax
12. WHEN I use nested imports THEN the system SHALL resolve imports recursively (imported files can import other files)
13. WHEN I work with import paths THEN the system SHALL resolve relative paths relative to the importing file's location
14. WHEN I serialize schemas with imports THEN the system SHALL preserve import references rather than inlining content
15. WHEN import resolution fails THEN the system SHALL provide clear error messages indicating which file and import path failed
### Requirement LEX-11

**User Story:** As a developer working with LEX:2026.0.3.2, I want to use the new edge type syntax with semantic endpoint names and integrated direction, so that I can write more readable and expressive edge type definitions.

#### Acceptance Criteria

1. WHEN I define a directed edge type THEN the system SHALL support the `directed:` wrapper containing endpoint and label specifications
2. WHEN I define an undirected edge type THEN the system SHALL support the `undirected:` wrapper containing endpoint and label specifications
3. WHEN I specify an edge label THEN the system SHALL support the `via:` keyword within the direction wrapper
4. WHEN I specify an edge label THEN the system SHALL support `arc:` as a synonym for `via:`
5. WHEN I define directed edge endpoints THEN the system SHALL support the primary syntax: `from:` for source and `to:` for target
6. WHEN I define directed edge endpoints THEN the system SHALL support synonym set 1: `tail:` for source and `head:` for target
7. WHEN I define directed edge endpoints THEN the system SHALL support synonym set 2: `src:` for source and `dst:` or `dest:` for target
8. WHEN I define undirected edge endpoints THEN the system SHALL support the primary syntax: `between:` for first endpoint and `and:` for second endpoint
9. WHEN I define a self-loop edge THEN the system SHALL support the `SAME` keyword to indicate the second endpoint is the same as the first
10. WHEN I define a self-loop edge THEN the system SHALL support `SELF` as a synonym for `SAME`
11. WHEN I reference node types in endpoints THEN the system SHALL support typeLabel strings (e.g., `from: Person`)
12. WHEN I reference node types in endpoints THEN the system SHALL support typeIdentifier arrays (e.g., `from: [Person, Employee]`)
13. WHEN I reference node types in endpoints THEN the system SHALL support index integers (e.g., `from: 0`)
14. WHEN I define edge-only node types THEN the system SHALL support inline node type definitions within endpoint specifications
15. WHEN I define abstract endpoint requirements THEN the system SHALL support `abstract:` wrapper for endpoint node types (e.g., `to: abstract: Person`)
16. WHEN I define abstract endpoint requirements THEN the system SHALL support `abstractSupertype:` as a synonym for `abstract:`
17. WHEN I omit the edge label THEN the system SHALL allow anonymous edge types without `via:` or `arc:` keywords
18. WHEN I omit properties THEN the system SHALL allow edge types without `implies:` block when no properties are defined
19. WHEN I work with the API THEN the system SHALL provide all synonym accessors (getVia, getArc, getFrom, getTail, getSrc, getTo, getHead, getDst, getDest, getBetween, getAnd) with no canonical form
20. WHEN I migrate from old syntax THEN the system SHALL continue to validate old syntax (`direction:`, `firstEndpointNodeType:`, `secondEndpointNodeType:`) but mark it as deprecated
### Requirement LEX-12

**User Story:** As a developer designing type hierarchies, I want to use abstract, sealed, and final type modifiers, so that I can control type instantiation and extension in my schemas.

#### Acceptance Criteria

1. WHEN I define an abstract type THEN the system SHALL support the `abstract:` wrapper around nodeType or edgeType definitions
2. WHEN I define an abstract type THEN the system SHALL support `abstractSupertype:` as a synonym for `abstract:`
3. WHEN I work with abstract types THEN the system SHALL prevent direct instantiation of abstract types (only subtypes can be instantiated)
4. WHEN I define a sealed hierarchy THEN the system SHALL support the `sealed:` wrapper around a collection of related types
5. WHEN I work with sealed hierarchies THEN the system SHALL ensure no types outside the sealed block can extend types within it
6. WHEN I work with sealed hierarchies THEN the system SHALL treat all leaf types in the hierarchy as implicitly final
7. WHEN I define a final type THEN the system SHALL support the `final:` wrapper around nodeType or edgeType definitions
8. WHEN I work with final types THEN the system SHALL prevent any subtyping of final types
9. WHEN I validate type hierarchies THEN the system SHALL enforce the equivalence rule: `sealed:` ≡ `final:` on all leaf subtypes
10. WHEN I use abstract interpretation with allowSubtypesOf THEN the system SHALL reject schemas where all element types are final (abstract interpretation requires extensible types)
11. WHEN I use abstract interpretation with allowSubtypesOf THEN the system SHALL reject schemas where all element types are in sealed hierarchies
12. WHEN I work with the API THEN the system SHALL provide `isAbstract()` method to check if a type is abstract
13. WHEN I work with the API THEN the system SHALL provide `isFinal()` method to check if a type is final
14. WHEN I work with the API THEN the system SHALL provide `isSealed()` method to check if a type is part of a sealed hierarchy
15. WHEN I work with the API THEN the system SHALL provide `getSealedHierarchy()` method to retrieve all types in a sealed hierarchy
16. WHEN I validate schemas THEN the system SHALL use application-level semantic validation to enforce abstract/sealed/final constraints (JSON Schema validates syntax only)
17. WHEN I document type hierarchies THEN the system SHALL clearly indicate which types are abstract, sealed, or final in schema metadata
### Requirement LEX-13

**User Story:** As a developer defining graph types, I want to specify default values for graph type characteristics in a required defaults block, so that I can configure minimum/maximum labels and properties consistently.

#### Acceptance Criteria

1. WHEN I define a graphType THEN the system SHALL require a `defaults:` block as a mandatory property
2. WHEN I specify defaults THEN the system SHALL support inline definition with properties like graphPreferredName, nodePreferredName, edgePreferredName
3. WHEN I specify defaults THEN the system SHALL support import syntax: `defaults: import: "file.yaml"`
4. WHEN I define node type constraints THEN the system SHALL support `nodeTypeMinimumLabels` with default value 1
5. WHEN I define node type constraints THEN the system SHALL support `nodeTypeMaximumLabels` as optional integer
6. WHEN I define node type constraints THEN the system SHALL support `nodeTypeMinimumPropertyTypes` with default value 0
7. WHEN I define node type constraints THEN the system SHALL support `nodeTypeMaximumPropertyTypes` as optional integer
8. WHEN I define edge type constraints THEN the system SHALL support `edgeTypeMinimumLabels` with default value 1
9. WHEN I define edge type constraints THEN the system SHALL support `edgeTypeMaximumLabels` as optional integer
10. WHEN I define edge type constraints THEN the system SHALL support `edgeTypeMinimumPropertyTypes` with default value 0
11. WHEN I define edge type constraints THEN the system SHALL support `edgeTypeMaximumPropertyTypes` as optional integer
12. WHEN I specify preferred names THEN the system SHALL support `graphPreferredName` with values "GRAPH" or "PROPERTY GRAPH"
13. WHEN I specify preferred names THEN the system SHALL support `nodePreferredName` with values "NODE" or "VERTEX"
14. WHEN I specify preferred names THEN the system SHALL support `edgePreferredName` with values "EDGE" or "RELATIONSHIP"
15. WHEN I import defaults THEN the system SHALL resolve the import path relative to the importing file
16. WHEN I validate graphType THEN the system SHALL ensure defaults block is present and valid
17. WHEN I share common defaults THEN the system SHALL allow multiple graphTypes to import the same defaults file
### Requirement LEX-14

**User Story:** As a developer working with edge type hierarchies, I want edge types to support subtyping with covariant endpoint types, so that I can create specialized edge types that work with specialized node types.

#### Acceptance Criteria

1. WHEN I define edge type subtyping THEN the system SHALL support the subtype relation (<:) with reflexive and transitive properties (Armstrong's Axioms)
2. WHEN I determine if edge type S is a subtype of edge type T THEN the system SHALL verify that S's property types are a subtype of T's property types (structural subtyping)
3. WHEN I determine if edge type S is a subtype of edge type T THEN the system SHALL verify that S's endpoint node types are subtypes of T's endpoint node types
4. WHEN I work with directed edge subtyping THEN the system SHALL require source <: source AND destination <: destination (covariant in both endpoints)
5. WHEN I work with undirected edge subtyping THEN the system SHALL allow endpoints to match in either order
6. WHEN I work with edge direction subtyping THEN the system SHALL require direction compatibility (DIRECTED <: DIRECTED, UNDIRECTED <: UNDIRECTED)
7. WHEN I work with self-loop edges THEN the system SHALL handle SAME endpoint keyword with special subtyping rules
8. WHEN I define edge subtypes using implies THEN the system SHALL support `supertypes:` property listing parent edge type labels
9. WHEN I define edge subtypes using extends THEN the system SHALL support `extends:` property with `adding:` block for incremental definition
10. WHEN I validate edge type hierarchies THEN the system SHALL ensure all subtype relationships satisfy the covariant endpoint rule
11. WHEN I work with the API THEN the system SHALL provide methods to query edge type supertypes and subtypes
12. WHEN I work with the API THEN the system SHALL provide methods to check if one edge type is a subtype of another
13. WHEN I instantiate edges THEN the system SHALL allow edges of subtype S to satisfy constraints requiring supertype T
14. WHEN I define complex edge hierarchies THEN the system SHALL support multiple levels of edge type inheritance
15. WHEN I combine node and edge subtyping THEN the system SHALL correctly handle cases like CLOSE_FRIEND(Employee, Employee) <: KNOWS(Person, Person)
### Requirement LEX-15

**User Story:** As a developer defining property types, I want to specify notNull constraints on individual properties, so that I can enforce mandatory property values at the schema level.

#### Acceptance Criteria

1. WHEN I define a property type THEN the system SHALL support an optional `notNull:` boolean property
2. WHEN I set notNull to true THEN the system SHALL require that property to have a non-null value in all instances
3. WHEN I set notNull to false or omit it THEN the system SHALL allow null values for that property
4. WHEN I validate graph instances THEN the system SHALL check that all notNull properties have non-null values
5. WHEN I work with property inheritance THEN the system SHALL preserve notNull constraints from supertypes
6. WHEN I define subtypes THEN the system SHALL allow subtypes to add notNull constraints to inherited properties
7. WHEN I serialize schemas THEN the system SHALL preserve notNull property values
8. WHEN validation fails for notNull THEN the system SHALL provide clear error messages indicating which property and element violated the constraint
9. WHEN I work with the API THEN the system SHALL provide methods to query whether a property type has notNull constraint
10. WHEN I work with GQL:2027 compatibility THEN the system SHALL relate notNull to GQL's constraint framework
11. WHEN I work with SQL compatibility THEN the system SHALL map notNull to SQL's NOT NULL constraint
### Requirement LEX-16

**User Story:** As a developer organizing schemas in catalogs, I want to use lightweight references instead of embedded definitions, so that I can maintain a clean separation between catalog structure and actual schema content.

#### Acceptance Criteria

1. WHEN I add graphs to a catalog THEN the system SHALL use `graphReferences` containing only metadata (name, qualifiedName, optional filePath)
2. WHEN I add graph schemas to a catalog THEN the system SHALL use `graphSchemaReferences` containing only metadata (name, qualifiedName, optional filePath)
3. WHEN I create graph references THEN the system SHALL require `name` and `qualifiedName` properties
4. WHEN I create graph schema references THEN the system SHALL require `name` and `qualifiedName` properties
5. WHEN I specify file paths in references THEN the system SHALL support optional `filePath` property pointing to the actual definition file
6. WHEN I place references in directories THEN the system SHALL only allow references in leaf directories (directories without subdirectories)
7. WHEN I attempt to place references in non-leaf directories THEN the system SHALL reject the catalog as invalid
8. WHEN I work with catalog structure THEN the system SHALL ensure directories can contain either subdirectories OR references, not both
9. WHEN I serialize catalogs THEN the system SHALL use reference objects rather than embedding full graph or schema definitions
10. WHEN I resolve references THEN the system SHALL use filePath if provided, otherwise use qualifiedName to locate definitions
11. WHEN I validate catalogs THEN the system SHALL check that all references have valid qualifiedName format (starting with "/")
12. WHEN I work with the API THEN the system SHALL provide methods to navigate from references to actual definitions
13. WHEN I work with the API THEN the system SHALL provide methods to list all references in a catalog
14. WHEN reference resolution fails THEN the system SHALL provide clear error messages indicating which reference and path failed
