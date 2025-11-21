#!/usr/bin/env python3
"""
Tests for element type classes with TypeInterpretation support.
Tests NodeType, EdgeType (with undirected support), and GraphType (with collection-level interpretations).
"""

import pytest
from src.grasch.types import (
    NodeType, EdgeType, GraphType, ArcType, EdgeDirection,
    ContentRecordType, NodeTypeBuilder, EdgeTypeBuilder, GraphTypeBuilder
)
from src.grasch.type_interpretation import TypeInterpretation


class TestNodeTypeInterpretation:
    """Tests for NodeType with TypeInterpretation support."""
    
    def test_default_interpretation(self):
        """Test default interpretation for NodeType."""
        content_type = ContentRecordType([], [], ['Person'])
        node_type = NodeType(content_type)
        
        # Should have default exactlyOf: concrete: interpretation
        assert node_type.interpretation.typeReference == "Person"
        assert node_type.isExactMatch() is True
        assert node_type.isConcrete() is True
        assert node_type.isAbstract() is False
        assert node_type.allowsSubtypes() is False
    
    def test_custom_interpretation(self):
        """Test setting custom interpretation."""
        content_type = ContentRecordType([], [], ['Vehicle'])
        interp = TypeInterpretation.subtypesAbstract("Vehicle")
        node_type = NodeType(content_type, interpretation=interp)
        
        assert node_type.interpretation == interp
        assert node_type.allowsSubtypes() is True
        assert node_type.isAbstract() is True
        assert node_type.isExactMatch() is False
        assert node_type.isConcrete() is False
    
    def test_builder_with_interpretation(self):
        """Test NodeTypeBuilder with interpretation."""
        content_type = ContentRecordType([], [], ['Employee'])
        
        # Build with abstract interpretation
        node_type = (NodeTypeBuilder(content_type)
                     .setAbstract()
                     .create())
        
        assert node_type.isAbstract() is True
        assert node_type.allowsSubtypes() is True


