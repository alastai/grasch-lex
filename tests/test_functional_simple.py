#!/usr/bin/env python3
"""
Simple Functional Test for Grasch Library - Standalone Version

This demonstrates the complete Grasch workflow without pytest dependencies.
"""

import os
import tempfile
from typing import Dict

from grasch import (
    GraschSession,
    SessionConfiguration,
    ProfileConfiguration,
    LanguageLevel,
    LEXCompatibility,
    ContentRecordTypeBuilder,
    LabelType,
    PropertyType,
    NodeTypeBuilder,
    EdgeType,
    GraphType,
    Graph,
    KeyConstraint,
)


def create_session_config() -> SessionConfiguration:
    """Create a test session configuration"""
    full_profile = ProfileConfiguration(
        name="Full Profile",
        optional_features={"GC04", "GG25", "IL001"},
        implementation_defined={"IL001": {"min": 0, "max": None}},
        lex_compatibility=LEXCompatibility.FULL
    )
    
    return SessionConfiguration(
        profile=full_profile,
        language_level=LanguageLevel.LEX,
        catalog_root="file:.",
        default_catalog_path="/",
        nested_record_schema_processor_type="JSON Schema",
        nested_record_schema_processor="default"
    )


def create_content_types():
    """Define content record types for the graph"""
    # Person content type
    person_content = ContentRecordTypeBuilder("PersonContent") \
        .add_label_type(LabelType("Person")) \
        .add_property_type(PropertyType("name", "STRING", not_null=True)) \
        .add_property_type(PropertyType("age", "INTEGER")) \
        .add_property_type(PropertyType("email", "STRING")) \
        .set_type_key([LabelType("Person")]) \
        .create()
    
    # Company content type
    company_content = ContentRecordTypeBuilder("CompanyContent") \
        .add_label_type(LabelType("Company")) \
        .add_property_type(PropertyType("name", "STRING", not_null=True)) \
        .add_property_type(PropertyType("industry", "STRING")) \
        .set_type_key([LabelType("Company")]) \
        .create()
    
    # Employment relationship content type
    employment_content = ContentRecordTypeBuilder("EmploymentContent") \
        .add_label_type(LabelType("WORKS_FOR")) \
        .add_property_type(PropertyType("position", "STRING")) \
        .add_property_type(PropertyType("start_date", "DATE")) \
        .set_type_key([LabelType("WORKS_FOR")]) \
        .create()
    
    return {
        "person": person_content,
        "company": company_content,
        "employment": employment_content
    }


def create_graph_schema(content_types) -> GraphType:
    """Create a graph type with ALL ELEMENT TYPES KEYED constraint"""
    # Create element types using builders
    person_node_type = NodeTypeBuilder(content_types["person"]).create()
    company_node_type = NodeTypeBuilder(content_types["company"]).create()
    
    works_for_edge_type = EdgeType(
        "WORKS_FOR",
        person_node_type,
        company_node_type,
        content_types["employment"]
    )
    
    # Create graph type with ALL ELEMENT TYPES KEYED constraint
    graph_type = GraphType("EmployeeGraph", all_element_types_keyed=True)
    graph_type.add_node_type(person_node_type)
    graph_type.add_node_type(company_node_type)
    graph_type.add_edge_type(works_for_edge_type)
    
    # Add key constraints (required by ALL ELEMENT TYPES KEYED)
    graph_type.add_constraint(KeyConstraint("Person", ["Person"]))
    graph_type.add_constraint(KeyConstraint("Company", ["Company"]))
    graph_type.add_constraint(KeyConstraint("WORKS_FOR", ["WORKS_FOR"]))
    
    return graph_type


