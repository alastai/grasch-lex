"""
Simple tests for edge type subtyping with endpoint covariance
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.grasch.api.builders import (
    GraphTypeBuilder, NodeTypeBuilder, EdgeTypeBuilder
)


def test_edge_reflexive():
    """Edge type is subtype of itself (reflexive)"""
    person = NodeTypeBuilder("Person").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    
    gt = GraphTypeBuilder().addNodeType(person).addEdgeType(knows).build()
    
    assert knows.isSubtypeOf("KNOWS", gt)


def test_edge_hierarchy():
    """Edge type hierarchy through supertypes"""
    person = NodeTypeBuilder("Person").build()
    relationship = EdgeTypeBuilder("RELATIONSHIP", "Person", "Person").build()
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person") \
        .withSupertypes(["RELATIONSHIP"]).build()
    
    gt = GraphTypeBuilder() \
        .addNodeType(person) \
        .addEdgeType(relationship) \
        .addEdgeType(knows) \
        .build()
    
    assert knows.isSubtypeOf("RELATIONSHIP", gt)


def test_edge_covariant_endpoints():
    """Edge type subtyping with covariant endpoints"""
    person = NodeTypeBuilder("Person").build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    
    knows_person = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    knows_employee = EdgeTypeBuilder("KNOWS_EMP", "Employee", "Employee").build()
    
    gt = GraphTypeBuilder() \
        .addNodeType(person) \
        .addNodeType(employee) \
        .addEdgeType(knows_person) \
        .addEdgeType(knows_employee) \
        .build()
    
    # KNOWS(Employee, Employee) <: KNOWS(Person, Person)
    assert knows_employee.isSubtypeOf("KNOWS", gt)


def test_edge_direction_mismatch():
    """Direction must match for subtyping"""
    person = NodeTypeBuilder("Person").build()
    directed = EdgeTypeBuilder("KNOWS_DIR", "Person", "Person").build()
    undirected = EdgeTypeBuilder("KNOWS_UNDIR", "Person", "Person") \
        .asUndirected().build()
    
    gt = GraphTypeBuilder() \
        .addNodeType(person) \
        .addEdgeType(directed) \
        .addEdgeType(undirected) \
        .build()
    
    assert not directed.isSubtypeOf("KNOWS_UNDIR", gt)
    assert not undirected.isSubtypeOf("KNOWS_DIR", gt)


def test_edge_mixed_endpoints():
    """Covariant in source, same destination"""
    person = NodeTypeBuilder("Person").build()
    employee = NodeTypeBuilder("Employee").withSupertypes(["Person"]).build()
    company = NodeTypeBuilder("Company").build()
    
    works_person = EdgeTypeBuilder("WORKS_AT", "Person", "Company").build()
    works_employee = EdgeTypeBuilder("WORKS_EMP", "Employee", "Company").build()
    
    gt = GraphTypeBuilder() \
        .addNodeType(person) \
        .addNodeType(employee) \
        .addNodeType(company) \
        .addEdgeType(works_person) \
        .addEdgeType(works_employee) \
        .build()
    
    # WORKS_AT(Employee, Company) <: WORKS_AT(Person, Company)
    assert works_employee.isSubtypeOf("WORKS_AT", gt)


def test_edge_not_subtype():
    """Unrelated edge types are not subtypes"""
    person = NodeTypeBuilder("Person").build()
    company = NodeTypeBuilder("Company").build()
    
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    owns = EdgeTypeBuilder("OWNS", "Person", "Company").build()
    
    gt = GraphTypeBuilder() \
        .addNodeType(person) \
        .addNodeType(company) \
        .addEdgeType(knows) \
        .addEdgeType(owns) \
        .build()
    
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
    
    gt = GraphTypeBuilder() \
        .addNodeType(entity) \
        .addNodeType(person) \
        .addNodeType(employee) \
        .addEdgeType(rel) \
        .addEdgeType(knows) \
        .addEdgeType(friend) \
        .build()
    
    # Transitive: FRIEND <: KNOWS <: REL
    assert friend.isSubtypeOf("KNOWS", gt)
    assert friend.isSubtypeOf("REL", gt)
    assert knows.isSubtypeOf("REL", gt)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
