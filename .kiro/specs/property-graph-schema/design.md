# Design Document

## Overview

Grasch is a Python library that implements a LEX-extended GQL Catalog, providing a comprehensive system for managing property graphs with advanced constraint capabilities and configurable compliance levels. The system follows the orthogonal architecture of Profile + Language Level, where profiles define feature subsets and implementation choices while language levels (GQL or LEX) determine syntax and extension capabilities.

The design leverages Kuzu as an embedded graph database for storing the complete system as interconnected graph structures: the Catalog tree, Information Schema Graphs (ISGs), and content type lattices. This creates a unified graph-theoretic foundation while supporting multiple representation formats including tabular/columnar storage for analytics integration.

**Profile + Language Level Architecture**: Grasch supports multiple profiles (e.g., Cypher Profile, Full Profile) that can be combined with different language levels (GQL, LEX) to create a matrix of permissible configurations. This allows targeting specific compatibility requirements (like openCypher compatibility) while maintaining the flexibility to use LEX extensions where profile constraints permit.

## Architecture

### Core Architectural Principles

1. **Profile + Language Level Orthogonality**: Profiles define feature subsets and implementation choices independently of language level (GQL vs LEX)
2. **Graph-Centric Storage**: All system components (Catalog, ISGs, content type lattices) are stored as graphs in Kuzu
3. **Multi-Format Support**: Leverage existing schema languages (JSON Schema, Parquet, Arrow) rather than inventing new ones
4. **Constraint Evolution**: Version-specific constraint catalogs (LEX-2026 → LEX-202x) with monotonic capability expansion
5. **Thread Safety**: Thread-local user sessions with proper synchronization for shared resources
6. **Strong Typing**: Comprehensive Python type annotations for portability to other strongly-typed languages
7. **Modular Design**: Independent development of record schemas and graph structures
8. **Compatibility Matrix**: Clear documentation of which profile-language combinations are permissible and supported

### Profile-Aware Three-Layer API Model

The core API follows a three-layer model that separates concerns between object manipulation, declarative statements, and delta-based modifications, with all layers respecting the active profile and language level configuration:

