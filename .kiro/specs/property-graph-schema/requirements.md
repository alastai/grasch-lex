# Requirements Document

## Introduction

This feature involves creating a Python library called Grasch that acts as a LEX-extended GQL Catalog according to the GQL (Graph Query Language) specification with LEX (Language Extensions) capabilities. LEX is an extension of GQL, and Grasch implements both the GQL core and LEX extensions with configurable compliance modes. The library will provide a structured way to define and manage named primary catalog objects (graphs, graph types, tables, procedures, JSON Schema definitions) within a hierarchical filesystem-like structure. The Catalog has a root directory ("/"), directories forming a tree structure with unique names among siblings, and GQL-schemas (leaf nodes) containing named primary catalog objects with fully-qualified names. Directories can only contain other directories or GQL-schemas, while GQL-schemas can only contain named primary catalog objects.

**LEX Architecture Principle**: Grasch follows the pattern of GQL core + LEX extensions at all levels of detail, with both GQL and LEX supporting profile mechanisms. Profiles and GQL vs LEX are orthogonal in principle but form a matrix of permissible combinations in practice. The system can be configured with a profile (defining feature subsets and implementation choices) and a language level (GQL or LEX), with this pattern applying to builders, APIs, scripting mechanisms, and all other components.

**Terminology Note**: In Grasch, "schema" refers to a description of a set of instances (following standard computer science usage). We distinguish between:
- **Graph schemas**: Graph types with additional user-defined constraints (descriptions of graph structure)
- **Graphs/Graph instances**: Instances of graph schemas (actual graph data conforming to the schema)
- **GQL-schemas**: Containers of primary catalog objects that are leaf nodes in the Catalog (GQL-specific terminology)

The library will model the fundamental concepts of elements (nodes and edges) with content records, element types with content types (content record types), graph types, and their relationships within this hierarchical Catalog structure. Elements have distinct identities and content records, while element types define content types as proper record types with nested structure. Content types consist of a vector of label types (with constant label datatype) followed by nested record types for properties, enabling hierarchical data structures similar to JSON documents within graph elements. Each graph type contains a bounded content type lattice with ANY_CONTENT_TYPE (empty attribute set) as the top element and NO_CONTENT_TYPE (uninhabitable) as the bottom element.

## Requirements

### Requirement 1

**User Story:** As a developer working with GQL property graphs, I want to define attribute types as the unified base kind, with label types and property types as subkinds, so that I can have a consistent API and representation for all attribute types.

#### Acceptance Criteria

1. WHEN I define an attribute type THEN the system SHALL require a name (string identifier) and a datatype
2. WHEN I define a label type THEN the system SHALL create it as a subkind of attribute type with a special constant label datatype
3. WHEN I define a property type THEN the system SHALL create it as a subkind of attribute type with GQL data types (string, integer, float, boolean, datetime, etc.) and record types for nested structures
4. WHEN I query attribute types THEN the system SHALL provide a unified representation that includes both label types and property types
5. WHEN I define attribute types THEN the system SHALL ensure each has a unique identifier within its scope
6. IF I specify constraints on attribute types THEN the system SHALL validate values against those constraints regardless of subkind

### Requirement 2

**User Story:** As a developer working with GQL property graphs, I want to define content record types as proper record types with nested structure, so that I can model hierarchical data similar to JSON documents within graph elements.

#### Acceptance Criteria

1. WHEN I create a content record type THEN the system SHALL allow me to specify a collection of attribute types (both label types and property types)
2. WHEN I query a content record type for its attribute types THEN the system SHALL return a unified collection containing both label types and property types with consistent representation
3. WHEN I create a content record type THEN the system SHALL organize attribute types into a vector of label types followed by a nested map structure for property types
4. WHEN I define the property portion of a content record type THEN the system SHALL support nested map structures that are morphologically identical to JSON documents or XML documents without attributes or id/refs
5. WHEN I define property types within the nested map THEN the system SHALL allow datatypes that can themselves be record types, enabling arbitrary nesting depth
6. WHEN I work with the nested map portion THEN the system SHALL provide the same structural capabilities as JSON (objects, arrays, primitive values) but with strong typing
7. WHEN I conceptualize the structure THEN the system SHALL treat the graph element itself as the root element of a JSON document (level 0) with properties as the root's children (level 1)
8. WHEN I specify required vs optional fields THEN the system SHALL distinguish between mandatory and optional elements at each level of the nested map
9. WHEN I define a type key THEN the system SHALL allow me to specify a subset of label types (which are attribute types) as the unique identifier
10. WHEN I define nested map structures THEN the system SHALL ensure proper type safety and validation at all levels of nesting
11. WHEN I serialize content records THEN the system SHALL be able to represent the complete structure as a JSON document with the element as root and properties as children
12. WHEN I define a content type THEN the system SHALL allow me to reference a JSON Schema definition by its catalog name to define the set of property types instead of defining them individually
13. WHEN I use a JSON Schema reference THEN the system SHALL treat the referenced JSON Schema definition as the authoritative definition of the nested map structure for properties
14. WHEN I reference a JSON Schema definition by catalog name THEN the system SHALL automatically maintain synchronization when the JSON Schema definition is updated
15. WHEN I compare two content record types A and B THEN the system SHALL determine that A is a supertype of B if the set of attribute types in A is a subset of the set of attribute types in B
16. WHEN I work with content record type hierarchies THEN the system SHALL organize them in a type lattice based on Formal Concept Analysis principles
17. WHEN I validate an instance against a content record type THEN the system SHALL allow instances of subtypes to be valid for supertypes (since subtypes have all attributes of their supertypes plus additional ones)

### Requirement 3

**User Story:** As a developer working with GQL property graphs, I want to work with content type hierarchies organized in a bounded type lattice, so that I can leverage subtyping relationships based on attribute type inclusion with well-defined top and bottom elements.

#### Acceptance Criteria

1. WHEN I define multiple content types THEN the system SHALL organize them in a bounded type lattice based on their attribute type relationships
2. WHEN content type A has attribute types that are a subset of content type B's attribute types THEN the system SHALL recognize A as a supertype of B
3. WHEN I query for supertypes of a content type THEN the system SHALL return all types whose attribute types are subsets of the queried type's attribute types
4. WHEN I query for subtypes of a content type THEN the system SHALL return all types whose attribute types are supersets of the queried type's attribute types
5. WHEN I validate instances THEN the system SHALL allow instances of subtypes to satisfy supertype constraints (since subtypes contain all supertype attributes plus additional ones)
6. WHEN I work with the type lattice THEN the system SHALL provide operations to navigate up and down the hierarchy
7. WHEN I compute the lattice THEN the system SHALL handle the mathematical properties of partial ordering (reflexivity, antisymmetry, transitivity)
8. WHEN I create a graph type THEN the system SHALL automatically include ANY_CONTENT_TYPE as the top element with an empty set of attribute types
9. WHEN I create a graph type THEN the system SHALL automatically include NO_CONTENT_TYPE as the bottom element that is uninhabitable and has no subtypes
10. WHEN I work with the content type lattice THEN the system SHALL ensure ANY_CONTENT_TYPE is a supertype of all other content types
11. WHEN I work with the content type lattice THEN the system SHALL ensure every content type (except NO_CONTENT_TYPE) is a supertype of NO_CONTENT_TYPE

### Requirement 4

**User Story:** As a developer working with GQL property graphs, I want to define element types (node types and edge types) using content record types, so that I can leverage the common structure while adding element-specific constraints.

#### Acceptance Criteria

1. WHEN I create a node type THEN the system SHALL base it on a content record type
2. WHEN I create an edge type THEN the system SHALL base it on a content record type
3. WHEN I define an edge type THEN the system SHALL allow me to specify source and target node types
4. WHEN I define element types THEN the system SHALL enforce valid source-target node type combinations for edge types
5. WHEN I define type keys THEN the system SHALL ensure uniqueness within the set of all node types in the graph type
6. WHEN I define type keys THEN the system SHALL ensure uniqueness within the set of all edge types in the graph type
7. WHEN I define type keys THEN the system SHALL allow the same key label set to be used for both a node type and an edge type within the same graph type

### Requirement 5

**User Story:** As a developer, I want to configure Grasch with GQL/LEX compliance modes and customizable defaults, so that I can control whether LEX extensions are allowed and customize behavior while having sensible fallbacks for unspecified settings.

#### Acceptance Criteria

1. WHEN I initialize Grasch THEN the system SHALL provide each user with a dedicated, discrete copy of the library for their user session
2. WHEN I initialize my user session THEN the system SHALL allow me to specify a profile (e.g., Cypher Profile, Full Profile) that defines supported optional features and implementation-defined choices
3. WHEN I initialize my user session THEN the system SHALL allow me to specify a language level: GQL or LEX
4. WHEN I operate with GQL language level THEN the system SHALL enforce GQL syntax and semantics within the constraints of the specified profile
5. WHEN I operate with LEX language level THEN the system SHALL allow LEX extensions that are compatible with the specified profile, rejecting incompatible combinations
6. WHEN I initialize my user session THEN the system SHALL provide a set of "default defaults" for all configurable settings including a default JSON Schema processor, a default profile, and a default language level
7. WHEN I configure my session THEN the system SHALL allow me to swap out the JSON Schema processor implementation for a different one
8. WHEN I set user defaults in my session THEN the system SHALL use my defaults instead of the default defaults for my session only
9. WHEN I don't specify a default for a setting THEN the system SHALL use the corresponding default default
10. WHEN I work with path names in my session THEN the system SHALL allow me to set one default Catalog path at any time (if catalog support is included in the active GQL profile)
11. WHEN no default path prefix is set in my session THEN the system SHALL use "/" (solidus) as the default default path prefix (if catalog support is available)
12. WHEN the root directory is also a GQL-schema THEN the system SHALL allow primary catalog objects to be placed directly at the root level (if catalog support is available)
13. WHEN I define a primary catalog object named "Foo" within a GQL-schema at my session's default path THEN the system SHALL assign it the fully-qualified name "<default_path>/Foo"
14. WHEN my session's default path is the default default "/" THEN primary catalog objects get FQNs of the form "/<name>"
15. WHEN I change my session's default path THEN the system SHALL apply the new default path to subsequent unqualified path operations
16. WHEN I attempt to use LEX extensions with GQL language level THEN the system SHALL provide clear error messages indicating that LEX features require LEX language level
17. WHEN I attempt to use LEX extensions incompatible with the active profile THEN the system SHALL provide clear error messages indicating the specific profile constraint that is violated
18. WHEN I attempt to use features not included in the active profile THEN the system SHALL provide clear error messages indicating the specific feature that requires a different profile
19. WHEN I switch profiles or language levels during a session THEN the system SHALL validate that existing catalog contents are compatible with the new profile-language combination

### Requirement 6

**User Story:** As a developer, I want to work with a GQL Catalog that contains primary catalog objects including graph types, so that I can manage multiple schemas according to GQL specification standards.

#### Acceptance Criteria

1. WHEN I create a Catalog THEN the system SHALL provide a GQL-compliant catalog structure organized hierarchically like a filesystem
2. WHEN I work with a Catalog THEN the system SHALL provide a root directory denoted by solidus "/"
3. WHEN I create directories in the Catalog THEN the system SHALL organize them in a tree structure with string names unique among children of each parent directory
4. WHEN I add primary catalog objects THEN the system SHALL place them within GQL-schemas (leaf nodes) with string names unique among their siblings
5. WHEN I reference any GQL-schema THEN the system SHALL provide a fully-qualified name starting with "/" and consisting of successive directory names separated by "/" and terminating with "/" + GQL-schema name
6. WHEN I work with directories THEN the system SHALL ensure they can only contain other directories or GQL-schemas
7. WHEN I work with GQL-schemas THEN the system SHALL ensure they can only contain named primary catalog objects (graphs, graph types, tables, procedures, JSON Schema definitions)
8. WHEN I reference a primary catalog object THEN the system SHALL provide a fully-qualified name consisting of the GQL-schema's fully-qualified path name + "/" + the primary catalog object's name
9. WHEN I work with a Catalog THEN the system SHALL allow me to store and manage multiple types of named primary catalog objects (graphs, graph types, tables, procedures, JSON Schema definitions) within GQL-schemas
10. WHEN I navigate the Catalog THEN the system SHALL provide filesystem-like operations for traversing directories and accessing GQL-schemas and their contained primary catalog objects
11. WHEN I serialize a Catalog THEN the system SHALL preserve the complete hierarchical structure including all directory paths, GQL-schemas, and named primary catalog objects
12. WHEN I store a JSON Schema definition as a primary catalog object THEN the system SHALL allow other primary catalog objects to reference it by its catalog name
13. WHEN a JSON Schema definition is updated THEN the system SHALL ensure that all referring graph types are updated synchronously to reflect the changes

### Requirement 7

**User Story:** As a developer, I want to define graph types (schemas) that contain multiple element types, so that I can model complete graph structures according to GQL standards.

#### Acceptance Criteria

1. WHEN I create a graph type THEN the system SHALL allow me to define multiple node types within it
2. WHEN I create a graph type THEN the system SHALL allow me to define multiple edge types within it
3. WHEN I define a graph type THEN the system SHALL ensure type key uniqueness is enforced separately for node types and edge types (allowing the same key label set for both a node type and edge type)
4. WHEN I define a graph type THEN the system SHALL allow me to specify which node types can be connected by which edge types
5. WHEN I define a graph type THEN the system SHALL ensure all element types are properly defined with their content record types

### Requirement 8

**User Story:** As a developer, I want to validate graph elements against my GQL schema, so that I can ensure data integrity and GQL compliance before persisting to the database.

#### Acceptance Criteria

1. WHEN I validate an element (node or edge) against the schema THEN the system SHALL verify the element's content record conforms to its element type's content record type
2. WHEN I validate a content record THEN the system SHALL check that all required fields at each nesting level have corresponding values
3. WHEN I validate a content record THEN the system SHALL verify property values in the nested map match their property type's datatype including nested record type validation
4. WHEN I validate a content record THEN the system SHALL verify labels conform to the label types (constant label datatype)
5. WHEN I validate nested map structures THEN the system SHALL recursively validate all levels of the hierarchy similar to JSON schema validation
6. WHEN I validate an edge THEN the system SHALL verify the source and target nodes are compatible types as defined in the edge type
7. WHEN I validate elements THEN the system SHALL verify proper record type structure including nested record validation
8. WHEN I validate an element against a content type that references a JSON Schema definition THEN the system SHALL validate the properties nested data map against the referenced JSON Schema using the configured JSON Schema processor
9. WHEN I configure Grasch THEN the system SHALL allow me to specify which JSON Schema processor implementation to use
10. WHEN no JSON Schema processor is configured THEN the system SHALL use a default JSON Schema processor implementation
11. IF validation fails THEN the system SHALL provide clear error messages indicating what GQL constraints were violated including the specific nesting level and any JSON Schema validation errors

