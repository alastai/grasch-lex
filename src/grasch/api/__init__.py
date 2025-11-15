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
    NodeType,
    EdgeType,
)

from .impl import (
    CatalogImpl,
    GraphSchemaImpl,
    GraphTypeImpl,
    GraphImpl,
    ConstraintImpl,
    StorageSchemaImpl,
    NodeTypeImpl,
    EdgeTypeImpl,
)

__all__ = [
    # Interfaces
    "Catalog",
    "GraphSchema",
    "GraphType",
    "Graph",
    "Constraint",
    "StorageSchema",
    "NodeType",
    "EdgeType",
    # Implementations
    "CatalogImpl",
    "GraphSchemaImpl",
    "GraphTypeImpl",
    "GraphImpl",
    "ConstraintImpl",
    "StorageSchemaImpl",
    "NodeTypeImpl",
    "EdgeTypeImpl",
]