```
┌─────────────────────────────────────────────────────────────┐
│              Delta-Based Modification Layer                 │
│                        (Top Layer)                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Takes: Existing Catalog State + Modification Delta     │ │
│  │  Produces: New End-State of Catalog                     │ │
│  │  Operations: ADD, REMOVE, UPDATE, REPLACE               │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│              Declarative Catalog Layer                     │
│                      (Middle Layer)                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Pure Declarative Statements (No Amendments/Deletions)  │ │
│  │  Operations: DECLARE GRAPH SCHEMA, DECLARE CATALOG      │ │
│  │  Immutable: Each statement creates complete definition   │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│               Schema Object Interface                       │
│                      (Bottom Layer)                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Direct Object Manipulation and Construction            │ │
│  │  Operations: Create, Configure, Validate Objects        │ │
│  │  Types: GraphType, ContentType, Constraint, etc.        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

                              ↕ ↕ ↕

┌─────────────────────────────────────────────────────────────┐
│                     Storage Layer                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Kuzu Embedded Graph Database               │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │ │
│  │  │ Catalog     │ │ Information │ │ Content Type        │ │ │
│  │  │ Tree        │ │ Schema      │ │ Lattices            │ │ │
│  │  │ Graph       │ │ Graphs      │ │                     │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### API Layer Responsibilities

#### Layer 1: Schema Object Interface (Bottom)
- **Purpose**: Direct manipulation of schema objects and their properties
- **Characteristics**: Mutable objects, imperative operations, fine-grained control
- **Examples**: 
  ```python
  graph_type = GraphType("MyGraph")
  graph_type.add_node_type(node_type)
  graph_type.add_constraint(key_constraint)
  ```

#### Layer 2: Declarative Catalog Layer (Middle)  
- **Purpose**: Complete, immutable declarations of catalog contents
- **Characteristics**: No amendments or deletions, pure declarative statements
- **Examples**:
  ```python
  CREATE OR REPLACE GRAPH SCHEMA "MySchema" AS {
      node_types: [...],
      edge_types: [...],
      constraints: [...]
  }
  
  CREATE OR REPLACE CATALOG "/production" AS {
      directories: [...],
      schemas: [...]
  }
  ```

#### Layer 3: Delta-Based Modification Layer (Top)
- **Purpose**: Transform existing catalog state through delta operations
- **Characteristics**: Takes current state + delta → produces new state
- **Examples**:
  ```python
  catalog_delta = CatalogDelta()
      .add_schema("/new/path", schema_def)
      .drop_object("/old/path/object")
      .alter_constraints("/existing/schema", new_constraints)
  
  new_catalog_state = apply_delta(current_catalog, catalog_delta)
  ```

## Profile and Language Level Management

### Profile System Architecture

Grasch implements a sophisticated profile system that defines subsets of language features and implementation-defined choices. Profiles are orthogonal to language levels, creating a matrix of supported configurations.

#### Profile Types

**Cypher Profile**:
- Compatible with openCypher/Cypher 9/Cypher 5.0
- No catalog support (GC04 disabled)
- Edge label cardinality: min=1, max=1 (IL001)
- Key label sets are singleton and equal to the single edge label
- Simplified graph type system

**Full Profile**:
- All optional GQL features enabled
- Full catalog management (GC04 enabled)
- Multiple edge labels supported (IL001: min=0, max=unlimited)
- Advanced graph type features (GG25, etc.)
- Complete ISG support

#### Language Levels

**GQL Language Level**:
- Standard GQL syntax and semantics
- Features limited by active profile
- No LEX extensions

**LEX Language Level**:
- GQL syntax plus LEX extensions
- LEX extensions must be compatible with active profile
- Additional DDL commands (CREATE/DROP DIRECTORY, SHOW commands)
- IRI-based catalog identification

#### Profile-Language Compatibility Matrix

```
                    | GQL Language Level | LEX Language Level
--------------------|-------------------|-------------------
Cypher Profile      | ✓ Supported       | ⚠️  Limited LEX*
Full Profile        | ✓ Supported       | ✓ Full LEX Support

* LEX extensions that conflict with Cypher Profile constraints are rejected
```

### Profile Configuration Interface

```python
class ProfileConfiguration:
    """Defines a specific GQL/LEX profile"""
    name: str
    optional_features: Set[str]  # e.g., {'GC04', 'GG25'}
    implementation_defined: Dict[str, Any]  # e.g., {'IL001': {'min': 1, 'max': 1}}
    lex_compatibility: LEXCompatibility
    
class LEXCompatibility(Enum):
    FULL = "full"           # All LEX extensions allowed
    LIMITED = "limited"     # Some LEX extensions may be rejected
    NONE = "none"          # No LEX extensions allowed

class LanguageLevel(Enum):
    GQL = "gql"
    LEX = "lex"

class SessionConfiguration:
    """Session-level configuration"""
    profile: ProfileConfiguration
    language_level: LanguageLevel
    default_catalog_path: Optional[str]
    json_schema_processor: ISchemaProcessor
```

## Components and Interfaces

### 1. Three-Layer API Components

#### Layer 1: Schema Object Interface Component

**Purpose**: Direct manipulation and construction of schema objects.

**Key Classes**:
- `GraphType`: Mutable graph type builder
- `ContentRecordType`: Mutable content type builder  
- `Constraint`: Constraint object hierarchy
- `AttributeType`: Label and property type builders

**Interfaces**:
```python
class ISchemaObjectBuilder(Protocol):
    """Base interface for mutable schema object construction"""
    def validate(self) -> ValidationResult
    def build(self) -> 'SchemaObject'

class IGraphTypeBuilder(ISchemaObjectBuilder):
    def add_node_type(self, node_type: NodeType) -> 'IGraphTypeBuilder'
    def add_edge_type(self, edge_type: EdgeType) -> 'IGraphTypeBuilder'
    def add_constraint(self, constraint: Constraint) -> 'IGraphTypeBuilder'
    def set_name(self, name: str) -> 'IGraphTypeBuilder'