### Requirement 9

**User Story:** As a developer, I want to serialize and deserialize GQL schema definitions, so that I can store and share schemas across different environments.

#### Acceptance Criteria

1. WHEN I serialize a graph type THEN the system SHALL export it to JSON format preserving the complete GQL structure including content record types
2. WHEN I serialize a graph type THEN the system SHALL export it to YAML format preserving the complete GQL structure including content record types
3. WHEN I deserialize a schema THEN the system SHALL reconstruct the full graph type object with all attribute types, content record types, and element types
4. WHEN I deserialize a schema THEN the system SHALL validate the GQL schema structure including disjoint union constraints
5. WHEN I serialize schemas THEN the system SHALL preserve the distinction between label types and property types within content types
6. WHEN I serialize schemas with JSON Schema references THEN the system SHALL preserve the reference information and allow reconstruction of the original schema structure

### Requirement 10

**User Story:** As a developer, I want to programmatically inspect GQL schema definitions, so that I can build tools and applications that work with the schema metadata.

#### Acceptance Criteria

1. WHEN I query the graph type THEN the system SHALL provide a list of all defined element types (node and edge types)
2. WHEN I inspect an element type THEN the system SHALL provide details about its content record type including label types and property types
3. WHEN I inspect a content record type THEN the system SHALL show the vector of label types and the nested record type structure for properties
4. WHEN I query relationships THEN the system SHALL show which node types can be connected by which edge types
5. WHEN I inspect type keys THEN the system SHALL show which label types comprise the unique identifier for each element type
6. WHEN I query "show me all the attribute types of this content record type" THEN the system SHALL return a single, unified collection containing both label types and property types with consistent representation
7. WHEN I inspect individual attribute types THEN the system SHALL indicate whether each is a label type subkind (with constant label datatype) or property type subkind (with various datatypes including nested record types)
8. WHEN I inspect nested map structures THEN the system SHALL provide hierarchical navigation identical to JSON document inspection but with type information
9. WHEN I work with attribute types programmatically THEN the system SHALL provide a unified interface that works consistently for both label types and property types

### Requirement 11

**User Story:** As a developer, I want Grasch to use Kuzu as an embedded graph database for storing and managing all graph structures, so that I can have efficient persistence and querying capabilities for the Catalog tree, ISGs, and content type lattices.

#### Acceptance Criteria

1. WHEN I initialize Grasch THEN the system SHALL use Kuzu as the embedded graph database for all graph storage and operations
2. WHEN I work with the Catalog tree structure THEN the system SHALL store it as a graph in Kuzu with directories as nodes and containment relationships as edges
3. WHEN I work with Information Schema Graphs (ISGs) THEN the system SHALL store each ISG as a subgraph within the Kuzu database
4. WHEN I work with content type lattices THEN the system SHALL store each lattice as a subgraph within the Kuzu database with proper subtype relationship edges
5. WHEN I create connections between Catalog nodes and ISG type nodes THEN the system SHALL represent these as edges in the Kuzu database
6. WHEN I perform graph operations (traversal, querying, analysis) THEN the system SHALL leverage Kuzu's native graph capabilities for efficient execution
7. WHEN I need to query across multiple graph structures THEN the system SHALL use Kuzu's query capabilities to perform complex operations spanning the Catalog tree, ISGs, and content type lattices
8. WHEN I work with graph persistence THEN the system SHALL rely on Kuzu's built-in persistence mechanisms to automatically save all changes to disk
9. WHEN I initialize a user session THEN the system SHALL create or connect to a Kuzu database instance at the specified location
10. WHEN I work with concurrent access THEN the system SHALL leverage Kuzu's concurrency control mechanisms while adding additional session-level locking as needed
11. WHEN I serialize or export data THEN the system SHALL be able to extract graph structures from Kuzu and convert them to standard formats (JSON, YAML)
12. WHEN I import data THEN the system SHALL be able to load graph structures into Kuzu from standard formats while maintaining all relationships

### Requirement 12

**User Story:** As a developer, I want to work with persistent Catalog instances with controlled access, so that I can ensure data integrity and prevent corruption from concurrent modifications.

#### Acceptance Criteria

1. WHEN I initialize a user session THEN the system SHALL require me to specify the name and location of the persistent Kuzu database
2. WHEN I specify a database location THEN the system SHALL create the Kuzu database if it doesn't exist or connect to the existing database if it does
3. WHEN I attempt to access a Catalog THEN the system SHALL check for existing locks and prevent multiple concurrent access to the same Catalog instance
4. WHEN I successfully acquire access to a Catalog THEN the system SHALL establish an exclusive lock to prevent other sessions from accessing the same Catalog instance
5. WHEN my session ends or I explicitly release the Catalog THEN the system SHALL release the exclusive lock to allow other sessions to access it
6. WHEN I attempt to access a Catalog that is already locked by another session THEN the system SHALL provide a clear error message indicating the Catalog is currently in use
7. WHEN I work with a persistent Catalog THEN the system SHALL automatically save changes through Kuzu's persistence mechanisms
8. WHEN I query the Catalog location THEN the system SHALL provide the full path to the Kuzu database file or directory
9. IF the Kuzu database becomes corrupted or inaccessible THEN the system SHALL provide clear error messages and prevent further operations until resolved
10. WHEN I work with the Kuzu database THEN the system SHALL ensure proper transaction handling for atomic operations across multiple graph structures

### Requirement 13

**User Story:** As a developer, I want to work with schema graphs that represent the structure of graph types, so that I can visualize and analyze the relationships between element types and their associated content types within the content type lattice.

#### Acceptance Criteria

1. WHEN I create a graph type (graph schema) THEN the system SHALL automatically generate a corresponding schema graph representation
2. WHEN I work with a schema graph THEN the system SHALL create a node for each node type defined in the graph type
3. WHEN I work with a schema graph THEN the system SHALL create an edge for each edge type defined in the graph type
4. WHEN I inspect a schema graph node (representing a node type) THEN the system SHALL provide direct edge connection to its associated content type node in the content type lattice
5. WHEN I work with schema graph edges (representing edge types) THEN the system SHALL create edge-reflection nodes to enable proper association with content types
6. WHEN I create an edge-reflection node for an edge type THEN the system SHALL connect the edge-reflection node to the corresponding content type node in the content type lattice via an edge
7. WHEN I query the association between an edge type and its content type THEN the system SHALL traverse through the edge-reflection node to access the content type information
8. WHEN I query the schema graph THEN the system SHALL show the connections between node types through edge types as defined in the graph type
9. WHEN I work with the content type lattice THEN the system SHALL recognize it as a graph structure with nodes representing content types and edges representing subtype relationships
10. WHEN I navigate the content type lattice THEN the system SHALL provide graph traversal operations to move between supertypes and subtypes
11. WHEN I work with the Catalog structure THEN the system SHALL recognize it as a tree graph with directories as internal nodes and GQL-schemas as leaf nodes
12. WHEN I analyze the system THEN the system SHALL provide access to three distinct graph structures: the Catalog tree, the content type lattice within each graph type, and the schema graph (including edge-reflection nodes) for each graph type
13. WHEN I work with a graph schema (graph type + constraints) THEN the system SHALL distinguish it from the basic graph type and associate additional constraint information with the schema graph
14. WHEN I serialize or export schema information THEN the system SHALL preserve the graph-theoretic relationships at all levels (Catalog tree, content type lattice, and schema graph with edge-reflection nodes)

### Requirement 14

**User Story:** As a developer, I want to work with Information Schema Graphs (ISGs) that describe the structure of graph types, so that I can have a standardized representation of graph schemas that addresses the gap in the GQL standard.

#### Acceptance Criteria

1. WHEN I work with graph schema graphs THEN the system SHALL recognize them as Information Schema Graphs (ISGs) which is the proper terminology for graphs that describe the structure of graph types
2. WHEN I reference ISGs in documentation or APIs THEN the system SHALL use "Information Schema Graph" as the primary term with "schema graph" as an acceptable shorthand
3. WHEN I work with the GQL standard THEN the system SHALL acknowledge that GQL lacks a formal definition of Information Schema Graphs and provide this as an extension
4. WHEN I create a graph type THEN the system SHALL automatically generate its corresponding Information Schema Graph (ISG)
5. WHEN I work with ISGs THEN the system SHALL ensure they follow consistent structural patterns that can describe any graph type
6. WHEN I create the library's meta-schema THEN the system SHALL include an ISG that describes all possible ISGs (a meta-ISG)
7. WHEN I work with the meta-ISG THEN the system SHALL use it to validate and ensure consistency of all other ISGs in the system
8. WHEN I query ISG capabilities THEN the system SHALL provide operations to analyze, validate, and transform Information Schema Graphs
9. WHEN I export or serialize ISGs THEN the system SHALL use terminology and structure that clearly identifies them as Information Schema Graphs
10. WHEN I work with multiple graph types THEN the system SHALL ensure each has its own distinct ISG while maintaining consistency through the meta-ISG

### Requirement 15

**User Story:** As a developer, I want to visualize subgraphs of the complete Grasch graph structure using g.V(), so that I can explore and understand the relationships between Catalog components, ISGs, and content type lattices.

#### Acceptance Criteria

1. WHEN I work with the complete Grasch system THEN the system SHALL recognize that the Catalog tree, all ISGs, and all content type lattices together form one large interconnected graph
2. WHEN I want to visualize parts of the system THEN the system SHALL integrate with the g.V() library for graph visualization
3. WHEN I request visualization of a subgraph THEN the system SHALL be able to extract the relevant portion from the Kuzu database and format it for g.V() rendering
4. WHEN I visualize the Catalog tree THEN the system SHALL show directories, GQL-schemas, and their hierarchical relationships
5. WHEN I visualize an ISG THEN the system SHALL show element types, content types, and their relationships within a single graph type
6. WHEN I visualize a content type lattice THEN the system SHALL show the subtype/supertype relationships between content types
7. WHEN I visualize cross-component relationships THEN the system SHALL show connections between Catalog nodes and ISG type nodes
8. WHEN I request different visualization scopes THEN the system SHALL support filtering to show specific subgraphs (e.g., just one ISG, just the Catalog tree, or combinations)
9. WHEN I interact with visualizations THEN the system SHALL provide navigation capabilities to explore connected components
10. WHEN I export visualizations THEN the system SHALL support standard graph visualization formats compatible with g.V()
11. WHEN I customize visualizations THEN the system SHALL allow styling and layout options appropriate for different types of graph structures (trees, lattices, general graphs)
12. WHEN I work with large graphs THEN the system SHALL provide performance optimizations for visualizing subsets of the complete graph structure

### Requirement 16

**User Story:** As a developer, I want to use JSON Schema extensions with standardized library-defined types for defining property datatypes in content record types, so that I can bridge the gap between JSON Schema's type system and GQL/SQL datatypes.

#### Acceptance Criteria

1. WHEN I define property types within content record types using JSON Schema THEN the system SHALL support an extension mechanism for specifying GQL and SQL datatypes
2. WHEN I work with JSON Schema extensions THEN the system SHALL provide a standardized library of predefined types that specialize JSON's builtin types (string, number, boolean, etc.)
3. WHEN I use library-defined types THEN the system SHALL map them to appropriate GQL and SQL datatypes for cross-system compatibility
4. WHEN I validate property values THEN the system SHALL enforce both JSON Schema constraints and the additional GQL/SQL datatype constraints
5. WHEN I serialize schemas THEN the system SHALL preserve both the JSON Schema structure and the library-defined type extensions

### Requirement 17

**User Story:** As a developer, I want to use LEX catalog DDL commands to create and manage directory structures and GQL-schemas in the catalog, so that I can organize my schemas hierarchically using DDL syntax that extends GQL's existing capabilities.

**GQL Standard Summary**: GQL provides USE <graph_expression> for specifying working graphs in statements and AT <schema_reference> for schema context in procedures. Schema references support absolute paths like "/production/analytics/schema1" and relative paths like "../schema2", "HOME_SCHEMA", "CURRENT_SCHEMA". However, GQL lacks DDL commands to CREATE/DROP directories or GQL-schemas, and has no SHOW commands for catalog inspection.

**Examples of GQL Standard Usage**:
- `USE /production/graphs/customer_graph` (absolute graph reference)
- `AT /production/schemas/customer_schema` (absolute schema reference in procedure)
- `USE ../test_graphs/sample_graph` (relative graph reference)
- `AT HOME_SCHEMA` (predefined schema reference)

#### Acceptance Criteria

1. WHEN I use LEX catalog DDL THEN the system SHALL provide CREATE DIRECTORY syntax for creating catalog directories (missing from GQL standard)
2. WHEN I use LEX catalog DDL THEN the system SHALL provide DROP DIRECTORY syntax for removing catalog directories (missing from GQL standard)
3. WHEN I use LEX catalog DDL THEN the system SHALL provide CREATE GQL SCHEMA syntax for creating GQL-schema containers (missing from GQL standard)
4. WHEN I use LEX catalog DDL THEN the system SHALL provide DROP GQL SCHEMA syntax for removing GQL-schema containers (missing from GQL standard)
5. WHEN I create directories or schemas THEN the system SHALL support both absolute paths (starting with "/") and relative paths from the current default path
6. WHEN I create nested directories THEN the system SHALL support CREATE DIRECTORY with recursive creation (similar to mkdir -p)
7. WHEN I work with GQL's existing USE clause THEN the system SHALL support USE <graph_expression> for specifying the working graph within statements (GQL standard feature)
8. WHEN I work with GQL's existing AT clause THEN the system SHALL support AT <schema_reference> for specifying the schema context within procedures (GQL standard feature)
9. WHEN I use GQL schema references THEN the system SHALL support absolute paths (e.g., "/dir1/dir2/schema_name") and relative paths (e.g., "../schema_name", "HOME_SCHEMA", "CURRENT_SCHEMA") as defined in the GQL standard
10. WHEN I work with LEX SHOW commands THEN the system SHALL provide SHOW DIRECTORIES, SHOW SCHEMAS, and SHOW GRAPH SCHEMA commands for catalog navigation and ISG examination (LEX extension, not in GQL or SQL standards)
11. WHEN I use SHOW GRAPH SCHEMA THEN the system SHALL display the Information Schema Graph (ISG) structure for examining graph schema metadata
12. WHEN I create directories or schemas THEN the system SHALL validate that names are unique among siblings and follow GQL naming conventions
13. WHEN I perform directory operations THEN the system SHALL maintain referential integrity for all contained GQL-schemas and their primary catalog objects
14. WHEN I use LEX directory/schema DDL in GQL-strict mode THEN the system SHALL reject CREATE/DROP DIRECTORY and CREATE/DROP GQL SCHEMA commands with clear error messages
15. WHEN I use LEX SHOW commands in GQL-strict mode THEN the system SHALL reject these commands as they are LEX extensions not present in GQL or SQL standards
16. WHEN I use LEX catalog DDL in LEX-extended mode THEN the system SHALL execute all LEX directory, schema, and SHOW commands as extensions to the GQL standard
17. WHEN I work with builders and APIs THEN the system SHALL provide both GQL-strict methods (using existing USE and AT clauses with schema references) and LEX-extended methods (including CREATE/DROP DIRECTORY/SCHEMA and SHOW commands)

