"""
LEX:2026.0.3.2 Python API

Provides interfaces and implementation classes for working with LEX graph schemas.
All classes can be constructed from YAML specifications or specification fragments.
"""

from .interfaces import (
    Catalog,
    GraphSchema,
    GraphType,
    Graph,
    Constraint,
    StorageSchema,
    NodeTypes,
    EdgeTypes,
    TypeInterpretation,
    NodeType,
    EdgeType,
    PropertyType,
)

from .implementations import (
    CatalogImpl,
    GraphSchemaImpl,
    GraphTypeImpl,
    GraphImpl,
    ConstraintImpl,
    StorageSchemaImpl,
    NodeTypesImpl,
    EdgeTypesImpl,
    TypeInterpretationImpl,
    NodeTypeImpl,
    EdgeTypeImpl,
    PropertyTypeImpl,
)

from .builders import (
    CatalogBuilder,
    GraphSchemaBuilder,
    GraphTypeBuilder,
    NodeTypesBuilder,
    EdgeTypesBuilder,
    TypeInterpretationBuilder,
    NodeTypeBuilder,
    EdgeTypeBuilder,
    PropertyTypeBuilder,
    GraphBuilder,
    ConstraintBuilder,
    StorageSchemaBuilder,
)

__all__ = [
    # Interfaces
    "Catalog",
    "GraphSchema",
    "GraphType",
    "Graph",
    "Constraint",
    "StorageSchema",
    "NodeTypes",
    "EdgeTypes",
    "TypeInterpretation",
    "NodeType",
    "EdgeType",
    "PropertyType",
    # Implementations
    "CatalogImpl",
    "GraphSchemaImpl",
    "GraphTypeImpl",
    "GraphImpl",
    "ConstraintImpl",
    "StorageSchemaImpl",
    "NodeTypesImpl",
    "EdgeTypesImpl",
    "TypeInterpretationImpl",
    "NodeTypeImpl",
    "EdgeTypeImpl",
    "PropertyTypeImpl",
    # Builders
    "CatalogBuilder",
    "GraphSchemaBuilder",
    "GraphTypeBuilder",
    "NodeTypesBuilder",
    "EdgeTypesBuilder",
    "TypeInterpretationBuilder",
    "NodeTypeBuilder",
    "EdgeTypeBuilder",
    "PropertyTypeBuilder",
    "GraphBuilder",
    "ConstraintBuilder",
    "StorageSchemaBuilder",
]