```

#### Layer 2: Declarative Catalog Interface Component

**Purpose**: Pure declarative statements for complete catalog definitions.

**Key Classes**:
- `CatalogDeclaration`: Immutable complete catalog definition
- `GraphSchemaDeclaration`: Immutable complete graph schema definition
- `DeclarativeParser`: Parses declarative statements from DDL/YAML

**Interfaces**:
```python
class IDeclarativeCatalog(Protocol):
    """Pure declarative catalog operations - no amendments/deletions"""
    def create_or_replace_catalog(self, declaration: CatalogDeclaration) -> CatalogState
    def create_or_replace_graph_schema(self, path: str, declaration: GraphSchemaDeclaration) -> SchemaState
    def parse_declaration(self, ddl_statement: str) -> Declaration

class CatalogDeclaration:
    """Immutable complete catalog definition"""
    directories: List[DirectoryDeclaration]
    schemas: List[SchemaDeclaration]
    
    def validate(self) -> ValidationResult
    def to_catalog_state(self) -> CatalogState

class GraphSchemaDeclaration:
    """Immutable complete graph schema definition"""
    name: str
    node_types: List[NodeTypeDeclaration]
    edge_types: List[EdgeTypeDeclaration]
    constraints: List[ConstraintDeclaration]
    
    def validate(self) -> ValidationResult
    def to_schema_state(self) -> SchemaState
```

#### Layer 3: Delta-Based Modification Component

**Purpose**: Transform existing catalog state through delta operations.

**Key Classes**:
- `CatalogDelta`: Represents a set of modifications to apply
- `DeltaOperation`: Individual modification operations (ADD, REMOVE, UPDATE)
- `CatalogStateManager`: Manages state transitions

**Interfaces**:
```python
class ICatalogDelta(Protocol):
    """Delta-based catalog modifications"""
    def add_schema(self, path: str, schema: GraphSchemaDeclaration) -> 'ICatalogDelta'
    def drop_object(self, fqn: str) -> 'ICatalogDelta'
    def alter_constraints(self, schema_path: str, constraints: List[Constraint]) -> 'ICatalogDelta'
    def replace_schema(self, path: str, schema: GraphSchemaDeclaration) -> 'ICatalogDelta'

class ICatalogStateManager(Protocol):
    """Manages catalog state transitions"""
    def get_current_state(self) -> CatalogState
    def apply_delta(self, delta: CatalogDelta) -> CatalogState
    def rollback_to_state(self, state_id: str) -> CatalogState
    def get_state_history(self) -> List[CatalogStateSnapshot]

class CatalogDelta:
    """Represents modifications to apply to catalog state"""
    operations: List[DeltaOperation]
    
    def add_operation(self, op: DeltaOperation) -> 'CatalogDelta'
    def validate_against_state(self, current_state: CatalogState) -> ValidationResult
    def preview_result(self, current_state: CatalogState) -> CatalogState

class DeltaOperation(ABC):
    """Base class for delta operations"""
    operation_type: Literal['ADD', 'DROP', 'ALTER', 'REPLACE']
    target_path: str
    
class AddSchemaOperation(DeltaOperation):
    schema_declaration: GraphSchemaDeclaration
    
class DropObjectOperation(DeltaOperation):
    object_fqn: str
    
class AlterConstraintsOperation(DeltaOperation):
    new_constraints: List[Constraint]