### Requirement 18

**User Story:** As a developer, I want to identify catalogs using IRI (Internationalized Resource Identifier) syntax as a LEX extension to GQL, so that I can uniquely identify and reference catalogs across distributed systems.

#### Acceptance Criteria

1. WHEN I create or reference a catalog THEN the system SHALL support IRI syntax as a LEX extension for catalog identification
2. WHEN I specify a catalog IRI THEN the system SHALL support standard IRI components (scheme, authority, path, query, fragment)
3. WHEN I work with catalog IRIs THEN the system SHALL provide validation to ensure IRI syntax compliance according to RFC 3987
4. WHEN I use catalog IRIs THEN the system SHALL support both absolute IRIs and relative IRI references
5. WHEN I resolve IRI references THEN the system SHALL provide base IRI resolution according to RFC 3986 rules
6. WHEN I work with distributed catalogs THEN the system SHALL use IRIs to establish unique identity across different catalog instances
7. WHEN I serialize catalog references THEN the system SHALL preserve IRI information for cross-system compatibility
8. WHEN I configure catalog connections THEN the system SHALL support IRI-based catalog discovery and connection establishment
9. WHEN I use IRI identification in GQL-strict mode THEN the system SHALL reject IRI syntax and require standard GQL catalog naming
10. WHEN I use IRI identification in LEX-extended mode THEN the system SHALL treat this as a LEX extension with full IRI support
11. WHEN I work with IRI-identified catalogs THEN the system SHALL provide mapping between IRI references and local catalog paths for internal operations
12. WHEN I validate IRI syntax THEN the system SHALL provide clear error messages for malformed IRIs with specific guidance on correction
13. WHEN I work with IRI fragments THEN the system SHALL support using fragments to reference specific objects within a catalog (e.g., catalog-iri#/path/to/schema/object)
14. WHEN I work with builders and APIs THEN the system SHALL provide both GQL-strict catalog naming methods and LEX-extended IRI-based methods

### Requirement 19

**User Story:** As a developer, I want Grasch to support profiles that define specific subsets of language features and implementation-defined choices for both GQL and LEX, so that I can target specific compatibility requirements while maintaining orthogonality between profile selection and language level.

#### Acceptance Criteria

1. WHEN I initialize Grasch THEN the system SHALL allow me to specify both a profile (defining feature subsets) and a language level (GQL or LEX)
2. WHEN I work with profiles THEN the system SHALL support profile definitions that specify values for implementation-defined features (like minimum/maximum label set cardinalities) that apply to both GQL and LEX
3. WHEN I use a Cypher Profile THEN the system SHALL limit features to those compatible with openCypher/Cypher 9/Cypher 5.0 including no catalog support and edge label cardinality of min=1, max=1
4. WHEN I use a Cypher Profile with GQL THEN the system SHALL enforce GQL syntax and semantics within the Cypher feature subset (e.g., singleton edge label sets with GQL syntax)
5. WHEN I use a Cypher Profile with LEX THEN the system SHALL determine whether LEX extensions are compatible with the Cypher Profile constraints, potentially rejecting LEX features that conflict with profile limitations
6. WHEN I use a Full Profile THEN the system SHALL support all optional features including full catalog management, multiple edge labels, and advanced graph type features
7. WHEN I define a profile THEN the system SHALL specify which optional features are included (e.g., GC04 for Graph management, GG25 for relaxed key label set uniqueness)
8. WHEN I define a profile THEN the system SHALL specify values for implementation-defined choices (e.g., IL001 for label set cardinalities, IL003 for key label set cardinalities)
9. WHEN I work with profile documents THEN the system SHALL support profile definitions as structured documents or objects that can be used by libraries like Grasch
10. WHEN I operate under a specific profile and language level THEN the system SHALL reject features not included in that profile-language combination with clear error messages
11. WHEN I validate against a profile-language combination THEN the system SHALL ensure all graph types, constraints, and operations conform to both the profile's feature set and the language level's capabilities
12. WHEN I work with the profile-language matrix THEN the system SHALL provide clear documentation of which combinations are permissible and which LEX extensions may be incompatible with restrictive profiles
13. WHEN I serialize or export configurations THEN the system SHALL include both profile and language level information to ensure compatibility when sharing schemas or configurations

### Requirement 20

**User Story:** As a developer, I want Grasch to implement content record types as unified sets of attribute types with proper lattice ordering based on mandatory vs optional properties, so that I can work with mathematically sound subtyping relationships that reflect GQL semantics.

#### Acceptance Criteria

1. WHEN I define a content record type THEN the system SHALL represent it as a set of attribute types where each attribute type has a name and datatype
2. WHEN I work with attribute types THEN the system SHALL support both label types (with LABEL_TYPE datatype containing a singleton constant) and property types (with standard datatypes like STRING, INT, etc.)
3. WHEN I specify element types with optional and mandatory properties THEN the system SHALL generate exactly two content record types: mandatory content record type (mcrt) containing only mandatory attribute types, and complete content record type (ccrt) containing all attribute types
4. WHEN I work with content type lattices THEN the system SHALL order content types such that a wider set of attribute types is a subtype of a narrower set (CRT₁ ≤ CRT₂ iff CRT₁ ⊆ CRT₂)
5. WHEN I define multiple element types THEN the system SHALL ensure each content record type appears exactly once in the content type lattice, discarding duplicates that arise from different element type specifications
6. WHEN I attempt to define a graph type where two node types generate identical content types THEN the system SHALL reject the specification as invalid
7. WHEN I attempt to define a graph type where two edge types generate identical content types THEN the system SHALL reject the specification as invalid
8. WHEN different element types (one node type, one edge type) generate the same content types THEN the system SHALL accept this as valid and discard the duplicate content type
9. WHEN I work with content type ordering THEN the system SHALL ensure mcrt ≤ ccrt for each element type since the mandatory attribute types are a subset of all attribute types
10. WHEN I validate element instances THEN the system SHALL allow instances of subtypes to satisfy supertype constraints since subtypes contain all supertype attributes plus additional ones

### Requirement 21

**User Story:** As a developer, I want Grasch to support both structural and nominal-like typing through strategic use of labels, so that I can achieve type safety while maintaining GQL's structural flexibility.

#### Acceptance Criteria

1. WHEN I work with content record types THEN the system SHALL implement structural typing where two content types are identical if and only if their attribute type sets are equal (order irrelevant)
2. WHEN I compare content types structurally THEN the system SHALL treat {name:STRING, age:INT} as identical to {age:INT, name:STRING} since set equality ignores order
3. WHEN I want to distinguish structurally identical types THEN the system SHALL allow me to add distinguishing labels that make the attribute type sets different
4. WHEN I use distinguishing labels THEN the system SHALL treat {Person, name:STRING, age:INT} as different from {Employee, name:STRING, age:INT} due to different label attributes
5. WHEN I define type keys (key label sets) THEN the system SHALL use them as pseudo-identifiers for content types
6. WHEN I use singleton key label sets THEN the system SHALL allow the single label identifier to serve as a pseudo-type name (e.g., key {Person} enables "Person" as type name)
7. WHEN I use multi-label key sets THEN the system SHALL treat them as compound identifiers for the content type
8. WHEN I work with type validation THEN the system SHALL enforce that elements conform to their content type's complete attribute type set
9. WHEN I perform type checking THEN the system SHALL use structural comparison for type compatibility while respecting label-based type discrimination
10. WHEN I serialize or display types THEN the system SHALL provide both structural representation (full attribute type set) and nominal representation (using key label sets as type names when available)

### Requirement 22

**User Story:** As a developer, I want Grasch to implement spectral types for element conformance based on mandatory and optional properties, so that I can validate graph instances against the proper interval of acceptable content record types.

#### Acceptance Criteria

1. WHEN I define element types with mandatory and optional properties THEN the system SHALL create a spectral type as an inclusive interval [ccrt, mcrt] where ccrt is the complete content record type and mcrt is the mandatory content record type
2. WHEN I work with lattice ordering THEN the system SHALL ensure ccrt ≤ mcrt (complete type is subtype of mandatory type) since smaller attribute sets are higher in the lattice than larger attribute sets
3. WHEN I validate element instances THEN the system SHALL check that the element's content record lies within the spectral type interval [ccrt, mcrt]
4. WHEN an element is conformant in the spectrum of a type THEN the system SHALL accept it as valid for that element type
5. WHEN I use GQL property type syntax THEN the system SHALL support property name and datatype separation using space (e.g., "name STRING NOT NULL") or double colon (e.g., "name :: STRING NOT NULL") or TYPED keyword (e.g., "name TYPED STRING NOT NULL")
6. WHEN I specify property nullability THEN the system SHALL treat NOT NULL as a type modifier, not a separate type, with properties defaulting to NULL-allowed unless explicitly marked NOT NULL
7. WHEN I work with mandatory properties THEN the system SHALL include only NOT NULL properties in the mandatory content record type (mcrt)
8. WHEN I work with complete properties THEN the system SHALL include all properties (both NOT NULL and NULL-allowed) in the complete content record type (ccrt)
9. WHEN I validate property values THEN the system SHALL enforce that mandatory properties must be present and non-null, while optional properties may be absent or null
10. WHEN I display spectral types THEN the system SHALL show the conformance interval clearly indicating the range of acceptable content record variations
11. WHEN I work with element instances THEN the system SHALL allow any content record that falls between the complete type (lower bound) and mandatory type (upper bound) in the lattice ordering
12. WHEN I serialize spectral type information THEN the system SHALL preserve both the interval bounds and the GQL syntax for property type specifications

### Requirement 23

**User Story:** As a developer, I want all Grasch builders, APIs, and scripting mechanisms to follow the profile + language level pattern, so that I can consistently control feature availability and syntax across all system components.

#### Acceptance Criteria

1. WHEN I work with any Grasch builder THEN the system SHALL provide methods that respect the active profile and language level combination
2. WHEN I work with any Grasch API THEN the system SHALL clearly distinguish between profile-defined features and language-level capabilities
3. WHEN I use scripting mechanisms THEN the system SHALL support scripts that comply with the active profile-language combination with clear mode indicators
4. WHEN I configure a builder with a specific profile THEN the system SHALL reject features not included in that profile regardless of language level
5. WHEN I configure a builder with LEX language level THEN the system SHALL allow LEX extensions that are compatible with the active profile
6. WHEN I work with constraint definitions THEN the system SHALL distinguish between profile-available constraints and language-level constraint syntax
7. WHEN I use DDL (Data Definition Language) statements THEN the system SHALL support syntax appropriate to the language level within the constraints of the active profile
8. WHEN I work with validation mechanisms THEN the system SHALL provide validation for both profile compliance and language level compliance
9. WHEN I serialize or export configurations THEN the system SHALL clearly mark which features require specific profiles vs specific language levels
10. WHEN I migrate between profile-language combinations THEN the system SHALL provide tools to identify and handle features that would be incompatible with the target combination
11. WHEN I work with error handling THEN the system SHALL provide profile and language-aware error messages that indicate whether issues are profile violations or language level problems
12. WHEN I use any system component THEN the system SHALL maintain the profile + language level pattern consistently across all levels of detail
13. WHEN I work with content type lattices THEN the system SHALL ensure all lattice operations respect the active profile's constraints on attribute types and structural features
14. WHEN I work with spectral types THEN the system SHALL ensure all spectral type operations and validations respect the active profile and language level configurationlean, array, object) to match GQL and SQL datatypes
3. WHEN I use library-defined types THEN the system SHALL provide predefined extensions for common GQL datatypes (integer, float, datetime, duration, etc.)
4. WHEN I use library-defined types THEN the system SHALL provide predefined extensions for common SQL datatypes (varchar, decimal, timestamp, etc.)
5. WHEN I define custom extensions THEN the system SHALL allow me to create new specialized types based on JSON Schema's base types
6. WHEN I validate property values THEN the system SHALL enforce both JSON Schema constraints and the additional GQL/SQL datatype constraints
7. WHEN I serialize schemas with extensions THEN the system SHALL preserve the extension information for proper reconstruction
8. WHEN I work with different JSON Schema processors THEN the system SHALL ensure extension compatibility across different implementations

### Requirement 17

**User Story:** As a developer, I want to distinguish between GQL:graph and LEX:graph concepts, so that I can understand the structural equivalence and constraint extensions that LEX provides over the GQL standard.

#### Acceptance Criteria

1. WHEN I work with GQL:graph concepts THEN the system SHALL recognize them as ISO GQL Standard graph definitions without value constraints
2. WHEN I work with LEX:GQL:graph concepts THEN the system SHALL treat them as structurally equivalent to GQL:graph (same type/structure)
3. WHEN I work with LEX:graph concepts THEN the system SHALL recognize them as extended graphs that may have value constraints applied
4. WHEN I define a LEX:graph THEN the system SHALL allow it to have key constraints on elements (which GQL:graph cannot have)
5. WHEN I define a LEX:graph THEN the system SHALL allow it to have cardinality constraints on elements (which GQL:graph cannot have)
6. WHEN I work with constraint-free LEX:graph instances THEN the system SHALL recognize them as functionally equivalent to GQL:graph instances
7. WHEN I reference concepts without prefixes THEN the system SHALL assume LEX: namespace implicitly
8. WHEN I establish equivalence between standards THEN the system SHALL support notation like "GQL:concept = LEX:concept" for identical concepts
9. WHEN I use synonym notation THEN the system SHALL support "GQL:LEX:concept" as shorthand for equivalence statements

### Requirement 18

**User Story:** As a developer, I want to work with LEX constraint systems that are version-specific and user-configurable, so that I can apply appropriate value constraints to graphs based on the LEX version capabilities.

#### Acceptance Criteria

1. WHEN I work with GQL:graph instances THEN the system SHALL provide zero constraint options (no value constraints available)
2. WHEN I work with LEX-2026:graph instances THEN the system SHALL provide a specific set of n constraint types available for user selection
3. WHEN I work with future LEX-202x:graph instances THEN the system SHALL provide an expanded set of m > n constraint types where m exceeds the LEX-2026 constraint count
4. WHEN I design a graph THEN the system SHALL allow me to choose which available constraints to apply from the version-specific constraint catalog
5. WHEN I apply constraints THEN the system SHALL allow me to set specific constraint values according to my requirements
6. WHEN I work with constraint catalogs THEN the system SHALL ensure LEX-2026 includes at minimum key constraints and cardinality constraints
7. WHEN I upgrade LEX versions THEN the system SHALL maintain backward compatibility with existing constraint types while adding new constraint capabilities
8. WHEN I query available constraints THEN the system SHALL provide the complete list of constraint types available for the current LEX version
9. WHEN I validate graphs THEN the system SHALL enforce only the constraints that have been explicitly applied by the user
10. WHEN I work with constraint evolution THEN the system SHALL ensure that constraint capabilities expand monotonically across LEX versions (newer versions have all constraints of older versions plus additional ones)

