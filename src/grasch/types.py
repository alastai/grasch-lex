"""
Type system for content record types, element types, and graph types.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum
import uuid
from src.grasch.type_interpretation import TypeInterpretation


class AttributeType:
    """Base class for label types and property types"""
    def __init__(self, name: str, datatype: str):
        self.name = name
        self.datatype = datatype


class LabelType(AttributeType):
    """Label type with constant label datatype"""
    def __init__(self, name: str):
        super().__init__(name, "LABEL_DATATYPE")


class PropertyType(AttributeType):
    """Property type with GQL datatypes"""
    def __init__(self, name: str, datatype: str, notNull: bool = False):
        super().__init__(name, datatype)
        self.notNull = notNull


class ContentRecordType:
    """Hierarchical record structure with label types and property structure"""
    def __init__(self, labelTypes: List[LabelType], propertyTypes: List[PropertyType], typeIdentifier: Optional[List[str]] = None):
        self.labelTypes = tuple(labelTypes)  # Make immutable tuple
        self.propertyTypes = tuple(propertyTypes)  # Make immutable tuple
        self._typeIdentifier = tuple(typeIdentifier) if typeIdentifier else tuple()
    
    @property
    def name(self) -> Optional[str]:
        """Return the pseudo-name if type identifier is a singleton set, None otherwise"""
        if len(self._typeIdentifier) == 1:
            return self._typeIdentifier[0]
        return None
    
    @property
    def identifier(self) -> List[str]:
        """Return the type identifier as a list of label identifiers"""
        return list(self._typeIdentifier)
    
    @property
    def typeKey(self) -> Optional[List[LabelType]]:
        """Return LabelType objects for the type identifier"""
        if self._typeIdentifier:
            return [LabelType(labelId) for labelId in self._typeIdentifier]
        return None
    
    @property
    def labels(self) -> List[str]:
        """Return the label names as strings"""
        return [label.name for label in self.labelTypes]


class LabelTypeBuilder:
    """Builder for LabelType instances"""
    def __init__(self, name: str):
        self.name = name
    
    def create(self) -> LabelType:
        """Create and return the LabelType instance"""
        return LabelType(self.name)


class PropertyTypeBuilder:
    """Builder for PropertyType instances"""
    def __init__(self, name: str, datatype: str):
        self.name = name
        self.datatype = datatype
        self._not_null: bool = False
    
    def setNotNull(self, notNull: bool = True) -> 'PropertyTypeBuilder':
        """Set the not null constraint"""
        self._notNull = notNull
        return self
    
    def create(self) -> PropertyType:
        """Create and return the PropertyType instance"""
        return PropertyType(self.name, self.datatype, self._not_null)


class ContentRecordTypeBuilder:
    """Builder for ContentRecordType instances with comprehensive build/add pattern"""
    def __init__(self):
        self._labelTypes: List[LabelType] = []
        self._propertyTypes: List[PropertyType] = []
        self._typeIdentifier: Optional[List[str]] = None
    
    # Build methods - return builders for contained objects
    def buildLabelType(self, name: str) -> LabelTypeBuilder:
        """Build a label type - returns LabelTypeBuilder"""
        return LabelTypeBuilder(name)
    
    def buildPropertyType(self, name: str, datatype: str) -> PropertyTypeBuilder:
        """Build a property type - returns PropertyTypeBuilder"""
        return PropertyTypeBuilder(name, datatype)
    
    # Add methods - accept pre-built objects
    def addLabelType(self, labelType: LabelType) -> 'ContentRecordTypeBuilder':
        """Add a pre-built label type"""
        self._labelTypes.append(labelType)
        return self
    
    def addLabelTypes(self, labelTypes: List[LabelType]) -> 'ContentRecordTypeBuilder':
        """Add multiple pre-built label types"""
        self._labelTypes.extend(labelTypes)
        return self
    
    def addPropertyType(self, propertyType: PropertyType) -> 'ContentRecordTypeBuilder':
        """Add a pre-built property type"""
        self._propertyTypes.append(propertyType)
        return self
    
    def addPropertyTypes(self, propertyTypes: List[PropertyType]) -> 'ContentRecordTypeBuilder':
        """Add multiple pre-built property types"""
        self._propertyTypes.extend(propertyTypes)
        return self
    
    # Convenience methods
    def addLabel(self, label: str) -> 'ContentRecordTypeBuilder':
        """Convenience method that creates and adds LabelType"""
        return self.addLabelType(LabelType(label))
    
    def addLabels(self, labels: List[str]) -> 'ContentRecordTypeBuilder':
        """Convenience method that creates and adds multiple LabelTypes"""
        for label in labels:
            self.addLabelType(LabelType(label))
        return self
    
    def addTypeName(self, typeName: str) -> 'ContentRecordTypeBuilder':
        """Add a single type name (convenience method for singleton type identifier)"""
        return self.addTypeIdentifier([typeName])
    
    def addTypeIdentifier(self, typeIdentifier: List[str]) -> 'ContentRecordTypeBuilder':
        """Set the type identifier (key label set as strings)"""
        self._typeIdentifier = typeIdentifier
        return self
    
    def addTypeKey(self, typeIdentifier: List[str]) -> 'ContentRecordTypeBuilder':
        """Synonym for addTypeIdentifier"""
        return self.addTypeIdentifier(typeIdentifier)
    
    def addTypeKeyLabelSet(self, typeIdentifier: List[str]) -> 'ContentRecordTypeBuilder':
        """Synonym for addTypeIdentifier"""
        return self.addTypeIdentifier(typeIdentifier)
    
    def setTypeKey(self, keyLabels: List[LabelType]) -> 'ContentRecordTypeBuilder':
        """Convert LabelType objects to string identifiers"""
        typeIdentifier = [label.name for label in keyLabels]
        return self.addTypeIdentifier(typeIdentifier)
    
    def create(self) -> ContentRecordType:
        """Create and return the ContentRecordType instance"""
        return ContentRecordType(self._labelTypes, self._propertyTypes, self._typeIdentifier)


# Alias for clarity in ElementType context
RecordContentType = ContentRecordType


class ElementType(ABC):
    """Abstract base class for all element types (nodes and edges)"""
    def __init__(self, name: str, identifyingContentType: ContentRecordType):
        self.elementId = str(uuid.uuid4())  # System-generated UUID
        self.name = name
        self.identifyingContentType = identifyingContentType
    
    @abstractmethod
    def getElementKind(self) -> str:
        """Return the kind of element (node or edge)"""
        pass


class NodeType(ElementType):
    """Node type based on content record type with type interpretation support"""
    def __init__(self, contentType: ContentRecordType, interpretation: Optional[TypeInterpretation] = None):
        # NodeType name is derived from content type pseudo-name, or first identifier if available
        nodeName = contentType.name or (contentType.identifier[0] if contentType.identifier else "UnnamedNode")
        super().__init__(nodeName, contentType)
        self.contentType = contentType  # Keep for backward compatibility
        self._interpretation = interpretation or TypeInterpretation.exactlyConcrete(nodeName)
    
    @property
    def interpretation(self) -> TypeInterpretation:
        """Get the type interpretation for this node type"""
        return self._interpretation
    
    def isAbstract(self) -> bool:
        """Check if this node type is abstract (cannot be directly instantiated)"""
        return self._interpretation.isAbstract()
    
    def isConcrete(self) -> bool:
        """Check if this node type is concrete (can be directly instantiated)"""
        return self._interpretation.isConcrete()
    
    def isExactMatch(self) -> bool:
        """Check if this node type requires exact type match"""
        return self._interpretation.isExactMatch()
    
    def allowsSubtypes(self) -> bool:
        """Check if this node type allows subtypes"""
        return self._interpretation.allowsSubtypes()
    
    def getElementKind(self) -> str:
        return "node"


class NodeTypeBuilder:
    """Builder for NodeType instances with type interpretation support"""
    def __init__(self, contentType: ContentRecordType):
        self.contentType = contentType
        self._interpretation: Optional[TypeInterpretation] = None
    
    def setInterpretation(self, interpretation: TypeInterpretation) -> 'NodeTypeBuilder':
        """Set the type interpretation"""
        self._interpretation = interpretation
        return self
    
    def setAbstract(self) -> 'NodeTypeBuilder':
        """Set as abstract (subtypesOf: abstract:)"""
        nodeName = self.contentType.name or (self.contentType.identifier[0] if self.contentType.identifier else "UnnamedNode")
        self._interpretation = TypeInterpretation.subtypesAbstract(nodeName)
        return self
    
    def setConcrete(self) -> 'NodeTypeBuilder':
        """Set as concrete (exactlyOf: concrete:) - this is the default"""
        nodeName = self.contentType.name or (self.contentType.identifier[0] if self.contentType.identifier else "UnnamedNode")
        self._interpretation = TypeInterpretation.exactlyConcrete(nodeName)
        return self
    
    def create(self) -> NodeType:
        """Create and return the NodeType instance"""
        return NodeType(self.contentType, self._interpretation)


class EdgeDirection:
    """Direction specification as an ordered pair (tail_reference, head_reference)"""
    def __init__(self, tailReference: str, headReference: str):
        """
        Create a direction specification.
        
        Args:
            tailReference: Either "first" or "second" - which endpoint is the tail
            headReference: Either "first" or "second" - which endpoint is the head
        """
        if tailReference not in ("first", "second"):
            raise ValueError("tailReference must be 'first' or 'second'")
        if headReference not in ("first", "second"):
            raise ValueError("headReference must be 'first' or 'second'")
        
        self.tailReference = tailReference
        self.headReference = headReference
    
    def __repr__(self):
        return f"EdgeDirection(tail={self.tailReference}, head={self.headReference})"
    
    @classmethod
    def firstToSecond(cls):
        """Convenience method: direction from first node to second node"""
        return cls("first", "second")
    
    @classmethod
    def secondToFirst(cls):
        """Convenience method: direction from second node to first node"""
        return cls("second", "first")


class ArcType:
    """Arc type - the content type portion of an edge type"""
    def __init__(self, contentType: ContentRecordType):
        self.contentType = contentType
        # Arc name is derived from content type pseudo-name, or first identifier if available
        self.name = contentType.name or (contentType.identifier[0] if contentType.identifier else "UnnamedArc")
    
    def __repr__(self):
        return f"ArcType(name={self.name}, contentType={self.contentType})"


class ArcTypeBuilder:
    """Builder for ArcType instances"""
    def __init__(self, contentType: ContentRecordType):
        self.contentType = contentType
    
    def create(self) -> ArcType:
        """Create and return the ArcType instance"""
        return ArcType(self.contentType)


class EdgeType(ElementType):
    """Edge type with endpoint node types, direction, arc type, and component-level type interpretations"""
    def __init__(self, name: str, first_node_type: NodeType, second_node_type: NodeType, 
                 arc_type: ArcType, direction: Optional[EdgeDirection] = None,
                 interpretation: Optional[TypeInterpretation] = None,
                 fromInterpretation: Optional[TypeInterpretation] = None,
                 viaInterpretation: Optional[TypeInterpretation] = None,
                 toInterpretation: Optional[TypeInterpretation] = None):
        super().__init__(name, arc_type.contentType)
        self.first_node_type = first_node_type
        self.second_node_type = second_node_type
        self.arc_type = arc_type
        self.direction = direction
        
        # Edge-level interpretation (for the edge type itself)
        self._interpretation = interpretation or TypeInterpretation.exactlyConcrete(name)
        
        # Component-level interpretations (independent of edge-level)
        # For directed: from, via, to
        # For undirected: between, via, and
        self._fromInterpretation = fromInterpretation or TypeInterpretation.exactlyConcrete(
            first_node_type.name
        )
        self._viaInterpretation = viaInterpretation or TypeInterpretation.exactlyConcrete(
            arc_type.name
        )
        self._toInterpretation = toInterpretation or TypeInterpretation.exactlyConcrete(
            second_node_type.name
        )
        
        # Backward compatibility
        self.arc_content_type = arc_type.contentType
    
    def getElementKind(self) -> str:
        return "edge"
    
    # Edge-level interpretation methods
    @property
    def interpretation(self) -> TypeInterpretation:
        """Get the edge-level type interpretation"""
        return self._interpretation
    
    def isAbstract(self) -> bool:
        """Check if this edge type is abstract (edge-level)"""
        return self._interpretation.isAbstract()
    
    def isConcrete(self) -> bool:
        """Check if this edge type is concrete (edge-level)"""
        return self._interpretation.isConcrete()
    
    def isExactMatch(self) -> bool:
        """Check if this edge type requires exact match (edge-level)"""
        return self._interpretation.isExactMatch()
    
    def allowsSubtypes(self) -> bool:
        """Check if this edge type allows subtypes (edge-level)"""
        return self._interpretation.allowsSubtypes()
    
    # Component-level interpretation properties
    @property
    def fromInterpretation(self) -> TypeInterpretation:
        """Get interpretation for from/between component"""
        return self._fromInterpretation
    
    @property
    def viaInterpretation(self) -> TypeInterpretation:
        """Get interpretation for via/arc component"""
        return self._viaInterpretation
    
    @property
    def toInterpretation(self) -> TypeInterpretation:
        """Get interpretation for to/and component"""
        return self._toInterpretation
    
    # Aliases for undirected edges
    @property
    def betweenInterpretation(self) -> TypeInterpretation:
        """Alias for fromInterpretation (undirected: between)"""
        return self._fromInterpretation
    
    @property
    def arcInterpretation(self) -> TypeInterpretation:
        """Alias for viaInterpretation (arc synonym)"""
        return self._viaInterpretation
    
    @property
    def andInterpretation(self) -> TypeInterpretation:
        """Alias for toInterpretation (undirected: and)"""
        return self._toInterpretation
    
    # Component-specific query methods for from/between
    def fromIsAbstract(self) -> bool:
        """Check if from/between component is abstract"""
        return self._fromInterpretation.isAbstract()
    
    def fromIsConcrete(self) -> bool:
        """Check if from/between component is concrete"""
        return self._fromInterpretation.isConcrete()
    
    def fromIsExactMatch(self) -> bool:
        """Check if from/between component requires exact match"""
        return self._fromInterpretation.isExactMatch()
    
    def fromAllowsSubtypes(self) -> bool:
        """Check if from/between component allows subtypes"""
        return self._fromInterpretation.allowsSubtypes()
    
    # Component-specific query methods for via/arc
    def viaIsAbstract(self) -> bool:
        """Check if via/arc component is abstract"""
        return self._viaInterpretation.isAbstract()
    
    def viaIsConcrete(self) -> bool:
        """Check if via/arc component is concrete"""
        return self._viaInterpretation.isConcrete()
    
    def viaIsExactMatch(self) -> bool:
        """Check if via/arc component requires exact match"""
        return self._viaInterpretation.isExactMatch()
    
    def viaAllowsSubtypes(self) -> bool:
        """Check if via/arc component allows subtypes"""
        return self._viaInterpretation.allowsSubtypes()
    
    # Component-specific query methods for to/and
    def toIsAbstract(self) -> bool:
        """Check if to/and component is abstract"""
        return self._toInterpretation.isAbstract()
    
    def toIsConcrete(self) -> bool:
        """Check if to/and component is concrete"""
        return self._toInterpretation.isConcrete()
    
    def toIsExactMatch(self) -> bool:
        """Check if to/and component requires exact match"""
        return self._toInterpretation.isExactMatch()
    
    def toAllowsSubtypes(self) -> bool:
        """Check if to/and component allows subtypes"""
        return self._toInterpretation.allowsSubtypes()
    
    @property
    def isDirected(self) -> bool:
        """Check if the edge type has a direction specified"""
        return self.direction is not None
    
    @property
    def isUndirected(self) -> bool:
        """Check if the edge type has no direction specified"""
        return self.direction is None
    
    @property
    def tailNodeType(self) -> Optional[NodeType]:
        """Get the tail (source) node type for directed edges, None for undirected"""
        if not self.isDirected:
            return None
        
        if self.direction.tailReference == "first":
            return self.first_node_type
        else:
            return self.second_node_type
    
    @property
    def headNodeType(self) -> Optional[NodeType]:
        """Get the head (target) node type for directed edges, None for undirected"""
        if not self.isDirected:
            return None
        
        if self.direction.headReference == "first":
            return self.first_node_type
        else:
            return self.second_node_type
    
    @property
    def sourceType(self) -> NodeType:
        """Backward compatibility property - maps to tail for directed edges, first for undirected"""
        if self.isDirected:
            return self.tailNodeType
        return self.first_node_type
    
    @property
    def targetType(self) -> NodeType:
        """Backward compatibility property - maps to head for directed edges, second for undirected"""
        if self.isDirected:
            return self.headNodeType
        return self.second_node_type


class EdgeTypeBuilder:
    """Builder for EdgeType instances with comprehensive build/add pattern and type interpretation support"""
    def __init__(self, name: str):
        self.name = name
        self._first_node_type: Optional[NodeType] = None
        self._second_node_type: Optional[NodeType] = None
        self._arc_type: Optional[ArcType] = None
        self._direction: Optional[EdgeDirection] = None
        self._interpretation: Optional[TypeInterpretation] = None
        self._fromInterpretation: Optional[TypeInterpretation] = None
        self._viaInterpretation: Optional[TypeInterpretation] = None
        self._toInterpretation: Optional[TypeInterpretation] = None
    
    # Build methods - return builders for contained objects
    def buildFirstNodeType(self, content_type: ContentRecordType) -> NodeTypeBuilder:
        """Build the first endpoint node type - returns NodeTypeBuilder"""
        return NodeTypeBuilder(content_type)
    
    def buildSecondNodeType(self, content_type: ContentRecordType) -> NodeTypeBuilder:
        """Build the second endpoint node type - returns NodeTypeBuilder"""
        return NodeTypeBuilder(content_type)
    
    def buildArcType(self, content_type: ContentRecordType) -> ArcTypeBuilder:
        """Build the arc type - returns ArcTypeBuilder"""
        return ArcTypeBuilder(content_type)
    
    # Add methods - accept pre-built objects
    def addFirstNodeType(self, node_type: NodeType) -> 'EdgeTypeBuilder':
        """Add a pre-built first endpoint node type"""
        self._first_node_type = node_type
        return self
    
    def addSecondNodeType(self, node_type: NodeType) -> 'EdgeTypeBuilder':
        """Add a pre-built second endpoint node type"""
        self._second_node_type = node_type
        return self
    
    def addArcType(self, arc_type: ArcType) -> 'EdgeTypeBuilder':
        """Add a pre-built arc type"""
        self._arc_type = arc_type
        return self
    
    def addDirection(self, direction: EdgeDirection) -> 'EdgeTypeBuilder':
        """Add direction specification"""
        self._direction = direction
        return self
    
    def setDirected(self, tail_reference: str = "first", head_reference: str = "second") -> 'EdgeTypeBuilder':
        """Convenience method to set direction as directed"""
        self._direction = EdgeDirection(tail_reference, head_reference)
        return self
    
    def setUndirected(self) -> 'EdgeTypeBuilder':
        """Convenience method to set as undirected (no direction)"""
        self._direction = None
        return self
    
    # Edge-level interpretation methods
    def setInterpretation(self, interpretation: TypeInterpretation) -> 'EdgeTypeBuilder':
        """Set the edge-level type interpretation"""
        self._interpretation = interpretation
        return self
    
    def setAbstract(self) -> 'EdgeTypeBuilder':
        """Set edge as abstract (subtypesOf: abstract:)"""
        self._interpretation = TypeInterpretation.subtypesAbstract(self.name)
        return self
    
    def setConcrete(self) -> 'EdgeTypeBuilder':
        """Set edge as concrete (exactlyOf: concrete:) - this is the default"""
        self._interpretation = TypeInterpretation.exactlyConcrete(self.name)
        return self
    
    # Component-level interpretation methods
    def setFromInterpretation(self, interpretation: TypeInterpretation) -> 'EdgeTypeBuilder':
        """Set interpretation for from/between component"""
        self._fromInterpretation = interpretation
        return self
    
    def setViaInterpretation(self, interpretation: TypeInterpretation) -> 'EdgeTypeBuilder':
        """Set interpretation for via/arc component"""
        self._viaInterpretation = interpretation
        return self
    
    def setToInterpretation(self, interpretation: TypeInterpretation) -> 'EdgeTypeBuilder':
        """Set interpretation for to/and component"""
        self._toInterpretation = interpretation
        return self
    
    # Aliases for undirected edges
    def setBetweenInterpretation(self, interpretation: TypeInterpretation) -> 'EdgeTypeBuilder':
        """Alias for setFromInterpretation (undirected: between)"""
        return self.setFromInterpretation(interpretation)
    
    def setArcInterpretation(self, interpretation: TypeInterpretation) -> 'EdgeTypeBuilder':
        """Alias for setViaInterpretation (arc synonym)"""
        return self.setViaInterpretation(interpretation)
    
    def setAndInterpretation(self, interpretation: TypeInterpretation) -> 'EdgeTypeBuilder':
        """Alias for setToInterpretation (undirected: and)"""
        return self.setToInterpretation(interpretation)
    
    def create(self) -> EdgeType:
        """Create and return the EdgeType instance"""
        if self._first_node_type is None:
            raise ValueError("First node type must be set")
        if self._second_node_type is None:
            raise ValueError("Second node type must be set")
        if self._arc_type is None:
            raise ValueError("Arc type must be set")
        
        return EdgeType(
            name=self.name,
            first_node_type=self._first_node_type,
            second_node_type=self._second_node_type,
            arc_type=self._arc_type,
            direction=self._direction,
            interpretation=self._interpretation,
            fromInterpretation=self._fromInterpretation,
            viaInterpretation=self._viaInterpretation,
            toInterpretation=self._toInterpretation
        )


class GraphType:
    """GQL graph type with LEX constraint extensions and type interpretation support"""
    def __init__(self, name: str, allElementTypesKeyed: bool = False, 
                 interpretation: Optional[TypeInterpretation] = None):
        self.name = name
        self.nodeTypes: List[NodeType] = []
        self.edgeTypes: List[EdgeType] = []
        self.constraints: List['KeyConstraint'] = []
        self.allElementTypesKeyed = allElementTypesKeyed
        self._interpretation = interpretation or TypeInterpretation.exactlyConcrete(name)
    
    @property
    def interpretation(self) -> TypeInterpretation:
        """Get the type interpretation for this graph type"""
        return self._interpretation
    
    def isAbstract(self) -> bool:
        """Check if this graph type is abstract (cannot be directly instantiated)"""
        return self._interpretation.isAbstract()
    
    def isConcrete(self) -> bool:
        """Check if this graph type is concrete (can be directly instantiated)"""
        return self._interpretation.isConcrete()
    
    def isExactMatch(self) -> bool:
        """Check if this graph type requires exact type match"""
        return self._interpretation.isExactMatch()
    
    def allowsSubtypes(self) -> bool:
        """Check if this graph type allows subtypes"""
        return self._interpretation.allowsSubtypes()
    
    def addNodeType(self, nodeType: NodeType) -> None:
        self.nodeTypes.append(nodeType)
    
    def addEdgeType(self, edgeType: EdgeType) -> None:
        self.edgeTypes.append(edgeType)
    
    def addConstraint(self, constraint: 'KeyConstraint') -> None:
        self.constraints.append(constraint)


class GraphTypeBuilder:
    """Builder for GraphType instances with comprehensive build/add pattern"""
    def __init__(self, name: str):
        self.name = name
        self._nodeTypes: List[NodeType] = []
        self._edgeTypes: List[EdgeType] = []
        self._constraints: List['KeyConstraint'] = []
        self._allElementTypesKeyed: bool = False
    
    # Build methods - return builders for contained objects
    def buildNodeType(self, content_type: ContentRecordType) -> NodeTypeBuilder:
        """Build a node type - returns NodeTypeBuilder"""
        return NodeTypeBuilder(content_type)
    
    def buildEdgeType(self, name: str) -> EdgeTypeBuilder:
        """Build an edge type - returns EdgeTypeBuilder"""
        return EdgeTypeBuilder(name)
    
    def buildContentRecordType(self) -> ContentRecordTypeBuilder:
        """Build a content record type - returns ContentRecordTypeBuilder"""
        return ContentRecordTypeBuilder()
    
    # Add methods - accept pre-built objects
    def addNodeType(self, nodeType: NodeType) -> 'GraphTypeBuilder':
        """Add a pre-built node type"""
        self._nodeTypes.append(nodeType)
        return self
    
    def addNodeTypes(self, nodeTypes: List[NodeType]) -> 'GraphTypeBuilder':
        """Add multiple pre-built node types"""
        self._nodeTypes.extend(nodeTypes)
        return self
    
    def addEdgeType(self, edgeType: EdgeType) -> 'GraphTypeBuilder':
        """Add a pre-built edge type"""
        self._edgeTypes.append(edgeType)
        return self
    
    def addEdgeTypes(self, edgeTypes: List[EdgeType]) -> 'GraphTypeBuilder':
        """Add multiple pre-built edge types"""
        self._edgeTypes.extend(edgeTypes)
        return self
    
    def addConstraint(self, constraint: 'KeyConstraint') -> 'GraphTypeBuilder':
        """Add a constraint"""
        self._constraints.append(constraint)
        return self
    
    def setAllElementTypesKeyed(self, keyed: bool = True) -> 'GraphTypeBuilder':
        """Set the all element types keyed flag"""
        self._allElementTypesKeyed = keyed
        return self
    
    def create(self) -> GraphType:
        """Create and return the GraphType instance"""
        graph_type = GraphType(
            name=self.name,
            allElementTypesKeyed=self._allElementTypesKeyed
        )
        
        # Add all collected components
        for nodeType in self._nodeTypes:
            graph_type.addNodeType(nodeType)
        
        for edgeType in self._edgeTypes:
            graph_type.addEdgeType(edgeType)
        
        for constraint in self._constraints:
            graph_type.addConstraint(constraint)
        
        return graph_type


class Graph:
    """Graph instance conforming to a graph type"""
    def __init__(self, name: str, graph_type: GraphType):
        self.name = name
        self.graph_type = graph_type
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
    
    def insertNode(self, labels: List[str], properties: Dict[str, Any]) -> int:
        """Insert a node with labels and properties"""
        node = {
            'labels': labels,
            'properties': properties,
            'id': len(self.nodes)
        }
        self.nodes.append(node)
        return node['id']
    
    def insertEdge(self, sourceId: int, targetId: int, labels: List[str], properties: Dict[str, Any]) -> int:
        """Insert an edge between nodes"""
        edge = {
            'source_id': sourceId,
            'target_id': targetId,
            'labels': labels,
            'properties': properties,
            'id': len(self.edges)
        }
        self.edges.append(edge)
        return edge['id']