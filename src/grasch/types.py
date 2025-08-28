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
        super().__init__(name, "LABEL_TYPE")


class PropertyType(AttributeType):
    """Property type with GQL datatypes"""
    def __init__(self, name: str, datatype: str, not_null: bool = False):
        super().__init__(name, datatype)
        self.not_null = not_null


class ContentRecordType:
    """Hierarchical record structure with label types and property structure"""
    def __init__(self, name: str, label_types: List[LabelType], property_types: List[PropertyType], type_key: Optional[List[LabelType]] = None):
        self.name = name
        self.label_types = tuple(label_types)  # Make immutable tuple
        self.property_types = tuple(property_types)  # Make immutable tuple
        self.type_key = tuple(type_key) if type_key else None


class ContentRecordTypeBuilder:
    """Builder for ContentRecordType instances"""
    def __init__(self, name: str):
        self.name = name
        self._label_types: List[LabelType] = []
        self._property_types: List[PropertyType] = []
        self._type_key: Optional[List[LabelType]] = None
    
    def add_label_type(self, label_type: LabelType) -> 'ContentRecordTypeBuilder':
        """Add a label type and return self for chaining"""
        self._label_types.append(label_type)
        return self
    
    def add_property_type(self, property_type: PropertyType) -> 'ContentRecordTypeBuilder':
        """Add a property type and return self for chaining"""
        self._property_types.append(property_type)
        return self
    
    def set_type_key(self, key_labels: List[LabelType]) -> 'ContentRecordTypeBuilder':
        """Set the type key and return self for chaining"""
        self._type_key = key_labels
        return self
    
    def create(self) -> ContentRecordType:
        """Create and return the ContentRecordType instance"""
        return ContentRecordType(self.name, self._label_types, self._property_types, self._type_key)


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
        # NodeType name is derived from content type, no user input needed
        super().__init__(content_type.name, content_type)
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


class EdgeType(ElementType):
    """Edge type with endpoint node types, direction, and arc content type"""
    def __init__(self, name: str, first_node_type: NodeType, second_node_type: NodeType, 
                 arc_content_type: ContentRecordType, direction: Optional[EdgeDirection] = None):
        super().__init__(name, arc_content_type)
        self.first_node_type = first_node_type
        self.second_node_type = second_node_type
        self.arc_content_type = arc_content_type  # Keep for backward compatibility
        self.direction = direction
    
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