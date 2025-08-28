"""
Type system for content record types, element types, and graph types.
"""

from typing import List, Dict, Any, Optional


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
    def __init__(self, name: str):
        self.name = name
        self.label_types: List[LabelType] = []
        self.property_types: List[PropertyType] = []
        self.type_key: Optional[List[LabelType]] = None
    
    def add_label_type(self, label_type: LabelType):
        self.label_types.append(label_type)
    
    def add_property_type(self, property_type: PropertyType):
        self.property_types.append(property_type)
    
    def set_type_key(self, key_labels: List[LabelType]):
        self.type_key = key_labels


class NodeType:
    """Node type based on content record type"""
    def __init__(self, name: str, content_type: ContentRecordType):
        self.name = name
        self.content_type = content_type


class EdgeType:
    """Edge type with source/target node types and arc content type"""
    def __init__(self, name: str, source_type: NodeType, target_type: NodeType, arc_content_type: ContentRecordType):
        self.name = name
        self.source_type = source_type
        self.target_type = target_type
        self.arc_content_type = arc_content_type


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