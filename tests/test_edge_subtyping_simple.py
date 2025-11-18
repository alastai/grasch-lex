"""
Simple tests for edge type subtyping with endpoint covariance
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


def test_edge_reflexive():
    """Edge type is subtype of itself (reflexive)"""
    person = NodeTypeBuilder("Person").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    
    gt = build_graph_type([person], [knows])
    
    assert knows.isSubtypeOf("KNOWS", gt)


def test_edge_hierarchy():
    """Edge type hierarchy through supertypes"""
    person = NodeTypeBuilder("Person").build()
    relationship = EdgeTypeBuilder("RELATIONSHIP", "Person", "Person").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person") \
        .withSupertypes(["RELATIONSHIP"]).build()
    
    gt = build_graph_type([person], [relationship, knows])
    
    assert knows.isSubtypeOf("RELATIONSHIP", gt)


def test_edge_covariant_endpoints():
    """Edge type subtyping with covariant endpoints"""
    person = NodeTypeBuilder("Person").build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    
    knows_person = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    knows_employee = EdgeTypeBuilder("KNOWS_EMP", "Employee", "Employee").build()
    
    gt = build_graph_type([person, employee], [knows_person, knows_employee])
    
    # KNOWS(Employee, Employee) <: KNOWS(Person, Person)
    assert knows_employee.isSubtypeOf("KNOWS", gt)


def test_edge_direction_mismatch():
    """Direction must match for subtyping"""
    person = NodeTypeBuilder("Person").build()
    directed = EdgeTypeBuilder("KNOWS_DIR", "Person", "Person").build()
    undirected = EdgeTypeBuilder("KNOWS_UNDIR", "Person", "Person") \
        .asUndirected().build()
    
    gt = build_graph_type([person], [directed, undirected])
    
    assert not directed.isSubtypeOf("KNOWS_UNDIR", gt)
    assert not undirected.isSubtypeOf("KNOWS_DIR", gt)


def test_edge_mixed_endpoints():
    """Covariant in source, same destination"""
    person = NodeTypeBuilder("Person").build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    company = NodeTypeBuilder("Company").build()
    
    works_person = EdgeTypeBuilder("WORKS_AT", "Person", "Company").build()
    works_employee = EdgeTypeBuilder("WORKS_EMP", "Employee", "Company").build()
    
    gt = build_graph_type([person, employee, company], [works_person, works_employee])
    
    # WORKS_AT(Employee, Company) <: WORKS_AT(Person, Company)
    assert works_employee.isSubtypeOf("WORKS_AT", gt)


def test_edge_not_subtype():
    """Unrelated edge types are not subtypes"""
    person = NodeTypeBuilder("Person").build()
    company = NodeTypeBuilder("Company").build()
    
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    owns = EdgeTypeBuilder("OWNS", "Person", "Company").build()
    
    gt = build_graph_type([person, company], [knows, owns])
    
    assert not knows.isSubtypeOf("OWNS", gt)
    assert not owns.isSubtypeOf("KNOWS", gt)


def test_edge_transitive():
    """Transitive subtyping through multiple levels"""
    entity = NodeTypeBuilder("Entity").build()
    person = NodeTypeBuilder("Person").withSupertypes(["Entity"]).build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    
    rel = EdgeTypeBuilder("REL", "Entity", "Entity").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person") \
        .withSupertypes(["REL"]).build()
    friend = EdgeTypeBuilder("FRIEND", "Employee", "Employee") \
        .withSupertypes(["KNOWS"]).build()
    
    gt = build_graph_type([entity, person, employee], [rel, knows, friend])
    
    # Transitive: FRIEND <: KNOWS <: REL
    assert friend.isSubtypeOf("KNOWS", gt)
    assert friend.isSubtypeOf("REL", gt)
    assert knows.isSubtypeOf("REL", gt)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