```

### 2. Catalog Management Component

**Purpose**: Manages the hierarchical filesystem-like structure of the GQL Catalog with LEX extensions for directory and schema management.

**Key Classes**:
- `Catalog`: Root container with thread-safe access control and IRI identification support
- `Directory`: Internal nodes in the catalog tree
- `GQLSchema`: Leaf nodes containing Primary Catalog Objects
- `CatalogPath`: Strongly-typed path representation supporting both traditional paths and IRIs
- `LEXCatalogDDL`: LEX extensions for catalog DDL commands

**GQL Standard Features**:
- `USE <graph_expression>` for working graph specification
- `AT <schema_reference>` for schema context in procedures
- Schema references with absolute/relative paths

**LEX Extensions** (when LEX language level is active and profile permits):
- `CREATE DIRECTORY <path>` - Create catalog directories
- `DROP DIRECTORY <path>` - Remove catalog directories  
- `CREATE GQL SCHEMA <path>` - Create GQL-schema containers
- `DROP GQL SCHEMA <path>` - Remove GQL-schema containers
- `SHOW DIRECTORIES [AT <path>]` - List directory contents
- `SHOW SCHEMAS [AT <path>]` - List GQL-schemas
- `SHOW GRAPH SCHEMA <schema_name>` - Display ISG structure
- IRI-based catalog identification (e.g., `catalog://example.com/production#/schemas/customer`)

**Interfaces**:
```python
class ICatalog(Protocol):
    def create_directory(self, path: CatalogPath) -> Directory
    def create_gql_schema(self, path: CatalogPath) -> GQLSchema
    def get_object(self, fqn: str) -> Optional[PrimaryCatalogObject]
    def list_contents(self, path: CatalogPath) -> List[Union[Directory, GQLSchema]]
    
    # LEX extensions (available when language_level == LEX)
    def create_directory_ddl(self, ddl: str) -> None
    def drop_directory_ddl(self, ddl: str) -> None
    def show_directories_ddl(self, ddl: str) -> List[Directory]

class IGQLSchema(Protocol):
    def add_object(self, obj: PrimaryCatalogObject) -> None
    def get_object(self, name: str) -> Optional[PrimaryCatalogObject]
    def list_objects(self) -> List[PrimaryCatalogObject]

class ICatalogIRI(Protocol):
    """LEX extension for IRI-based catalog identification"""
    def resolve_iri(self, iri: str) -> CatalogPath
    def to_iri(self, path: CatalogPath) -> str
    def validate_iri(self, iri: str) -> ValidationResult
```

### 2. Primary Catalog Objects (PCO) Component

**Purpose**: Implements the various types of objects that can be stored in GQL-schemas.

**Key Classes**:
- `GraphType`: GQL:graph type definitions (PCOs) with LEX constraint extensions
- `Graph`: Graph instances (PCOs) conforming to graph types  
- `Table`: Tabular representations of graph elements (PCOs)
- `Procedure`: Stored procedures for graph operations (PCOs)
- `NestedPropertiesRecordSchema`: Reusable record structure definitions (PCOs)

**GQL Command Distinction**:
- `CREATE GRAPH TYPE`: Creates a Primary Catalog Object that specifies permitted structure and property datatypes for graphs
- `CREATE GRAPH`: Creates a graph instance (also a PCO) that conforms to a graph type's structural and datatype constraints

**GQL CREATE GRAPH TYPE Structure** (from ISO standard):
```sql
CREATE [OR REPLACE] [PROPERTY] GRAPH TYPE [IF NOT EXISTS] 
    <catalog_graph_type_parent_and_name> 
    <graph_type_source>

-- Where graph_type_source can be:
-- 1. [AS] COPY OF <graph_type_reference>
-- 2. <graph_type_like_graph>  
-- 3. [AS] <nested_graph_type_specification>
```

**LEX Extensions to GQL CREATE GRAPH TYPE**:
- Add constraint specifications to the graph type definition
- Support for LEX-specific constraint types (key constraints, cardinality constraints)  
- Version-specific constraint catalogs (LEX-2026 vs future versions)

**LEX CREATE OR REPLACE GRAPH SCHEMA Syntax** (Layer 2 - Declarative):
```sql
CREATE OR REPLACE GRAPH SCHEMA <schema_path> AS {
    -- GQL:graph type structure (nodes, edges, properties)
    gql_graph_type: <nested_graph_type_specification>,
    
    -- LEX constraint extensions
    constraints: [
        KEY CONSTRAINT ON <element_type> (<attribute_list>),
        CARDINALITY CONSTRAINT ON <relationship> (min: <n>, max: <m>),
        -- Additional LEX-2026 constraints...
    ]
}
```