class TestEdgeTypeInterpretation:
    """Tests for EdgeType with TypeInterpretation support including undirected edges."""
    
    def test_default_interpretation(self):
        """Test default interpretation for EdgeType."""
        person_content = ContentRecordType([], [], ['Person'])
        knows_content = ContentRecordType([], [], ['KNOWS'])
        
        person_node = NodeType(person_content)
        knows_arc = ArcType(knows_content)
        
        edge_type = EdgeType(
            'KNOWS',
            person_node,
            person_node,
            knows_arc,
            EdgeDirection.firstToSecond()
        )
        
        # Should have default exactlyOf: concrete: interpretation
        assert edge_type.interpretation.typeReference == "KNOWS"
        assert edge_type.isExactMatch() is True
        assert edge_type.isConcrete() is True
    
    def test_component_level_interpretations(self):
        """Test component-level interpretations for directed edges."""
        person_content = ContentRecordType([], [], ['Person'])
        manages_content = ContentRecordType([], [], ['MANAGES'])
        
        person_node = NodeType(person_content)
        manages_arc = ArcType(manages_content)
        
        edge_type = EdgeType(
            'MANAGES',
            person_node,
            person_node,
            manages_arc,
            EdgeDirection.firstToSecond(),
            fromInterpretation=TypeInterpretation.subtypesAbstract('Person'),
            viaInterpretation=TypeInterpretation.exactlyConcrete('MANAGES'),
            toInterpretation=TypeInterpretation.exactlyConcrete('Person')
        )
        
        # Test from component
        assert edge_type.fromInterpretation.typeReference == 'Person'
        assert edge_type.fromIsAbstract() is True
        assert edge_type.fromAllowsSubtypes() is True
        assert edge_type.fromIsExactMatch() is False
        assert edge_type.fromIsConcrete() is False
        
        # Test via component
        assert edge_type.viaInterpretation.typeReference == 'MANAGES'
        assert edge_type.viaIsConcrete() is True
        assert edge_type.viaIsExactMatch() is True
        assert edge_type.viaIsAbstract() is False
        assert edge_type.viaAllowsSubtypes() is False
        
        # Test to component
        assert edge_type.toInterpretation.typeReference == 'Person'
        assert edge_type.toIsConcrete() is True
        assert edge_type.toIsExactMatch() is True
        assert edge_type.toIsAbstract() is False
        assert edge_type.toAllowsSubtypes() is False
    
    def test_undirected_edge_aliases(self):
        """Test undirected edge aliases (between, arc, and)."""
        person_content = ContentRecordType([], [], ['Person'])
        friend_content = ContentRecordType([], [], ['FRIEND'])
        
        person_node = NodeType(person_content)
        friend_arc = ArcType(friend_content)
        
        # Create undirected edge (no direction specified)
        edge_type = EdgeType(
            'FRIEND',
            person_node,
            person_node,
            friend_arc,
            None,  # No direction = undirected
            fromInterpretation=TypeInterpretation.subtypesAbstract('Person'),
            viaInterpretation=TypeInterpretation.exactlyConcrete('FRIEND'),
            toInterpretation=TypeInterpretation.subtypesAbstract('Person')
        )
        
        # Test that edge is undirected
        assert edge_type.isUndirected is True
        assert edge_type.isDirected is False
        
        # Test undirected aliases work
        assert edge_type.betweenInterpretation == edge_type.fromInterpretation
        assert edge_type.arcInterpretation == edge_type.viaInterpretation
        assert edge_type.andInterpretation == edge_type.toInterpretation
        
        # Verify the interpretations through aliases
        assert edge_type.betweenInterpretation.isAbstract() is True
        assert edge_type.arcInterpretation.isConcrete() is True
        assert edge_type.andInterpretation.allowsSubtypes() is True
    
    def test_directed_vs_undirected(self):
        """Test directed vs undirected edge properties."""
        person_content = ContentRecordType([], [], ['Person'])
        arc_content = ContentRecordType([], [], ['EDGE'])
        
        person_node = NodeType(person_content)
        arc = ArcType(arc_content)
        
        # Directed edge
        directed_edge = EdgeType(
            'DIRECTED',
            person_node,
            person_node,
            arc,
            EdgeDirection.firstToSecond()
        )
        
        assert directed_edge.isDirected is True
        assert directed_edge.isUndirected is False
        assert directed_edge.tailNodeType is not None
        assert directed_edge.headNodeType is not None
        
        # Undirected edge
        undirected_edge = EdgeType(
            'UNDIRECTED',
            person_node,
            person_node,
            arc,
            None
        )
        
        assert undirected_edge.isDirected is False
        assert undirected_edge.isUndirected is True
        assert undirected_edge.tailNodeType is None
        assert undirected_edge.headNodeType is None
    
    def test_component_interpretations_independence(self):
        """Test that component interpretations are independent of edge-level interpretation."""
        person_content = ContentRecordType([], [], ['Person'])
        supervises_content = ContentRecordType([], [], ['SUPERVISES'])
        
        person_node = NodeType(person_content)
        supervises_arc = ArcType(supervises_content)
        
        # Edge-level is abstract, but components have different interpretations
        edge_type = EdgeType(
            'SUPERVISES',
            person_node,
            person_node,
            supervises_arc,
            EdgeDirection.firstToSecond(),
            interpretation=TypeInterpretation.subtypesAbstract('SUPERVISES'),
            fromInterpretation=TypeInterpretation.exactlyConcrete('Manager'),
            viaInterpretation=TypeInterpretation.exactlyConcrete('SUPERVISES'),
            toInterpretation=TypeInterpretation.subtypesAbstract('Employee')
        )
        
        # Edge-level is abstract
        assert edge_type.isAbstract() is True
        assert edge_type.allowsSubtypes() is True
        
        # But components have independent interpretations
        assert edge_type.fromIsConcrete() is True
        assert edge_type.fromIsExactMatch() is True
        
        assert edge_type.viaIsConcrete() is True
        assert edge_type.viaIsExactMatch() is True
        
        assert edge_type.toIsAbstract() is True
        assert edge_type.toAllowsSubtypes() is True


