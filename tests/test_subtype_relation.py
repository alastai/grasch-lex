"""
Test subtype relation properties (Armstrong's Axioms)
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.grasch.api.builders import (
    GraphTypeBuilder, NodeTypeBuilder, EdgeTypeBuilder
)


def test_reflexive_property():
    """Test that every type is a subtype of itself (reflexive)"""
    # Create a node type
    person = NodeTypeBuilder().withTypeLabel("Person").build()
    
    # Create graph type with the node type
    graph_type = GraphTypeBuilder().addNodeType(person).build()
    
    # Reflexive: Person <: Person
    assert person.isSubtypeOf("Person", graph_type)


def test_transitive_property():
    """Test that subtype relation is transitive"""
    # Create graph type
    graph_type = GraphTypeImpl()
    
    # Create type hierarchy: Entity -> Person -> Employee
    entity = NodeTypeImpl(typeLabel="Entity")
    person = NodeTypeImpl(typeLabel="Person", supertypes=["Entity"])
    employee = NodeTypeImpl(typeLabel="Employee", supertypes=["Person"])
    
    graph_type.addNodeType(entity)
    graph_type.addNodeType(person)
    graph_type.addNodeType(employee)
    
    # Direct subtype: Person <: Entity
    assert person.isSubtypeOf("Entity", graph_type)
    
    # Direct subtype: Employee <: Person
    assert employee.isSubtypeOf("Person", graph_type)
    
    # Transitive: Employee <: Entity (through Person)
    assert employee.isSubtypeOf("Entity", graph_type)


def test_not_subtype():
    """Test that unrelated types are not subtypes"""
    graph_type = GraphTypeImpl()
    
    person = NodeTypeImpl(typeLabel="Person")
    company = NodeTypeImpl(typeLabel="Company")
    
    graph_type.addNodeType(person)
    graph_type.addNodeType(company)
    
    # Person is not a subtype of Company
    assert not person.isSubtypeOf("Company", graph_type)
    
    # Company is not a subtype of Person
    assert not company.isSubtypeOf("Person", graph_type)


def test_multiple_inheritance():
    """Test subtype relation with multiple supertypes"""
    graph_type = GraphTypeImpl()
    
    # Create diamond hierarchy
    entity = NodeTypeImpl(typeLabel="Entity")
    person = NodeTypeImpl(typeLabel="Person", supertypes=["Entity"])
    organization = NodeTypeImpl(typeLabel="Organization", supertypes=["Entity"])
    employee = NodeTypeImpl(
        typeLabel="Employee",
        supertypes=["Person", "Organization"]
    )
    
    graph_type.addNodeType(entity)
    graph_type.addNodeType(person)
    graph_type.addNodeType(organization)
    graph_type.addNodeType(employee)
    
    # Employee <: Person
    assert employee.isSubtypeOf("Person", graph_type)
    
    # Employee <: Organization
    assert employee.isSubtypeOf("Organization", graph_type)
    
    # Employee <: Entity (through both paths)
    assert employee.isSubtypeOf("Entity", graph_type)


def test_edge_type_reflexive():
    """Test reflexive property for edge types"""
    graph_type = GraphTypeImpl()
    
    knows = EdgeTypeImpl(
        typeLabel="KNOWS",
        firstEndpointNodeType="Person",
        secondEndpointNodeType="Person"
    )
    graph_type.addEdgeType(knows)
    
    # Reflexive: KNOWS <: KNOWS
    assert knows.isSubtypeOf("KNOWS", graph_type)


def test_edge_type_transitive():
    """Test transitive property for edge types"""
    graph_type = GraphTypeImpl()
    
    # Create edge type hierarchy: RELATIONSHIP -> KNOWS -> CLOSE_FRIEND
    relationship = EdgeTypeImpl(
        typeLabel="RELATIONSHIP",
        firstEndpointNodeType="Person",
        secondEndpointNodeType="Person"
    )
    knows = EdgeTypeImpl(
        typeLabel="KNOWS",
        firstEndpointNodeType="Person",
        secondEndpointNodeType="Person",
        supertypes=["RELATIONSHIP"]
    )
    close_friend = EdgeTypeImpl(
        typeLabel="CLOSE_FRIEND",
        firstEndpointNodeType="Person",
        secondEndpointNodeType="Person",
        supertypes=["KNOWS"]
    )
    
    graph_type.addEdgeType(relationship)
    graph_type.addEdgeType(knows)
    graph_type.addEdgeType(close_friend)
    
    # Direct: KNOWS <: RELATIONSHIP
    assert knows.isSubtypeOf("RELATIONSHIP", graph_type)
    
    # Direct: CLOSE_FRIEND <: KNOWS
    assert close_friend.isSubtypeOf("KNOWS", graph_type)
    
    # Transitive: CLOSE_FRIEND <: RELATIONSHIP
    assert close_friend.isSubtypeOf("RELATIONSHIP", graph_type)


def test_jaguar_hierarchy():
    """Test with jaguar conservation hierarchy"""
    graph_type = GraphTypeImpl()
    
    # Create Animal -> Mammal -> BigCat -> Jaguar hierarchy
    animal = NodeTypeImpl(typeLabel="Animal")
    mammal = NodeTypeImpl(typeLabel="Mammal", supertypes=["Animal"])
    big_cat = NodeTypeImpl(typeLabel="BigCat", supertypes=["Mammal"])
    jaguar = NodeTypeImpl(typeLabel="Jaguar", supertypes=["BigCat"])
    
    graph_type.addNodeType(animal)
    graph_type.addNodeType(mammal)
    graph_type.addNodeType(big_cat)
    graph_type.addNodeType(jaguar)
    
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