### Requirement 19

**User Story:** As a developer, I want to apply constraints at both individual graph level and schema level, so that I can have flexible constraint management for different use cases.

#### Acceptance Criteria

1. WHEN I define constraints for an individual LEX:graph THEN the system SHALL allow me to apply constraints directly to that specific graph instance
2. WHEN I define constraints within a LEX:graph schema THEN the system SHALL allow me to specify constraints that apply to all graphs conforming to that schema
3. WHEN I work with graph-level constraints THEN the system SHALL apply them only to the specific graph instance where they are defined
4. WHEN I work with schema-level constraints THEN the system SHALL apply them to all graph instances that conform to that schema
5. WHEN I have both graph-level and schema-level constraints THEN the system SHALL apply both sets of constraints with appropriate precedence rules
6. WHEN I validate a graph with schema-level constraints THEN the system SHALL check constraint conformance as part of schema validation
7. WHEN I validate a graph with graph-level constraints THEN the system SHALL check constraint conformance as part of instance validation
8. WHEN I modify constraints THEN the system SHALL allow independent modification of graph-level and schema-level constraints
9. WHEN I query constraint sources THEN the system SHALL clearly indicate whether constraints originate from the graph instance or its schema
10. WHEN I work with constraint inheritance THEN the system SHALL define clear rules for how graph-level constraints interact with schema-level constraints

### Requirement 20

**User Story:** As a developer, I want to work with LEX:graph schema as a composition of GQL:graph type and LEX:constraints, so that I can have unified schema definitions that handle both structural and value validation.

#### Acceptance Criteria

1. WHEN I define a LEX:graph schema THEN the system SHALL require it to contain exactly one GQL:graph type component
2. WHEN I define a LEX:graph schema THEN the system SHALL require it to contain a set of LEX:constraints (which may be empty)
3. WHEN I work with LEX:graph schema composition THEN the system SHALL treat it as the combination: LEX:graph schema = GQL:graph type + LEX:constraints
4. WHEN I validate a LEX:graph against a LEX:graph schema THEN the system SHALL perform structural conformance validation against the GQL:graph type component
5. WHEN I validate a LEX:graph against a LEX:graph schema THEN the system SHALL perform value conformance validation against the LEX:constraints component
6. WHEN I query a LEX:graph schema THEN the system SHALL provide access to both the structural definition (GQL:graph type) and constraint definitions (LEX:constraints)
7. WHEN I modify a LEX:graph schema THEN the system SHALL allow independent modification of the GQL:graph type and LEX:constraints components
8. WHEN I create a LEX:graph schema with empty constraints THEN the system SHALL function as a pure structural schema equivalent to GQL:graph type
9. WHEN I work with schema conformance THEN the system SHALL ensure LEX:graph instances satisfy both structural requirements (from GQL:graph type) and value requirements (from LEX:constraints)
10. WHEN I serialize LEX:graph schemas THEN the system SHALL preserve both the GQL:graph type structure and the LEX:constraints definitions
11. WHEN I reference LEX:graph schemas THEN the system SHALL provide clear identification of which component (structure or constraints) is being accessed or modifiedlean, etc.)
3. WHEN I specify a property datatype THEN the system SHALL allow me to use library-defined types such as "gql:integer", "gql:float", "gql:datetime", "sql:varchar", "sql:decimal", etc.
4. WHEN I use a library-defined type THEN the system SHALL map it to the appropriate GQL or SQL datatype while maintaining JSON Schema validation capabilities
5. WHEN I define custom library types THEN the system SHALL allow me to create new standardized types that extend the base library
6. WHEN I validate property values THEN the system SHALL enforce both JSON Schema structural validation and the specific GQL/SQL datatype constraints
7. WHEN I serialize content with library-defined types THEN the system SHALL preserve the datatype information in the JSON Schema definition
8. WHEN I work with nested record structures THEN the system SHALL support library-defined types at any level of nesting within the JSON Schema
9. WHEN I reference JSON Schema definitions with library-defined types THEN the system SHALL maintain datatype fidelity across all references
10. WHEN I export or share schemas THEN the system SHALL include the library-defined type definitions to ensure portability
11. WHEN I work with different JSON Schema processors THEN the system SHALL provide a mechanism to register and use the library-defined type extensions
12. WHEN I query property datatypes programmatically THEN the system SHALL provide access to both the JSON Schema type and the specific GQL/SQL datatype information
13. WHEN I validate against library-defined types THEN the system SHALL provide clear error messages that reference both JSON Schema validation and GQL/SQL datatype constraints

### Requirement 17

**User Story:** As a developer, I want to use IRI-based addressing for catalogs and their contents, so that I can have globally unique identifiers that relate logical catalog paths to physical storage locations.

#### Acceptance Criteria

1. WHEN I create a catalog in a Kuzu database THEN the system SHALL generate a base IRI that reflects the database's file system location
2. WHEN I specify a catalog name THEN the system SHALL create a catalog IRI by appending "/" + catalog_name to the base IRI
3. WHEN I work with catalog paths THEN the system SHALL treat the root solidus "/" as an alias for the catalog IRI
4. WHEN I reference a directory in the catalog THEN the system SHALL create an IRI by extending the catalog IRI with the directory path
5. WHEN I reference a GQL-schema (leaf node) THEN the system SHALL create an IRI by extending the parent directory's IRI with "/" + schema_name
6. WHEN I reference a Primary Catalog Object (PCO) THEN the system SHALL create an IRI by extending the GQL-schema's IRI with "/" + PCO_name
7. WHEN I work with fully-qualified names THEN the system SHALL provide both traditional path notation ("/dir/schema/object") and IRI notation for the same logical entity
8. WHEN I serialize or export catalog references THEN the system SHALL support both IRI format and traditional path format
9. WHEN I share catalog objects across systems THEN the system SHALL use IRIs to provide globally unique identification that includes storage location context
10. WHEN I resolve an IRI THEN the system SHALL be able to locate the corresponding physical storage and logical catalog position
11. WHEN I work with multiple catalogs THEN the system SHALL ensure each has a unique base IRI that distinguishes it from other catalogs
12. WHEN I query catalog metadata THEN the system SHALL provide access to both the IRI and traditional path representations
13. WHEN I configure catalog access THEN the system SHALL allow specifying catalogs by either IRI or file system path
14. WHEN I work with catalog hierarchies THEN the system SHALL maintain IRI hierarchy that mirrors the logical catalog structure
15. WHEN I validate IRIs THEN the system SHALL ensure they conform to standard IRI syntax while maintaining catalog-specific semantics

### Requirement 18

**User Story:** As a developer, I want to use LEX (LDBC Extended GQL Schema) as a sophisticated schema validation language that extends GQL graph types, so that I can define graph schemas with additional constraints beyond what GQL provides.

#### Acceptance Criteria

1. WHEN I work with LEX THEN the system SHALL recognize it as "LDBC Extended GQL Schema" - a strict extension of GQL graph types
2. WHEN I define a LEX graph schema THEN the system SHALL require it to contain a GQL graph type as its structural foundation
3. WHEN I create a LEX graph schema THEN the system SHALL allow me to add constraints beyond the basic GQL graph type definition
4. WHEN I specify LEX constraints THEN the system SHALL support key constraints that define unique identifiers for element types
5. WHEN I specify LEX constraints THEN the system SHALL support cardinality constraints that limit the number of relationships or property values
6. WHEN I specify LEX constraints THEN the system SHALL support intra-record constraints that validate property values within a single element
7. WHEN I specify LEX constraints THEN the system SHALL support cross-property value relationships that validate dependencies between different properties
8. WHEN I validate against a LEX schema THEN the system SHALL first validate against the underlying GQL graph type structure
9. WHEN I validate against a LEX schema THEN the system SHALL additionally validate against all LEX-specific constraints
10. WHEN I work with LEX schemas THEN the system SHALL maintain backward compatibility with standard GQL graph types
11. WHEN I export LEX schemas THEN the system SHALL be able to extract the underlying GQL graph type for systems that don't support LEX extensions
12. WHEN I store LEX schemas in GQL-schemas THEN the system SHALL treat them as extended primary catalog objects
13. WHEN I work with LEX constraint validation THEN the system SHALL provide detailed error messages indicating which specific constraints were violated
14. WHEN I define LEX constraints THEN the system SHALL support constraint composition and dependency relationships between constraints
15. WHEN I work with LEX schemas THEN the system SHALL position Grasch as extending the GQL standard with enhanced validation capabilities
16. WHEN I serialize LEX schemas THEN the system SHALL preserve both the GQL graph type structure and the LEX constraint definitions
17. WHEN I work with ISGs for LEX schemas THEN the system SHALL represent both the structural elements and the constraint relationships in the graph representation

### Requirement 19

**User Story:** As a developer, I want to store data graphs (graph instances) as Primary Catalog Objects in GQL-schemas, with support for both user-defined schemas and schema-free operation, so that I can manage actual graph data alongside schema definitions.

#### Acceptance Criteria

1. WHEN I store a data graph in a GQL-schema THEN the system SHALL treat it as a Primary Catalog Object (PCO) distinct from graph schemas
2. WHEN I create a data graph THEN the system SHALL allow me to specify a user-defined graph schema (LEX or GQL graph type) for validation
3. WHEN I create a schema-free data graph THEN the system SHALL automatically assign it a default permissive schema
4. WHEN I work with the default permissive schema THEN the system SHALL recognize it as a very loose schema that permits the general property graph data model structure without additional constraints
5. WHEN I validate a schema-free graph THEN the system SHALL ensure it conforms to basic property graph principles (nodes, edges, properties) but without specific type or constraint validation
6. WHEN I work with schema-defined data graphs THEN the system SHALL validate all elements against the specified graph schema (GQL graph type or LEX schema)
7. WHEN I query data graphs THEN the system SHALL provide access to both the graph data and its associated schema information
8. WHEN I store multiple data graphs THEN the system SHALL allow them to use different schemas or be schema-free independently
9. WHEN I work with schema-free graphs THEN the system SHALL still maintain the distinction that they are "compliant with a schema" rather than truly schema-less
10. WHEN I convert between schema-free and schema-defined graphs THEN the system SHALL provide mechanisms to apply or remove schema constraints
11. WHEN I serialize data graphs THEN the system SHALL preserve both the graph data and the schema association (user-defined or default permissive)
12. WHEN I work with the Catalog THEN the system SHALL clearly distinguish between graph schemas (LEX/GQL definitions) and data graphs (instances) as different types of PCOs
13. WHEN I validate data graphs THEN the system SHALL provide appropriate error messages for schema violations in schema-defined graphs
14. WHEN I work with the default permissive schema THEN the system SHALL define it formally as part of the Grasch system rather than treating it as an absence of schema
15. WHEN I query schema information for data graphs THEN the system SHALL return either the user-defined schema reference or indicate the use of the default permissive schema

### Requirement 20

**User Story:** As a developer, I want LEX DDL to strictly extend GQL DDL, so that I can use existing GQL Data Definition Language constructs while adding LEX-specific constraint definitions.

#### Acceptance Criteria

1. WHEN I work with LEX DDL THEN the system SHALL support all existing GQL DDL syntax and semantics without modification
2. WHEN I define a LEX schema using DDL THEN the system SHALL require a valid GQL graph type definition as the foundation
3. WHEN I use GQL DDL constructs THEN the system SHALL interpret them exactly as specified in the GQL standard
4. WHEN I add LEX extensions to DDL THEN the system SHALL use additional syntax that does not conflict with existing GQL DDL keywords or constructs
5. WHEN I define LEX constraints in DDL THEN the system SHALL provide syntax for key constraints, cardinality constraints, intra-record constraints, and cross-property relationships
6. WHEN I parse LEX DDL THEN the system SHALL first validate the GQL DDL portions against the GQL standard
7. WHEN I parse LEX DDL THEN the system SHALL additionally validate the LEX extension portions against LEX syntax rules
8. WHEN I export LEX schemas THEN the system SHALL be able to generate both full LEX DDL and GQL-only DDL (by omitting LEX extensions)
9. WHEN I work with GQL-compliant tools THEN the system SHALL allow them to process the GQL DDL portions of LEX schemas while ignoring LEX extensions
10. WHEN I define LEX constraint syntax THEN the system SHALL use clear, intuitive keywords that extend the GQL DDL vocabulary naturally
11. WHEN I validate LEX DDL THEN the system SHALL provide error messages that distinguish between GQL DDL errors and LEX extension errors
12. WHEN I work with catalog operations THEN the system SHALL support both GQL DDL and LEX DDL for creating and modifying schemas
13. WHEN I demonstrate LEX as a strict extension THEN the system SHALL show that every valid GQL DDL statement is also valid LEX DDL
14. WHEN I work with LEX DDL THEN the system SHALL maintain the same semantic meaning for all GQL DDL constructs
15. WHEN I serialize LEX schemas THEN the system SHALL preserve the DDL representation alongside other serialization formats
16. WHEN I work with version compatibility THEN the system SHALL ensure LEX DDL can evolve while maintaining backward compatibility with GQL DDL

### Requirement 21

**User Story:** As a developer, I want to use LEX DDL commands that extend GQL DDL with new constructs and operations for managing Primary and Secondary Catalog Objects, so that I can perform comprehensive schema and data management operations.

#### Acceptance Criteria

1. WHEN I work with GQL DDL commands THEN the system SHALL support CREATE [OR REPLACE] and DELETE operations for Primary Catalog Objects (PCOs)
2. WHEN I work with LEX DDL commands THEN the system SHALL extend GQL DDL with additional operations for managing Secondary Catalog Objects (SCOs) within PCOs
3. WHEN I use ALTER commands THEN the system SHALL allow me to modify, add, or delete SCOs contained within a PCO
4. WHEN I work with graph schemas THEN the system SHALL support "CREATE [OR REPLACE] GRAPH SCHEMA <name> GRAPH TYPE <type_name>" syntax as an extension of GQL's graph type creation
5. WHEN I modify graph associations THEN the system SHALL support ALTER GRAPH commands to DROP existing graph types and ADD new ones
6. WHEN I work with SCO management THEN the system SHALL provide ALTER operations for modifying constraints, keys, and other secondary objects within LEX schemas
7. WHEN I use LEX DDL syntax THEN the system SHALL follow SQL-like patterns that extend naturally from GQL DDL syntax
8. WHEN I execute DDL commands THEN the system SHALL validate that the operations are appropriate for the target object types (PCO vs SCO)
9. WHEN I work with LEX-specific constructs THEN the system SHALL provide DDL syntax for creating and modifying constraint definitions within graph schemas
10. WHEN I use CREATE OR REPLACE operations THEN the system SHALL handle both GQL objects (graph types) and LEX objects (graph schemas) appropriately
11. WHEN I perform ALTER operations THEN the system SHALL maintain referential integrity between PCOs and their contained SCOs
12. WHEN I execute DDL commands THEN the system SHALL provide transaction support to ensure atomic operations across related objects
13. WHEN I work with DDL command validation THEN the system SHALL check both syntax correctness and semantic validity of operations
14. WHEN I use LEX DDL extensions THEN the system SHALL ensure they follow consistent naming and syntax patterns that feel natural to GQL DDL users
15. WHEN I manage complex schemas THEN the system SHALL support cascading operations where appropriate (e.g., dropping a graph type affects dependent objects)
16. WHEN I work with DDL command history THEN the system SHALL provide mechanisms to track and potentially reverse DDL operations

