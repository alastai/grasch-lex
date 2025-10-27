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
    catalog_root: str  # IRI for catalog base location (default: "file:.")
    default_catalog_path: Optional[str]  # Path relative to catalog_root
    nested_record_schema_processor_type: str  # e.g., "JSON Schema", "Parquet", "Arrow"
    nested_record_schema_processor: ISchemaProcessor  # Implementation class
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
- `CatalogRootResolver`: Handles catalog_root IRI resolution and path combination
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

class ICatalogRootResolver(Protocol):
    """Handles catalog_root IRI configuration and path resolution"""
    def set_catalog_root(self, root_iri: str) -> None
    def get_catalog_root(self) -> str
    def resolve_relative_path(self, relative_path: str) -> str
    def validate_root_iri(self, iri: str) -> ValidationResult
    def get_supported_schemes(self) -> Set[str]
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

@dataclass
class CatalogRootConfiguration:
    """Configuration for catalog root IRI and path resolution"""
    catalog_root: str  # IRI for catalog base location (e.g., "file:.", "file:///data/catalogs")
    supported_schemes: Set[str] = field(default_factory=lambda: {"file"})
    
    def resolve_path(self, relative_path: str) -> str:
        """Combine catalog_root IRI with relative path"""
        if self.catalog_root.startswith("file:"):
            # Handle file: scheme resolution
            base_path = self.catalog_root[5:]  # Remove "file:" prefix
            if base_path == ".":
                return relative_path
            return f"{base_path}/{relative_path.lstrip('/')}"
        else:
            # Handle other IRI schemes
            return f"{self.catalog_root.rstrip('/')}/{relative_path.lstrip('/')}"
    
    def validate_iri(self, iri: str) -> bool:
        """Validate that IRI uses supported scheme"""
        scheme = iri.split(":", 1)[0] if ":" in iri else ""
        return scheme in self.supported_schemes
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

## GQL Data Type System Analysis

### Corrected GQL Terminology

**IMPORTANT TERMINOLOGY CORRECTION**: Prior to this analysis, "datatype" was incorrectly used as a synonym for "property value type". This fundamental error must be corrected:

#### **Datatype (GQL Umbrella Term)**
- **Definition**: The type of any kind of data that can be stored in a graph
- **Scope**: ALL types in GQL that describe sets of values
- **Includes**: 
  - Property Value Types (STRING, INTEGER, BOOLEAN, etc.)
  - Record Types (structured collections of fields)
  - Node Types (define node structure and properties)  
  - Edge Types (define edge structure and properties)
  - Graph Types (define complete graph schemas)
  - Label Types
  - And other GQL type categories

#### **Property Value Type (Specific GQL Term)**
- **Definition**: The specific type that can be assigned to a property's value
- **GQL Spec Term**: "value type" (we use the longer, more specific term for clarity)
- **Scope**: Only the primitive and constructed types for property values
- **Examples**: STRING, INTEGER, BOOLEAN, DECIMAL, DATE, TIME, LIST, RECORD, etc.

#### **Corrected Type Hierarchy**
```
Datatype (GQL umbrella term for all types)
├── Property Value Types (for property values)
│   ├── Primitive Types (STRING, INTEGER, BOOLEAN, etc.)
│   └── Constructed Types (LIST, RECORD, etc.)
├── Record Types (structured field collections)
├── Element Types
│   ├── Node Types (define node structure)
│   └── Edge Types (define edge structure)
├── Graph Types (complete graph schemas)
├── Label Types
└── Other GQL datatypes...
```

#### **Grasch-Specific Terms (Not in GQL Spec)**
- **Content Record Type**: Set of attribute types (labels + property types) in union
- **Property Record Type**: Set of property types only
- **Property Type**: Pair of (name, property value type)
- **Property**: Triple of (name, property value type, value)

### JSON Schema Playground Pattern Analysis

Based on analysis of the `json-schema-playground-main` directory, I've identified two distinct approaches for integrating GQL types with JSON Schema:

#### Pattern 1: Reference-Based Approach (Main Files)
The primary approach uses JSON Schema `$ref` to reference GQL type definitions stored in a separate definitions file:

**Structure**:
- **gql-defs**: Central type definition file with `databaseType` property
- **gql-meta-schema**: Meta-schema for validating GQL type usage
- **customer-schema**: Example usage referencing types via `$ref`