This creates a `LEX:graph schema` PCO that combines:
1. **GQL:graph type** - structural definition (nodes, edges, property datatypes)
2. **LEX:constraints** - value constraints that govern graph instances

**Constraint System**:
```python
class ConstraintCatalog:
    """Version-specific constraint capabilities"""
    version: LEXVersion
    available_constraints: Set[Type[Constraint]]

class LEXGraph:
    """Extended graph with optional constraints"""
    structure: GQLGraphType  # Structural definition
    constraints: List[Constraint]  # Value constraints
    schema: Optional[LEXGraphSchema]  # Optional schema reference
```

### 3. Content Type System Component

**Purpose**: Manages the type lattice and hierarchical content structures.

**Key Classes**:
- `AttributeType`: Base class for label types and property types
- `ContentRecordType`: Proper record types with nested structure
- `ContentTypeLattice`: Bounded lattice with ANY_CONTENT_TYPE and NO_CONTENT_TYPE
- `ElementType`: Node types and edge types based on content record types

**Type Lattice Operations**:
```python
class IContentTypeLattice(Protocol):
    def add_content_type(self, content_type: ContentRecordType) -> None
    def get_supertypes(self, content_type: ContentRecordType) -> Set[ContentRecordType]
    def get_subtypes(self, content_type: ContentRecordType) -> Set[ContentRecordType]
    def is_subtype(self, subtype: ContentRecordType, supertype: ContentRecordType) -> bool
```

### 4. Schema Processing Component

**Purpose**: Handles multiple schema definition languages and validation.

**Key Interfaces**:
```python
class ISchemaProcessor(Protocol[T]):
    def validate(self, data: Any, schema: T) -> ValidationResult
    def parse_schema(self, schema_def: str) -> T
    def extract_property_types(self, schema: T) -> List[PropertyType]

class SchemaProcessorRegistry:
    """Registry for different schema processors"""
    def register_processor(self, format: str, processor: ISchemaProcessor) -> None
    def get_processor(self, format: str) -> ISchemaProcessor
```

### 5. Information Schema Graph (ISG) Component

**Purpose**: Creates and manages graph representations of graph type structures.

**Key Classes**:
- `InformationSchemaGraph`: Unified ISG combining schema graph and content type lattice
- `TypeNode`: Represents the graph type itself with connections to catalog
- `EdgeReflectionNode`: Enables edge types to connect to content types
- `SchemaGraphBuilder`: Constructs ISGs from graph type definitions

## Data Models

### Core Data Structures

#### 1. Catalog Tree Structure
```python
@dataclass
class CatalogNode:
    name: str
    parent: Optional['CatalogNode']
    children: Dict[str, 'CatalogNode']
    node_type: Literal['directory', 'gql_schema']
    iri: Optional[str] = None  # LEX extension for IRI identification

@dataclass
class PrimaryCatalogObject:
    name: str
    object_type: PCOType
    fully_qualified_name: str
    schema_container: 'GQLSchema'
    profile_requirements: Set[str]  # Required profile features
    language_level: LanguageLevel   # Minimum language level required

@dataclass
class CatalogPath:
    """Unified path representation supporting traditional paths and IRIs"""
    path: str
    is_iri: bool = False
    base_iri: Optional[str] = None
```

#### 2. Graph Type and Constraint Model
```python
@dataclass
class GQLGraphType:
    """Pure structural graph type from GQL standard"""
    name: str
    node_types: List[NodeType]
    edge_types: List[EdgeType]
    
@dataclass
class LEXGraphSchema:
    """LEX extension: structure + constraints"""
    gql_graph_type: GQLGraphType
    constraints: List[Constraint]
    
class Constraint(ABC):
    """Base class for all LEX constraints"""
    constraint_type: str
    target_elements: List[ElementType]
    
class KeyConstraint(Constraint):
    key_attributes: List[AttributeType]
    
class CardinalityConstraint(Constraint):
    min_cardinality: int
    max_cardinality: Optional[int]
```

