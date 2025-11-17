"""
Test edge type subtyping with endpoint covariance
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.grasch.api.builders import (
    GraphTypeBuilder, NodeTypeBuilder, EdgeTypeBuilder
)


def test_edge_type_reflexive():
    """Test reflexive property for edge types"""
    person = NodeTypeBuilder("Person").build()
    knows = EdgeTypeBuilder("KNOWS") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("DIRECTED") \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(person) \
        .addEdgeType(knows) \
        .build()
    
    # Reflexive: KNOWS <: KNOWS
    assert knows.isSubtypeOf("KNOWS", graph_type)


def test_edge_type_hierarchy():
    """Test edge type hierarchy without endpoint changes"""
    person = NodeTypeBuilder().withTypeLabel("Person").build()
    
    relationship = EdgeTypeBuilder() \
        .withTypeLabel("RELATIONSHIP") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("DIRECTED") \
        .build()
    
    knows = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("DIRECTED") \
        .withSupertypes(["RELATIONSHIP"]) \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(person) \
        .addEdgeType(relationship) \
        .addEdgeType(knows) \
        .build()
    
    # KNOWS <: RELATIONSHIP (through type hierarchy)
    assert knows.isSubtypeOf("RELATIONSHIP", graph_type)


def test_edge_type_covariant_endpoints():
    """Test edge type subtyping with covariant endpoint node types"""
    # Create node type hierarchy: Person -> Employee
    person = NodeTypeBuilder().withTypeLabel("Person").build()
    employee = NodeTypeBuilder() \
        .withTypeLabel("Employee") \
        .withSupertypes(["Person"]) \
        .build()
    
    # Create edge types with different endpoint types
    knows_person = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("DIRECTED") \
        .build()
    
    knows_employee = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS_EMPLOYEE") \
        .withFirstEndpointNodeType("Employee") \
        .withSecondEndpointNodeType("Employee") \
        .withDirection("DIRECTED") \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(person) \
        .addNodeType(employee) \
        .addEdgeType(knows_person) \
        .addEdgeType(knows_employee) \
        .build()
    
    # KNOWS(Employee, Employee) <: KNOWS(Person, Person) via covariant endpoints
    assert knows_employee.isSubtypeOf("KNOWS", graph_type)


def test_edge_type_mixed_endpoints():
    """Test edge type with mixed endpoint types"""
    person = NodeTypeBuilder().withTypeLabel("Person").build()
    employee = NodeTypeBuilder() \
        .withTypeLabel("Employee") \
        .withSupertypes(["Person"]) \
        .build()
    company = NodeTypeBuilder().withTypeLabel("Company").build()
    
    # Person works at Company
    works_at_person = EdgeTypeBuilder() \
        .withTypeLabel("WORKS_AT") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Company") \
        .withDirection("DIRECTED") \
        .build()
    
    # Employee works at Company
    works_at_employee = EdgeTypeBuilder() \
        .withTypeLabel("WORKS_AT_EMPLOYEE") \
        .withFirstEndpointNodeType("Employee") \
        .withSecondEndpointNodeType("Company") \
        .withDirection("DIRECTED") \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(person) \
        .addNodeType(employee) \
        .addNodeType(company) \
        .addEdgeType(works_at_person) \
        .addEdgeType(works_at_employee) \
        .build()
    
    # WORKS_AT(Employee, Company) <: WORKS_AT(Person, Company)
    # Source is covariant: Employee <: Person
    # Destination is same: Company <: Company
    assert works_at_employee.isSubtypeOf("WORKS_AT", graph_type)


def test_edge_type_direction_mismatch():
    """Test that direction must match for subtyping"""
    person = NodeTypeBuilder().withTypeLabel("Person").build()
    
    knows_directed = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS_DIRECTED") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("DIRECTED") \
        .build()
    
    knows_undirected = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS_UNDIRECTED") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("UNDIRECTED") \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(person) \
        .addEdgeType(knows_directed) \
        .addEdgeType(knows_undirected) \
        .build()
    
    # DIRECTED is not a subtype of UNDIRECTED
    assert not knows_directed.isSubtypeOf("KNOWS_UNDIRECTED", graph_type)
    
    # UNDIRECTED is not a subtype of DIRECTED
    assert not knows_undirected.isSubtypeOf("KNOWS_DIRECTED", graph_type)


def test_edge_type_undirected_symmetric():
    """Test undirected edge type subtyping with symmetric endpoints"""
    person = NodeTypeBuilder().withTypeLabel("Person").build()
    employee = NodeTypeBuilder() \
        .withTypeLabel("Employee") \
        .withSupertypes(["Person"]) \
        .build()
    
    # Undirected edges can match endpoints in either order
    knows_person = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("UNDIRECTED") \
        .build()
    
    knows_employee = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS_EMPLOYEE") \
        .withFirstEndpointNodeType("Employee") \
        .withSecondEndpointNodeType("Employee") \
        .withDirection("UNDIRECTED") \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(person) \
        .addNodeType(employee) \
        .addEdgeType(knows_person) \
        .addEdgeType(knows_employee) \
        .build()
    
    # KNOWS(Employee, Employee) <: KNOWS(Person, Person)
    assert knows_employee.isSubtypeOf("KNOWS", graph_type)


def test_edge_type_self_loop():
    """Test edge type subtyping with self-loops (SAME endpoint)"""
    person = NodeTypeBuilder().withTypeLabel("Person").build()
    
    # Self-loop edge type
    self_reference = EdgeTypeBuilder() \
        .withTypeLabel("SELF_REF") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("SAME") \
        .withDirection("DIRECTED") \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(person) \
        .addEdgeType(self_reference) \
        .build()
    
    # Reflexive: SELF_REF <: SELF_REF
    assert self_reference.isSubtypeOf("SELF_REF", graph_type)


def test_edge_type_combined_hierarchy_and_endpoints():
    """Test edge type subtyping with both type hierarchy and endpoint covariance"""
    # Node hierarchy: Entity -> Person -> Employee
    entity = NodeTypeBuilder().withTypeLabel("Entity").build()
    person = NodeTypeBuilder() \
        .withTypeLabel("Person") \
        .withSupertypes(["Entity"]) \
        .build()
    employee = NodeTypeBuilder() \
        .withTypeLabel("Employee") \
        .withSupertypes(["Person"]) \
        .build()
    
    # Edge hierarchy: RELATIONSHIP -> KNOWS
    relationship = EdgeTypeBuilder() \
        .withTypeLabel("RELATIONSHIP") \
        .withFirstEndpointNodeType("Entity") \
        .withSecondEndpointNodeType("Entity") \
        .withDirection("DIRECTED") \
        .build()
    
    knows = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("DIRECTED") \
        .withSupertypes(["RELATIONSHIP"]) \
        .build()
    
    close_friend = EdgeTypeBuilder() \
        .withTypeLabel("CLOSE_FRIEND") \
        .withFirstEndpointNodeType("Employee") \
        .withSecondEndpointNodeType("Employee") \
        .withDirection("DIRECTED") \
        .withSupertypes(["KNOWS"]) \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(entity) \
        .addNodeType(person) \
        .addNodeType(employee) \
        .addEdgeType(relationship) \
        .addEdgeType(knows) \
        .addEdgeType(close_friend) \
        .build()
    
    # Direct hierarchy: CLOSE_FRIEND <: KNOWS
    assert close_friend.isSubtypeOf("KNOWS", graph_type)
    
    # Transitive hierarchy: CLOSE_FRIEND <: RELATIONSHIP
    assert close_friend.isSubtypeOf("RELATIONSHIP", graph_type)
    
    # KNOWS <: RELATIONSHIP (through hierarchy)
    assert knows.isSubtypeOf("RELATIONSHIP", graph_type)


def test_edge_type_not_subtype():
    """Test that unrelated edge types are not subtypes"""
    person = NodeTypeBuilder().withTypeLabel("Person").build()
    company = NodeTypeBuilder().withTypeLabel("Company").build()
    
    knows = EdgeTypeBuilder() \
        .withTypeLabel("KNOWS") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Person") \
        .withDirection("DIRECTED") \
        .build()
    
    owns = EdgeTypeBuilder() \
        .withTypeLabel("OWNS") \
        .withFirstEndpointNodeType("Person") \
        .withSecondEndpointNodeType("Company") \
        .withDirection("DIRECTED") \
        .build()
    
    graph_type = GraphTypeBuilder() \
        .addNodeType(person) \
        .addNodeType(company) \
        .addEdgeType(knows) \
        .addEdgeType(owns) \
        .build()
    
    # KNOWS is not a subtype of OWNS (different endpoints)
    assert not knows.isSubtypeOf("OWNS", graph_type)
    
    # OWNS is not a subtype of KNOWS (different endpoints)
    assert not owns.isSubtypeOf("KNOWS", graph_type)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