**Type Definition Pattern**:
```json
{
  "gql.string": {
    "databaseType": "gql.string",
    "type": "string"
  },
  "gql.int32": {
    "databaseType": "gql.int32", 
    "type": "integer",
    "minimum": -2147483648,
    "maximum": 2147483647
  }
}
```

**Usage Pattern**:
```json
{
  "first_name": {
    "type": "string"
  },
  "date_of_birth": {
    "$ref": "https://iso.org/wg3/gql-defs#/gql.date"
  },
  "discount": {
    "$ref": "https://iso.org/wg3/gql-defs#/gql.int8",
    "minimum": 0,
    "exclusiveMaximum": 100
  }
}
```

#### Pattern 2: Experimental Implementations (Ruins Directory)
The ruins directory contains experimental/deprecated implementations that were abandoned during development:

**Experimental Content**:
- Alternative type definition approaches that didn't work
- Extended integer types that may be part of complete GQL specification
- **Special value handling**: `gql.boolSpecial` (unknown/true/false), `gql.floatingPointSpecial` (+inf/-inf/NaN)

**Note**: The "ruins" directory represents abandoned experiments and should not be considered authoritative for GQL type definitions.

### Complete GQL Property Value Types Catalog

Based on analysis of the GQL specification (sections 4.13 and 4.17), here is the **complete catalog of GQL property value types** as defined in the official standard:

#### **Atomic Property Value Types**

| **Base Type Category** | **GQL Property Value Type Keywords** | **JSON Schema Pattern** | **Description** |
|------------------------|--------------------------------------|-------------------------|-----------------|
| **Boolean Types** | `BOOL`, `BOOLEAN` | `{"databaseType": "gql.boolean", "type": "boolean"}` | Truth values (true, false, null) |
| **Character String Types** | `STRING`, `CHAR`, `VARCHAR` | `{"databaseType": "gql.string", "type": "string"}` | Unicode character sequences |
| **Byte String Types** | `BYTES`, `BINARY`, `VARBINARY` | `{"databaseType": "gql.bytes", "type": "string"}` | Byte sequences |
| **Signed Exact Numeric Types** | `DECIMAL`, `DEC`, `SMALLINT`, `SMALL INTEGER`, `SIGNED SMALL INTEGER`, `INT`, `INTEGER`, `SIGNED INTEGER`, `INT16`, `INTEGER16`, `SIGNED INTEGER16`, `INT32`, `INTEGER32`, `SIGNED INTEGER32`, `INT64`, `INTEGER64`, `SIGNED INTEGER64`, `INT128`, `INTEGER128`, `SIGNED INTEGER128`, `INT256`, `INTEGER256`, `SIGNED INTEGER256`, `BIGINT`, `BIG INTEGER`, `SIGNED BIG INTEGER` | `{"databaseType": "gql.int32", "type": "integer"}` | Signed exact numbers with various precisions |
| **Unsigned Exact Numeric Types** | `USMALLINT`, `UNSIGNED SMALL INTEGER`, `UINT`, `UNSIGNED INTEGER`, `UINT16`, `UNSIGNED INTEGER16`, `UINT32`, `UNSIGNED INTEGER32`, `UINT64`, `UNSIGNED INTEGER64`, `UINT128`, `UNSIGNED INTEGER128`, `UINT256`, `UNSIGNED INTEGER256`, `UBIGINT`, `UNSIGNED BIG INTEGER` | `{"databaseType": "gql.uint32", "type": "integer"}` | Unsigned exact numbers with various precisions |
| **Approximate Numeric Types** | `FLOAT`, `FLOAT16`, `FLOAT32`, `FLOAT64`, `FLOAT128`, `FLOAT256`, `REAL`, `DOUBLE`, `DOUBLE PRECISION` | `{"databaseType": "gql.float64", "type": "number"}` | Floating point numbers with various precisions |
| **Temporal Instant Types** | `ZONED DATETIME`, `LOCAL DATETIME`, `DATE`, `ZONED TIME`, `LOCAL TIME` | `{"databaseType": "gql.date", "type": "string"}` | Date and time values |
| **Temporal Duration Types** | `DURATION(YEAR TO MONTH)`, `DURATION(DAY TO SECOND)` | `{"databaseType": "gql.duration", "type": "string"}` | Time intervals |
| **Vector Types** | `VECTOR` | `{"databaseType": "gql.vector", "type": "array"}` | Vector data (new in GQL) |
| **Immaterial Types** | `NULL`, `NULL NOT NULL`, `NOTHING` | `{"databaseType": "gql.null", "type": "null"}` | Null and empty types |

