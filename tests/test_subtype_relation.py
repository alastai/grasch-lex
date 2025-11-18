"""
Test subtype relation properties (Armstrong's Axioms)
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.grasch.api.builders import (
    GraphTypeBuilder, NodeTypeBuilder, EdgeTypeBuilder,
    NodeTypesBuilder, EdgeTypesBuilder, TypeInterpretationBuilder
)


def build_graph_type(node_types_list, edge_types_list):
    """Helper to build GraphType from lists of NodeType and EdgeType objects"""
    node_interp = TypeInterpretationBuilder("exact")
    for nt in node_types_list:
        node_interp.addType(nt)
    node_types = NodeTypesBuilder().addInterpretation(node_interp.build()).build()
    
    edge_interp = TypeInterpretationBuilder("exact")
    for et in edge_types_list:
        edge_interp.addType(et)
    edge_types = EdgeTypesBuilder().addInterpretation(edge_interp.build()).build()
    
    return GraphTypeBuilder().withNodeTypes(node_types).withEdgeTypes(edge_types).build()


def test_reflexive_property():
    """Test that every type is a subtype of itself (reflexive)"""
    # Create a node type
    person = NodeTypeBuilder("Person").build()
    
    # Create graph type with the node type (need at least one edge type)
    dummy_edge = EdgeTypeBuilder("DUMMY", "Person", "Person").build()
    graph_type = build_graph_type([person], [dummy_edge])
    
    # Reflexive: Person <: Person
    assert person.isSubtypeOf("Person", graph_type)


def test_transitive_property():
    """Test that subtype relation is transitive"""
    # Create type hierarchy: Entity -> Person -> Employee
    entity = NodeTypeBuilder("Entity").build()
    person = NodeTypeBuilder("Person").withSupertypes(["Entity"]).build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    
    dummy_edge = EdgeTypeBuilder("DUMMY", "Entity", "Entity").build()
    graph_type = build_graph_type([entity, person, employee], [dummy_edge])
    
    # Direct subtype: Person <: Entity
    assert person.isSubtypeOf("Entity", graph_type)
    
    # Direct subtype: Employee <: Person
    assert employee.isSubtypeOf("Person", graph_type)
    
    # Transitive: Employee <: Entity (through Person)
    assert employee.isSubtypeOf("Entity", graph_type)


def test_not_subtype():
    """Test that unrelated types are not subtypes"""
    person = NodeTypeBuilder("Person").build()
    company = NodeTypeBuilder("Company").build()
    
    dummy_edge = EdgeTypeBuilder("DUMMY", "Person", "Person").build()
    graph_type = build_graph_type([person, company], [dummy_edge])
    
    # Person is not a subtype of Company
    assert not person.isSubtypeOf("Company", graph_type)
    
    # Company is not a subtype of Person
    assert not company.isSubtypeOf("Person", graph_type)


def test_multiple_inheritance():
    """Test subtype relation with multiple supertypes"""
    # Create diamond hierarchy
    entity = NodeTypeBuilder("Entity").build()
    person = NodeTypeBuilder("Person").withSupertypes(["Entity"]).build()
    organization = NodeTypeBuilder("Organization").withSupertypes(["Entity"]).build()
    employee = NodeTypeBuilder("Employee") \
        .withSupertypes(["Person", "Organization"]).build()
    
    dummy_edge = EdgeTypeBuilder("DUMMY", "Entity", "Entity").build()
    graph_type = build_graph_type([entity, person, organization, employee], [dummy_edge])
    
    # Employee <: Person
    assert employee.isSubtypeOf("Person", graph_type)
    
    # Employee <: Organization
    assert employee.isSubtypeOf("Organization", graph_type)
    
    # Employee <: Entity (through both paths)
    assert employee.isSubtypeOf("Entity", graph_type)


def test_edge_type_reflexive():
    """Test reflexive property for edge types"""
    person = NodeTypeBuilder("Person").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    
    graph_type = build_graph_type([person], [knows])
    
    # Reflexive: KNOWS <: KNOWS
    assert knows.isSubtypeOf("KNOWS", graph_type)


def test_edge_type_transitive():
    """Test transitive property for edge types"""
    person = NodeTypeBuilder("Person").build()
    
    # Create edge type hierarchy: RELATIONSHIP -> KNOWS -> CLOSE_FRIEND
    relationship = EdgeTypeBuilder("RELATIONSHIP", "Person", "Person").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person") \
        .withSupertypes(["RELATIONSHIP"]).build()
    close_friend = EdgeTypeBuilder("CLOSE_FRIEND", "Person", "Person") \
        .withSupertypes(["KNOWS"]).build()
    
    graph_type = build_graph_type([person], [relationship, knows, close_friend])
    
    # Direct: KNOWS <: RELATIONSHIP
    assert knows.isSubtypeOf("RELATIONSHIP", graph_type)
    
    # Direct: CLOSE_FRIEND <: KNOWS
    assert close_friend.isSubtypeOf("KNOWS", graph_type)
    
    # Transitive: CLOSE_FRIEND <: RELATIONSHIP
    assert close_friend.isSubtypeOf("RELATIONSHIP", graph_type)


def test_jaguar_hierarchy():
    """Test with jaguar conservation hierarchy"""
    # Create Animal -> Mammal -> BigCat -> Jaguar hierarchy
    animal = NodeTypeBuilder("Animal").build()
    mammal = NodeTypeBuilder("Mammal").withSupertypes(["Animal"]).build()
    big_cat = NodeTypeBuilder("BigCat").withSupertypes(["Mammal"]).build()
    jaguar = NodeTypeBuilder("Jaguar").withSupertypes(["BigCat"]).build()
    
    dummy_edge = EdgeTypeBuilder("DUMMY", "Animal", "Animal").build()
    graph_type = build_graph_type([animal, mammal, big_cat, jaguar], [dummy_edge])
    
    # Reflexive
    assert jaguar.isSubtypeOf("Jaguar", graph_type)
    
    # Direct supertypes
    assert jaguar.isSubtypeOf("BigCat", graph_type)
    assert big_cat.isSubtypeOf("Mammal", graph_type)
    assert mammal.isSubtypeOf("Animal", graph_type)
    
    # Transitive through multiple levels
    assert jaguar.isSubtypeOf("Mammal", graph_type)
    assert jaguar.isSubtypeOf("Animal", graph_type)
    assert big_cat.isSubtypeOf("Animal", graph_type)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