### Requirement 22

**User Story:** As a developer, I want to use DDL as both executable commands and serialization format for catalog definitions, so that I can store, share, and recreate catalog states through declarative "it shall be thus" statements.

#### Acceptance Criteria

1. WHEN I work with DDL scripts THEN the system SHALL treat them as both executable command sequences and serialization formats for catalog definitions
2. WHEN I serialize a catalog or catalog portion THEN the system SHALL generate DDL scripts that represent the complete state using CREATE statements
3. WHEN I execute a DDL script THEN the system SHALL treat it as deserialization that recreates the catalog state represented by the script
4. WHEN I work with catalog serialization THEN the system SHALL provide multiple serialization formats (DDL, JSON, YAML) with DDL as the primary executable format
5. WHEN I create declarative DDL THEN the system SHALL support "it shall be thus" semantics where statements describe desired end states rather than incremental changes
6. WHEN I work with DDL script execution THEN the system SHALL distinguish between imperative operations (CREATE, ALTER, DROP) and declarative state descriptions
7. WHEN I serialize catalog definitions THEN the system SHALL generate DDL that focuses on CREATE statements representing the final desired state
8. WHEN I work with catalog maintenance THEN the system SHALL provide deserialization interfaces that can process various serialization formats
9. WHEN I use DDL for state representation THEN the system SHALL minimize the use of ALTER and DROP statements in favor of comprehensive CREATE statements that define complete objects
10. WHEN I execute declarative DDL THEN the system SHALL handle the transformation from "it shall be thus" statements to the necessary imperative operations
11. WHEN I work with catalog versioning THEN the system SHALL support generating DDL scripts that represent specific catalog states at different points in time
12. WHEN I share catalog definitions THEN the system SHALL provide DDL scripts as a portable, human-readable format for catalog exchange
13. WHEN I work with catalog backup and restore THEN the system SHALL use DDL serialization as one method for preserving and recreating catalog states
14. WHEN I process DDL scripts THEN the system SHALL validate that the resulting catalog state matches the intended declarative description
15. WHEN I work with complex catalog structures THEN the system SHALL generate DDL scripts that handle dependencies and ordering requirements automatically
16. WHEN I use DDL as serialization THEN the system SHALL ensure round-trip fidelity between catalog state and DDL representation

### Requirement 23

**User Story:** As a developer, I want to use YAML/JSON scripts as equivalent alternatives to DDL scripts for catalog definition, so that I can choose the most appropriate format while maintaining identical functionality and bidirectional transformation capabilities.

#### Acceptance Criteria

1. WHEN I define catalog content THEN the system SHALL support YAML scripts as functionally equivalent alternatives to DDL scripts
2. WHEN I define catalog content THEN the system SHALL support JSON scripts as functionally equivalent alternatives to DDL scripts
3. WHEN I create a catalog using YAML scripts THEN the system SHALL produce identical results to using equivalent DDL scripts
4. WHEN I create a catalog using JSON scripts THEN the system SHALL produce identical results to using equivalent DDL scripts
5. WHEN I work with YAML/JSON formats THEN the system SHALL represent the same information content as CREATE [OR REPLACE] <PCO> DDL commands
6. WHEN I transform between formats THEN the system SHALL provide programmatic transformation from DDL to YAML/JSON and vice versa
7. WHEN I validate format equivalence THEN the system SHALL ensure that any YAML script can be programmatically transformed into a DDL script with identical semantic effect
8. WHEN I validate format equivalence THEN the system SHALL ensure that any JSON script can be programmatically transformed into a DDL script with identical semantic effect
9. WHEN I work with canonicalization THEN the system SHALL provide the ability to canonicalize information content across DDL, YAML, and JSON formats
10. WHEN I use the library as a canonicalizer THEN the system SHALL produce consistent canonical representations regardless of input format
11. WHEN I work with YAML/JSON scripts THEN the system SHALL support all LEX constructs and constraints that are available in LEX DDL
12. WHEN I serialize catalog state THEN the system SHALL offer DDL, YAML, and JSON as output format options with guaranteed equivalence
13. WHEN I validate transformations THEN the system SHALL ensure round-trip fidelity: DDL→YAML→DDL and DDL→JSON→DDL produce identical results
14. WHEN I work with mixed formats THEN the system SHALL allow importing from one format and exporting to another while preserving all information
15. WHEN I use YAML/JSON for version control THEN the system SHALL provide formats that are diff-friendly and human-readable
16. WHEN I work with tooling integration THEN the system SHALL support standard YAML/JSON processing tools while maintaining semantic correctness
17. WHEN I validate semantic equivalence THEN the system SHALL ensure that catalog operations produce identical graph structures regardless of input format

### Requirement 24

**User Story:** As a developer, I want JSON Schema definitions for YAML/JSON serialization formats, so that I can have formal validation and an alternate representation of LEX's EBNF grammar through structured schema definitions.

#### Acceptance Criteria

1. WHEN I work with YAML serialization formats THEN the system SHALL provide JSON Schema definitions that validate all valid YAML script formats
2. WHEN I work with JSON serialization formats THEN the system SHALL provide JSON Schema definitions that validate all valid JSON script formats
3. WHEN I define LEX constructs THEN the system SHALL maintain JSON Schema definitions that represent the same information content as the EBNF grammar of LEX DDL
4. WHEN I validate YAML/JSON scripts THEN the system SHALL use JSON Schema validation to ensure structural and semantic correctness
5. WHEN I work with JSON Schema for LEX THEN the system SHALL treat it as an alternate formal representation of LEX's grammar and syntax rules
6. WHEN I define graph schema serialization THEN the system SHALL provide specific JSON Schema definitions for graph schema definition formats
7. WHEN I work with catalog object definitions THEN the system SHALL provide JSON Schema definitions for each type of Primary Catalog Object (PCO) serialization
8. WHEN I extend LEX with new constructs THEN the system SHALL update the corresponding JSON Schema definitions to maintain consistency with the EBNF grammar
9. WHEN I validate serialization formats THEN the system SHALL ensure that JSON Schema validation catches the same errors that would be caught by LEX DDL parsing
10. WHEN I work with tooling integration THEN the system SHALL provide JSON Schema definitions that enable IDE support, validation, and auto-completion for YAML/JSON scripts
11. WHEN I document LEX formats THEN the system SHALL use JSON Schema as both validation mechanism and documentation of valid structure
12. WHEN I work with format evolution THEN the system SHALL maintain versioned JSON Schema definitions that correspond to different versions of LEX grammar
13. WHEN I validate transformation correctness THEN the system SHALL ensure that YAML/JSON scripts conforming to the JSON Schema produce valid LEX DDL when transformed
14. WHEN I work with schema composition THEN the system SHALL provide modular JSON Schema definitions that can be combined for complex catalog structures
15. WHEN I generate documentation THEN the system SHALL be able to produce human-readable format specifications from the JSON Schema definitions
16. WHEN I work with cross-validation THEN the system SHALL ensure that the JSON Schema definitions and EBNF grammar represent identical language constraints
17. WHEN I use JSON Schema for validation THEN the system SHALL provide clear error messages that relate JSON Schema violations to LEX semantic requirements

### Requirement 25

**User Story:** As a developer, I want to understand the formal mathematical correspondence between GQL graph types and their schema graph representations, so that I can work with the precise structural relationships between type definitions and their graph representations.

#### Acceptance Criteria

1. WHEN I work with GQL graph types THEN the system SHALL recognize them as structure definitions GT = (NT, ET) where NT is the set of node types and ET is the set of edge types
2. WHEN I create a schema graph for a graph type THEN the system SHALL generate SG = (N, E) where N is the set of nodes and E is the set of edges in the schema graph
3. WHEN I establish correspondence between graph types and schema graphs THEN the system SHALL ensure each member of N (schema graph nodes) corresponds to exactly one member of NT (node types)
4. WHEN I establish correspondence between graph types and schema graphs THEN the system SHALL ensure each member of E (schema graph edges) corresponds to exactly one member of ET (edge types)
5. WHEN I work with schema graph nodes THEN the system SHALL ensure each node represents exactly one node type from the original graph type definition
6. WHEN I work with schema graph edges THEN the system SHALL ensure each edge represents exactly one edge type from the original graph type definition
7. WHEN I validate the correspondence THEN the system SHALL ensure |N| = |NT| (cardinality of schema graph nodes equals cardinality of node types)
8. WHEN I validate the correspondence THEN the system SHALL ensure |E| = |ET| (cardinality of schema graph edges equals cardinality of edge types)
9. WHEN I work with bidirectional mapping THEN the system SHALL provide functions to map from graph type elements to schema graph elements and vice versa
10. WHEN I analyze schema graphs THEN the system SHALL preserve all structural information from the original graph type definition
11. WHEN I work with schema graph transformations THEN the system SHALL ensure that changes to the schema graph can be reflected back to the graph type definition
12. WHEN I validate schema graph integrity THEN the system SHALL ensure the one-to-one correspondence is maintained throughout all operations
13. WHEN I work with complex graph types THEN the system SHALL maintain the formal correspondence regardless of the complexity of NT and ET
14. WHEN I serialize schema graphs THEN the system SHALL preserve the mathematical relationship between GT and SG
15. WHEN I work with schema graph analysis THEN the system SHALL leverage the formal correspondence to provide precise structural insights
16. WHEN I document the system THEN the system SHALL clearly express the mathematical relationship GT = (NT, ET) ↔ SG = (N, E)

### Requirement 26

**User Story:** As a developer, I want to define GQL graph types through discrete member-by-member definition, so that I can specify each node type and edge type as individual objects rather than through set operations or bulk definitions.

#### Acceptance Criteria

1. WHEN I define a GQL graph type THEN the system SHALL require me to define each node type nt ∈ NT as a discrete, individual object
2. WHEN I define a GQL graph type THEN the system SHALL require me to define each edge type et ∈ ET as a discrete, individual object
3. WHEN I create node types THEN the system SHALL not support bulk or set-based operations for defining multiple node types simultaneously
4. WHEN I create edge types THEN the system SHALL not support bulk or set-based operations for defining multiple edge types simultaneously
5. WHEN I work with graph type definition THEN the system SHALL enforce member-by-member definition as the only valid approach for GQL compliance
6. WHEN I define element types THEN the system SHALL require explicit specification of each type's properties, constraints, and relationships individually
7. WHEN I validate graph type definitions THEN the system SHALL ensure each nt and et has been explicitly and individually defined
8. WHEN I work with DDL for graph types THEN the system SHALL require separate CREATE statements or clauses for each node type and edge type
9. WHEN I serialize graph types THEN the system SHALL represent each node type and edge type as distinct, individually specified objects
10. WHEN I work with YAML/JSON serialization THEN the system SHALL require explicit enumeration of each node type and edge type as separate objects
11. WHEN I import graph type definitions THEN the system SHALL process each node type and edge type definition individually
12. WHEN I validate GQL compliance THEN the system SHALL ensure the member-by-member definition approach aligns with GQL standard requirements
13. WHEN I work with graph type modification THEN the system SHALL require individual operations on specific node types or edge types rather than set-based modifications
14. WHEN I analyze graph types THEN the system SHALL provide access to each nt ∈ NT and et ∈ ET as individually defined and accessible objects
15. WHEN I work with type introspection THEN the system SHALL present each element type as a discrete object with its own definition and properties
16. WHEN I document graph type structure THEN the system SHALL clearly show the individual definition of each member of NT and ET

### Requirement 27

**User Story:** As a developer, I want LEX to optimize both user workflow and representation size for graph schema definition, so that I can define schemas efficiently and achieve optimal validation performance through compact representations.

#### Acceptance Criteria

1. WHEN I define LEX graph schemas THEN the system SHALL provide optimization mechanisms that reduce the user's work compared to member-by-member GQL definition
2. WHEN I work with LEX schema representation THEN the system SHALL minimize the size of the information content representation
3. WHEN I use LEX for instance validation THEN the system SHALL leverage compact schema representations to optimize validation space complexity
4. WHEN I use LEX for instance validation THEN the system SHALL leverage compact schema representations to optimize validation time complexity
5. WHEN I define multiple similar element types THEN the system SHALL provide mechanisms to avoid repetitive individual definitions
6. WHEN I work with schema patterns THEN the system SHALL support pattern-based or template-based definition approaches that reduce redundancy
7. WHEN I serialize LEX schemas THEN the system SHALL produce more compact representations than equivalent member-by-member GQL definitions
8. WHEN I validate graph instances THEN the system SHALL use the compact schema representation to perform faster validation operations
9. WHEN I work with large schemas THEN the system SHALL provide scalable definition approaches that don't require exponential user effort
10. WHEN I optimize schema representation THEN the system SHALL maintain full semantic equivalence with the underlying GQL graph type
11. WHEN I work with schema compression THEN the system SHALL identify and eliminate redundancy in schema definitions
12. WHEN I define schema hierarchies THEN the system SHALL leverage inheritance or composition patterns to reduce definition overhead
13. WHEN I work with validation optimization THEN the system SHALL pre-compute or cache validation structures from compact schema representations
14. WHEN I analyze schema complexity THEN the system SHALL provide metrics showing the optimization benefits of LEX over pure GQL approaches
15. WHEN I work with schema evolution THEN the system SHALL maintain optimization benefits as schemas are modified over time
16. WHEN I balance optimization with compliance THEN the system SHALL ensure that LEX optimizations don't compromise GQL compatibility of the underlying graph type

### Requirement 28

**User Story:** As a developer, I want LEX to exploit subtyping relationships for schema optimization, so that I can define element types at supertype levels and validate subtypes through supertype expressions using RDFS-style subclass semantics.

#### Acceptance Criteria

