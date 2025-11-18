"""
Test edge type subtyping with endpoint covariance
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


def test_edge_type_reflexive():
    """Test reflexive property for edge types"""
    person = NodeTypeBuilder("Person").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    
    graph_type = build_graph_type([person], [knows])
    
    # Reflexive: KNOWS <: KNOWS
    assert knows.isSubtypeOf("KNOWS", graph_type)


def test_edge_type_hierarchy():
    """Test edge type hierarchy without endpoint changes"""
    person = NodeTypeBuilder("Person").build()
    
    relationship = EdgeTypeBuilder("RELATIONSHIP", "Person", "Person").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person") \
        .withSupertypes(["RELATIONSHIP"]).build()
    
    graph_type = build_graph_type([person], [relationship, knows])
    
    # KNOWS <: RELATIONSHIP (through type hierarchy)
    assert knows.isSubtypeOf("RELATIONSHIP", graph_type)


def test_edge_type_covariant_endpoints():
    """Test edge type subtyping with covariant endpoint node types"""
    # Create node type hierarchy: Person -> Employee
    person = NodeTypeBuilder("Person").build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    
    # Create edge types with different endpoint types
    knows_person = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    knows_employee = EdgeTypeBuilder("KNOWS_EMPLOYEE", "Employee", "Employee").build()
    
    graph_type = build_graph_type([person, employee], [knows_person, knows_employee])
    
    # KNOWS(Employee, Employee) <: KNOWS(Person, Person) via covariant endpoints
    assert knows_employee.isSubtypeOf("KNOWS", graph_type)


def test_edge_type_mixed_endpoints():
    """Test edge type with mixed endpoint types"""
    person = NodeTypeBuilder("Person").build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    company = NodeTypeBuilder("Company").build()
    
    # Person works at Company
    works_at_person = EdgeTypeBuilder("WORKS_AT", "Person", "Company").build()
    
    # Employee works at Company
    works_at_employee = EdgeTypeBuilder("WORKS_AT_EMPLOYEE", "Employee", "Company").build()
    
    graph_type = build_graph_type([person, employee, company], [works_at_person, works_at_employee])
    
    # WORKS_AT(Employee, Company) <: WORKS_AT(Person, Company)
    # Source is covariant: Employee <: Person
    # Destination is same: Company <: Company
    assert works_at_employee.isSubtypeOf("WORKS_AT", graph_type)


def test_edge_type_direction_mismatch():
    """Test that direction must match for subtyping"""
    person = NodeTypeBuilder("Person").build()
    
    knows_directed = EdgeTypeBuilder("KNOWS_DIRECTED", "Person", "Person").build()
    knows_undirected = EdgeTypeBuilder("KNOWS_UNDIRECTED", "Person", "Person") \
        .asUndirected().build()
    
    graph_type = build_graph_type([person], [knows_directed, knows_undirected])
    
    # DIRECTED is not a subtype of UNDIRECTED
    assert not knows_directed.isSubtypeOf("KNOWS_UNDIRECTED", graph_type)
    
    # UNDIRECTED is not a subtype of DIRECTED
    assert not knows_undirected.isSubtypeOf("KNOWS_DIRECTED", graph_type)


def test_edge_type_undirected_symmetric():
    """Test undirected edge type subtyping with symmetric endpoints"""
    person = NodeTypeBuilder("Person").build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    
    # Undirected edges can match endpoints in either order
    knows_person = EdgeTypeBuilder("KNOWS", "Person", "Person").asUndirected().build()
    knows_employee = EdgeTypeBuilder("KNOWS_EMPLOYEE", "Employee", "Employee") \
        .asUndirected().build()
    
    graph_type = build_graph_type([person, employee], [knows_person, knows_employee])
    
    # KNOWS(Employee, Employee) <: KNOWS(Person, Person)
    assert knows_employee.isSubtypeOf("KNOWS", graph_type)


def test_edge_type_self_loop():
    """Test edge type subtyping with self-loops (SAME endpoint)"""
    person = NodeTypeBuilder("Person").build()
    
    # Self-loop edge type
    self_reference = EdgeTypeBuilder("SELF_REF", "Person", "SAME").build()
    
    graph_type = build_graph_type([person], [self_reference])
    
    # Reflexive: SELF_REF <: SELF_REF
    assert self_reference.isSubtypeOf("SELF_REF", graph_type)


def test_edge_type_combined_hierarchy_and_endpoints():
    """Test edge type subtyping with both type hierarchy and endpoint covariance"""
    # Node hierarchy: Entity -> Person -> Employee
    entity = NodeTypeBuilder("Entity").build()
    person = NodeTypeBuilder("Person").withSupertypes(["Entity"]).build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    
    # Edge hierarchy: RELATIONSHIP -> KNOWS
    relationship = EdgeTypeBuilder("RELATIONSHIP", "Entity", "Entity").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person") \
        .withSupertypes(["RELATIONSHIP"]).build()
    close_friend = EdgeTypeBuilder("CLOSE_FRIEND", "Employee", "Employee") \
        .withSupertypes(["KNOWS"]).build()
    
    graph_type = build_graph_type(
        [entity, person, employee],
        [relationship, knows, close_friend]
    )
    
    # Direct hierarchy: CLOSE_FRIEND <: KNOWS
    assert close_friend.isSubtypeOf("KNOWS", graph_type)
    
    # Transitive hierarchy: CLOSE_FRIEND <: RELATIONSHIP
    assert close_friend.isSubtypeOf("RELATIONSHIP", graph_type)
    
    # KNOWS <: RELATIONSHIP (through hierarchy)
    assert knows.isSubtypeOf("RELATIONSHIP", graph_type)


def test_edge_type_not_subtype():
    """Test that unrelated edge types are not subtypes"""
    person = NodeTypeBuilder("Person").build()
    company = NodeTypeBuilder("Company").build()
    
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    owns = EdgeTypeBuilder("OWNS", "Person", "Company").build()
    
    graph_type = build_graph_type([person, company], [knows, owns])
    
    # KNOWS is not a subtype of OWNS (different endpoints)
    assert not knows.isSubtypeOf("OWNS", graph_type)
    
    # OWNS is not a subtype of KNOWS (different endpoints)
    assert not owns.isSubtypeOf("KNOWS", graph_type)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
