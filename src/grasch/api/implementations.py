"""
LEX:2026.0.3.2 API Implementations

Concrete implementations of the API interfaces.
"""

from __future__ import annotations
from typing import List, Dict, Optional, Any
from .interfaces import (
    Catalog, GraphSchema, GraphType, Graph, Constraint, StorageSchema,
    NodeTypes, EdgeTypes, TypeInterpretation, NodeType, EdgeType, PropertyType
)


class CatalogImpl(Catalog):
    """Implementation of Catalog interface"""
    
    def __init__(self, pathName: str, iri: Optional[str] = None):
        self.__pathName = pathName
        self.__iri = iri
        self.__graphSchemas: List[GraphSchema] = []
        self.__graphs: List[Graph] = []
    
    def getPathName(self) -> str:
        return self.__pathName
    
    def getIRI(self) -> Optional[str]:
        return self.__iri
    
    def getGraphSchemas(self) -> List[GraphSchema]:
        return self.__graphSchemas.copy()
    
    def getGraphs(self) -> List[Graph]:
        return self.__graphs.copy()
    
    def findGraphSchema(self, pathName: str) -> Optional[GraphSchema]:
        for schema in self.__graphSchemas:
            if schema.getPathName() == pathName:
                return schema
        return None
    
    def findGraph(self, pathName: str) -> Optional[Graph]:
        for graph in self.__graphs:
            if graph.getPathName() == pathName:
                return graph
        return None
    
    def addGraphSchema(self, schema: GraphSchema) -> None:
        """Add a graph schema to this catalog"""
        self.__graphSchemas.append(schema)
    
    def addGraph(self, graph: Graph) -> None:
        """Add a graph to this catalog"""
        self.__graphs.append(graph)


class GraphSchemaImpl(GraphSchema):
    """Implementation of GraphSchema interface"""
    
    def __init__(
        self,
        pathName: str,
        graphType: GraphType,
        valueTypeSystemName: str = "CANONICAL",
        principal: Optional[str] = None
    ):
        self.__pathName = pathName
        self.__graphType = graphType
        self.__valueTypeSystemName = valueTypeSystemName
        self.__principal = principal
        self.__constraints: Dict[str, Constraint] = {}
    
    def getPathName(self) -> str:
        return self.__pathName
    
    def getPrincipal(self) -> Optional[str]:
        return self.__principal
    
    def getValueTypeSystemName(self) -> str:
        return self.__valueTypeSystemName
    
    def getGraphType(self) -> GraphType:
        return self.__graphType
    
    def getConstraints(self) -> Dict[str, Constraint]:
        return self.__constraints.copy()
    
    def findConstraint(self, name: str) -> Optional[Constraint]:
        return self.__constraints.get(name)
    
    def addConstraint(self, constraint: Constraint) -> None:
        """Add a constraint to this schema"""
        self.__constraints[constraint.getName()] = constraint


class GraphTypeImpl(GraphType):
    """Implementation of GraphType interface"""
    
    def __init__(
        self,
        nodeTypes: NodeTypes,
        edgeTypes: EdgeTypes,
        nodeTypeMinimumLabels: int = 1,
        edgeTypeMinimumLabels: int = 1
    ):
        self.__nodeTypes = nodeTypes
        self.__edgeTypes = edgeTypes
        self.__nodeTypeMinimumLabels = nodeTypeMinimumLabels
        self.__edgeTypeMinimumLabels = edgeTypeMinimumLabels
    
    def getNodeTypes(self) -> NodeTypes:
        return self.__nodeTypes
    
    def getEdgeTypes(self) -> EdgeTypes:
        return self.__edgeTypes
    
    def findNodeType(self, typeLabel: str) -> Optional[NodeType]:
        return self.__nodeTypes.findNodeType(typeLabel)
    
    def findEdgeType(self, typeLabel: str) -> Optional[EdgeType]:
        return self.__edgeTypes.findEdgeType(typeLabel)
    
    def getNodeTypeMinimumLabels(self) -> int:
        return self.__nodeTypeMinimumLabels
    
    def getEdgeTypeMinimumLabels(self) -> int:
        return self.__edgeTypeMinimumLabels