#### 3. Content Record Type Model
```python
@dataclass
class ContentRecordType:
    """Hierarchical record structure"""
    label_types: List[LabelType]  # Vector of label types
    property_structure: PropertyStructure  # Nested map structure
    type_key: Optional[List[LabelType]]  # Subset of label types
    
class PropertyStructure:
    """Nested map structure for properties"""
    properties: Dict[str, PropertyType]
    required_properties: Set[str]
    
class PropertyType(AttributeType):
    datatype: Union[PrimitiveType, RecordType, ArrayType]
    constraints: List[PropertyConstraint]
```

#### 4. Tabular Representation Model
```python
@dataclass
class ElementTable:
    """Table representation of graph elements"""
    table_name: str
    record_schema: RecordSchema  # JSON Schema, Parquet, Arrow, etc.
    element_type: ElementType
    partition_info: Optional[PartitionInfo]
    
class RecordSchema(ABC):
    """Abstract base for different schema formats"""
    schema_format: str
    schema_definition: Any
    
class JSONSchemaRecord(RecordSchema):
    schema_definition: Dict[str, Any]
    
class ParquetSchemaRecord(RecordSchema):
    schema_definition: 'pyarrow.Schema'
```

### Graph Storage Model in Kuzu

#### 1. Catalog Tree Graph
```
Nodes: Directory, GQLSchema, PCO
Edges: contains, references
Properties: name, path, object_type
```

#### 2. Information Schema Graph (ISG)
```
Nodes: TypeNode, NodeType, EdgeType, EdgeReflectionNode, ContentType
Edges: has_node_type, has_edge_type, connects_to, subtype_of, reflects
Properties: type_name, attribute_types, constraints
```

#### 3. Cross-Component Connections
```
Edges: catalog_to_type (connects GQLSchema to TypeNode)
       type_to_lattice (connects TypeNode to ContentTypeLattice)
```

## Error Handling

### Exception Hierarchy
```python
class GraschError(Exception):
    """Base exception for all Grasch errors"""
    
class CatalogError(GraschError):
    """Catalog-related errors"""
    
class ValidationError(GraschError):
    """Schema and constraint validation errors"""
    error_path: str
    constraint_violated: str
    
class ConstraintError(GraschError):
    """Constraint definition and application errors"""
    
class SchemaProcessingError(GraschError):
    """Schema parsing and processing errors"""
    schema_format: str
    line_number: Optional[int]
```

### Error Context and Recovery
- Detailed error messages with path information
- Validation error aggregation for batch operations
- Graceful degradation for non-critical schema processing errors
- Transaction rollback for atomic catalog operations

## Testing Strategy

### Unit Testing
- **Component isolation**: Mock Kuzu database for pure logic testing
- **Type system testing**: Comprehensive lattice operation validation
- **Constraint testing**: All constraint types and combinations
- **Schema processing**: Each supported schema format

### Integration Testing
- **End-to-end workflows**: Complete catalog creation and usage
- **Multi-format interoperability**: JSON Schema ↔ Parquet ↔ Arrow
- **Kuzu integration**: Real database operations and persistence
- **Thread safety**: Concurrent access patterns

### Performance Testing
- **Large catalog scalability**: Thousands of PCOs and deep hierarchies
- **Complex lattice operations**: Performance with large type lattices
- **Tabular representation**: Large-scale element table operations
- **Memory usage**: Efficient handling of large graph structures

### Property-Based Testing
- **Lattice properties**: Mathematical properties of partial ordering
- **Constraint satisfaction**: Generated graphs satisfy applied constraints
- **Serialization roundtrips**: Preserve semantics across formats
- **Path resolution**: Catalog path operations maintain consistency

This design provides a solid foundation for implementing the comprehensive requirements while maintaining flexibility for future extensions and ensuring robust operation in production environments.