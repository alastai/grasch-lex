"""
LEX:2026.0.3.2 API Builders

Fluent builder classes for constructing API objects.
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any
from .interfaces import (
    Catalog, GraphSchema, GraphType, Graph, Constraint, StorageSchema,
    NodeTypes, EdgeTypes, TypeInterpretation, NodeType, EdgeType, PropertyType
)
from .implementations import (
    CatalogImpl, GraphSchemaImpl, GraphTypeImpl, GraphImpl,
    NodeTypesImpl, EdgeTypesImpl, TypeInterpretationImpl,
    NodeTypeImpl, EdgeTypeImpl, PropertyTypeImpl,
    ConstraintImpl, StorageSchemaImpl
)


class CatalogBuilder:
    """Fluent builder for Catalog objects"""
    
    def __init__(self, pathName: str):
        self.__pathName = pathName
        self.__iri: Optional[str] = None
        self.__graphSchemas: List[GraphSchema] = []
        self.__graphs: List[Graph] = []
    
    def withIRI(self, iri: str) -> CatalogBuilder:
        """Set the catalog IRI"""
        self.__iri = iri
        return self
    
    def addGraphSchema(self, schema: GraphSchema) -> CatalogBuilder:
        """Add a graph schema"""
        self.__graphSchemas.append(schema)
        return self
    
    def addGraph(self, graph: Graph) -> CatalogBuilder:
        """Add a graph"""
        self.__graphs.append(graph)
        return self
    
    def build(self) -> Catalog:
        """Build the Catalog instance"""
        catalog = CatalogImpl(self.__pathName, self.__iri)
        for schema in self.__graphSchemas:
            catalog.addGraphSchema(schema)
        for graph in self.__graphs:
            catalog.addGraph(graph)
        return catalog


class GraphSchemaBuilder:
    """Fluent builder for GraphSchema objects"""
    
    def __init__(self, pathName: str):
        self.__pathName = pathName
        self.__graphType: Optional[GraphType] = None
        self.__valueTypeSystemName: str = "CANONICAL"
        self.__principal: Optional[str] = None
        self.__constraints: List[Constraint] = []
    
    def withGraphType(self, graphType: GraphType) -> GraphSchemaBuilder:
        """Set the graph type"""
        self.__graphType = graphType
        return self
    
    def withValueTypeSystem(self, systemName: str) -> GraphSchemaBuilder:
        """Set the value type system name"""
        self.__valueTypeSystemName = systemName
        return self
    
    def withPrincipal(self, principal: str) -> GraphSchemaBuilder:
        """Set the principal/owner"""
        self.__principal = principal
        return self
    
    def addConstraint(self, constraint: Constraint) -> GraphSchemaBuilder:
        """Add a constraint"""
        self.__constraints.append(constraint)
        return self
    
    def build(self) -> GraphSchema:
        """Build the GraphSchema instance"""
        if self.__graphType is None:
            raise ValueError("GraphType is required")
        
        schema = GraphSchemaImpl(
            self.__pathName,
            self.__graphType,
            self.__valueTypeSystemName,
            self.__principal
        )
        for constraint in self.__constraints:
            schema.addConstraint(constraint)
        return schema


class GraphTypeBuilder:
    """Fluent builder for GraphType objects"""
    
    def __init__(self) -> None:
        self.__nodeTypes: Optional[NodeTypes] = None
        self.__edgeTypes: Optional[EdgeTypes] = None
        self.__nodeTypeMinimumLabels: int = 1
        self.__edgeTypeMinimumLabels: int = 1
    
    def withNodeTypes(self, nodeTypes: NodeTypes) -> GraphTypeBuilder:
        """Set the node types collection"""
        self.__nodeTypes = nodeTypes
        return self
    
    def withEdgeTypes(self, edgeTypes: EdgeTypes) -> GraphTypeBuilder:
        """Set the edge types collection"""
        self.__edgeTypes = edgeTypes
        return self
    
    def withNodeTypeMinimumLabels(self, count: int) -> GraphTypeBuilder:
        """Set minimum labels for node types"""
        self.__nodeTypeMinimumLabels = count
        return self
    
    def withEdgeTypeMinimumLabels(self, count: int) -> GraphTypeBuilder:
        """Set minimum labels for edge types"""
        self.__edgeTypeMinimumLabels = count
        return self
    
    def build(self) -> GraphType:
        """Build the GraphType instance"""
        if self.__nodeTypes is None:
            raise ValueError("NodeTypes is required")
        if self.__edgeTypes is None:
            raise ValueError("EdgeTypes is required")
        
        return GraphTypeImpl(
            self.__nodeTypes,
            self.__edgeTypes,
            self.__nodeTypeMinimumLabels,
            self.__edgeTypeMinimumLabels
        )


class NodeTypesBuilder:
    """Fluent builder for NodeTypes collection"""
    
    def __init__(self) -> None:
        self.__interpretations: List[TypeInterpretation] = []
    
    def addInterpretation(self, interpretation: TypeInterpretation) -> NodeTypesBuilder:
        """Add a type interpretation"""
        self.__interpretations.append(interpretation)
        return self
    
    def build(self) -> NodeTypes:
        """Build the NodeTypes instance"""
        return NodeTypesImpl(self.__interpretations)


class EdgeTypesBuilder:
    """Fluent builder for EdgeTypes collection"""
    
    def __init__(self) -> None:
        self.__interpretations: List[TypeInterpretation] = []
    
    def addInterpretation(self, interpretation: TypeInterpretation) -> EdgeTypesBuilder:
        """Add a type interpretation"""
        self.__interpretations.append(interpretation)
        return self
    
    def build(self) -> EdgeTypes:
        """Build the EdgeTypes instance"""
        return EdgeTypesImpl(self.__interpretations)


class TypeInterpretationBuilder:
    """Fluent builder for TypeInterpretation objects"""
    
    def __init__(self, interpretationMode: str):
        """
        Create a type interpretation builder.
        
        Args:
            interpretationMode: 'exact', 'allowSubtypes', or 'abstractSupertypes'
        """
        self.__interpretationMode = interpretationMode
        self.__types: List[NodeType | EdgeType] = []
        self.__nestedInterpretations: List[TypeInterpretation] = []
    
    def addType(self, typ: NodeType | EdgeType) -> TypeInterpretationBuilder:
        """Add a type to this interpretation"""
        self.__types.append(typ)
        return self
    
    def addNestedInterpretation(self, interpretation: TypeInterpretation) -> TypeInterpretationBuilder:
        """Add a nested interpretation"""
        self.__nestedInterpretations.append(interpretation)
        return self
    
    def build(self) -> TypeInterpretation:
        """Build the TypeInterpretation instance"""
        return TypeInterpretationImpl(
            self.__interpretationMode,
            self.__types,
            self.__nestedInterpretations
        )


class NodeTypeBuilder:
    """Fluent builder for NodeType objects"""
    
    def __init__(self, typeLabel: str):
        self.__typeLabel = typeLabel
        self.__labels: List[str] = [typeLabel]
        self.__propertyTypes: List[PropertyType] = []
        self.__supertypes: List[str] = []
        self.__isAbstract: bool = False
    
    def withLabels(self, labels: List[str]) -> NodeTypeBuilder:
        """Set all labels (including typeLabel)"""
        self.__labels = labels
        return self
    
    def addLabel(self, label: str) -> NodeTypeBuilder:
        """Add an additional label"""
        if label not in self.__labels:
            self.__labels.append(label)
        return self
    
    def addPropertyType(self, propertyType: PropertyType) -> NodeTypeBuilder:
        """Add a property type"""
        self.__propertyTypes.append(propertyType)
        return self
    
    def addProperty(self, name: str, valueType: str, notNull: bool = False) -> NodeTypeBuilder:
        """Add a property type (convenience method)"""
        self.__propertyTypes.append(PropertyTypeImpl(name, valueType, notNull))
        return self
    
    def withSupertypes(self, supertypes: List[str]) -> NodeTypeBuilder:
        """Set supertype labels"""
        self.__supertypes = supertypes
        return self
    
    def addSupertype(self, supertype: str) -> NodeTypeBuilder:
        """Add a supertype label"""
        if supertype not in self.__supertypes:
            self.__supertypes.append(supertype)
        return self
    
    def asAbstract(self) -> NodeTypeBuilder:
        """Mark this type as abstract"""
        self.__isAbstract = True
        return self
    
    def build(self) -> NodeType:
        """Build the NodeType instance"""
        return NodeTypeImpl(
            self.__typeLabel,
            self.__labels,
            self.__propertyTypes,
            self.__supertypes,
            self.__isAbstract
        )


class EdgeTypeBuilder:
    """Fluent builder for EdgeType objects"""
    
    def __init__(
        self,
        typeLabel: str,
        firstEndpointNodeType: str,
        secondEndpointNodeType: str
    ):
        self.__typeLabel = typeLabel
        self.__firstEndpointNodeType = firstEndpointNodeType
        self.__secondEndpointNodeType = secondEndpointNodeType
        self.__direction: str = "DIRECTED"
        self.__labels: List[str] = [typeLabel]
        self.__propertyTypes: List[PropertyType] = []
        self.__supertypes: List[str] = []
    
    def withDirection(self, direction: str) -> EdgeTypeBuilder:
        """Set edge direction (DIRECTED or UNDIRECTED)"""
        self.__direction = direction
        return self
    
    def asUndirected(self) -> EdgeTypeBuilder:
        """Mark this edge as undirected"""
        self.__direction = "UNDIRECTED"
        return self
    
    def withLabels(self, labels: List[str]) -> EdgeTypeBuilder:
        """Set all labels (including typeLabel)"""
        self.__labels = labels
        return self
    
    def addLabel(self, label: str) -> EdgeTypeBuilder:
        """Add an additional label"""
        if label not in self.__labels:
            self.__labels.append(label)
        return self
    
    def addPropertyType(self, propertyType: PropertyType) -> EdgeTypeBuilder:
        """Add a property type"""
        self.__propertyTypes.append(propertyType)
        return self
    
    def addProperty(self, name: str, valueType: str, notNull: bool = False) -> EdgeTypeBuilder:
        """Add a property type (convenience method)"""
        self.__propertyTypes.append(PropertyTypeImpl(name, valueType, notNull))
        return self
    
    def withSupertypes(self, supertypes: List[str]) -> EdgeTypeBuilder:
        """Set supertype labels"""
        self.__supertypes = supertypes
        return self
    
    def addSupertype(self, supertype: str) -> EdgeTypeBuilder:
        """Add a supertype label"""
        if supertype not in self.__supertypes:
            self.__supertypes.append(supertype)
        return self
    
    def build(self) -> EdgeType:
        """Build the EdgeType instance"""
        return EdgeTypeImpl(
            self.__typeLabel,
            self.__firstEndpointNodeType,
            self.__secondEndpointNodeType,
            self.__direction,
            self.__labels,
            self.__propertyTypes,
            self.__supertypes
        )


class PropertyTypeBuilder:
    """Fluent builder for PropertyType objects"""
    
    def __init__(self, name: str, valueType: str):
        self.__name = name
        self.__valueType = valueType
        self.__notNull: bool = False
    
    def asNotNull(self) -> PropertyTypeBuilder:
        """Mark this property as NOT NULL"""
        self.__notNull = True
        return self
    
    def build(self) -> PropertyType:
        """Build the PropertyType instance"""
        return PropertyTypeImpl(self.__name, self.__valueType, self.__notNull)


class GraphBuilder:
    """Fluent builder for Graph objects"""
    
    def __init__(self, pathName: str):
        self.__pathName = pathName
        self.__graphSchema: Optional[GraphSchema] = None
        self.__principal: Optional[str] = None
        self.__storageSchema: Optional[StorageSchema] = None
        self.__constraints: List[Constraint] = []
    
    def withGraphSchema(self, graphSchema: GraphSchema) -> GraphBuilder:
        """Set the graph schema"""
        self.__graphSchema = graphSchema
        return self
    
    def withPrincipal(self, principal: str) -> GraphBuilder:
        """Set the principal/owner"""
        self.__principal = principal
        return self
    
    def withStorageSchema(self, storageSchema: StorageSchema) -> GraphBuilder:
        """Set the storage schema"""
        self.__storageSchema = storageSchema
        return self
    
    def addConstraint(self, constraint: Constraint) -> GraphBuilder:
        """Add a constraint"""
        self.__constraints.append(constraint)
        return self
    
    def build(self) -> Graph:
        """Build the Graph instance"""
        graph = GraphImpl(
            self.__pathName,
            self.__graphSchema,
            self.__principal,
            self.__storageSchema
        )
        for constraint in self.__constraints:
            graph.addConstraint(constraint)
        return graph


class ConstraintBuilder:
    """Fluent builder for Constraint objects"""
    
    def __init__(self, name: str, subject: str):
        self.__name = name
        self.__subject = subject
        self.__constraintPattern: str = ""
        self.__uniqueKeyComponentPropertyNames: List[str] = []
    
    def withConstraintPattern(self, pattern: str) -> ConstraintBuilder:
        """Set the constraint pattern"""
        self.__constraintPattern = pattern
        return self
    
    def withUniqueKeyComponents(self, propertyNames: List[str]) -> ConstraintBuilder:
        """Set unique key component property names"""
        self.__uniqueKeyComponentPropertyNames = propertyNames
        return self
    
    def build(self) -> Constraint:
        """Build the Constraint instance"""
        return ConstraintImpl(
            self.__name,
            self.__subject,
            self.__constraintPattern,
            self.__uniqueKeyComponentPropertyNames
        )


class StorageSchemaBuilder:
    """Fluent builder for StorageSchema objects"""
    
    def __init__(self, storageType: str):
        self.__storageType = storageType
        self.__properties: Dict[str, Any] = {}
    
    def withProperty(self, key: str, value: Any) -> StorageSchemaBuilder:
        """Add a storage property"""
        self.__properties[key] = value
        return self
    
    def withProperties(self, properties: Dict[str, Any]) -> StorageSchemaBuilder:
        """Set all storage properties"""
        self.__properties = properties.copy()
        return self
    
    def build(self) -> StorageSchema:
        """Build the StorageSchema instance"""
        return StorageSchemaImpl(self.__storageType, self.__properties)