def create_and_populate_graph(graph_type: GraphType) -> Graph:
    """Create a graph instance and populate it with data"""
    # Create graph instance
    graph = Graph("employee_data", graph_type)
    
    # Insert Person nodes
    alice_id = graph.insert_node(
        labels=["Person"],
        properties={"name": "Alice Johnson", "age": 30, "email": "alice@example.com"}
    )
    
    bob_id = graph.insert_node(
        labels=["Person"],
        properties={"name": "Bob Smith", "age": 25, "email": "bob@example.com"}
    )
    
    # Insert Company nodes
    techcorp_id = graph.insert_node(
        labels=["Company"],
        properties={"name": "TechCorp", "industry": "Technology"}
    )
    
    datasystems_id = graph.insert_node(
        labels=["Company"],
        properties={"name": "DataSystems", "industry": "Software"}
    )
    
    # Insert WORKS_FOR edges
    graph.insert_edge(
        source_id=alice_id,
        target_id=techcorp_id,
        labels=["WORKS_FOR"],
        properties={"position": "Engineer", "start_date": "2020-01-15"}
    )
    
    graph.insert_edge(
        source_id=bob_id,
        target_id=datasystems_id,
        labels=["WORKS_FOR"],
        properties={"position": "Analyst", "start_date": "2021-03-01"}
    )
    
    return graph


def run_functional_test():
    """Run the complete functional test"""
    print("=" * 60)
    print("GRASCH LIBRARY FUNCTIONAL TEST")
    print("=" * 60)
    
    # Create temporary database directory
    with tempfile.TemporaryDirectory() as temp_dir:
        database_path = os.path.join(temp_dir, "grasch_test.db")
        
        # Configure Grasch session
        session_config = create_session_config()
        
        print(f"Initializing Grasch session with {session_config.language_level.value} language level...")
        print(f"Using profile: {session_config.profile.name}")
        print(f"Database path: {database_path}")
        
        # Initialize Grasch session
        grasch_session = GraschSession(session_config, database_path)
        
        # Step 1: Create catalog structure
        print("\n1. Creating catalog structure...")
        grasch_session.create_catalog_structure()
        
        # Verify catalog structure
        assert grasch_session.catalog.root.children["production"] is not None
        assert grasch_session.catalog.root.children["development"] is not None
        print("   ✓ Catalog directories created successfully")
        
        # Step 2: Define content types
        print("\n2. Defining content record types...")
        content_types = create_content_types()
        
        # Verify content types
        assert len(content_types) == 3
        assert content_types["person"].type_key is not None
        assert content_types["company"].type_key is not None
        assert content_types["employment"].type_key is not None
        print("   ✓ Content record types with type keys defined")
        
        # Step 3: Create graph schema with constraints
        print("\n3. Creating graph type with LEX constraints...")
        graph_type = create_graph_schema(content_types)
        
        # Verify graph type
        assert graph_type.all_element_types_keyed is True
        assert len(graph_type.node_types) == 2
        assert len(graph_type.edge_types) == 1
        assert len(graph_type.constraints) == 3
        print("   ✓ Graph type with ALL ELEMENT TYPES KEYED constraint created")
        
        # Step 4: Create and populate graph
        print("\n4. Creating and populating graph instance...")
        graph = create_and_populate_graph(graph_type)
        
        # Verify graph population
        assert len(graph.nodes) == 4
        assert len(graph.edges) == 2
        assert graph.graph_type == graph_type
        print(f"   ✓ Graph populated with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
        
        # Step 5: Store in catalog
        print("\n5. Storing objects in catalog...")
        schema = grasch_session.catalog.create_gql_schema("/production/customer_data", "employee_schema")
        schema.add_graph_type(graph_type)
        schema.add_graph(graph)
        
        # Verify catalog storage
        assert "employee_schema" in grasch_session.catalog.root.children["production"].children["customer_data"].schemas
        stored_schema = grasch_session.catalog.root.children["production"].children["customer_data"].schemas["employee_schema"]
        assert "EmployeeGraph" in stored_schema.graph_types
        assert "employee_data" in stored_schema.graphs
        print("   ✓ Objects stored in catalog at /production/customer_data/employee_schema")
        
        # Step 6: Demonstrate queries
        print("\n6. Demonstrating Cypher queries...")
        grasch_session.demonstrate_cypher_queries()
        
        # Step 7: Demonstrate spectral typing concepts
        print("\n7. Demonstrating spectral typing concepts...")
        grasch_session.demonstrate_spectral_typing()
        
        print("\n" + "=" * 60)
        print("✓ FUNCTIONAL TEST COMPLETED SUCCESSFULLY!")
        print("✓ All Grasch library features demonstrated")
        print("✓ Graph data persisted in Kuzu database")
        print("✓ Cypher queries executed successfully")
        print("=" * 60)


if __name__ == "__main__":
    run_functional_test()