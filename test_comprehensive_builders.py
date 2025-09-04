#!/usr/bin/env python3
"""
Comprehensive test demonstrating the new builder pattern for GQL graph types.

This test shows the complete containment hierarchy:
ContentRecordType → NodeType/ArcType → EdgeType → GraphType

Each builder class XBuilder has:
- buildY() methods that return YBuilder instances
- addY() methods that accept pre-built Y instances
"""

from src.grasch.types import (
    ContentRecordTypeBuilder, NodeTypeBuilder, ArcTypeBuilder, EdgeTypeBuilder, GraphTypeBuilder,
    LabelTypeBuilder, PropertyTypeBuilder, EdgeDirection,
    ContentRecordType, NodeType, ArcType, EdgeType, GraphType,
    LabelType, PropertyType
)


def test_comprehensive_builder_pattern():
    """Test the complete builder pattern with build/add methods"""
    
    print("=== Testing Comprehensive Builder Pattern ===\n")
    
    # 1. Build content record types using build methods
    print("1. Building ContentRecordType using buildX() methods:")
    
    person_content_builder = ContentRecordTypeBuilder()
    
    # Use build methods to get builders, then create and add
    person_label_builder = person_content_builder.buildLabelType("Person")
    person_label = person_label_builder.create()
    person_content_builder.addLabelType(person_label)
    
    name_prop_builder = person_content_builder.buildPropertyType("name", "STRING")
    name_prop = name_prop_builder.setNotNull(True).create()
    person_content_builder.addPropertyType(name_prop)
    
    age_prop_builder = person_content_builder.buildPropertyType("age", "INTEGER")
    age_prop = age_prop_builder.create()
    person_content_builder.addPropertyType(age_prop)
    
    person_content = person_content_builder.addTypeIdentifier(["Person"]).create()
    
    print(f"   Created PersonContent: {person_content.name}")
    print(f"   Labels: {[label.name for label in person_content.label_types]}")
    print(f"   Properties: {[(prop.name, prop.datatype) for prop in person_content.property_types]}")
    
    # 2. Build company content using add methods with pre-built objects
    print("\n2. Building ContentRecordType using addX() methods:")
    
    company_label = LabelType("Company")
    company_name_prop = PropertyType("name", "STRING", not_null=True)
    industry_prop = PropertyType("industry", "STRING")
    
    company_content = (ContentRecordTypeBuilder()
                      .addLabelType(company_label)
                      .addPropertyType(company_name_prop)
                      .addPropertyType(industry_prop)
                      .addTypeIdentifier(["Company"])
                      .create())
    
    print(f"   Created CompanyContent: {company_content.name}")
    print(f"   Labels: {[label.name for label in company_content.label_types]}")
    print(f"   Properties: {[(prop.name, prop.datatype) for prop in company_content.property_types]}")
    
    # 3. Build node types using both patterns
    print("\n3. Building NodeTypes:")
    
    # Using build method from graph type builder
    graph_builder = GraphTypeBuilder("EmploymentGraph")
    person_node_builder = graph_builder.buildNodeType(person_content)
    person_node = person_node_builder.create()
    
    # Using pre-built content type
    company_node = NodeTypeBuilder(company_content).create()
    
    print(f"   Created PersonNode: {person_node.name}")
    print(f"   Created CompanyNode: {company_node.name}")
    
    # 4. Build arc type for employment relationship
    print("\n4. Building ArcType:")
    
    employment_content = (ContentRecordTypeBuilder()
                         .add_label("WORKS_FOR")
                         .addPropertyType(PropertyType("position", "STRING"))
                         .addPropertyType(PropertyType("start_date", "DATE"))
                         .addTypeIdentifier(["WORKS_FOR"])
                         .create())
    
    employment_arc = ArcTypeBuilder(employment_content).create()
    print(f"   Created EmploymentArc: {employment_arc.name}")
    
    # 5. Build edge type using comprehensive builder
    print("\n5. Building EdgeType using comprehensive builder:")
    
    edge_builder = EdgeTypeBuilder("PersonWorksForCompany")
    
    # Method 1: Using build methods (would create new node types)
    # first_node_builder = edge_builder.buildFirstNodeType(person_content)
    # second_node_builder = edge_builder.buildSecondNodeType(company_content)
    # arc_builder = edge_builder.buildArcType(employment_content)
    
    # Method 2: Using add methods with pre-built objects
    employment_edge = (edge_builder
                      .addFirstNodeType(person_node)
                      .addSecondNodeType(company_node)
                      .addArcType(employment_arc)
                      .setDirected("first", "second")  # Person -> Company
                      .create())
    
    print(f"   Created EdgeType: {employment_edge.name}")
    print(f"   First node: {employment_edge.first_node_type.name}")
    print(f"   Second node: {employment_edge.second_node_type.name}")
    print(f"   Arc type: {employment_edge.arc_type.name}")
    print(f"   Directed: {employment_edge.is_directed}")
    print(f"   Tail -> Head: {employment_edge.tail_node_type.name} -> {employment_edge.head_node_type.name}")
    
    # 6. Build complete graph type
    print("\n6. Building GraphType using comprehensive builder:")
    
    # Method 1: Using build methods
    graph_builder = GraphTypeBuilder("EmploymentGraph")
    
    # Build content types from scratch
    person_content_builder2 = graph_builder.buildContentRecordType()
    person_content2 = (person_content_builder2
                      .add_label("Person")
                      .addPropertyType(PropertyType("name", "STRING", not_null=True))
                      .addTypeIdentifier(["Person"])
                      .create())
    
    # Build node type from content type
    person_node_builder2 = graph_builder.buildNodeType(person_content2)
    person_node2 = person_node_builder2.create()
    
    # Method 2: Using add methods with pre-built objects
    employment_graph = (graph_builder
                       .addNodeType(person_node)
                       .addNodeType(company_node)
                       .addNodeType(person_node2)  # Show we can add multiple
                       .addEdgeType(employment_edge)
                       .setAllElementTypesKeyed(True)
                       .create())
    
    print(f"   Created GraphType: {employment_graph.name}")
    print(f"   Node types: {[nt.name for nt in employment_graph.node_types]}")
    print(f"   Edge types: {[et.name for et in employment_graph.edge_types]}")
    print(f"   All element types keyed: {employment_graph.all_element_types_keyed}")
    
    # 7. Demonstrate recursive building from top level
    print("\n7. Demonstrating recursive building from GraphType level:")
    
    # Start with graph type builder and build everything recursively
    complete_graph_builder = GraphTypeBuilder("CompleteGraph")
    
    # Build a complete edge type from scratch using nested builders
    edge_builder2 = complete_graph_builder.buildEdgeType("PersonKnowsPerson")
    
    # Build first node type
    person_content_builder3 = ContentRecordTypeBuilder()
    person_content3 = (person_content_builder3
                      .add_label("Person")
                      .addPropertyType(PropertyType("name", "STRING"))
                      .create())
    
    first_node_builder = edge_builder2.buildFirstNodeType(person_content3)
    first_node = first_node_builder.create()
    
    # Build second node type (same type)
    second_node_builder = edge_builder2.buildSecondNodeType(person_content3)
    second_node = second_node_builder.create()
    
    # Build arc type
    knows_content = (ContentRecordTypeBuilder()
                    .add_label("KNOWS")
                    .addPropertyType(PropertyType("since", "DATE"))
                    .create())
    
    arc_builder = edge_builder2.buildArcType(knows_content)
    arc = arc_builder.create()
    
    # Complete the edge type
    knows_edge = (edge_builder2
                 .addFirstNodeType(first_node)
                 .addSecondNodeType(second_node)
                 .addArcType(arc)
                 .setUndirected()  # Undirected friendship
                 .create())
    
    # Add to graph
    complete_graph = (complete_graph_builder
                     .addNodeType(first_node)
                     .addEdgeType(knows_edge)
                     .create())
    
    print(f"   Created complete graph: {complete_graph.name}")
    print(f"   With edge: {knows_edge.name} (undirected: {knows_edge.is_undirected})")
    
    print("\n=== Builder Pattern Test Complete ===")
    
    return employment_graph, complete_graph


if __name__ == "__main__":
    test_comprehensive_builder_pattern()