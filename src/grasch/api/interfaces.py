"""
LEX:2026.0.3.2 API Interfaces

Defines abstract interfaces for all primary catalog objects and their components.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Iterator, Any


class Catalog(ABC):
    """
    Interface for a graph catalog - hierarchical collection of named primary catalog objects.
    """
    
    @abstractmethod
    def getPathName(self) -> str:
        """Get the catalog path name"""
        pass
    
    @abstractmethod
    def getIRI(self) -> Optional[str]:
        """Get the optional IRI for global identification"""
        pass
    
    @abstractmethod
    def getGraphSchemas(self) -> List[GraphSchema]:
        """Get all graph schemas in this catalog"""
        pass
    
    @abstractmethod
    def getGraphs(self) -> List[Graph]:
        """Get all graphs in this catalog"""
        pass
    
    @abstractmethod
    def findGraphSchema(self, pathName: str) -> Optional[GraphSchema]:
        """Find a graph schema by path name"""
        pass
    
    @abstractmethod
    def findGraph(self, pathName: str) -> Optional[Graph]:
        """Find a graph by path name"""
        pass


class GraphSchema(ABC):
    """
    Interface for a graph schema - structural graph type plus constraints.
    """
    
    @abstractmethod
    def getPathName(self) -> str:
        """Get the schema path name"""
        pass
    
    @abstractmethod
    def getPrincipal(self) -> Optional[str]:
        """Get the owner/principal of this schema"""
        pass
    
    @abstractmethod
    def getValueTypeSystemName(self) -> str:
        """Get the value type system name (CANONICAL, CYPHER, GQL, SQL)"""
        pass
    
    @abstractmethod
    def getGraphType(self) -> GraphType:
        """Get the graph type definition"""
        pass
    
    @abstractmethod
    def getConstraints(self) -> Dict[str, Constraint]:
        """Get all constraints defined in this schema"""
        pass
    
    @abstractmethod
    def findConstraint(self, name: str) -> Optional[Constraint]:
        """Find a constraint by name"""
        pass


class GraphType(ABC):
    """
    Interface for a graph type - defines node types, edge types, and their properties.
    """
    
    @abstractmethod
    def getNodeTypes(self) -> NodeTypes:
        """Get the node types collection"""
        pass
    
    @abstractmethod
    def getEdgeTypes(self) -> EdgeTypes:
        """Get the edge types collection"""
        pass
    
    @abstractmethod
    def findNodeType(self, typeLabel: str) -> Optional[NodeType]:
        """Find a node type by type label (searches all interpretations)"""
        pass
    
    @abstractmethod
    def findEdgeType(self, typeLabel: str) -> Optional[EdgeType]:
        """Find an edge type by type label (searches all interpretations)"""
        pass
    
    @abstractmethod
    def getNodeTypeMinimumLabels(self) -> int:
        """Get minimum number of labels for node types"""
        pass
    
    @abstractmethod
    def getEdgeTypeMinimumLabels(self) -> int:
        """Get minimum number of labels for edge types"""
        pass


class NodeTypes(ABC):
    """
    Interface for a collection of node type interpretations.
    Represents the hierarchical structure of type definitions with inheritance.
    """
    
    @abstractmethod
    def getInterpretations(self) -> List[TypeInterpretation]:
        """Get all type interpretations in this collection"""
        pass
    
    @abstractmethod
    def getAllNodeTypes(self) -> List[NodeType]:
        """Get flattened list of all node types across all interpretations"""
        pass
    
    @abstractmethod
    def findNodeType(self, typeLabel: str) -> Optional[NodeType]:
        """Find a node type by type label"""
        pass


class EdgeTypes(ABC):
    """
    Interface for a collection of edge type interpretations.
    Represents the hierarchical structure of type definitions with inheritance.
    """
    
    @abstractmethod
    def getInterpretations(self) -> List[TypeInterpretation]:
        """Get all type interpretations in this collection"""
        pass
    
    @abstractmethod
    def getAllEdgeTypes(self) -> List[EdgeType]:
        """Get flattened list of all edge types across all interpretations"""
        pass
    
    @abstractmethod
    def findEdgeType(self, typeLabel: str) -> Optional[EdgeType]:
        """Find an edge type by type label"""
        pass


class TypeInterpretation(ABC):
    """
    Interface for a type interpretation - a set of types with possible subtypes.
    Can be nested to represent hierarchical type structures.
    """
    
    @abstractmethod
    def getInterpretationMode(self) -> str:
        """Get interpretation mode: 'exact', 'allowSubtypes', or 'abstractSupertypes'"""
        pass
    
    @abstractmethod
    def getTypes(self) -> List[NodeType | EdgeType]:
        """Get types defined in this interpretation"""
        pass
    
    @abstractmethod
    def getNestedInterpretations(self) -> List[TypeInterpretation]:
        """Get nested type interpretations (for hierarchical structures)"""
        pass
    
    @abstractmethod
    def isAbstract(self) -> bool:
        """Check if this interpretation defines abstract supertypes"""
        pass


class NodeType(ABC):
    """
    Interface for a node type definition.
    """
    
    @abstractmethod
    def getTypeLabel(self) -> str:
        """Get the type label"""
        pass
    
    @abstractmethod
    def getLabels(self) -> List[str]:
        """Get all labels (including typeLabel)"""
        pass
    
    @abstractmethod
    def getPropertyTypes(self) -> List[PropertyType]:
        """Get all property types"""
        pass
    
    @abstractmethod
    def getSupertypes(self) -> List[str]:
        """Get supertype labels if this type extends others"""
        pass
    
    @abstractmethod
    def isAbstract(self) -> bool:
        """Check if this is an abstract type"""
        pass
    
    @abstractmethod
    def isSubtypeOf(self, otherTypeLabel: str, graphType: GraphType) -> bool:
        """
        Check if this type is a subtype of another type.
        
        Implements Armstrong's Axioms:
        - Reflexive: Every type is a subtype of itself
        - Transitive: If A <: B and B <: C, then A <: C
        
        Args:
            otherTypeLabel: The type label to check against
            graphType: The graph type context for resolving supertypes
            
        Returns:
            True if this type is a subtype of otherTypeLabel
        """
        pass


class EdgeType(ABC):
    """
    Interface for an edge type definition.
    """
    
    @abstractmethod
    def getTypeLabel(self) -> str:
        """Get the type label"""
        pass
    
    @abstractmethod
    def getLabels(self) -> List[str]:
        """Get all labels (including typeLabel)"""
        pass
    
    @abstractmethod
    def getPropertyTypes(self) -> List[PropertyType]:
        """Get all property types"""
        pass
    
    @abstractmethod
    def getSupertypes(self) -> List[str]:
        """Get supertype labels if this type extends others"""
        pass
    
    @abstractmethod
    def getDirection(self) -> str:
        """Get edge direction (DIRECTED or UNDIRECTED)"""
        pass
    
    @abstractmethod
    def isSubtypeOf(self, otherTypeLabel: str, graphType: GraphType) -> bool:
        """
        Check if this type is a subtype of another type.
        
        Implements Armstrong's Axioms:
        - Reflexive: Every type is a subtype of itself
        - Transitive: If A <: B and B <: C, then A <: C
        
        Args:
            otherTypeLabel: The type label to check against
            graphType: The graph type context for resolving supertypes
            
        Returns:
            True if this type is a subtype of otherTypeLabel
        """
        pass
    
    @abstractmethod
    def getFirstEndpointNodeType(self) -> str:
        """Get first endpoint node type label"""
        pass
    
    @abstractmethod
    def getSecondEndpointNodeType(self) -> str:
        """Get second endpoint node type label"""
        pass


class PropertyType(ABC):
    """
    Interface for a property type definition.
    """
    
    @abstractmethod
    def getName(self) -> str:
        """Get property name"""
        pass
    
    @abstractmethod
    def getValueType(self) -> str:
        """Get value type"""
        pass
    
    @abstractmethod
    def isNotNull(self) -> bool:
        """Check if property is NOT NULL"""
        pass


class Graph(ABC):
    """
    Interface for a graph instance.
    """
    
    @abstractmethod
    def getPathName(self) -> str:
        """Get the graph path name"""
        pass
    
    @abstractmethod
    def getPrincipal(self) -> Optional[str]:
        """Get the owner/principal of this graph"""
        pass
    
    @abstractmethod
    def getGraphSchema(self) -> Optional[GraphSchema]:
        """Get the graph schema this graph conforms to"""
        pass
    
    @abstractmethod
    def getConstraints(self) -> Dict[str, Constraint]:
        """Get constraints defined for this graph"""
        pass
    
    @abstractmethod
    def getStorageSchema(self) -> Optional[StorageSchema]:
        """Get the storage schema"""
        pass


class Constraint(ABC):
    """
    Interface for a constraint definition.
    """
    
    @abstractmethod
    def getName(self) -> str:
        """Get constraint name"""
        pass
    
    @abstractmethod
    def getSubject(self) -> str:
        """Get constraint subject (KEY, UNIQUE, etc.)"""
        pass
    
    @abstractmethod
    def getConstraintPattern(self) -> str:
        """Get the constraint pattern"""
        pass
    
    @abstractmethod
    def getUniqueKeyComponentPropertyNames(self) -> List[str]:
        """Get property names for unique key components"""
        pass


class StorageSchema(ABC):
    """
    Interface for a storage schema definition.
    """
    
    @abstractmethod
    def getStorageType(self) -> str:
        """Get storage type identifier"""
        pass
    
    @abstractmethod
    def getProperties(self) -> Dict[str, Any]:
        """Get all storage properties"""
        pass