1. WHEN I work with LEX subtyping THEN the system SHALL establish subtype relationships where S is a subtype of T if any member of S can be transformed into or contains a member of T
2. WHEN I work with subclass relationships THEN the system SHALL recognize that S is a subclass of T if any member of S is also a member of T (RDFS semantics)
3. WHEN I establish subtype relationships THEN the system SHALL provide correspondence between subtype membership and subclass membership transformations
4. WHEN I define node types at supertype level THEN the system SHALL allow me to create "supertype expressions" that can validate multiple related subtypes
5. WHEN I define edge types at supertype level THEN the system SHALL allow me to create "supertype expressions" that can validate multiple related subtypes
6. WHEN I validate subtype instances THEN the system SHALL use supertype expressions to test validity of expressions whose operands are subtypes of the supertype expression's operands
7. WHEN I work with supertype expressions THEN the system SHALL automatically handle validation for all subtypes without requiring individual subtype definitions
8. WHEN I establish subtyping hierarchies THEN the system SHALL leverage the mathematical relationship between subtype and subclass membership
9. WHEN I optimize schema definitions THEN the system SHALL use supertype expressions to reduce the number of explicit type definitions required
10. WHEN I validate instances against supertypes THEN the system SHALL ensure that subtype instances satisfy supertype constraints through the transformation relationship
11. WHEN I work with type hierarchies THEN the system SHALL provide mechanisms to navigate and query subtype/supertype relationships
12. WHEN I define constraints at supertype level THEN the system SHALL automatically apply them to all subtypes through the subclass relationship
13. WHEN I work with subtype transformations THEN the system SHALL ensure that the transformation from subtype member to supertype member preserves semantic validity
14. WHEN I use supertype expressions for validation THEN the system SHALL achieve the optimization goals of reduced definition work and compact representation
15. WHEN I work with RDFS-style semantics THEN the system SHALL maintain consistency with established semantic web subclass relationship principles
16. WHEN I combine subtyping with other LEX features THEN the system SHALL ensure that subtype relationships work correctly with constraints, keys, and other schema elements

### Requirement 29

**User Story:** As a developer, I want to use concrete subtyping patterns like SQL schema metadata modeling, so that I can define abstract supertypes and validate concrete subtypes through supertype expressions using Cypher/GQL-like pattern notation.

#### Acceptance Criteria

1. WHEN I model SQL schema metadata THEN the system SHALL allow me to define "table" as an abstract supertype with "base_table" and "view" as concrete subtypes
2. WHEN I define subtype relationships THEN the system SHALL recognize that base_table and view are subtypes of table
3. WHEN I create supertype expressions THEN the system SHALL allow patterns like (schema)-[CONTAINS]-(table) that apply to all subtypes of table
4. WHEN I validate against supertype patterns THEN the system SHALL accept (schema)-[CONTAINS]-(base_table) and (schema)-[CONTAINS]-(view) as valid instances of the supertype pattern
5. WHEN I work with abstract supertypes THEN the system SHALL ensure that abstract types like "table" cannot be directly instantiated but only through their concrete subtypes
6. WHEN I use Cypher/GQL-like pattern notation THEN the system SHALL interpret () as node/node type indicators and [] as edge/edge type indicators
7. WHEN I specify type names without : or {} THEN the system SHALL treat names like "schema", "table", and "CONTAINS" as the actual names of node types and edge types
8. WHEN I define edge patterns with supertypes THEN the system SHALL validate that the edge type (CONTAINS) can connect the specified node types (schema to table and all table subtypes)
9. WHEN I work with subtype validation THEN the system SHALL ensure that only the defined subtypes (base_table, view) are accepted as instances of the abstract supertype (table)
10. WHEN I create complex schema hierarchies THEN the system SHALL support multiple levels of subtyping (e.g., materialized_view as subtype of view, which is subtype of table)
11. WHEN I define supertype constraints THEN the system SHALL apply them to all subtypes automatically (e.g., constraints on table apply to both base_table and view)
12. WHEN I work with pattern matching THEN the system SHALL use supertype patterns to match any valid subtype instance in the graph
13. WHEN I optimize schema definitions THEN the system SHALL allow one supertype pattern to replace multiple individual subtype patterns
14. WHEN I work with metadata modeling THEN the system SHALL support common patterns like containment, inheritance, and composition through supertype expressions
15. WHEN I validate graph instances THEN the system SHALL correctly identify subtype instances as valid matches for supertype patterns
16. WHEN I document schema patterns THEN the system SHALL clearly show the relationship between abstract supertypes and their concrete subtypes

### Requirement 30

**User Story:** As a developer, I want content types to be organized in a mathematically rigorous type lattice using Formal Concept Analysis (FCA), so that I can work with precise subtype relationships based on attribute type containment.

#### Acceptance Criteria

1. WHEN I work with content types THEN the system SHALL recognize them as consisting of a set of label types and a set of property types (where property types are level 1 members of a tree structure)
2. WHEN I compare content types CTS and CTT THEN the system SHALL determine that CTS <: CTT (CTS is a subtype of CTT) if CTS contains all the label types and property types of CTT
3. WHEN I establish subtype relationships THEN the system SHALL use the notation CTS <: CTT to indicate CTS is a subtype of CTT, and CTT :> CTS to indicate CTT is a supertype of CTS
4. WHEN I work with type ordering THEN the system SHALL recognize that CTS is less than, smaller than, and lower than CTT when CTS <: CTT
5. WHEN I organize content types THEN the system SHALL use Formal Concept Analysis (FCA) to establish the order relation among content types
6. WHEN I work with the content type collection THEN the system SHALL organize it as a lattice whose members are content types with order relations established by FCA
7. WHEN I reference the structure THEN the system SHALL call it a "type lattice" or "type hierarchy" based on the FCA ordering
8. WHEN I validate subtype relationships THEN the system SHALL ensure that if CTS <: CTT, then every attribute type in CTS is also present in CTT
9. WHEN I work with lattice operations THEN the system SHALL provide meet (greatest lower bound) and join (least upper bound) operations for content types
10. WHEN I navigate the type lattice THEN the system SHALL allow traversal up (to supertypes) and down (to subtypes) the hierarchy
11. WHEN I work with lattice properties THEN the system SHALL ensure the structure satisfies mathematical lattice properties (partial order with meets and joins)
12. WHEN I analyze type relationships THEN the system SHALL use FCA principles to determine the most specific common supertype and most general common subtype
13. WHEN I validate instances THEN the system SHALL leverage the lattice structure to determine type compatibility and substitutability
14. WHEN I optimize type checking THEN the system SHALL use the lattice structure to perform efficient subtype relationship queries
15. WHEN I work with complex type hierarchies THEN the system SHALL maintain FCA-based ordering regardless of the number or complexity of content types
16. WHEN I serialize type lattices THEN the system SHALL preserve the FCA-based order relationships and lattice structure

### Requirement 31

**User Story:** As a developer, I want to understand the mathematical relationship between content type lattices and element type lattices, so that I can work with node type lattices as sub-lattices of content type lattices based on their content type mappings.

#### Acceptance Criteria

1. WHEN I work with node types THEN the system SHALL recognize that every node type is distinguished by its content type and by nothing else
2. WHEN I map node types to content types THEN the system SHALL ensure that every node type in a set of node types is mapped to exactly one element in the content type lattice
3. WHEN I establish node type relationships THEN the system SHALL create a node type lattice that is a sub-lattice of the content type lattice
4. WHEN I work with node type subtyping THEN the system SHALL derive the subtype relationships from the underlying content type subtype relationships
5. WHEN I have node types NT1 and NT2 with content types CT1 and CT2 THEN the system SHALL establish NT1 <: NT2 if and only if CT1 <: CT2
6. WHEN I work with the node type lattice THEN the system SHALL ensure it preserves the order relationships from the content type lattice
7. WHEN I navigate node type hierarchies THEN the system SHALL provide the same lattice operations (meet, join) available in the content type lattice
8. WHEN I work with node type validation THEN the system SHALL use the content type lattice structure to determine node type compatibility
9. WHEN I optimize node type operations THEN the system SHALL leverage the sub-lattice relationship to perform efficient node type relationship queries
10. WHEN I work with multiple node types sharing content types THEN the system SHALL handle the mapping correctly while maintaining lattice properties
11. WHEN I analyze node type relationships THEN the system SHALL trace them back to the underlying content type relationships in the parent lattice
12. WHEN I work with node type substitutability THEN the system SHALL determine it based on the content type subtype relationships
13. WHEN I serialize node type lattices THEN the system SHALL preserve the sub-lattice relationship to the content type lattice
14. WHEN I work with edge types THEN the system SHALL establish similar but more complex relationships due to additional edge-specific constraints (source/target node types)
15. WHEN I work with element type lattices THEN the system SHALL maintain mathematical consistency between content type lattices and their corresponding element type sub-lattices
16. WHEN I validate the lattice correspondence THEN the system SHALL ensure that the node type lattice structure is isomorphic to the relevant portion of the content type lattice

### Requirement 32

**User Story:** As a developer, I want to understand edge types as triples (first node, arc, second node) with proper distinction between arcs and edges, so that I can work with the more complex lattice relationships that arise from edge type structure.

#### Acceptance Criteria

