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
    
    def addGraphType(self, graphType: GraphType):
        self.graph_types[graphType.name] = graphType
    
    def addGraph(self, graph: Graph):
        self.graphs[graph.name] = graph


class CatalogPath:
    """Unified path representation supporting traditional paths and IRIs"""
    def __init__(self, path: str, isIri: bool = False, baseIri: Optional[str] = None):
        self.path = path
        self.isIri = isIri
        self.baseIri = baseIri


class Catalog:
    """Root catalog with hierarchical structure"""
    def __init__(self, databasePath: str, catalogRootConfig=None):
        self.databasePath = databasePath
        self.catalogRootConfig = catalogRootConfig
        self.root = Directory("/", "/")
        self.currentPath = "/"
    
    def createDirectory(self, path: str) -> Directory:
        """Create a directory in the catalog"""
        parts = path.strip('/').split('/')
        current = self.root
        currentPath = ""
        
        for part in parts:
            if part:
                currentPath += f"/{part}"
                if part not in current.children:
                    current.children[part] = Directory(part, currentPath)
                current = current.children[part]
        
        return current
    
    def create_gql_schema(self, path: str, name: str) -> GQLSchema:
        """Create a GQL-schema in the specified directory"""
        directory = self.createDirectory(path)
        schemaPath = f"{path.rstrip('/')}/{name}"
        schema = GQLSchema(name, schemaPath)
        directory.schemas[name] = schema
        return schema