#### **Reference Property Value Types**

| **Reference Type Category** | **GQL Keywords** | **Description** |
|------------------------------|------------------|-----------------|
| **Binding Table Reference** | `BINDING TABLE`, `TABLE` | References to binding tables |
| **Graph Reference** | `ANY PROPERTY GRAPH`, `PROPERTY GRAPH`, `ANY GRAPH`, `GRAPH` | References to property graphs |
| **Node Reference** | `ANY NODE`, `NODE`, `ANY VERTEX`, `VERTEX` | References to graph nodes |
| **Edge Reference** | `ANY EDGE`, `EDGE`, `ANY RELATIONSHIP`, `RELATIONSHIP` | References to graph edges |

#### **Constructed Property Value Types**

| **Constructed Type** | **Description** | **JSON Schema Pattern** |
|---------------------|-----------------|-------------------------|
| **Record Types** | Structured types with named fields | `{"databaseType": "gql.record", "type": "object", "properties": {...}}` |
| **List Types** | Ordered collections of values | `{"databaseType": "gql.list", "type": "array", "items": {...}}` |

#### **Key Findings from GQL Specification**

1. **INT128, INT256, UINT128, UINT256 are OFFICIAL GQL types** - not LEX extensions
2. **FLOAT16, FLOAT128, FLOAT256 are also official GQL types**
3. **Complete temporal type system** with both instant and duration types
4. **Vector types** are newly added to GQL (mentioned in the specification)
5. **Reference types** for graphs, nodes, edges, and tables
6. **Constructed types** include both RECORD and LIST types

### JSON Schema Integration Mapping

The JSON Schema playground demonstrates how to map GQL property value types to JSON Schema patterns:

| **GQL Property Value Type** | **JSON Schema Pattern** | **Value Range/Constraints** |
|----------------------------|-------------------------|----------------------------|
| `BOOLEAN` | `{"databaseType": "gql.boolean", "type": "boolean"}` | true, false, null |
| `STRING` | `{"databaseType": "gql.string", "type": "string"}` | Unicode character sequence |
| `INT32` | `{"databaseType": "gql.int32", "type": "integer", "minimum": -2147483648, "maximum": 2147483647}` | -2³¹ to 2³¹-1 |
| `INT64` | `{"databaseType": "gql.int64", "type": "integer", "minimum": -9223372036854775808, "maximum": 9223372036854775807}` | -2⁶³ to 2⁶³-1 |
| `INT128` | `{"databaseType": "gql.int128", "type": "integer", "minimum": -170141183460469231731687303715884105728, "maximum": 170141183460469231731687303715884105727}` | -2¹²⁷ to 2¹²⁷-1 |
| `UINT32` | `{"databaseType": "gql.uint32", "type": "integer", "minimum": 0, "maximum": 4294967295}` | 0 to 2³²-1 |
| `UINT64` | `{"databaseType": "gql.uint64", "type": "integer", "minimum": 0, "maximum": 18446744073709551615}` | 0 to 2⁶⁴-1 |
| `FLOAT32` | `{"databaseType": "gql.float32", "type": "number"}` | 32-bit IEEE 754 |
| `FLOAT64` | `{"databaseType": "gql.float64", "type": "number"}` | 64-bit IEEE 754 |
| `DATE` | `{"databaseType": "gql.date", "type": "string", "pattern": "^(0[1-9]|[12][0-9]|3[01])[- /.]"}` | Calendar date |
| `RECORD` | `{"databaseType": "gql.record", "type": "object", "properties": {...}}` | Structured type with named fields |
| `LIST` | `{"databaseType": "gql.list", "type": "array", "items": {...}}` | Ordered collection |

**Note**: The playground correctly implements the official GQL property value types, confirming that INT128, INT256, UINT128, UINT256, and FLOAT16 are part of the standard GQL specification, not extensions.

### Special Value Handling

The playground demonstrates sophisticated handling of special values:

**Boolean Special Values**:
```json
{
  "gql.boolSpecial": {
    "enum": ["unknown", "true", "false"],
    "format": "gql.boolSpecial"
  }
}
```

**Floating Point Special Values**:
```json
{
  "gql.floatingPointSpecial": {
    "enum": ["+inf", "-inf", "NaN"],
    "format": "gql.floatingPointSpecial"
  }
}
```

