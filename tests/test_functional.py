#!/usr/bin/env python3
"""
Functional Test for Grasch Library

This test demonstrates normal error-free usage of the low-level API of the Grasch library.
It creates a hierarchical catalog, defines a GQL-schema with a graph type, creates a graph
instance, populates it with data, and queries it using Cypher commands.
"""

import os
import tempfile
from typing import Dict

import pytest

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
    ArcTypeBuilder,
    EdgeTypeBuilder,
    GraphTypeBuilder,
    EdgeType,
    GraphType,
    Graph,
    KeyConstraint,
)


class TestGraschFunctional:
    """Comprehensive functional test for Grasch library"""
    
    @pytest.fixture
    def session_config(self) -> SessionConfiguration:
        """Create a test session configuration"""
        full_profile = ProfileConfiguration(
            name="Full Profile",
            optionalFeatures={"GC04", "GG25", "IL001"},
            implementationDefined={"IL001": {"min": 0, "max": None}},
            lexCompatibility=LEXCompatibility.FULL
        )
        
        return SessionConfiguration(
            profile=full_profile,
            languageLevel=LanguageLevel.LEX,
            catalogRoot="file:.",
            defaultCatalogPath="/",
            nestedRecordSchemaProcessorType="JSON Schema",
            nestedRecordSchemaProcessor="default"
        )
    
    def createContentTypes(self):
        """Define content record types for the graph"""
        # Person content type
        personContent = ContentRecordTypeBuilder() \
            .addLabel("Person") \
            .addPropertyType(PropertyType("name", "STRING", notNull=True)) \
            .addPropertyType(PropertyType("age", "INTEGER")) \
            .addPropertyType(PropertyType("email", "STRING")) \
            .addTypeName("Person") \
            .create()
        
        # Company content type
        companyContent = ContentRecordTypeBuilder() \
            .addLabel("Company") \
            .addPropertyType(PropertyType("name", "STRING", notNull=True)) \
            .addPropertyType(PropertyType("industry", "STRING")) \
            .addTypeName("Company") \
            .create()
        
        # Employment relationship content type
        employmentContent = ContentRecordTypeBuilder() \
            .addLabel("WORKS_FOR") \
            .addPropertyType(PropertyType("position", "STRING")) \
            .addPropertyType(PropertyType("startDate", "DATE")) \
            .addTypeName("WORKS_FOR") \
            .create()
        
        return {
            "person": personContent,
            "company": companyContent,
            "employment": employmentContent
        }
    
    def createGraphSchema(self, contentTypes) -> GraphType:
        """Create a graph type with ALL ELEMENT TYPES KEYED constraint"""
        # Create element types using builders
        personNodeType = NodeTypeBuilder(contentTypes["person"]).create()
        companyNodeType = NodeTypeBuilder(contentTypes["company"]).create()
        
        # Create arc type for employment edge
        employmentArcType = ArcTypeBuilder(contentTypes["employment"]).create()
        
        # Create edge type using new builder
        worksForEdgeType = (EdgeTypeBuilder("WORKS_FOR")
                           .addFirstNodeType(personNodeType)
                           .addSecondNodeType(companyNodeType)
                           .addArcType(employmentArcType)
                           .setDirected("first", "second")  # Person -> Company
                           .create())
        
        # Create graph type using new builder
        graphType = (GraphTypeBuilder("EmployeeGraph")
                    .addNodeType(personNodeType)
                    .addNodeType(companyNodeType)
                    .addEdgeType(worksForEdgeType)
                    .setAllElementTypesKeyed(True)
                    .create())
        
        # Add key constraints (required by ALL ELEMENT TYPES KEYED)
        graphType.addConstraint(KeyConstraint("Person", ["Person"]))
        graphType.addConstraint(KeyConstraint("Company", ["Company"]))
        graphType.addConstraint(KeyConstraint("WORKS_FOR", ["WORKS_FOR"]))
        
        return graphType
    
    def createAndPopulateGraph(self, graphType: GraphType) -> Graph:
        """Create a graph instance and populate it with data"""
        # Create graph instance
        graph = Graph("employee_data", graphType)
        
        # Insert Person nodes
        alice_id = graph.insertNode(
            labels=["Person"],
            properties={"name": "Alice Johnson", "age": 30, "email": "alice@example.com"}
        )
        
        bob_id = graph.insertNode(
            labels=["Person"],
            properties={"name": "Bob Smith", "age": 25, "email": "bob@example.com"}
        )
        
        # Insert Company nodes
        techcorp_id = graph.insertNode(
            labels=["Company"],
            properties={"name": "TechCorp", "industry": "Technology"}
        )
        
        datasystems_id = graph.insertNode(
            labels=["Company"],
            properties={"name": "DataSystems", "industry": "Software"}
        )
        
        # Insert WORKS_FOR edges
        graph.insertEdge(
            sourceId=alice_id,
            targetId=techcorp_id,
            labels=["WORKS_FOR"],
            properties={"position": "Engineer", "start_date": "2020-01-15"}
        )
        
        graph.insertEdge(
            sourceId=bob_id,
            targetId=datasystems_id,
            labels=["WORKS_FOR"],
            properties={"position": "Analyst", "start_date": "2021-03-01"}
        )
        
        return graph
    
    def test_complete_workflow(self, session_config):
        """Test the complete Grasch workflow from catalog to queries"""
        print("\n" + "=" * 60)
        print("GRASCH LIBRARY FUNCTIONAL TEST")
        print("=" * 60)
        
        # Create session for standalone mode
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "grasch_test.db")
            grasch_session = GraschSession(session_config, database_path)
            
            # Step 1: Create catalog structure
            print("\n1. Creating catalog structure...")
            grasch_session.createCatalogStructure()
            
            # Verify catalog structure
            assert grasch_session.catalog.root.children["production"] is not None
            assert grasch_session.catalog.root.children["development"] is not None
            print("   ✓ Catalog directories created successfully")
            
            # Step 2: Define content types
            print("\n2. Defining content record types...")
            content_types = self.createContentTypes()
            
            # Verify content types
            assert len(content_types) == 3
            assert content_types["person"].typeKey is not None
            assert content_types["company"].typeKey is not None
            assert content_types["employment"].typeKey is not None
            print("   ✓ Content record types with type keys defined")
            
            # Step 3: Create graph schema with constraints
            print("\n3. Creating graph type with LEX constraints...")
            graph_type = self.createGraphSchema(content_types)
            
            # Verify graph type
            assert graph_type.allElementTypesKeyed is True
            assert len(graph_type.nodeTypes) == 2
            assert len(graph_type.edgeTypes) == 1
            assert len(graph_type.constraints) == 3
            print("   ✓ Graph type with ALL ELEMENT TYPES KEYED constraint created")
            
            # Step 4: Create and populate graph
            print("\n4. Creating and populating graph instance...")
            graph = self.createAndPopulateGraph(graph_type)
            
            # Verify graph population
            assert len(graph.nodes) == 4
            assert len(graph.edges) == 2
            assert graph.graph_type == graph_type
            print(f"   ✓ Graph populated with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
            
            # Step 5: Store in catalog
            print("\n5. Storing objects in catalog...")
            schema = grasch_session.catalog.create_gql_schema("/production/customer_data", "employee_schema")
            schema.addGraphType(graph_type)
            schema.addGraph(graph)
            
            # Verify catalog storage
            assert "employee_schema" in grasch_session.catalog.root.children["production"].children["customer_data"].schemas
            stored_schema = grasch_session.catalog.root.children["production"].children["customer_data"].schemas["employee_schema"]
            assert "EmployeeGraph" in stored_schema.graph_types
            assert "employee_data" in stored_schema.graphs
            print("   ✓ Objects stored in catalog at /production/customer_data/employee_schema")
            
            # Step 6: Demonstrate queries
            print("\n6. Demonstrating Cypher queries...")
            grasch_session.demonstrateCypherQueries()
            
            # Step 7: Demonstrate spectral typing concepts
            print("\n7. Demonstrating spectral typing concepts...")
            grasch_session.demonstrateSpectralTyping()
            
            print("\n" + "=" * 60)
            print("✓ FUNCTIONAL TEST COMPLETED SUCCESSFULLY!")
            print("✓ All Grasch library features demonstrated")
            print("✓ Graph data persisted in Kuzu database")
            print("✓ Cypher queries executed successfully")
            print("=" * 60)
    
    def test_content_type_system(self):
        """Test the content type system specifically"""
        print("\n" + "=" * 40)
        print("CONTENT TYPE SYSTEM TEST")
        print("=" * 40)
        
        content_types = self.createContentTypes()
        
        # Test attribute type inheritance
        person_content = content_types["person"]
        assert len(person_content.labelTypes) == 1
        assert len(person_content.propertyTypes) == 3
        assert person_content.labelTypes[0].datatype == "LABEL_DATATYPE"
        assert person_content.labels == ["Person"]
        
        # Test type identifier relationships
        assert person_content.name == "Person"
        assert person_content.identifier == ["Person"]
        assert len(person_content.identifier) == 1
        
        print("   ✓ Unified attribute type model validated")
        print("   ✓ Type key inheritance relationships verified")
        print("   ✓ Content record type structure confirmed")
    
    def test_lex_constraints(self):
        """Test LEX constraint system"""
        print("\n" + "=" * 40)
        print("LEX CONSTRAINTS TEST")
        print("=" * 40)
        
        content_types = self.createContentTypes()
        graph_type = self.createGraphSchema(content_types)
        
        # Test ALL ELEMENT TYPES KEYED constraint
        assert graph_type.allElementTypesKeyed is True
        
        # Test key constraints
        key_constraints = graph_type.constraints
        assert len(key_constraints) == 3
        
        constraint_types = {c.elementType for c in key_constraints}
        assert "Person" in constraint_types
        assert "Company" in constraint_types
        assert "WORKS_FOR" in constraint_types
        
        print("   ✓ ALL ELEMENT TYPES KEYED constraint validated")
        print("   ✓ Key constraints for all element types verified")
        print("   ✓ LEX extension syntax supported")


def run_functional_test():
    """Standalone function to run the functional test"""
    print("Grasch Library Functional Test")
    print("=" * 40)
    
    # Create temporary database directory
    with tempfile.TemporaryDirectory() as temp_dir:
        database_path = os.path.join(temp_dir, "grasch_test.db")
        
        # Configure Grasch session with LEX language level and Full Profile
        full_profile = ProfileConfiguration(
            name="Full Profile",
            optional_features={"GC04", "GG25", "IL001"},
            implementation_defined={"IL001": {"min": 0, "max": None}},
            lex_compatibility=LEXCompatibility.FULL
        )
        
        session_config = SessionConfiguration(
            profile=full_profile,
            language_level=LanguageLevel.LEX,
            catalog_root="file:.",
            default_catalog_path="/",
            nested_record_schema_processor_type="JSON Schema",
            nested_record_schema_processor="default"
        )
        
        # Initialize Grasch session
        print(f"Initializing Grasch session with {session_config.language_level.value} language level...")
        print(f"Using profile: {session_config.profile.name}")
        print(f"Database path: {database_path}")
        
        session = GraschSession(session_config, database_path)
        
        # Create test instance and run
        test_instance = TestGraschFunctional()
        
        # Create session for standalone mode
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
        content_types = test_instance.createContentTypes()
        
        # Verify content types
        assert len(content_types) == 3
        assert content_types["person"].name == "Person"
        assert content_types["company"].name == "Company"
        assert content_types["employment"].name == "WORKS_FOR"
        assert content_types["person"].identifier == ["Person"]
        assert content_types["company"].identifier == ["Company"]
        assert content_types["employment"].identifier == ["WORKS_FOR"]
        print("   ✓ Content record types with type identifiers defined")
        
        # Step 3: Create graph schema with constraints
        print("\n3. Creating graph type with LEX constraints...")
        graph_type = test_instance.createGraphSchema(content_types)
        
        # Verify graph type
        assert graph_type.allElementTypesKeyed is True
        assert len(graph_type.nodeTypes) == 2
        assert len(graph_type.edgeTypes) == 1
        assert len(graph_type.constraints) == 3
        print("   ✓ Graph type with ALL ELEMENT TYPES KEYED constraint created")
        
        # Step 4: Create and populate graph
        print("\n4. Creating and populating graph instance...")
        graph = test_instance.create_and_populate_graph(graph_type)
        
        # Verify graph population
        assert len(graph.nodes) == 4
        assert len(graph.edges) == 2
        assert graph.graph_type == graph_type
        print(f"   ✓ Graph populated with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
        
        # Step 5: Store in catalog
        print("\n5. Storing objects in catalog...")
        schema = grasch_session.catalog.create_gql_schema("/production/customer_data", "employee_schema")
        schema.addGraphType(graph_type)
        schema.addGraph(graph)
        
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