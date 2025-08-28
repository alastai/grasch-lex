"""
Catalog management for hierarchical GQL schema organization.
"""

from typing import Dict, Optional
from .types import GraphType, Graph


class Directory:
    """Catalog directory"""
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.children: Dict[str, 'Directory'] = {}
        self.schemas: Dict[str, 'GQLSchema'] = {}


class GQLSchema:
    """GQL-schema container for primary catalog objects"""
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.graph_types: Dict[str, GraphType] = {}
        self.graphs: Dict[str, Graph] = {}
    
    def add_graph_type(self, graph_type: GraphType):
        self.graph_types[graph_type.name] = graph_type
    
    def add_graph(self, graph: Graph):
        self.graphs[graph.name] = graph


class CatalogPath:
    """Unified path representation supporting traditional paths and IRIs"""
    def __init__(self, path: str, is_iri: bool = False, base_iri: Optional[str] = None):
        self.path = path
        self.is_iri = is_iri
        self.base_iri = base_iri


class Catalog:
    """Root catalog with hierarchical structure"""
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.root = Directory("/", "/")
        self.current_path = "/"
    
    def create_directory(self, path: str) -> Directory:
        """Create a directory in the catalog"""
        parts = path.strip('/').split('/')
        current = self.root
        current_path = ""
        
        for part in parts:
            if part:
                current_path += f"/{part}"
                if part not in current.children:
                    current.children[part] = Directory(part, current_path)
                current = current.children[part]
        
        return current
    
    def create_gql_schema(self, path: str, name: str) -> GQLSchema:
        """Create a GQL-schema in the specified directory"""
        directory = self.create_directory(path)
        schema_path = f"{path.rstrip('/')}/{name}"
        schema = GQLSchema(name, schema_path)
        directory.schemas[name] = schema
        return schema