### Integration Pattern for Grasch

Based on this analysis, Grasch should implement the following integration pattern:

1. **Property Value Type Identification**: Use `databaseType` property to identify GQL property value types
2. **JSON Schema Compatibility**: Support both direct type definitions and `$ref` patterns
3. **Parameter Specification**: Handle type parameters as additional JSON Schema properties
4. **Complete GQL Support**: Support all GQL property value types as defined in the official specification
5. **Special Value Support**: Handle null, infinity, and NaN values appropriately
6. **Validation Integration**: Use JSON Schema validation for property value type checking

**Example Implementation Pattern**:
```python
class GQLPropertyValueTypeDefinition:
    """Represents a GQL property value type with JSON Schema integration"""
    property_value_type_name: str
    database_type: str  # e.g., "gql.string", "gql.int32"
    json_schema_base: Dict[str, Any]
    parameters: Dict[str, Any]  # Type constraints like maxLength, precision, scale

class GQLPropertyValueTypeRegistry:
    """Registry of all supported GQL property value types"""
    def get_property_value_type_definition(self, gql_type: str) -> GQLPropertyValueTypeDefinition
    def validate_json_schema_compatibility(self, schema: Dict[str, Any]) -> ValidationResult
    def convert_to_json_schema(self, property_value_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]
    def apply_type_constraints(self, base_property_value_type: str, constraints: Dict[str, Any]) -> Dict[str, Any]

class PropertyType:
    """Grasch-specific: Pair of (name, property value type)"""
    name: str
    property_value_type: GQLPropertyValueTypeDefinition

class Property:
    """Grasch-specific: Triple of (name, property value type, value)"""
    name: str
    property_value_type: GQLPropertyValueTypeDefinition
    value: Any  # Must be member of property_value_type (viewing type as set)
```

This analysis provides the foundation for implementing GQL property value type compatibility in Grasch through the proven JSON Schema integration pattern, using correct GQL terminology where **datatype** is the umbrella term and **property value type** is the specific category for property values.

### Intermediate Language Value Types (ILVT) System

**Purpose**: A universal type mapping hub that enables interoperability between GQL, SQL Foundation, JSON Schema extensions, and future type systems through a centralized intermediate representation.

#### **Architecture Overview**

The ILVT system creates a union of all supported value types from different systems and provides bidirectional mappings:

```
┌─────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│ GQL Property│◄──►│ Intermediate        │◄──►│ SQL Foundation  │
│ Value Types │    │ Language Value      │    │ Data Types      │
└─────────────┘    │ Types (ILVT)        │    └─────────────────┘
                   │                     │
┌─────────────┐    │                     │    ┌─────────────────┐
│ JSON Schema │◄──►│                     │◄──►│ Future Type     │
│ Extensions  │    │                     │    │ Systems         │
└─────────────┘    └─────────────────────┘    └─────────────────┘
```

#### **Core ILVT Type Registry**

