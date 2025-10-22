"""
Grasch: LEX-extended GQL Catalog library for property graph schema management.

This library implements a comprehensive system for managing property graphs with
advanced constraint capabilities and configurable compliance levels following
the GQL (Graph Query Language) specification with LEX (Language Extensions).
"""

__version__ = "0.1.0"
__author__ = "Grasch Development Team"

# Core exports (these would be the actual implementation classes)
from .core import (
    GraschSession,
    SessionConfiguration,
    ProfileConfiguration,
    LanguageLevel,
    LanguageTypes,
    LEXCompatibility,
    CatalogRootConfiguration,
)

from .catalog import (
    Catalog,
    Directory,
    GQLSchema,
    CatalogPath,
)

from .types import (
    AttributeType,
    LabelType,
    PropertyType,
    ContentRecordType,
    ContentRecordTypeBuilder,
    LabelTypeBuilder,
    PropertyTypeBuilder,
    NodeType,
    NodeTypeBuilder,
    ArcType,
    ArcTypeBuilder,
    EdgeType,
    EdgeTypeBuilder,
    EdgeDirection,
    GraphType,
    GraphTypeBuilder,
    Graph,
)

from .constraints import (
    KeyConstraint,
)

from .value_types import (
    ValueType,
    ValidationResult,
    ValidationError,
    ILVTType,
    LanguageTypeMapper,
    validateValue,
    isValidValue,
    getTypeForValue,
    convertLegacyDatatype,
    getLanguageTypeName,
    translateType,
    isTypeCompatible,
    inferPreciseType,
)

from .schemas import (
    load_gql_descriptors_schema,
    get_schema_path,
)

from .validation import (
    SchemaValidator,
    ValidationError as SchemaValidationError,
    validate_graph_schema,
)

__all__ = [
    # Core classes
    "GraschSession",
    "SessionConfiguration", 
    "ProfileConfiguration",
    "LanguageLevel",
    "LEXCompatibility",
    "CatalogRootConfiguration",
    
    # Catalog management
    "Catalog",
    "Directory", 
    "GQLSchema",
    "CatalogPath",
    
    # Type system
    "AttributeType",
    "LabelType",
    "PropertyType", 
    "ContentRecordType",
    "ContentRecordTypeBuilder",
    "LabelTypeBuilder",
    "PropertyTypeBuilder",
    "NodeType",
    "NodeTypeBuilder",
    "ArcType",
    "ArcTypeBuilder",
    "EdgeType",
    "EdgeTypeBuilder",
    "EdgeDirection",
    "GraphType",
    "GraphTypeBuilder",
    "Graph",
    
    # Constraints
    "KeyConstraint",
    
    # Value types and validation
    "ValueType",
    "ValidationResult",
    "ValidationError",
    "ILVTType",
    "LanguageTypeMapper",
    "validateValue",
    "isValidValue",
    "getTypeForValue",
    "convertLegacyDatatype",
    "getLanguageTypeName",
    "translateType",
    "isTypeCompatible",
    "inferPreciseType",
    
    # Schema validation
    "load_gql_descriptors_schema",
    "get_schema_path",
    "SchemaValidator",
    "SchemaValidationError", 
    "validate_graph_schema",
]