1. WHEN I work with edge types THEN the system SHALL recognize them as triples of (first node, arc, second node)
2. WHEN I work with directed edges THEN the system SHALL order the first node before the second node with direction from first to second
3. WHEN I work with undirected edges THEN the system SHALL treat first and second nodes as mathematically unordered but potentially lexically ordered in text representations
4. WHEN I distinguish edge components THEN the system SHALL use "arc" to represent the edge connector (the line between points) and "edge" to represent the complete structure (points connected by a line)
5. WHEN I work with edge type content THEN the system SHALL recognize that each node type (first and second) has its own content type
6. WHEN I work with arc content THEN the system SHALL recognize that the arc itself has a content type (the edge's own properties and labels)
7. WHEN I establish edge type subtyping THEN the system SHALL consider the content types of all three components: first node type, arc, and second node type
8. WHEN I compare edge types ET1 and ET2 THEN the system SHALL determine subtyping based on the relationships between their respective triple components
9. WHEN I work with edge type lattices THEN the system SHALL handle the complexity arising from the triple structure rather than simple content type mapping
10. WHEN I validate edge type relationships THEN the system SHALL ensure compatibility of first node type, arc content type, and second node type
11. WHEN I work with edge type substitutability THEN the system SHALL consider all three components of the triple in determining valid substitutions
12. WHEN I optimize edge type operations THEN the system SHALL account for the increased complexity compared to node type operations
13. WHEN I serialize edge types THEN the system SHALL preserve the triple structure and the content types of all three components
14. WHEN I work with edge type hierarchies THEN the system SHALL provide lattice operations that handle the multi-dimensional nature of edge type relationships
15. WHEN I analyze edge connectivity THEN the system SHALL use the first and second node type constraints to determine valid edge instantiations
16. WHEN I work with mixed directed/undirected edges THEN the system SHALL handle the different ordering semantics appropriately in the same schema

### Requirement 33

**User Story:** As a developer, I want formal mathematical rules for edge type subtyping based on component-wise content type relationships, so that I can determine edge type subtype relationships through systematic comparison of first node, arc, and second node content types.

#### Acceptance Criteria

1. WHEN I compare edge types SET and TET THEN the system SHALL first verify they have the same orientation (both directed or both undirected)
2. WHEN I work with directed edge types THEN the system SHALL ensure both are directed from first to second for subtyping comparison
3. WHEN I establish edge type subtyping THEN the system SHALL use the notation ct(x) to denote "content type of x"
4. WHEN I evaluate edge type subtyping SET <: TET THEN the system SHALL require ct(first(SET)) <: ct(first(TET))
5. WHEN I evaluate edge type subtyping SET <: TET THEN the system SHALL require ct(second(SET)) <: ct(second(TET))
6. WHEN I evaluate edge type subtyping SET <: TET THEN the system SHALL require ct(arc(SET)) <: ct(arc(TET))
7. WHEN all content type subtyping conditions are met THEN the system SHALL conclude that first(SET) <: first(TET)
8. WHEN all content type subtyping conditions are met THEN the system SHALL conclude that second(SET) <: second(TET)
9. WHEN all content type subtyping conditions are met THEN the system SHALL conclude that arc(SET) <: arc(TET)
10. WHEN all component subtyping relationships are established THEN the system SHALL conclude that SET <: TET
11. WHEN edge types have different orientations THEN the system SHALL not establish subtyping relationships between them
12. WHEN directed edges have different directions THEN the system SHALL not establish subtyping relationships between them
13. WHEN I work with edge type lattices THEN the system SHALL use these component-wise subtyping rules to establish the lattice order
14. WHEN I validate edge type substitutability THEN the system SHALL ensure that SET can be substituted for TET only when SET <: TET
15. WHEN I optimize edge type checking THEN the system SHALL use the component-wise subtyping rules for efficient relationship determination
16. WHEN I work with complex edge type hierarchies THEN the system SHALL apply these rules consistently across all edge type comparisons
17. WHEN I serialize edge type relationships THEN the system SHALL preserve the component-wise subtyping information

### Requirement 34

**User Story:** As a developer, I want to understand the complete lattice system for any schema, so that I can work with the comprehensive relationships between schema graphs, content type lattices, node type lattices, and edge type lattices as an integrated mathematical structure.

#### Acceptance Criteria

1. WHEN I work with any schema THEN the system SHALL provide four interconnected mathematical structures: schema graph, content type lattice, node type lattice, and edge type lattice
2. WHEN I analyze the node type lattice THEN the system SHALL recognize it as a sub-lattice of the content type lattice
3. WHEN I analyze the edge type lattice THEN the system SHALL recognize it as related to the content type lattice through the component-wise subtyping rules
4. WHEN I work with schema structure THEN the system SHALL ensure the schema graph provides the structural representation while the lattices provide the type hierarchy relationships
5. WHEN I navigate between structures THEN the system SHALL provide clear mappings between schema graph elements and their corresponding lattice elements
6. WHEN I work with node types THEN the system SHALL show their representation in both the schema graph (as nodes) and the node type lattice (with subtype relationships)
7. WHEN I work with edge types THEN the system SHALL show their representation in both the schema graph (as edges) and the edge type lattice (with component-wise subtype relationships)
8. WHEN I analyze type relationships THEN the system SHALL use the content type lattice as the foundational structure from which node and edge type lattices derive their ordering
9. WHEN I work with schema validation THEN the system SHALL leverage all four structures: schema graph for structure, and the three lattices for type compatibility checking
10. WHEN I optimize schema operations THEN the system SHALL use the lattice relationships to perform efficient type checking and validation across all structures
11. WHEN I serialize schemas THEN the system SHALL preserve all four mathematical structures and their interconnections
12. WHEN I work with schema evolution THEN the system SHALL maintain consistency across all four structures when schemas are modified
13. WHEN I analyze schema complexity THEN the system SHALL provide metrics and insights based on the properties of all four mathematical structures
14. WHEN I work with schema visualization THEN the system SHALL be able to display the relationships between schema graphs and their associated lattices
15. WHEN I validate schema consistency THEN the system SHALL ensure that the lattice structures are consistent with the schema graph structure
16. WHEN I work with schema transformations THEN the system SHALL maintain the mathematical relationships between all four structures throughout the transformation process

### Requirement 35

**User Story:** As a developer, I want LEX to support multiple validation conformance modes (exact-type, subtype, and proper-subtype), so that I can write compressed validation rules using supertype expressions and control the strictness of instance validation.

#### Acceptance Criteria

1. WHEN I validate instances in GQL THEN the system SHALL require every element in the instance to correspond exactly to an element type in the schema
2. WHEN I validate instances in LEX THEN the system SHALL support three conformance modes: exact-type conformant, subtype-conformant, and proper-subtype conformant
3. WHEN I use exact-type conformance THEN the system SHALL require instance elements to match schema element types exactly (GQL behavior)
4. WHEN I use subtype-conformance THEN the system SHALL allow instance elements whose content types are subtypes (including exact matches) of schema element types
5. WHEN I use proper-subtype conformance THEN the system SHALL allow instance elements whose content types are proper subtypes (excluding exact matches) of schema element types
6. WHEN I work with proper-subtype conformance THEN the system SHALL enforce that abstract types like "table" can only be instantiated through concrete subtypes like "base_table" or "view"
7. WHEN I define validation rules THEN the system SHALL allow me to specify which conformance mode applies to each element type or validation context
8. WHEN I write compressed validation rules THEN the system SHALL enable expressions in terms of supertypes that automatically handle all valid subtypes
9. WHEN I use supertype expressions for validation THEN the system SHALL leverage the node type and edge type lattices to determine valid conformance
10. WHEN I validate node instances THEN the system SHALL use the node type lattice to determine conformance based on the specified conformance mode
11. WHEN I validate edge instances THEN the system SHALL use the edge type lattice and component-wise conformance rules based on the specified conformance mode
12. WHEN I work with abstract element types THEN the system SHALL enforce proper-subtype conformance to prevent direct instantiation of abstract types
13. WHEN I optimize validation performance THEN the system SHALL use compressed supertype rules instead of enumerating all possible subtypes
14. WHEN I specify validation constraints THEN the system SHALL allow different conformance modes for different parts of the same schema
15. WHEN I work with schema evolution THEN the system SHALL maintain conformance mode specifications as schemas are modified
16. WHEN I document validation rules THEN the system SHALL clearly indicate which conformance mode is being used for each validation rule
17. WHEN I validate complex instances THEN the system SHALL apply the appropriate conformance mode consistently across all elements in the instance

### Requirement 36

**User Story:** As a developer, I want to understand that Grasch implements LEX-2026 (the first version of LEX), which focuses on node types and edge types, so that I can work within the defined scope while being aware of future LEX-202x capabilities.

#### Acceptance Criteria

1. WHEN I work with LEX THEN the system SHALL recognize "LEX" as a casual synonym for "LEX-2026" unless otherwise specified
2. WHEN I work with LEX-2026 THEN the system SHALL focus exclusively on node types and edge types as the primary element types
3. WHEN I define LEX-2026 scope THEN the system SHALL include all previously defined LEX features: subtyping, lattices, validation conformance modes, supertype expressions, and constraint definitions
4. WHEN I work with Grasch THEN the system SHALL implement LEX-2026 capabilities and not attempt to implement future LEX-202x features
5. WHEN I reference LEX versions THEN the system SHALL clearly distinguish between LEX-2026 (current implementation scope) and LEX-202x (future versions)
6. WHEN I document LEX-2026 THEN the system SHALL note that it is the first version of LEX and establishes the foundational concepts
7. WHEN I work with LEX-2026 limitations THEN the system SHALL acknowledge that more advanced ideas will be addressed in LEX-202x successors
8. WHEN I plan for future versions THEN the system SHALL design LEX-2026 in a way that allows for extension to LEX-202x without breaking compatibility
9. WHEN I work with version identification THEN the system SHALL clearly mark schemas, DDL, and serializations as LEX-2026 compliant
10. WHEN I validate LEX compliance THEN the system SHALL ensure conformance to LEX-2026 specifications
11. WHEN I work with standards positioning THEN the system SHALL present LEX-2026 as the initial extension to GQL that establishes the LEX framework
12. WHEN I document system capabilities THEN the system SHALL clearly state that Grasch implements LEX-2026 and not future LEX versions
13. WHEN I work with compatibility THEN the system SHALL ensure that LEX-2026 schemas will be forward-compatible with future LEX-202x versions
14. WHEN I reference advanced features THEN the system SHALL note them as future LEX-202x capabilities without implementing them in Grasch
15. WHEN I work with LEX evolution THEN the system SHALL provide a foundation that can be extended for future LEX versions

### Requirement 37

**User Story:** As a developer, I want to understand the future direction of LEX-202x regarding subgraph types, so that I can appreciate how LEX-2026's node and edge types will generalize to subgraph types in future versions (without implementing these features in Grasch).

#### Acceptance Criteria

1. WHEN I consider LEX-202x future capabilities THEN the system SHALL note that it will expand beyond node types and edge types to subgraph types
2. WHEN I understand graph structure G = (N, E) THEN the system SHALL recognize that both N and E may be empty, making the whole graph empty
3. WHEN I work with isolated nodes THEN the system SHALL note that each isolated node (when E is empty) forms a subgraph of G
4. WHEN I work with individual edges THEN the system SHALL note that any member of E may be viewed as a subgraph of G
5. WHEN I understand subgraph relationships THEN the system SHALL recognize that nodes and edges are special cases of subgraphs
6. WHEN I work with subgraph definition THEN the system SHALL note that subgraph SG ⊆ G requires N(SG) ⊆ N(G) and E(SG) ⊆ E(G)
7. WHEN I consider type generalization THEN the system SHALL note that node types and edge types are special cases of subgraph types
8. WHEN I understand LEX-202x subtyping THEN the system SHALL note that subgraph subtyping will be an extension/generalization of LEX-2026 edge type subtyping rules
9. WHEN I work with LEX-2026 THEN the system SHALL NOT implement subgraph types but SHALL acknowledge them as future LEX-202x capabilities
10. WHEN I document future capabilities THEN the system SHALL clearly mark subgraph type features as LEX-202x scope, not LEX-2026
11. WHEN I design LEX-2026 architecture THEN the system SHALL consider how node and edge type handling could extend to subgraph types in future versions
12. WHEN I work with current limitations THEN the system SHALL acknowledge that LEX-2026 handles only the special cases (nodes, edges) of the more general subgraph concept
13. WHEN I consider mathematical foundations THEN the system SHALL note that LEX-202x will extend the lattice and subtyping concepts to handle arbitrary subgraphs
14. WHEN I plan for evolution THEN the system SHALL ensure LEX-2026 foundations are compatible with future subgraph type extensions
15. WHEN I reference advanced features THEN the system SHALL treat subgraph types as illustrative of LEX-202x direction without implementation commitment

### Requirement 38

**User Story:** As a developer, I want LEX-2026 to support schema derivation from existing graphs through core reduction and graph homomorphisms, so that I can automatically generate schemas from graph instances by abstracting property values to datatypes.

#### Acceptance Criteria

1. WHEN I work with LEX-2026 schema derivation THEN the system SHALL support reducing any graph to a core using graph homomorphisms
2. WHEN I perform core reduction THEN the system SHALL use the resulting core as a graph schema
3. WHEN I derive schemas from graphs THEN the system SHALL reverse the transformation from graph type to schema graph
4. WHEN I work with property abstraction THEN the system SHALL ignore property values and concentrate only on datatypes during schema derivation
5. WHEN I use homomorphism-based reduction THEN the system SHALL provide automatic schema inference capabilities
6. WHEN I work with schema inference THEN the system SHALL derive schemas from existing graph instances
7. WHEN I perform reverse transformation THEN the system SHALL convert schema graphs back to graph types through the inverse process
8. WHEN I extract datatypes THEN the system SHALL abstract property values to their datatypes during schema derivation
9. WHEN I work with core graphs THEN the system SHALL recognize them as representing the essential structural patterns of the original graph
10. WHEN I implement schema derivation THEN the system SHALL provide this as a core LEX-2026 capability in Grasch
11. WHEN I document schema derivation THEN the system SHALL clearly mark it as a LEX-2026 feature
12. WHEN I use mathematical foundations THEN the system SHALL employ graph homomorphisms as the theoretical basis for schema derivation
13. WHEN I work with automatic schema generation THEN the system SHALL provide LEX-2026 capabilities for inferring schemas from data
14. WHEN I integrate with other LEX-2026 features THEN the system SHALL ensure schema derivation works with subtyping, lattices, and validation conformance modes
15. WHEN I use schema derivation THEN the system SHALL demonstrate LEX-2026's mathematical sophistication in practical schema management

### Requirement 39

**User Story:** As a developer, I want a three-layer programming interface architecture with PSO (Programmatic Schema Objects) as the low-level foundation and DDL/YAML as higher-level interfaces, so that I can work with catalog objects at different levels of abstraction and integration.

#### Acceptance Criteria

1. WHEN I work with the programming interface architecture THEN the system SHALL provide three distinct layers: PSO (Programmatic Schema Objects), DDL interface, and YAML interface
2. WHEN I use the PSO interface THEN the system SHALL provide low-level programmatic API access to build objects representing points in the catalog hierarchy
3. WHEN I work with PSO objects THEN the system SHALL allow me to supply appropriate values for defining characteristics of catalog objects
4. WHEN I use PSO fluent builders THEN the system SHALL provide builder patterns for constructing complex catalog objects programmatically
5. WHEN I create isolated objects THEN the system SHALL allow me to define graph schemas as isolated objects separate from graphs
6. WHEN I work with object associations THEN the system SHALL allow me to associate isolated objects (like graph schemas and graphs) through object references
7. WHEN I integrate objects into catalogs THEN the system SHALL allow bringing cross-referenced objects into a catalog at a later stage
8. WHEN I use the DDL interface THEN the system SHALL provide higher-level, more restrictive interfaces layered above the PSO interface
9. WHEN I write LEX scripts THEN the system SHALL support sequences of GQL or LEX commands that create catalog objects, graph objects, and graph schema objects
10. WHEN I execute DDL commands THEN the system SHALL create relationships between catalog objects by calling down to the PSO interface
11. WHEN I use the YAML interface THEN the system SHALL support declarative definition of final catalog state through hierarchical YAML structures
12. WHEN I work with YAML declarations THEN the system SHALL translate hierarchical YAML structures into PSO interface calls
13. WHEN I work with interface layering THEN the system SHALL ensure that DDL and YAML interfaces both call down to the PSO interface for object creation and manipulation
14. WHEN I choose interface levels THEN the system SHALL allow me to work at the PSO level for maximum flexibility or at DDL/YAML levels for convenience and structure
15. WHEN I work with cross-interface compatibility THEN the system SHALL ensure that objects created through any interface can be accessed and manipulated through the PSO interface
16. WHEN I work with interface abstraction THEN the system SHALL provide appropriate levels of abstraction where higher-level interfaces hide PSO complexity while maintaining full functionality

### Requirement 40

**User Story:** As a developer, I want to use Pydantic definitions for record schema as an alternative to or supplement to JSON Schema property sets, so that I can leverage Python's type system and Pydantic's validation capabilities for defining content record structures.

#### Acceptance Criteria

1. WHEN I define content record types THEN the system SHALL support Pydantic model definitions as an alternative to JSON Schema property sets
2. WHEN I use Pydantic definitions THEN the system SHALL allow them as a supplement to JSON Schema, enabling mixed usage within the same schema
3. WHEN I work with Pydantic models THEN the system SHALL leverage Python's native type annotations for property type definitions
4. WHEN I define nested record structures THEN the system SHALL support Pydantic model composition and inheritance for hierarchical data structures
5. WHEN I validate content records THEN the system SHALL use Pydantic's built-in validation capabilities for property value validation
6. WHEN I work with Pydantic integration THEN the system SHALL maintain compatibility with the existing JSON Schema extension system for GQL/SQL datatypes
7. WHEN I use Pydantic models THEN the system SHALL automatically extract property types and constraints from Pydantic field definitions
8. WHEN I serialize content types THEN the system SHALL be able to convert between Pydantic model definitions and JSON Schema representations
9. WHEN I work with library-defined types THEN the system SHALL support Pydantic custom field types that map to GQL/SQL datatypes
10. WHEN I validate instances THEN the system SHALL use Pydantic validation for Pydantic-defined properties and JSON Schema validation for JSON Schema-defined properties
11. WHEN I work with mixed definitions THEN the system SHALL handle content record types that combine Pydantic models and JSON Schema property sets
12. WHEN I use Pydantic inheritance THEN the system SHALL properly map Pydantic model inheritance to content type subtyping relationships
13. WHEN I work with Pydantic field constraints THEN the system SHALL translate them to appropriate LEX constraint definitions
14. WHEN I export schemas THEN the system SHALL support exporting to both Pydantic model format and JSON Schema format
15. WHEN I work with Python ecosystem integration THEN the system SHALL leverage Pydantic's compatibility with FastAPI, SQLAlchemy, and other Python tools
16. WHEN I use Pydantic for content definition THEN the system SHALL maintain the same semantic meaning and validation behavior as equivalent JSON Schema definitions

### Requirement 41

**User Story:** As a developer, I want Grasch to be strongly-typed throughout using Python type annotations, so that I can have type safety and the library can be easily ported to other strongly-typed languages like TypeScript, Rust, or Java.

#### Acceptance Criteria

1. WHEN I work with Grasch code THEN the system SHALL use comprehensive Python type annotations throughout the entire codebase
2. WHEN I define functions and methods THEN the system SHALL provide type annotations for all parameters, return values, and class attributes
3. WHEN I work with complex data structures THEN the system SHALL use appropriate generic types, Union types, and Protocol types for precise type specification
4. WHEN I use the library THEN the system SHALL enable full type checking with mypy, pyright, or other Python type checkers
5. WHEN I work with PSO interface THEN the system SHALL provide strongly-typed builder patterns and fluent interfaces
6. WHEN I define catalog objects THEN the system SHALL use typed dataclasses, Pydantic models, or similar strongly-typed structures
7. WHEN I work with content types and lattices THEN the system SHALL use generic types to represent type relationships and hierarchies
8. WHEN I design the architecture THEN the system SHALL structure code in a way that facilitates porting to TypeScript, Rust, Java, or other strongly-typed languages
9. WHEN I define interfaces THEN the system SHALL use Protocol types or abstract base classes to define clear contracts
10. WHEN I work with error handling THEN the system SHALL use typed exceptions and Result/Option patterns where appropriate
11. WHEN I serialize and deserialize data THEN the system SHALL maintain type safety throughout the serialization process
12. WHEN I work with Kuzu database integration THEN the system SHALL provide strongly-typed wrappers and interfaces for database operations
13. WHEN I implement validation logic THEN the system SHALL use type-safe validation patterns that can be easily translated to other languages
14. WHEN I design APIs THEN the system SHALL avoid Python-specific idioms that would be difficult to port to other strongly-typed languages
15. WHEN I document the codebase THEN the system SHALL leverage type annotations for automatic documentation generation
16. WHEN I consider future ports THEN the system SHALL design core algorithms and data structures using patterns common to strongly-typed languages
17. WHEN I work with the library THEN the system SHALL provide IDE support through type annotations for autocompletion, error detection, and refactoring

### Requirement 42

**User Story:** As a developer, I want Grasch to be thread-safe with thread-associated user sessions, so that I can use the library safely in multi-threaded applications where each thread maintains its own isolated session state.

#### Acceptance Criteria

1. WHEN I use Grasch in a multi-threaded application THEN the system SHALL ensure thread-safe access to all shared resources and data structures
2. WHEN I create user sessions THEN the system SHALL associate each session with its creating thread using thread-local storage or similar mechanisms
3. WHEN I work with catalog operations THEN the system SHALL ensure that concurrent access to the same catalog from different threads is properly synchronized
4. WHEN I access session-specific data THEN the system SHALL automatically provide the correct session data for the current thread
5. WHEN I work with Kuzu database operations THEN the system SHALL ensure thread-safe database access and connection management
6. WHEN I use PSO interface objects THEN the system SHALL ensure that object creation and manipulation are thread-safe
7. WHEN I work with content type lattices THEN the system SHALL ensure that lattice operations and caching are thread-safe
8. WHEN I perform validation operations THEN the system SHALL ensure that validation state and caches are properly isolated between threads
9. WHEN I use DDL or YAML interfaces THEN the system SHALL ensure that parsing and execution are thread-safe
10. WHEN I work with schema derivation THEN the system SHALL ensure that graph analysis and core reduction operations are thread-safe
11. WHEN I access catalog locks THEN the system SHALL use thread-safe locking mechanisms that prevent deadlocks and race conditions
12. WHEN I work with serialization THEN the system SHALL ensure that concurrent serialization operations don't interfere with each other
13. WHEN I use visualization features THEN the system SHALL ensure that g.V() integration and graph extraction are thread-safe
14. WHEN I work with session defaults THEN the system SHALL ensure that each thread's session maintains its own independent default settings
15. WHEN I handle errors and exceptions THEN the system SHALL ensure that error states are properly isolated between threads
16. WHEN I work with type checking and validation THEN the system SHALL ensure that type system operations are thread-safe and don't share mutable state
17. WHEN I design the architecture THEN the system SHALL use immutable data structures where possible to minimize synchronization overhead

### Requirement 43

**User Story:** As a developer, I want to work with Nested Properties Record Schemas as a category of Primary Catalog Object, so that I can define reusable record structures independently of graph structure using multiple schema definition languages.

#### Acceptance Criteria

1. WHEN I work with Primary Catalog Objects THEN the system SHALL recognize Nested Properties Record Schemas as a distinct PCO category alongside graphs, graph types, tables, and procedures
2. WHEN I create a Nested Properties Record Schema THEN the system SHALL allow me to define it using JSON Schema as the primary schema definition language
3. WHEN I work with schema definition languages THEN the system SHALL support multiple comparable record schema definition languages beyond JSON Schema
4. WHEN I use alternative schema languages THEN the system SHALL support Parquet schema definitions for columnar data representations
5. WHEN I use alternative schema languages THEN the system SHALL support Apache Arrow schema definitions for analytics-friendly data structures
6. WHEN I design record schemas THEN the system SHALL allow me to work on content record types independently of any specific graph structure
7. WHEN I reference record schemas THEN the system SHALL allow content record types in graph types to reference Nested Properties Record Schemas by their catalog names
8. WHEN I update a Nested Properties Record Schema THEN the system SHALL automatically propagate changes to all content record types that reference it
9. WHEN I work with schema processors THEN the system SHALL provide pluggable architecture to support different validation libraries for different schema languages
10. WHEN I leverage existing tools THEN the system SHALL integrate with commonly-used libraries and tooling for each supported schema definition language
11. WHEN I work with developer skills THEN the system SHALL allow developers to use their existing knowledge of JSON Schema, Parquet, Arrow, or other schema languages
12. WHEN I serialize Nested Properties Record Schemas THEN the system SHALL preserve the original schema definition language and format
13. WHEN I validate content records THEN the system SHALL use the appropriate validator for the schema definition language of the referenced Nested Properties Record Schema
14. WHEN I work with schema evolution THEN the system SHALL support versioning and migration of Nested Properties Record Schemas
15. WHEN I design modular systems THEN the system SHALL enable teams to develop record schemas and graph structures independently and combine them later

### Requirement 44

**User Story:** As a developer, I want to conceptualize property graphs as graphs of trees (documents), so that I can understand and work with the hierarchical nature of graph elements where each element represents a document tree structure.

#### Acceptance Criteria

1. WHEN I work with property graphs THEN the system SHALL conceptualize them as graphs of trees where each element (node or edge) represents a document tree
2. WHEN I work with graph elements as trees THEN the system SHALL ensure that values are only associated with leaf nodes of each element's tree structure
3. WHEN I define minimal elements THEN the system SHALL support elements that consist only of themselves as the root node (no properties)
4. WHEN I define flat property records THEN the system SHALL support elements with root plus level 1 leaf nodes representing traditional key-value properties
5. WHEN I define full hierarchical elements THEN the system SHALL support elements with multi-level nested document structures of arbitrary depth
6. WHEN I work with element tree complexity THEN the system SHALL provide a spectrum from minimal trees (root only) to full hierarchies (deep nesting)
7. WHEN I conceptualize the structure THEN the system SHALL treat each graph element as the root of its own document tree with properties as child nodes
8. WHEN I work with nested properties THEN the system SHALL organize them as tree structures where intermediate nodes represent nested objects/maps and leaf nodes contain actual values
9. WHEN I validate element structures THEN the system SHALL ensure that the tree structure of each element conforms to its content record type definition
10. WHEN I serialize elements THEN the system SHALL be able to represent each element as both a graph node/edge and as a complete document tree
11. WHEN I work with graph traversal THEN the system SHALL provide operations that work at both the graph level (element-to-element relationships) and tree level (within-element property navigation)
12. WHEN I analyze property graphs THEN the system SHALL recognize them as two-level hierarchical structures: graphs (element relationships) containing trees (element internal structure)

### Requirement 45

**User Story:** As a developer, I want to represent graph elements using tabular structures with flexible record schemas, so that I can leverage columnar formats and analytics tools while maintaining the hierarchical nature of element data.

#### Acceptance Criteria

1. WHEN I work with graph element storage THEN the system SHALL support representing elements as records in tables where each record represents a graph element or part of a graph element
2. WHEN I use record schemas for tabular representation THEN the system SHALL support multiple schema formats including JSON Schema, Parquet schema, and Apache Arrow schema
3. WHEN I work with node tables THEN the system SHALL allow tables where each record represents a complete node element with its full tree structure
4. WHEN I work with edge tables THEN the system SHALL allow tables where each record represents a complete edge element with its full tree structure
5. WHEN I work with partitioned representations THEN the system SHALL support node tables that represent parts or blocks of a set partition for nodes
6. WHEN I work with partitioned representations THEN the system SHALL support edge tables that represent parts or blocks of a set partition for edges
7. WHEN I use columnar formats THEN the system SHALL leverage Parquet or Arrow schemas to define efficient columnar representations of element tree structures
8. WHEN I work with analytics integration THEN the system SHALL enable graph elements to be processed by analytics tools that work with columnar data formats
9. WHEN I define table schemas THEN the system SHALL ensure that the record schema can represent the full hierarchical tree structure of graph elements
10. WHEN I work with set partitioning THEN the system SHALL provide mechanisms to distribute large graphs across multiple table partitions while maintaining referential integrity
11. WHEN I query tabular representations THEN the system SHALL support both relational-style queries on element properties and graph-style traversal operations
12. WHEN I work with hybrid storage THEN the system SHALL enable combinations of graph topology storage (for relationships) and tabular element storage (for element data)
13. WHEN I use different record formats THEN the system SHALL allow the same logical graph to be represented using different physical record schema formats based on use case requirements
14. WHEN I work with large-scale analytics THEN the system SHALL enable integration with data lake and data warehouse architectures through standard columnar formats
15. WHEN I serialize graph data THEN the system SHALL support export to both graph formats (preserving topology) and tabular formats (preserving element data structure)
#
## Requirement 46

**User Story:** As a developer, I want to understand multi-conformance implications in spectral typing, so that I can handle cases where a single content record may conform to multiple content types and understand how key labels resolve ambiguity.

#### Acceptance Criteria

1. WHEN I have multiple structurally distinct content types THEN the system SHALL recognize that a single content record may conform to more than one content type
2. WHEN I insert a content record like `(:Person {name:'My name is Foo'})` THEN the system SHALL allow it to conform to multiple content types such as `(:Person {name::STRING NOT NULL, dob::DATE})` and `(:Person {name::STRING NOT NULL, dob::DATE, startDate::DATE})`
3. WHEN I work with multi-conformance scenarios THEN the system SHALL handle the theoretical possibility of non-specific typing where one record satisfies multiple type constraints
4. WHEN all content types in a graph type are keyed (have a key label set) THEN the system SHALL prevent type clashes because each content type becomes uniquely identified
5. WHEN I define key label sets for content types THEN the system SHALL use these keys to disambiguate between otherwise structurally similar content types
6. WHEN I work with keyed content types THEN the system SHALL ensure that the key label set makes each content type distinct even if their property structures overlap
7. WHEN I validate content records against multiple potential types THEN the system SHALL use key labels as the primary disambiguation mechanism
8. WHEN I design graph schemas THEN the system SHALL recommend using key label sets to avoid multi-conformance ambiguity in production systems
9. WHEN I work with unkeyed content types THEN the system SHALL acknowledge that multi-conformance is theoretically possible but may create ambiguity in type resolution
10. WHEN I analyze type safety THEN the system SHALL recognize that key labels provide a solution to the multi-conformance problem by making content types nominally distinct
11. WHEN I work with spectral type conformance intervals THEN the system SHALL handle cases where multiple [ccrt, mcrt] intervals may apply to the same content record
12. WHEN I resolve type ambiguity THEN the system SHALL prioritize key label matching over structural conformance when both mechanisms are available### R
equirement 47

**User Story:** As a developer using LEX extensions, I want to create graph schemas with mandatory keyed elements, so that I can enforce that every node and edge type has a key label set to prevent multi-conformance ambiguity.

#### Acceptance Criteria

1. WHEN I use LEX language level THEN the system SHALL support the syntax `CREATE GRAPH SCHEMA foo GRAPH TYPE ALL ELEMENT TYPES KEYED`
2. WHEN I create a graph schema with ALL ELEMENT TYPES KEYED constraint THEN the system SHALL require every node type and edge type to have a non-empty key label set
3. WHEN I define a node type A with ALL ELEMENT TYPES KEYED constraint THEN the system SHALL ensure that A has a content type A with a key label set K(A)
4. WHEN I define an edge type B with ALL ELEMENT TYPES KEYED constraint THEN the system SHALL ensure that B has a content type B with a key label set K(B)
5. WHEN I work with the mathematical relationship THEN the system SHALL enforce that K(A) ⊆ L(A), where K(A) is the key label set and L(A) is the set of all label types in content type A
6. WHEN I attempt to create an element type without a key label set in a ALL ELEMENT TYPES KEYED graph schema THEN the system SHALL reject the operation with a clear error message
7. WHEN I work with ALL ELEMENT TYPES KEYED constraint THEN the system SHALL ensure that multi-conformance ambiguity is eliminated because every content type is uniquely identified by its key labels
8. WHEN I use GQL language level THEN the system SHALL not support the ALL ELEMENT TYPES KEYED syntax as it is a LEX extension
9. WHEN I validate elements in a ALL ELEMENT TYPES KEYED graph schema THEN the system SHALL use the key label sets for definitive type identification
10. WHEN I define key label sets K(A) THEN the system SHALL ensure they consist only of label types (attribute types with LABEL_TYPE datatype) from the content type's label vector
11. WHEN I work with element type inheritance or subtyping THEN the system SHALL ensure that key label set relationships are preserved according to the content type lattice structure
12. WHEN I serialize a ALL ELEMENT TYPES KEYED graph schema THEN the system SHALL preserve the constraint information and all key label set definitions### Req
uirement 48

**User Story:** As a developer working with keyed element types, I want to understand the precise key inheritance semantics between content types and element types, so that I can properly design edge types that include endpoint identity for unique identification.

#### Acceptance Criteria

1. WHEN I define a node type (CTN1) with content type CTN1 THEN the system SHALL ensure that TK((CTN1)) = TK(CTN1), meaning the node type key is inherited directly from its content type key
2. WHEN I define an edge type (CTNTail)-[CTARC]->(CTNHead) THEN the system SHALL ensure that TK((CTNTail)-[CTARC]->(CTNHead)) = TK(CTARC), meaning the edge type key comes from the arc content type
3. WHEN I work with edge type uniqueness THEN the system SHALL require that the arc content type CTARC includes the identity of head and tail endpoint nodes in its key if the type key should identify a single edge type rather than a set of edge types with common arc content
4. WHEN I define arc content types for edges THEN the system SHALL allow the arc content type key to reference or include information about the endpoint node types to ensure edge type uniqueness
5. WHEN I work with edge types that share arc content structure THEN the system SHALL recognize that without endpoint identity in the arc content type key, multiple edge types may not be uniquely distinguished
6. WHEN I design edge type keys THEN the system SHALL provide mechanisms to include endpoint type information in the arc content type key to achieve proper edge type disambiguation
7. WHEN I validate edge type keys THEN the system SHALL ensure that TK(CTARC) provides sufficient information to uniquely identify the edge type within the graph schema
8. WHEN I work with the mathematical relationship THEN the system SHALL maintain that TK(CTARC) ⊆ L(CTARC), where the arc content type's key is a subset of its label types
9. WHEN I analyze edge type identity THEN the system SHALL distinguish between arc content type identity (which may be shared) and edge type identity (which must be unique when ALL ELEMENT TYPES KEYED is enforced)
10. WHEN I serialize edge type definitions THEN the system SHALL preserve the relationship between edge type keys and their arc content type keys including any endpoint identity information
11. WHEN I work with complex edge schemas THEN the system SHALL support arc content types that incorporate endpoint type information as part of their key label structure
12. WHEN I design graph schemas with multiple edge types THEN the system SHALL ensure that edge type keys provide unambiguous identification even when edge types share similar arc content structures
<!-
- Test comment added to trigger Agent Hook at $(date) -->