| **ILVT Type** | **Category** | **Description** | **Parameters** |
|---------------|--------------|-----------------|----------------|
| **Boolean Types** | | | |
| `boolean` | Logical | Boolean true/false values | - |
| **Integer Types** | | | |
| `int8` | Signed Integer | 8-bit signed integer (-128 to 127) | - |
| `int16` | Signed Integer | 16-bit signed integer | - |
| `int32` | Signed Integer | 32-bit signed integer | - |
| `int64` | Signed Integer | 64-bit signed integer | - |
| `int128` | Extended Integer | 128-bit signed integer | - |
| `int256` | Extended Integer | 256-bit signed integer | - |
| `uint8` | Unsigned Integer | 8-bit unsigned integer (0 to 255) | - |
| `uint16` | Unsigned Integer | 16-bit unsigned integer | - |
| `uint32` | Unsigned Integer | 32-bit unsigned integer | - |
| `uint64` | Unsigned Integer | 64-bit unsigned integer | - |
| `uint128` | Extended Integer | 128-bit unsigned integer | - |
| `uint256` | Extended Integer | 256-bit unsigned integer | - |
| **Decimal Types** | | | |
| `decimal` | Exact Numeric | Arbitrary precision decimal | `precision`, `scale` |
| `numeric` | Exact Numeric | Alias for decimal | `precision`, `scale` |
| **Floating Point Types** | | | |
| `float16` | Binary Float | 16-bit IEEE 754 floating point | - |
| `float32` | Binary Float | 32-bit IEEE 754 floating point | - |
| `float64` | Binary Float | 64-bit IEEE 754 floating point | - |
| `float128` | Extended Float | 128-bit IEEE 754 floating point | - |
| `float256` | Extended Float | 256-bit IEEE 754 floating point | - |
| `decfloat32` | Decimal Float | 32-bit decimal floating point | - |
| `decfloat64` | Decimal Float | 64-bit decimal floating point | - |
| `decfloat128` | Decimal Float | 128-bit decimal floating point | - |
| **String Types** | | | |
| `string` | Character String | Variable-length Unicode string | `max_length` |
| `char` | Character String | Fixed-length Unicode string | `length` |
| **Binary Types** | | | |
| `bytes` | Binary String | Variable-length binary data | `max_length` |
| `binary` | Binary String | Fixed-length binary data | `length` |
| **Temporal Types** | | | |
| `date` | Date/Time | Calendar date (year, month, day) | - |
| `time` | Date/Time | Time of day without timezone | `precision` |
| `time_tz` | Date/Time | Time of day with timezone | `precision` |
| `datetime` | Date/Time | Date and time without timezone | `precision` |
| `datetime_tz` | Date/Time | Date and time with timezone | `precision` |
| `duration` | Date/Time | Time interval/duration | `fields` |
| **Structured Types** | | | |
| `record` | Structured | Named field collection | `fields` |
| `array` | Collection | Ordered collection of same type | `element_type`, `max_cardinality` |
| `multiset` | Collection | Unordered collection with duplicates | `element_type` |
| **Special Types** | | | |
| `json` | Semi-Structured | JSON document | - |
| `vector` | Numeric Array | Fixed-size numeric vector | `dimension`, `element_type` |
| `null` | Special | Null/missing value | - |

#### **4-Way Type Mapping Tables**

##### **Boolean Types**
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `boolean` | `BOOLEAN`, `BOOL` | `BOOLEAN` | `data.boolean` |

##### **Integer Types**
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `int8` | *No GQL equivalent* | *No SQL equivalent* | `data.int8` |
| `int16` | `SMALLINT`, `INT16` | `SMALLINT` | `data.int16` |
| `int32` | `INTEGER`, `INT`, `INT32` | `INTEGER`, `INT` | `data.int32` |
| `int64` | `BIGINT`, `INT64` | `BIGINT` | `data.int64` |
| `int128` | `INT128` | *No SQL equivalent* | `data.int128` |
| `int256` | `INT256` | *No SQL equivalent* | `data.int256` |
| `uint8` | *No GQL equivalent* | *No SQL equivalent* | `data.uint8` |
| `uint16` | `UINT16` | *No SQL equivalent* | `data.uint16` |
| `uint32` | `UINT32` | *No SQL equivalent* | `data.uint32` |
| `uint64` | `UINT64` | *No SQL equivalent* | `data.uint64` |
| `uint128` | `UINT128` | *No SQL equivalent* | `data.uint128` |
| `uint256` | `UINT256` | *No SQL equivalent* | `data.uint256` |

##### **Decimal and Floating Point Types**
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `decimal` | `DECIMAL`, `DEC` | `DECIMAL`, `NUMERIC`, `DEC` | `data.decimal` |
| `numeric` | `NUMERIC` | `NUMERIC` | `data.numeric` |
| `float16` | `FLOAT16` | *No SQL equivalent* | `data.float16` |
| `float32` | `FLOAT`, `REAL`, `FLOAT32` | `REAL` | `data.float32` |
| `float64` | `DOUBLE`, `DOUBLE PRECISION`, `FLOAT64` | `DOUBLE PRECISION` | `data.float64` |
| `float128` | `FLOAT128` | *No SQL equivalent* | `data.float128` |
| `float256` | `FLOAT256` | *No SQL equivalent* | `data.float256` |
| `decfloat32` | *No GQL equivalent* | `DECFLOAT(7)` | `data.decfloat32` |
| `decfloat64` | *No GQL equivalent* | `DECFLOAT(16)` | `data.decfloat64` |
| `decfloat128` | *No GQL equivalent* | `DECFLOAT(34)` | `data.decfloat128` |

##### **String and Binary Types**
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `string` | `STRING` | `VARCHAR`, `CHARACTER VARYING` | `data.string` |
| `char` | `CHAR` | `CHAR`, `CHARACTER` | `data.char` |
| `bytes` | `BYTES` | `BLOB`, `BINARY LARGE OBJECT` | `data.bytes` |
| `binary` | `BINARY` | `BINARY` | `data.binary` |