class NodeTypesImpl(NodeTypes):
    """Implementation of NodeTypes interface"""
    
    def __init__(self, interpretations: List[TypeInterpretation]):
        self.__interpretations = interpretations
    
    def getInterpretations(self) -> List[TypeInterpretation]:
        return self.__interpretations.copy()
    
    def getAllNodeTypes(self) -> List[NodeType]:
        """Recursively collect all node types from all interpretations"""
        result: List[NodeType] = []
        
        def collectFromInterpretation(interp: TypeInterpretation) -> None:
            for typ in interp.getTypes():
                if isinstance(typ, NodeType):
                    result.append(typ)
            for nested in interp.getNestedInterpretations():
                collectFromInterpretation(nested)
        
        for interp in self.__interpretations:
            collectFromInterpretation(interp)
        
        return result
    
    def findNodeType(self, typeLabel: str) -> Optional[NodeType]:
        """Search for a node type by label across all interpretations"""
        for nodeType in self.getAllNodeTypes():
            if nodeType.getTypeLabel() == typeLabel:
                return nodeType
        return None


class EdgeTypesImpl(EdgeTypes):
    """Implementation of EdgeTypes interface"""
    
    def __init__(self, interpretations: List[TypeInterpretation]):
        self.__interpretations = interpretations
    
    def getInterpretations(self) -> List[TypeInterpretation]:
        return self.__interpretations.copy()
    
    def getAllEdgeTypes(self) -> List[EdgeType]:
        """Recursively collect all edge types from all interpretations"""
        result: List[EdgeType] = []
        
        def collectFromInterpretation(interp: TypeInterpretation) -> None:
            for typ in interp.getTypes():
                if isinstance(typ, EdgeType):
                    result.append(typ)
            for nested in interp.getNestedInterpretations():
                collectFromInterpretation(nested)
        
        for interp in self.__interpretations:
            collectFromInterpretation(interp)
        
        return result
    
    def findEdgeType(self, typeLabel: str) -> Optional[EdgeType]:
        """Search for an edge type by label across all interpretations"""
        for edgeType in self.getAllEdgeTypes():
            if edgeType.getTypeLabel() == typeLabel:
                return edgeType
        return None


class TypeInterpretationImpl(TypeInterpretation):
    """Implementation of TypeInterpretation interface"""
    
    def __init__(
        self,
        interpretationMode: str,
        types: List[NodeType | EdgeType],
        nestedInterpretations: Optional[List[TypeInterpretation]] = None
    ):
        if interpretationMode not in ('exact', 'allowSubtypes', 'abstractSupertypes'):
            raise ValueError(f"Invalid interpretation mode: {interpretationMode}")
        
        self.__interpretationMode = interpretationMode
        self.__types = types
        self.__nestedInterpretations = nestedInterpretations or []
    
    def getInterpretationMode(self) -> str:
        return self.__interpretationMode
    
    def getTypes(self) -> List[NodeType | EdgeType]:
        return self.__types.copy()
    
    def getNestedInterpretations(self) -> List[TypeInterpretation]:
        return self.__nestedInterpretations.copy()
    
    def isAbstract(self) -> bool:
        return self.__interpretationMode == 'abstractSupertypes'


class NodeTypeImpl(NodeType):
    """Implementation of NodeType interface"""
    
    def __init__(
        self,
        typeLabel: str,
        labels: Optional[List[str]] = None,
        propertyTypes: Optional[List[PropertyType]] = None,
        supertypes: Optional[List[str]] = None,
        isAbstract: bool = False
    ):
        self.__typeLabel = typeLabel
        self.__labels = labels or [typeLabel]
        self.__propertyTypes = propertyTypes or []
        self.__supertypes = supertypes or []
        self.__isAbstract = isAbstract
    
    def getTypeLabel(self) -> str:
        return self.__typeLabel
    
    def getLabels(self) -> List[str]:
        return self.__labels.copy()
    
    def getPropertyTypes(self) -> List[PropertyType]:
        return self.__propertyTypes.copy()
    
    def getSupertypes(self) -> List[str]:
        return self.__supertypes.copy()
    
    def isAbstract(self) -> bool:
        return self.__isAbstract