class TestGraphTypeInterpretation:
    """Tests for GraphType with TypeInterpretation support including collection-level interpretations."""
    
    def test_default_interpretation(self):
        """Test default interpretation for GraphType."""
        graph_type = GraphType('SocialNetwork')
        
        # Should have default exactlyOf: concrete: interpretation
        assert graph_type.interpretation.typeReference == 'SocialNetwork'
        assert graph_type.isExactMatch() is True
        assert graph_type.isConcrete() is True
        assert graph_type.isAbstract() is False
        assert graph_type.allowsSubtypes() is False
    
    def test_custom_interpretation(self):
        """Test setting custom interpretation."""
        interp = TypeInterpretation.subtypesAbstract('BaseGraph')
        graph_type = GraphType('BaseGraph', interpretation=interp)
        
        assert graph_type.interpretation == interp
        assert graph_type.allowsSubtypes() is True
        assert graph_type.isAbstract() is True
    
    def test_collection_level_interpretations(self):
        """Test collection-level interpretations for nodeTypes and edgeTypes."""
        node_types_interp = TypeInterpretation.subtypesAbstract('NodeTypes')
        edge_types_interp = TypeInterpretation.exactlyConcrete('EdgeTypes')
        
        graph_type = GraphType(
            'ComplexGraph',
            nodeTypesInterpretation=node_types_interp,
            edgeTypesInterpretation=edge_types_interp
        )
        
        # Verify collection interpretations
        assert graph_type.nodeTypesInterpretation == node_types_interp
        assert graph_type.nodeTypesInterpretation.allowsSubtypes() is True
        assert graph_type.nodeTypesInterpretation.isAbstract() is True
        
        assert graph_type.edgeTypesInterpretation == edge_types_interp
        assert graph_type.edgeTypesInterpretation.isExactMatch() is True
        assert graph_type.edgeTypesInterpretation.isConcrete() is True
    
    def test_collection_interpretations_can_be_none(self):
        """Test that collection interpretations can be None."""
        graph_type = GraphType('SimpleGraph')
        
        assert graph_type.nodeTypesInterpretation is None
        assert graph_type.edgeTypesInterpretation is None
    
    def test_collection_interpretations_setters(self):
        """Test setting collection interpretations after creation."""
        graph_type = GraphType('MutableGraph')
        
        # Initially None
        assert graph_type.nodeTypesInterpretation is None
        assert graph_type.edgeTypesInterpretation is None
        
        # Set interpretations
        node_interp = TypeInterpretation.subtypesAbstract('Nodes')
        edge_interp = TypeInterpretation.exactlyConcrete('Edges')
        
        graph_type.nodeTypesInterpretation = node_interp
        graph_type.edgeTypesInterpretation = edge_interp
        
        # Verify they were set
        assert graph_type.nodeTypesInterpretation == node_interp
        assert graph_type.edgeTypesInterpretation == edge_interp
    
    def test_builder_with_interpretations(self):
        """Test GraphTypeBuilder with all interpretation levels."""
        builder = GraphTypeBuilder('TestGraph')
        
        # Set graph-level interpretation
        builder.setAbstract()
        
        # Set collection-level interpretations
        builder.setNodeTypesInterpretation(
            TypeInterpretation.subtypesAbstract('AbstractNodes')
        )
        builder.setEdgeTypesInterpretation(
            TypeInterpretation.exactlyConcrete('ConcreteEdges')
        )
        
        graph_type = builder.create()
        
        # Verify graph-level interpretation
        assert graph_type.isAbstract() is True
        assert graph_type.allowsSubtypes() is True
        
        # Verify collection-level interpretations
        assert graph_type.nodeTypesInterpretation is not None
        assert graph_type.nodeTypesInterpretation.isAbstract() is True
        
        assert graph_type.edgeTypesInterpretation is not None
        assert graph_type.edgeTypesInterpretation.isConcrete() is True
    
    def test_collection_interpretations_independence(self):
        """Test that collection interpretations are independent of graph-level interpretation."""
        graph_type = GraphType(
            'MixedGraph',
            interpretation=TypeInterpretation.exactlyConcrete('MixedGraph'),
            nodeTypesInterpretation=TypeInterpretation.subtypesAbstract('AbstractNodes'),
            edgeTypesInterpretation=TypeInterpretation.subtypesConcrete('ConcreteEdges')
        )
        
        # Graph-level is exact match and concrete
        assert graph_type.isExactMatch() is True
        assert graph_type.isConcrete() is True
        
        # But nodeTypes collection allows subtypes and is abstract
        assert graph_type.nodeTypesInterpretation.allowsSubtypes() is True
        assert graph_type.nodeTypesInterpretation.isAbstract() is True
        
        # And edgeTypes collection allows subtypes but is concrete
        assert graph_type.edgeTypesInterpretation.allowsSubtypes() is True
        assert graph_type.edgeTypesInterpretation.isConcrete() is True