##### **Temporal Types**
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `date` | `DATE` | `DATE` | `data.date` |
| `time` | `LOCAL TIME` | `TIME` | `data.time` |
| `time_tz` | `ZONED TIME` | `TIME WITH TIME ZONE` | `data.timeWithTimezone` |
| `datetime` | `LOCAL DATETIME` | `TIMESTAMP` | `data.datetime` |
| `datetime_tz` | `ZONED DATETIME` | `TIMESTAMP WITH TIME ZONE` | `data.datetimeWithTimezone` |
| `duration` | `DURATION` | `INTERVAL` | `data.duration` |

##### **Structured and Special Types**
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `record` | `RECORD` | `ROW` | `data.record` |
| `array` | `LIST` | `ARRAY` | `data.array` |
| `multiset` | *No GQL equivalent* | `MULTISET` | `data.multiset` |
| `json` | `JSON` | `JSON` | `data.json` |
| `vector` | `VECTOR` | *No SQL equivalent* | `data.vector` |
| `null` | `NULL` | `NULL` | `data.null` |

#### **Implementation Framework**

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, Any, Set

class ILVTCategory(Enum):
    BOOLEAN = "boolean"
    SIGNED_INTEGER = "signed_integer"
    UNSIGNED_INTEGER = "unsigned_integer"
    DECIMAL = "decimal"
    BINARY_FLOAT = "binary_float"
    DECIMAL_FLOAT = "decimal_float"
    STRING = "string"
    BINARY = "binary"
    TEMPORAL = "temporal"
    STRUCTURED = "structured"
    COLLECTION = "collection"
    SPECIAL = "special"

@dataclass
class ILVTTypeDefinition:
    """Definition of an Intermediate Language Value Type"""
    ilvt_name: str
    category: ILVTCategory
    description: str
    parameters: Set[str]
    gql_equivalents: Set[str]
    sql_equivalents: Set[str]
    json_schema_extension: str
    
