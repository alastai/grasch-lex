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
    LEXCompatibility,
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
    NodeType,
    EdgeType,
    GraphType,
    Graph,
)

from .constraints import (
    KeyConstraint,
)

__all__ = [
    # Core classes
    "GraschSession",
    "SessionConfiguration", 
    "ProfileConfiguration",
    "LanguageLevel",
    "LEXCompatibility",
    
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
    "NodeType",
    "EdgeType",
    "GraphType",
    "Graph",
    
    # Constraints
    "KeyConstraint",
]