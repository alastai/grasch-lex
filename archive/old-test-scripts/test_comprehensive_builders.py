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
    
    personContentBuilder = ContentRecordTypeBuilder()
    
    # Use build methods to get builders, then create and add
    personLabelBuilder = personContentBuilder.buildLabelType("Person")
    personLabel = personLabelBuilder.create()
    personContentBuilder.addLabelType(personLabel)
    
    namePropBuilder = personContentBuilder.buildPropertyType("name", "STRING")
    nameProp = namePropBuilder.setNotNull(True).create()
    personContentBuilder.addPropertyType(nameProp)
    
    agePropBuilder = personContentBuilder.buildPropertyType("age", "INTEGER")
    ageProp = agePropBuilder.create()
    personContentBuilder.addPropertyType(ageProp)
    
    personContent = personContentBuilder.addTypeIdentifier(["Person"]).create()
    
    print(f"   Created PersonContent: {personContent.name}")
    print(f"   Labels: {[label.name for label in personContent.labelTypes]}")
    print(f"   Properties: {[(prop.name, prop.datatype) for prop in personContent.propertyTypes]}")
    
    # 2. Build company content using add methods with pre-built objects
    print("\n2. Building ContentRecordType using addX() methods:")
    
    companyLabel = LabelType("Company")
    companyNameProp = PropertyType("name", "STRING", not_null=True)
    industryProp = PropertyType("industry", "STRING")
    
    companyContent = (ContentRecordTypeBuilder()
                      .addLabelType(companyLabel)
                      .addPropertyType(companyNameProp)
                      .addPropertyType(industryProp)
                      .addTypeIdentifier(["Company"])
                      .create())
    
    print(f"   Created CompanyContent: {companyContent.name}")
    print(f"   Labels: {[label.name for label in companyContent.labelTypes]}")
    print(f"   Properties: {[(prop.name, prop.datatype) for prop in companyContent.propertyTypes]}")
    
    # 3. Build node types using both patterns
    print("\n3. Building NodeTypes:")
    
    # Using build method from graph type builder
    graphBuilder = GraphTypeBuilder("EmploymentGraph")
    personNodeBuilder = graphBuilder.buildNodeType(personContent)
    personNode = personNodeBuilder.create()
    
    # Using pre-built content type
    companyNode = NodeTypeBuilder(companyContent).create()
    
    print(f"   Created PersonNode: {personNode.name}")
    print(f"   Created CompanyNode: {companyNode.name}")
    
    # 4. Build arc type for employment relationship
    print("\n4. Building ArcType:")
    
    employmentContent = (ContentRecordTypeBuilder()
                         .addLabel("WORKS_FOR")
                         .addPropertyType(PropertyType("position", "STRING"))
                         .addPropertyType(PropertyType("startDate", "DATE"))
                         .addTypeIdentifier(["WORKS_FOR"])
                         .create())
    
    employmentArc = ArcTypeBuilder(employmentContent).create()
    print(f"   Created EmploymentArc: {employmentArc.name}")
    
    # 5. Build edge type using comprehensive builder
    print("\n5. Building EdgeType using comprehensive builder:")
    
    edgeBuilder = EdgeTypeBuilder("PersonWorksForCompany")
    
    # Method 1: Using build methods (would create new node types)
    # firstNodeBuilder = edgeBuilder.buildFirstNodeType(personContent)
    # secondNodeBuilder = edgeBuilder.buildSecondNodeType(companyContent)
    # arcBuilder = edgeBuilder.buildArcType(employmentContent)
    
    # Method 2: Using add methods with pre-built objects
    employmentEdge = (edgeBuilder
                      .addFirstNodeType(personNode)
                      .addSecondNodeType(companyNode)
                      .addArcType(employmentArc)
                      .setDirected("first", "second")  # Person -> Company
                      .create())
    
    print(f"   Created EdgeType: {employmentEdge.name}")
    print(f"   First node: {employmentEdge.firstNodeType.name}")
    print(f"   Second node: {employmentEdge.secondNodeType.name}")
    print(f"   Arc type: {employmentEdge.arcType.name}")
    print(f"   Directed: {employmentEdge.isDirected}")
    print(f"   Tail -> Head: {employmentEdge.tailNodeType.name} -> {employmentEdge.headNodeType.name}")
    
    # 6. Build complete graph type
    print("\n6. Building GraphType using comprehensive builder:")
    
    # Method 1: Using build methods
    graphBuilder = GraphTypeBuilder("EmploymentGraph")
    
    # Build content types from scratch
    personContentBuilder2 = graphBuilder.buildContentRecordType()
    personContent2 = (personContentBuilder2
                      .addLabel("Person")
                      .addPropertyType(PropertyType("name", "STRING", not_null=True))
                      .addTypeIdentifier(["Person"])
                      .create())
    
    # Build node type from content type
    personNodeBuilder2 = graphBuilder.buildNodeType(personContent2)
    personNode2 = personNodeBuilder2.create()
    
    # Method 2: Using add methods with pre-built objects
    employmentGraph = (graphBuilder
                       .addNodeType(personNode)
                       .addNodeType(companyNode)
                       .addNodeType(personNode2)  # Show we can add multiple
                       .addEdgeType(employmentEdge)
                       .setAllElementTypesKeyed(True)
                       .create())
    
    print(f"   Created GraphType: {employmentGraph.name}")
    print(f"   Node types: {[nt.name for nt in employmentGraph.nodeTypes]}")
    print(f"   Edge types: {[et.name for et in employmentGraph.edgeTypes]}")
    print(f"   All element types keyed: {employmentGraph.allElementTypesKeyed}")
    
    # 7. Demonstrate recursive building from top level
    print("\n7. Demonstrating recursive building from GraphType level:")
    
    # Start with graph type builder and build everything recursively
    completeGraphBuilder = GraphTypeBuilder("CompleteGraph")
    
    # Build a complete edge type from scratch using nested builders
    edgeBuilder2 = completeGraphBuilder.buildEdgeType("PersonKnowsPerson")
    
    # Build first node type
    personContentBuilder3 = ContentRecordTypeBuilder()
    personContent3 = (personContentBuilder3
                      .addLabel("Person")
                      .addPropertyType(PropertyType("name", "STRING"))
                      .create())
    
    firstNodeBuilder = edgeBuilder2.buildFirstNodeType(personContent3)
    firstNode = firstNodeBuilder.create()
    
    # Build second node type (same type)
    secondNodeBuilder = edgeBuilder2.buildSecondNodeType(personContent3)
    secondNode = secondNodeBuilder.create()
    
    # Build arc type
    knowsContent = (ContentRecordTypeBuilder()
                    .addLabel("KNOWS")
                    .addPropertyType(PropertyType("since", "DATE"))
                    .create())
    
    arcBuilder = edgeBuilder2.buildArcType(knowsContent)
    arc = arcBuilder.create()
    
    # Complete the edge type
    knowsEdge = (edgeBuilder2
                 .addFirstNodeType(firstNode)
                 .addSecondNodeType(secondNode)
                 .addArcType(arc)
                 .setUndirected()  # Undirected friendship
                 .create())
    
    # Add to graph
    completeGraph = (completeGraphBuilder
                     .addNodeType(firstNode)
                     .addEdgeType(knowsEdge)
                     .create())
    
    print(f"   Created complete graph: {completeGraph.name}")
    print(f"   With edge: {knowsEdge.name} (undirected: {knowsEdge.isUndirected})")
    
    print("\n=== Builder Pattern Test Complete ===")
    
    return employment_graph, complete_graph


if __name__ == "__main__":
    test_comprehensive_builder_pattern()