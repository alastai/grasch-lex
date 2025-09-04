"""
Type system for content record types, element types, and graph types.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum
import uuid


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
    def __init__(self, name: str, datatype: str, not_null: bool = False):
        super().__init__(name, datatype)
        self.not_null = not_null


class ContentRecordType:
    """Hierarchical record structure with label types and property structure"""
    def __init__(self, label_types: List[LabelType], property_types: List[PropertyType], type_identifier: Optional[List[str]] = None):
        self.label_types = tuple(label_types)  # Make immutable tuple
        self.property_types = tuple(property_types)  # Make immutable tuple
        self._type_identifier = tuple(type_identifier) if type_identifier else tuple()
    
    @property
    def name(self) -> Optional[str]:
        """Return the pseudo-name if type identifier is a singleton set, None otherwise"""
        if len(self._type_identifier) == 1:
            return self._type_identifier[0]
        return None
    
    @property
    def identifier(self) -> List[str]:
        """Return the type identifier as a list of label identifiers"""
        return list(self._type_identifier)
    
    @property
    def type_key(self) -> Optional[List[LabelType]]:
        """Backward compatibility: return LabelType objects for the type identifier"""
        if self._type_identifier:
            return [LabelType(label_id) for label_id in self._type_identifier]
        return None
    
    @property
    def labels(self) -> List[str]:
        """Return the label names as strings"""
        return [label.name for label in self.label_types]


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
    
    def setNotNull(self, not_null: bool = True) -> 'PropertyTypeBuilder':
        """Set the not null constraint"""
        self._not_null = not_null
        return self
    
    def create(self) -> PropertyType:
        """Create and return the PropertyType instance"""
        return PropertyType(self.name, self.datatype, self._not_null)


class ContentRecordTypeBuilder:
    """Builder for ContentRecordType instances with comprehensive build/add pattern"""
    def __init__(self):
        self._label_types: List[LabelType] = []
        self._property_types: List[PropertyType] = []
        self._type_identifier: Optional[List[str]] = None
    
    # Build methods - return builders for contained objects
    def buildLabelType(self, name: str) -> LabelTypeBuilder:
        """Build a label type - returns LabelTypeBuilder"""
        return LabelTypeBuilder(name)
    
    def buildPropertyType(self, name: str, datatype: str) -> PropertyTypeBuilder:
        """Build a property type - returns PropertyTypeBuilder"""
        return PropertyTypeBuilder(name, datatype)
    
    # Add methods - accept pre-built objects
    def addLabelType(self, label_type: LabelType) -> 'ContentRecordTypeBuilder':
        """Add a pre-built label type"""
        self._label_types.append(label_type)
        return self
    
    def addLabelTypes(self, label_types: List[LabelType]) -> 'ContentRecordTypeBuilder':
        """Add multiple pre-built label types"""
        self._label_types.extend(label_types)
        return self
    
    def addPropertyType(self, property_type: PropertyType) -> 'ContentRecordTypeBuilder':
        """Add a pre-built property type"""
        self._property_types.append(property_type)
        return self
    
    def addPropertyTypes(self, property_types: List[PropertyType]) -> 'ContentRecordTypeBuilder':
        """Add multiple pre-built property types"""
        self._property_types.extend(property_types)
        return self
    
    # Convenience methods for backward compatibility
    def add_label_type(self, label_type: LabelType) -> 'ContentRecordTypeBuilder':
        """Backward compatibility: add a label type"""
        return self.addLabelType(label_type)
    
    def add_label_types(self, label_types: List[LabelType]) -> 'ContentRecordTypeBuilder':
        """Backward compatibility: add multiple label types"""
        return self.addLabelTypes(label_types)
    
    def add_label(self, label: str) -> 'ContentRecordTypeBuilder':
        """Convenience method that creates and adds LabelType"""
        return self.addLabelType(LabelType(label))
    
    def add_labels(self, labels: List[str]) -> 'ContentRecordTypeBuilder':
        """Convenience method that creates and adds multiple LabelTypes"""
        for label in labels:
            self.addLabelType(LabelType(label))
        return self
    
    def add_property_type(self, property_type: PropertyType) -> 'ContentRecordTypeBuilder':
        """Backward compatibility: add a property type"""
        return self.addPropertyType(property_type)
    
    def add_type_name(self, type_name: str) -> 'ContentRecordTypeBuilder':
        """Add a single type name (convenience method for singleton type identifier)"""
        return self.addTypeIdentifier([type_name])
    
    def addTypeIdentifier(self, type_identifier: List[str]) -> 'ContentRecordTypeBuilder':
        """Set the type identifier (key label set as strings)"""
        self._type_identifier = type_identifier
        return self
    
    def add_type_identifier(self, type_identifier: List[str]) -> 'ContentRecordTypeBuilder':
        """Backward compatibility: set type identifier"""
        return self.addTypeIdentifier(type_identifier)
    
    def add_type_key(self, type_identifier: List[str]) -> 'ContentRecordTypeBuilder':
        """Synonym for add_type_identifier"""
        return self.addTypeIdentifier(type_identifier)
    
    def add_type_key_label_set(self, type_identifier: List[str]) -> 'ContentRecordTypeBuilder':
        """Synonym for add_type_identifier"""
        return self.addTypeIdentifier(type_identifier)
    
    def set_type_key(self, key_labels: List[LabelType]) -> 'ContentRecordTypeBuilder':
        """Backward compatibility: convert LabelType objects to string identifiers"""
        type_identifier = [label.name for label in key_labels]
        return self.addTypeIdentifier(type_identifier)
    
    def create(self) -> ContentRecordType:
        """Create and return the ContentRecordType instance"""
        return ContentRecordType(self._label_types, self._property_types, self._type_identifier)


# Alias for clarity in ElementType context
RecordContentType = ContentRecordType


class ElementType(ABC):
    """Abstract base class for all element types (nodes and edges)"""
    def __init__(self, name: str, identifying_content_type: ContentRecordType):
        self.element_id = str(uuid.uuid4())  # System-generated UUID
        self.name = name
        self.identifying_content_type = identifying_content_type
    
    @abstractmethod
    def get_element_kind(self) -> str:
        """Return the kind of element (node or edge)"""
        pass


class NodeType(ElementType):
    """Node type based on content record type"""
    def __init__(self, content_type: ContentRecordType):
        # NodeType name is derived from content type pseudo-name, or first identifier if available
        node_name = content_type.name or (content_type.identifier[0] if content_type.identifier else "UnnamedNode")
        super().__init__(node_name, content_type)
        self.content_type = content_type  # Keep for backward compatibility
    
    def get_element_kind(self) -> str:
        return "node"


class NodeTypeBuilder:
    """Builder for NodeType instances"""
    def __init__(self, content_type: ContentRecordType):
        self.content_type = content_type
    
    def create(self) -> NodeType:
        """Create and return the NodeType instance"""
        return NodeType(self.content_type)


class EdgeDirection:
    """Direction specification as an ordered pair (tail_reference, head_reference)"""
    def __init__(self, tail_reference: str, head_reference: str):
        """
        Create a direction specification.
        
        Args:
            tail_reference: Either "first" or "second" - which endpoint is the tail
            head_reference: Either "first" or "second" - which endpoint is the head
        """
        if tail_reference not in ("first", "second"):
            raise ValueError("tail_reference must be 'first' or 'second'")
        if head_reference not in ("first", "second"):
            raise ValueError("head_reference must be 'first' or 'second'")
        
        self.tail_reference = tail_reference
        self.head_reference = head_reference
    
    def __repr__(self):
        return f"EdgeDirection(tail={self.tail_reference}, head={self.head_reference})"
    
    @classmethod
    def first_to_second(cls):
        """Convenience method: direction from first node to second node"""
        return cls("first", "second")
    
    @classmethod
    def second_to_first(cls):
        """Convenience method: direction from second node to first node"""
        return cls("second", "first")


class ArcType:
    """Arc type - the content type portion of an edge type"""
    def __init__(self, content_type: ContentRecordType):
        self.content_type = content_type
        # Arc name is derived from content type pseudo-name, or first identifier if available
        self.name = content_type.name or (content_type.identifier[0] if content_type.identifier else "UnnamedArc")
    
    def __repr__(self):
        return f"ArcType(name={self.name}, content_type={self.content_type})"


class ArcTypeBuilder:
    """Builder for ArcType instances"""
    def __init__(self, content_type: ContentRecordType):
        self.content_type = content_type
    
    def create(self) -> ArcType:
        """Create and return the ArcType instance"""
        return ArcType(self.content_type)


class EdgeType(ElementType):
    """Edge type with endpoint node types, direction, and arc type"""
    def __init__(self, name: str, first_node_type: NodeType, second_node_type: NodeType, 
                 arc_type: ArcType, direction: Optional[EdgeDirection] = None):
        super().__init__(name, arc_type.content_type)
        self.first_node_type = first_node_type
        self.second_node_type = second_node_type
        self.arc_type = arc_type
        self.direction = direction
        
        # Backward compatibility
        self.arc_content_type = arc_type.content_type
    
    def get_element_kind(self) -> str:
        return "edge"
    
    @property
    def is_directed(self) -> bool:
        """Check if the edge type has a direction specified"""
        return self.direction is not None
    
    @property
    def is_undirected(self) -> bool:
        """Check if the edge type has no direction specified"""
        return self.direction is None
    
    @property
    def tail_node_type(self) -> Optional[NodeType]:
        """Get the tail (source) node type for directed edges, None for undirected"""
        if not self.is_directed:
            return None
        
        if self.direction.tail_reference == "first":
            return self.first_node_type
        else:
            return self.second_node_type
    
    @property
    def head_node_type(self) -> Optional[NodeType]:
        """Get the head (target) node type for directed edges, None for undirected"""
        if not self.is_directed:
            return None
        
        if self.direction.head_reference == "first":
            return self.first_node_type
        else:
            return self.second_node_type
    
    @property
    def source_type(self) -> NodeType:
        """Backward compatibility property - maps to tail for directed edges, first for undirected"""
        if self.is_directed:
            return self.tail_node_type
        return self.first_node_type
    
    @property
    def target_type(self) -> NodeType:
        """Backward compatibility property - maps to head for directed edges, second for undirected"""
        if self.is_directed:
            return self.head_node_type
        return self.second_node_type


class EdgeTypeBuilder:
    """Builder for EdgeType instances with comprehensive build/add pattern"""
    def __init__(self, name: str):
        self.name = name
        self._first_node_type: Optional[NodeType] = None
        self._second_node_type: Optional[NodeType] = None
        self._arc_type: Optional[ArcType] = None
        self._direction: Optional[EdgeDirection] = None
    
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
            direction=self._direction
        )


class GraphType:
    """GQL graph type with LEX constraint extensions"""
    def __init__(self, name: str, all_element_types_keyed: bool = False):
        self.name = name
        self.node_types: List[NodeType] = []
        self.edge_types: List[EdgeType] = []
        self.constraints: List['KeyConstraint'] = []
        self.all_element_types_keyed = all_element_types_keyed
    
    def add_node_type(self, node_type: NodeType):
        self.node_types.append(node_type)
    
    def add_edge_type(self, edge_type: EdgeType):
        self.edge_types.append(edge_type)
    
    def add_constraint(self, constraint: 'KeyConstraint'):
        self.constraints.append(constraint)


class GraphTypeBuilder:
    """Builder for GraphType instances with comprehensive build/add pattern"""
    def __init__(self, name: str):
        self.name = name
        self._node_types: List[NodeType] = []
        self._edge_types: List[EdgeType] = []
        self._constraints: List['KeyConstraint'] = []
        self._all_element_types_keyed: bool = False
    
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
    def addNodeType(self, node_type: NodeType) -> 'GraphTypeBuilder':
        """Add a pre-built node type"""
        self._node_types.append(node_type)
        return self
    
    def addNodeTypes(self, node_types: List[NodeType]) -> 'GraphTypeBuilder':
        """Add multiple pre-built node types"""
        self._node_types.extend(node_types)
        return self
    
    def addEdgeType(self, edge_type: EdgeType) -> 'GraphTypeBuilder':
        """Add a pre-built edge type"""
        self._edge_types.append(edge_type)
        return self
    
    def addEdgeTypes(self, edge_types: List[EdgeType]) -> 'GraphTypeBuilder':
        """Add multiple pre-built edge types"""
        self._edge_types.extend(edge_types)
        return self
    
    def addConstraint(self, constraint: 'KeyConstraint') -> 'GraphTypeBuilder':
        """Add a constraint"""
        self._constraints.append(constraint)
        return self
    
    def setAllElementTypesKeyed(self, keyed: bool = True) -> 'GraphTypeBuilder':
        """Set the all element types keyed flag"""
        self._all_element_types_keyed = keyed
        return self
    
    def create(self) -> GraphType:
        """Create and return the GraphType instance"""
        graph_type = GraphType(
            name=self.name,
            all_element_types_keyed=self._all_element_types_keyed
        )
        
        # Add all collected components
        for node_type in self._node_types:
            graph_type.add_node_type(node_type)
        
        for edge_type in self._edge_types:
            graph_type.add_edge_type(edge_type)
        
        for constraint in self._constraints:
            graph_type.add_constraint(constraint)
        
        return graph_type


class Graph:
    """Graph instance conforming to a graph type"""
    def __init__(self, name: str, graph_type: GraphType):
        self.name = name
        self.graph_type = graph_type
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
    
    def insert_node(self, labels: List[str], properties: Dict[str, Any]):
        """Insert a node with labels and properties"""
        node = {
            'labels': labels,
            'properties': properties,
            'id': len(self.nodes)
        }
        self.nodes.append(node)
        return node['id']
    
    def insert_edge(self, source_id: int, target_id: int, labels: List[str], properties: Dict[str, Any]):
        """Insert an edge between nodes"""
        edge = {
            'source_id': source_id,
            'target_id': target_id,
            'labels': labels,
            'properties': properties,
            'id': len(self.edges)
        }
        self.edges.append(edge)
        return edge['id']