class EdgeTypeImpl(EdgeType):
    """Implementation of EdgeType interface"""
    
    def __init__(
        self,
        typeLabel: str,
        firstEndpointNodeType: str,
        secondEndpointNodeType: str,
        direction: str = "DIRECTED",
        labels: Optional[List[str]] = None,
        propertyTypes: Optional[List[PropertyType]] = None,
        supertypes: Optional[List[str]] = None
    ):
        if direction not in ('DIRECTED', 'UNDIRECTED'):
            raise ValueError(f"Invalid direction: {direction}")
        
        self.__typeLabel = typeLabel
        self.__firstEndpointNodeType = firstEndpointNodeType
        self.__secondEndpointNodeType = secondEndpointNodeType
        self.__direction = direction
        self.__labels = labels or [typeLabel]
        self.__propertyTypes = propertyTypes or []
        self.__supertypes = supertypes or []
    
    def getTypeLabel(self) -> str:
        return self.__typeLabel
    
    def getLabels(self) -> List[str]:
        return self.__labels.copy()
    
    def getPropertyTypes(self) -> List[PropertyType]:
        return self.__propertyTypes.copy()
    
    def getSupertypes(self) -> List[str]:
        return self.__supertypes.copy()
    
    def getDirection(self) -> str:
        return self.__direction
    
    def getFirstEndpointNodeType(self) -> str:
        return self.__firstEndpointNodeType
    
    def getSecondEndpointNodeType(self) -> str:
        return self.__secondEndpointNodeType


class PropertyTypeImpl(PropertyType):
    """Implementation of PropertyType interface"""
    
    def __init__(
        self,
        name: str,
        valueType: str,
        notNull: bool = False
    ):
        self.__name = name
        self.__valueType = valueType
        self.__notNull = notNull
    
    def getName(self) -> str:
        return self.__name
    
    def getValueType(self) -> str:
        return self.__valueType
    
    def isNotNull(self) -> bool:
        return self.__notNull


class GraphImpl(Graph):
    """Implementation of Graph interface"""
    
    def __init__(
        self,
        pathName: str,
        graphSchema: Optional[GraphSchema] = None,
        principal: Optional[str] = None,
        storageSchema: Optional[StorageSchema] = None
    ):
        self.__pathName = pathName
        self.__graphSchema = graphSchema
        self.__principal = principal
        self.__storageSchema = storageSchema
        self.__constraints: Dict[str, Constraint] = {}
    
    def getPathName(self) -> str:
        return self.__pathName
    
    def getPrincipal(self) -> Optional[str]:
        return self.__principal
    
    def getGraphSchema(self) -> Optional[GraphSchema]:
        return self.__graphSchema
    
    def getConstraints(self) -> Dict[str, Constraint]:
        return self.__constraints.copy()
    
    def getStorageSchema(self) -> Optional[StorageSchema]:
        return self.__storageSchema
    
    def addConstraint(self, constraint: Constraint) -> None:
        """Add a constraint to this graph"""
        self.__constraints[constraint.getName()] = constraint


class ConstraintImpl(Constraint):
    """Implementation of Constraint interface"""
    
    def __init__(
        self,
        name: str,
        subject: str,
        constraintPattern: str,
        uniqueKeyComponentPropertyNames: Optional[List[str]] = None
    ):
        self.__name = name
        self.__subject = subject
        self.__constraintPattern = constraintPattern
        self.__uniqueKeyComponentPropertyNames = uniqueKeyComponentPropertyNames or []
    
    def getName(self) -> str:
        return self.__name
    
    def getSubject(self) -> str:
        return self.__subject
    
    def getConstraintPattern(self) -> str:
        return self.__constraintPattern
    
    def getUniqueKeyComponentPropertyNames(self) -> List[str]:
        return self.__uniqueKeyComponentPropertyNames.copy()


class StorageSchemaImpl(StorageSchema):
    """Implementation of StorageSchema interface"""
    
    def __init__(self, storageType: str, properties: Optional[Dict[str, Any]] = None):
        self.__storageType = storageType
        self.__properties = properties or {}
    
    def getStorageType(self) -> str:
        return self.__storageType
    
    def getProperties(self) -> Dict[str, Any]:
        return self.__properties.copy()