class ILVTRegistry:
    """Central registry for all ILVT type mappings"""
    
    def __init__(self):
        self._types: Dict[str, ILVTTypeDefinition] = {}
        self._gql_to_ilvt: Dict[str, str] = {}
        self._sql_to_ilvt: Dict[str, str] = {}
        self._json_to_ilvt: Dict[str, str] = {}
        self._initialize_core_types()
    
    def register_type(self, type_def: ILVTTypeDefinition) -> None:
        """Register a new ILVT type with all its mappings"""
        self._types[type_def.ilvt_name] = type_def
        
        # Build reverse mappings
        for gql_type in type_def.gql_equivalents:
            self._gql_to_ilvt[gql_type] = type_def.ilvt_name
        
        for sql_type in type_def.sql_equivalents:
            self._sql_to_ilvt[sql_type] = type_def.ilvt_name
        
        self._json_to_ilvt[type_def.json_schema_extension] = type_def.ilvt_name
    
    def gql_to_ilvt(self, gql_type: str) -> Optional[str]:
        """Convert GQL property value type to ILVT"""
        return self._gql_to_ilvt.get(gql_type)
    
    def ilvt_to_sql(self, ilvt_type: str) -> Optional[Set[str]]:
        """Convert ILVT to SQL Foundation types"""
        type_def = self._types.get(ilvt_type)
        return type_def.sql_equivalents if type_def else None
    
    def ilvt_to_json_schema(self, ilvt_type: str, parameters: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Convert ILVT to JSON Schema extension format"""
        type_def = self._types.get(ilvt_type)
        if not type_def:
            return None
        
        schema = {
            "databaseType": type_def.json_schema_extension,
            "type": self._get_json_base_type(type_def.category)
        }
        
        if parameters:
            schema.update(parameters)
        
        return schema
    
    def _get_json_base_type(self, category: ILVTCategory) -> str:
        """Map ILVT category to JSON Schema base type"""
        mapping = {
            ILVTCategory.BOOLEAN: "boolean",
            ILVTCategory.SIGNED_INTEGER: "integer",
            ILVTCategory.UNSIGNED_INTEGER: "integer",
            ILVTCategory.DECIMAL: "number",
            ILVTCategory.BINARY_FLOAT: "number",
            ILVTCategory.DECIMAL_FLOAT: "number",
            ILVTCategory.STRING: "string",
            ILVTCategory.BINARY: "string",
            ILVTCategory.TEMPORAL: "string",
            ILVTCategory.STRUCTURED: "object",
            ILVTCategory.COLLECTION: "array",
            ILVTCategory.SPECIAL: None
        }
        return mapping.get(category, "string")

class UniversalTypeMapper:
    """Universal type mapper using ILVT as intermediate representation"""
    
    def __init__(self):
        self.registry = ILVTRegistry()
    
    def convert_gql_to_sql(self, gql_type: str, parameters: Dict[str, Any] = None) -> Optional[str]:
        """Convert GQL type to SQL Foundation type via ILVT"""
        ilvt_type = self.registry.gql_to_ilvt(gql_type)
        if not ilvt_type:
            return None
        
        sql_types = self.registry.ilvt_to_sql(ilvt_type)
        if not sql_types:
            return None
        
        # Return the primary SQL type (first in set)
        primary_sql_type = next(iter(sql_types))
        
        # Apply parameters if needed
        if parameters and self._requires_parameters(primary_sql_type):
            return self._apply_sql_parameters(primary_sql_type, parameters)
        
        return primary_sql_type
    
    def convert_gql_to_json_schema(self, gql_type: str, parameters: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Convert GQL type to JSON Schema extension via ILVT"""
        ilvt_type = self.registry.gql_to_ilvt(gql_type)
        if not ilvt_type:
            return None
        
        return self.registry.ilvt_to_json_schema(ilvt_type, parameters)
```

#### **Benefits of ILVT System**

1. **Scalability**: Easy to add new type systems without modifying existing mappings
2. **Consistency**: Single source of truth for type definitions and relationships
3. **Extensibility**: Support for future type systems through ILVT hub
4. **Maintainability**: Centralized type registry with clear separation of concerns
5. **Interoperability**: Seamless conversion between any supported type systems

**Note**: This ILVT system is based on verified analysis of GQL property value types and SQL Foundation (ISO/IEC 9075-2) specifications, providing accurate type correspondence for multi-system interoperability.

This design provides a solid foundation for implementing the comprehensive requirements while maintaining flexibility for future extensions and ensuring robust operation in production environments.
## Addend
um: GQL:2027 CD1SP1 vs LEX-100 Constraint Framework Analysis

**Reference**: See [gql-2027-vs-lex-100-analysis.md](gql-2027-vs-lex-100-analysis.md) for complete analysis.

### **Key Finding: LEX-100 Constraint Framework is Incomplete**

Based on detailed analysis of GQL:2027 CD1SP1 constraint framework and LEX-100 specification, LEX-100 represents a **partial reorganization** rather than a complete alternative to GQL:2027 constraints.

### **Critical Gaps Identified:**

1. **Incomplete Constraint Descriptors**: LEX-100 acknowledges "The GQL specification is unclear to me with respect to descriptors in this area"
2. **Missing Enforcement Framework**: No constraint validation, checking, or enforcement semantics
3. **Simplified Structure**: LEX-100 constraint descriptors lack the richness of GQL:2027 CD1SP1
4. **Omitted Features**: No CREATE/DROP CONSTRAINT syntax, exception handling, or deferred enforcement

### **Design Decision: Implement Complete GQL:2027 CD1SP1 First**

**Recommendation for LEX:2026.0 Implementation:**

1. **Phase 1**: Implement complete GQL:2027 CD1SP1 constraint framework
   - Full constraint descriptors with subject sets, scopes, enforcement
   - CREATE/DROP CONSTRAINT statement support
   - KEY and UNIQUE constraint types with proper semantics
   - Exception handling (class 23, class G2)

2. **Phase 2**: Add LEX organizational alternative
   - Provide constraints-outside-graph-type organization
   - Ensure identical information content to GQL:2027 approach
   - Support both organizational patterns

3. **Phase 3**: Add LEX constraint extensions
   - Cardinality constraints (LEX:2026.1+)
   - Participation constraints (LEX:2026.1+)
   - Additional constraint types beyond GQL:2027

### **Architectural Impact:**

This analysis confirms that LEX:2026.0 must be built on a **complete** GQL:2027 CD1SP1 foundation, with LEX providing organizational alternatives and future extensions rather than replacing the GQL constraint framework.

The LEX-100 reorganization (constraints outside graph type) has conceptual merit but requires the full GQL:2027 constraint semantics to be meaningful and complete.