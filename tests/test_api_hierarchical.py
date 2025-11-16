"""
Test hierarchical type structures matching SNB-style patterns.
"""

from grasch.api import (
    GraphTypeBuilder,
    NodeTypesBuilder,
    EdgeTypesBuilder,
    TypeInterpretationBuilder,
    NodeTypeBuilder,
    EdgeTypeBuilder,
)


def test_snb_message_hierarchy():
    """
    Test SNB Message hierarchy:
    - Message (abstract)
      - Comment (concrete)
      - Post (concrete)
    """
    # Abstract supertype
    message = (
        NodeTypeBuilder("Message")
        .addProperty("id", "STRING", notNull=True)
        .addProperty("creationDate", "DATETIME", notNull=True)
        .addProperty("content", "STRING")
        .asAbstract()
        .build()
    )
    
    # Concrete subtypes
    comment = (
        NodeTypeBuilder("Comment")
        .addSupertype("Message")
        .addProperty("browserUsed", "STRING")
        .build()
    )
    
    post = (
        NodeTypeBuilder("Post")
        .addSupertype("Message")
        .addProperty("imageFile", "STRING")
        .addProperty("language", "STRING")
        .build()
    )
    
    # Create nested interpretation structure
    concrete_types_interp = (
        TypeInterpretationBuilder("exact")
        .addType(comment)
        .addType(post)
        .build()
    )
    
    abstract_interp = (
        TypeInterpretationBuilder("abstractSupertypes")
        .addType(message)
        .addNestedInterpretation(concrete_types_interp)
        .build()
    )
    
    node_types = (
        NodeTypesBuilder()
        .addInterpretation(abstract_interp)
        .build()
    )
    
    # Verify structure
    all_types = node_types.getAllNodeTypes()
    assert len(all_types) == 3
    
    message_type = node_types.findNodeType("Message")
    assert message_type is not None
    assert message_type.isAbstract() is True
    assert len(message_type.getPropertyTypes()) == 3
    
    comment_type = node_types.findNodeType("Comment")
    assert comment_type is not None
    assert comment_type.isAbstract() is False
    assert "Message" in comment_type.getSupertypes()
    
    post_type = node_types.findNodeType("Post")
    assert post_type is not None
    assert "Message" in post_type.getSupertypes()


def test_snb_organisation_hierarchy():
    """
    Test SNB Organisation hierarchy:
    - Organisation (abstract)
      - Company (concrete)
      - University (concrete)
    """
    organisation = (
        NodeTypeBuilder("Organisation")
        .addProperty("id", "STRING", notNull=True)
        .addProperty("name", "STRING", notNull=True)
        .addProperty("url", "STRING")
        .asAbstract()
        .build()
    )
    
    company = (
        NodeTypeBuilder("Company")
        .addSupertype("Organisation")
        .build()
    )
    
    university = (
        NodeTypeBuilder("University")
        .addSupertype("Organisation")
        .build()
    )
    
    concrete_interp = (
        TypeInterpretationBuilder("exact")
        .addType(company)
        .addType(university)
        .build()
    )
    
    abstract_interp = (
        TypeInterpretationBuilder("abstractSupertypes")
        .addType(organisation)
        .addNestedInterpretation(concrete_interp)
        .build()
    )
    
    node_types = (
        NodeTypesBuilder()
        .addInterpretation(abstract_interp)
        .build()
    )
    
    assert len(node_types.getAllNodeTypes()) == 3
    assert node_types.findNodeType("Organisation").isAbstract() is True
    assert node_types.findNodeType("Company").isAbstract() is False


def test_multiple_interpretations():
    """Test graph type with multiple separate interpretations"""
    # First interpretation: Person nodes (exact)
    person = NodeTypeBuilder("Person").addProperty("name", "STRING").build()
    person_interp = TypeInterpretationBuilder("exact").addType(person).build()
    
    # Second interpretation: Message hierarchy (abstract + subtypes)
    message = NodeTypeBuilder("Message").asAbstract().build()
    comment = NodeTypeBuilder("Comment").addSupertype("Message").build()
    post = NodeTypeBuilder("Post").addSupertype("Message").build()
    
    message_concrete_interp = (
        TypeInterpretationBuilder("exact")
        .addType(comment)
        .addType(post)
        .build()
    )
    
    message_abstract_interp = (
        TypeInterpretationBuilder("abstractSupertypes")
        .addType(message)
        .addNestedInterpretation(message_concrete_interp)
        .build()
    )
    
    # Combine into NodeTypes
    node_types = (
        NodeTypesBuilder()
        .addInterpretation(person_interp)
        .addInterpretation(message_abstract_interp)
        .build()
    )
    
    # Verify all types are accessible
    assert len(node_types.getInterpretations()) == 2
    assert len(node_types.getAllNodeTypes()) == 4
    assert node_types.findNodeType("Person") is not None
    assert node_types.findNodeType("Message") is not None
    assert node_types.findNodeType("Comment") is not None
    assert node_types.findNodeType("Post") is not None