class TestIntegrationScenarios:
    """Integration tests combining NodeType, EdgeType, and GraphType with interpretations."""
    
    def test_complete_graph_with_all_interpretation_levels(self):
        """Test a complete graph with interpretations at all levels."""
        # Create content types
        person_content = ContentRecordType([], [], ['Person'])
        employee_content = ContentRecordType([], [], ['Employee'])
        manages_content = ContentRecordType([], [], ['MANAGES'])
        
        # Create node types with interpretations
        person_node = NodeType(
            person_content,
            interpretation=TypeInterpretation.subtypesAbstract('Person')
        )
        employee_node = NodeType(
            employee_content,
            interpretation=TypeInterpretation.exactlyConcrete('Employee')
        )
        
        # Create edge type with component-level interpretations
        manages_arc = ArcType(manages_content)
        manages_edge = EdgeType(
            'MANAGES',
            employee_node,
            person_node,
            manages_arc,
            EdgeDirection.firstToSecond(),
            interpretation=TypeInterpretation.exactlyConcrete('MANAGES'),
            fromInterpretation=TypeInterpretation.exactlyConcrete('Employee'),
            viaInterpretation=TypeInterpretation.exactlyConcrete('MANAGES'),
            toInterpretation=TypeInterpretation.subtypesAbstract('Person')
        )
        
        # Create graph type with collection-level interpretations
        graph_type = GraphType(
            'OrgChart',
            interpretation=TypeInterpretation.exactlyConcrete('OrgChart'),
            nodeTypesInterpretation=TypeInterpretation.subtypesAbstract('OrgNodes'),
            edgeTypesInterpretation=TypeInterpretation.exactlyConcrete('OrgEdges')
        )
        
        graph_type.addNodeType(person_node)
        graph_type.addNodeType(employee_node)
        graph_type.addEdgeType(manages_edge)
        
        # Verify graph-level interpretation
        assert graph_type.isExactMatch() and graph_type.isConcrete()
        
        # Verify collection-level interpretations
        assert graph_type.nodeTypesInterpretation.allowsSubtypes()
        assert graph_type.nodeTypesInterpretation.isAbstract()
        assert graph_type.edgeTypesInterpretation.isExactMatch()
        assert graph_type.edgeTypesInterpretation.isConcrete()
        
        # Verify node type interpretations
        assert person_node.allowsSubtypes() and person_node.isAbstract()
        assert employee_node.isExactMatch() and employee_node.isConcrete()
        
        # Verify edge type interpretations
        assert manages_edge.isExactMatch() and manages_edge.isConcrete()
        assert manages_edge.fromIsExactMatch() and manages_edge.fromIsConcrete()
        assert manages_edge.viaIsExactMatch() and manages_edge.viaIsConcrete()
        assert manages_edge.toAllowsSubtypes() and manages_edge.toIsAbstract()
    
    def test_undirected_edge_in_graph(self):
        """Test undirected edges with interpretations in a graph."""
        person_content = ContentRecordType([], [], ['Person'])
        friend_content = ContentRecordType([], [], ['FRIEND'])
        
        person_node = NodeType(person_content)
        friend_arc = ArcType(friend_content)
        
        # Create undirected friendship edge
        friend_edge = EdgeType(
            'FRIEND',
            person_node,
            person_node,
            friend_arc,
            None,  # Undirected
            fromInterpretation=TypeInterpretation.subtypesAbstract('Person'),
            viaInterpretation=TypeInterpretation.exactlyConcrete('FRIEND'),
            toInterpretation=TypeInterpretation.subtypesAbstract('Person')
        )
        
        graph_type = GraphType('SocialNetwork')
        graph_type.addNodeType(person_node)
        graph_type.addEdgeType(friend_edge)
        
        # Verify undirected edge properties
        assert friend_edge.isUndirected is True
        assert friend_edge.isDirected is False
        
        # Verify aliases work
        assert friend_edge.betweenInterpretation.allowsSubtypes() is True
        assert friend_edge.arcInterpretation.isExactMatch() is True
        assert friend_edge.andInterpretation.allowsSubtypes() is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