def test_edge_types_with_message_hierarchy():
    """Test edge types that reference hierarchical node types"""
    # Node types
    person = NodeTypeBuilder("Person").build()
    message = NodeTypeBuilder("Message").asAbstract().build()
    comment = NodeTypeBuilder("Comment").addSupertype("Message").build()
    post = NodeTypeBuilder("Post").addSupertype("Message").build()
    
    # Edge types referencing the hierarchy
    has_creator = (
        EdgeTypeBuilder("HAS_CREATOR", "Message", "Person")
        .build()
    )
    
    reply_of = (
        EdgeTypeBuilder("REPLY_OF", "Comment", "Message")
        .build()
    )
    
    likes = (
        EdgeTypeBuilder("LIKES", "Person", "Message")
        .addProperty("creationDate", "DATETIME")
        .build()
    )
    
    edge_interp = (
        TypeInterpretationBuilder("exact")
        .addType(has_creator)
        .addType(reply_of)
        .addType(likes)
        .build()
    )
    
    edge_types = (
        EdgeTypesBuilder()
        .addInterpretation(edge_interp)
        .build()
    )
    
    assert len(edge_types.getAllEdgeTypes()) == 3
    
    has_creator_type = edge_types.findEdgeType("HAS_CREATOR")
    assert has_creator_type.getFirstEndpointNodeType() == "Message"
    assert has_creator_type.getSecondEndpointNodeType() == "Person"
    
    reply_of_type = edge_types.findEdgeType("REPLY_OF")
    assert reply_of_type.getFirstEndpointNodeType() == "Comment"
    assert reply_of_type.getSecondEndpointNodeType() == "Message"


def test_complete_snb_style_graph():
    """Test a complete SNB-style graph with hierarchical types"""
    # Node types: Person (exact)
    person = NodeTypeBuilder("Person").addProperty("id", "STRING").build()
    person_interp = TypeInterpretationBuilder("exact").addType(person).build()
    
    # Node types: Message hierarchy
    message = (
        NodeTypeBuilder("Message")
        .addProperty("id", "STRING")
        .addProperty("content", "STRING")
        .asAbstract()
        .build()
    )
    comment = NodeTypeBuilder("Comment").addSupertype("Message").build()
    post = NodeTypeBuilder("Post").addSupertype("Message").build()
    
    message_concrete = (
        TypeInterpretationBuilder("exact")
        .addType(comment)
        .addType(post)
        .build()
    )
    message_abstract = (
        TypeInterpretationBuilder("abstractSupertypes")
        .addType(message)
        .addNestedInterpretation(message_concrete)
        .build()
    )
    
    node_types = (
        NodeTypesBuilder()
        .addInterpretation(person_interp)
        .addInterpretation(message_abstract)
        .build()
    )
    
    # Edge types
    has_creator = EdgeTypeBuilder("HAS_CREATOR", "Message", "Person").build()
    likes = EdgeTypeBuilder("LIKES", "Person", "Message").build()
    
    edge_interp = (
        TypeInterpretationBuilder("exact")
        .addType(has_creator)
        .addType(likes)
        .build()
    )
    edge_types = EdgeTypesBuilder().addInterpretation(edge_interp).build()
    
    # Complete graph type
    graph_type = (
        GraphTypeBuilder()
        .withNodeTypes(node_types)
        .withEdgeTypes(edge_types)
        .build()
    )
    
    # Verify complete structure
    assert len(graph_type.getNodeTypes().getAllNodeTypes()) == 4
    assert len(graph_type.getEdgeTypes().getAllEdgeTypes()) == 2
    
    # Verify we can find all types
    assert graph_type.findNodeType("Person") is not None
    assert graph_type.findNodeType("Message") is not None
    assert graph_type.findNodeType("Comment") is not None
    assert graph_type.findNodeType("Post") is not None
    assert graph_type.findEdgeType("HAS_CREATOR") is not None
    assert graph_type.findEdgeType("LIKES") is not None


def test_deeply_nested_interpretations():
    """Test deeply nested interpretation structures"""
    # Level 3: Concrete types
    comment = NodeTypeBuilder("Comment").addSupertype("Message").build()
    post = NodeTypeBuilder("Post").addSupertype("Message").build()
    
    level3_interp = (
        TypeInterpretationBuilder("exact")
        .addType(comment)
        .addType(post)
        .build()
    )
    
    # Level 2: Message abstract type
    message = NodeTypeBuilder("Message").addSupertype("Content").asAbstract().build()
    
    level2_interp = (
        TypeInterpretationBuilder("abstractSupertypes")
        .addType(message)
        .addNestedInterpretation(level3_interp)
        .build()
    )
    
    # Level 1: Content abstract type
    content = NodeTypeBuilder("Content").asAbstract().build()
    
    level1_interp = (
        TypeInterpretationBuilder("abstractSupertypes")
        .addType(content)
        .addNestedInterpretation(level2_interp)
        .build()
    )
    
    node_types = NodeTypesBuilder().addInterpretation(level1_interp).build()
    
    # Verify all types are found
    all_types = node_types.getAllNodeTypes()
    assert len(all_types) == 4
    assert node_types.findNodeType("Content") is not None
    assert node_types.findNodeType("Message") is not None
    assert node_types.findNodeType("Comment") is not None
    assert node_types.findNodeType("Post") is not None


if __name__ == "__main__":
    test_snb_message_hierarchy()
    test_snb_organisation_hierarchy()
    test_multiple_interpretations()
    test_edge_types_with_message_hierarchy()
    test_complete_snb_style_graph()
    test_deeply_nested_interpretations()
    print("All hierarchical tests passed!")
