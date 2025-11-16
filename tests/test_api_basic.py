"""
Test basic API functionality with simple examples.
"""

from grasch.api import (
    CatalogBuilder,
    GraphSchemaBuilder,
    GraphTypeBuilder,
    NodeTypesBuilder,
    EdgeTypesBuilder,
    TypeInterpretationBuilder,
    NodeTypeBuilder,
    EdgeTypeBuilder,
    PropertyTypeBuilder,
)


def test_simple_node_type():
    """Test creating a simple node type"""
    person = (
        NodeTypeBuilder("Person")
        .addProperty("name", "STRING", notNull=True)
        .addProperty("age", "INTEGER")
        .build()
    )
    
    assert person.getTypeLabel() == "Person"
    assert person.getLabels() == ["Person"]
    assert len(person.getPropertyTypes()) == 2
    assert person.getPropertyTypes()[0].getName() == "name"
    assert person.getPropertyTypes()[0].isNotNull() is True
    assert person.getPropertyTypes()[1].getName() == "age"
    assert person.getPropertyTypes()[1].isNotNull() is False


def test_simple_edge_type():
    """Test creating a simple edge type"""
    knows = (
        EdgeTypeBuilder("KNOWS", "Person", "Person")
        .addProperty("since", "DATE")
        .build()
    )
    
    assert knows.getTypeLabel() == "KNOWS"
    assert knows.getDirection() == "DIRECTED"
    assert knows.getFirstEndpointNodeType() == "Person"
    assert knows.getSecondEndpointNodeType() == "Person"
    assert len(knows.getPropertyTypes()) == 1


def test_node_type_with_inheritance():
    """Test creating node types with inheritance"""
    # Abstract base type
    entity = (
        NodeTypeBuilder("Entity")
        .addProperty("id", "STRING", notNull=True)
        .asAbstract()
        .build()
    )
    
    # Concrete subtype
    person = (
        NodeTypeBuilder("Person")
        .addSupertype("Entity")
        .addProperty("name", "STRING")
        .build()
    )
    
    assert entity.isAbstract() is True
    assert person.isAbstract() is False
    assert person.getSupertypes() == ["Entity"]


def test_type_interpretation_exact():
    """Test creating an exact type interpretation"""
    person = NodeTypeBuilder("Person").addProperty("name", "STRING").build()
    company = NodeTypeBuilder("Company").addProperty("name", "STRING").build()
    
    interpretation = (
        TypeInterpretationBuilder("exact")
        .addType(person)
        .addType(company)
        .build()
    )
    
    assert interpretation.getInterpretationMode() == "exact"
    assert len(interpretation.getTypes()) == 2
    assert interpretation.isAbstract() is False


def test_type_interpretation_with_subtypes():
    """Test creating a type interpretation with subtype allowance"""
    message = NodeTypeBuilder("Message").addProperty("content", "STRING").build()
    
    interpretation = (
        TypeInterpretationBuilder("allowSubtypes")
        .addType(message)
        .build()
    )
    
    assert interpretation.getInterpretationMode() == "allowSubtypes"
    assert interpretation.isAbstract() is False


def test_nested_type_interpretations():
    """Test creating nested type interpretations"""
    # Abstract supertypes
    entity = NodeTypeBuilder("Entity").asAbstract().build()
    
    # Concrete subtypes
    person = NodeTypeBuilder("Person").addSupertype("Entity").build()
    company = NodeTypeBuilder("Company").addSupertype("Entity").build()
    
    # Nested interpretation for subtypes
    subtypes_interp = (
        TypeInterpretationBuilder("exact")
        .addType(person)
        .addType(company)
        .build()
    )
    
    # Top-level interpretation with abstract supertypes
    top_interp = (
        TypeInterpretationBuilder("abstractSupertypes")
        .addType(entity)
        .addNestedInterpretation(subtypes_interp)
        .build()
    )
    
    assert top_interp.isAbstract() is True
    assert len(top_interp.getNestedInterpretations()) == 1
    assert len(top_interp.getTypes()) == 1


def test_node_types_collection():
    """Test NodeTypes collection with multiple interpretations"""
    person = NodeTypeBuilder("Person").build()
    company = NodeTypeBuilder("Company").build()
    
    interpretation = (
        TypeInterpretationBuilder("exact")
        .addType(person)
        .addType(company)
        .build()
    )
    
    node_types = (
        NodeTypesBuilder()
        .addInterpretation(interpretation)
        .build()
    )
    
    assert len(node_types.getInterpretations()) == 1
    assert len(node_types.getAllNodeTypes()) == 2
    assert node_types.findNodeType("Person") is not None
    assert node_types.findNodeType("Company") is not None
    assert node_types.findNodeType("Unknown") is None


def test_edge_types_collection():
    """Test EdgeTypes collection"""
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    works_at = EdgeTypeBuilder("WORKS_AT", "Person", "Company").build()
    
    interpretation = (
        TypeInterpretationBuilder("exact")
        .addType(knows)
        .addType(works_at)
        .build()
    )
    
    edge_types = (
        EdgeTypesBuilder()
        .addInterpretation(interpretation)
        .build()
    )
    
    assert len(edge_types.getAllEdgeTypes()) == 2
    assert edge_types.findEdgeType("KNOWS") is not None
    assert edge_types.findEdgeType("WORKS_AT") is not None


def test_graph_type():
    """Test creating a complete graph type"""
    # Node types
    person = NodeTypeBuilder("Person").addProperty("name", "STRING").build()
    node_interp = TypeInterpretationBuilder("exact").addType(person).build()
    node_types = NodeTypesBuilder().addInterpretation(node_interp).build()
    
    # Edge types
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    edge_interp = TypeInterpretationBuilder("exact").addType(knows).build()
    edge_types = EdgeTypesBuilder().addInterpretation(edge_interp).build()
    
    # Graph type
    graph_type = (
        GraphTypeBuilder()
        .withNodeTypes(node_types)
        .withEdgeTypes(edge_types)
        .build()
    )
    
    assert graph_type.findNodeType("Person") is not None
    assert graph_type.findEdgeType("KNOWS") is not None
    assert graph_type.getNodeTypeMinimumLabels() == 1
    assert graph_type.getEdgeTypeMinimumLabels() == 1


def test_graph_schema():
    """Test creating a graph schema"""
    # Create a simple graph type
    person = NodeTypeBuilder("Person").build()
    node_interp = TypeInterpretationBuilder("exact").addType(person).build()
    node_types = NodeTypesBuilder().addInterpretation(node_interp).build()
    
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    edge_interp = TypeInterpretationBuilder("exact").addType(knows).build()
    edge_types = EdgeTypesBuilder().addInterpretation(edge_interp).build()
    
    graph_type = (
        GraphTypeBuilder()
        .withNodeTypes(node_types)
        .withEdgeTypes(edge_types)
        .build()
    )
    
    # Create schema
    schema = (
        GraphSchemaBuilder("social_network_schema")
        .withGraphType(graph_type)
        .withValueTypeSystem("CANONICAL")
        .withPrincipal("admin")
        .build()
    )
    
    assert schema.getPathName() == "social_network_schema"
    assert schema.getPrincipal() == "admin"
    assert schema.getValueTypeSystemName() == "CANONICAL"
    assert schema.getGraphType() is not None


def test_catalog():
    """Test creating a catalog with schemas"""
    # Create a simple schema
    person = NodeTypeBuilder("Person").build()
    node_interp = TypeInterpretationBuilder("exact").addType(person).build()
    node_types = NodeTypesBuilder().addInterpretation(node_interp).build()
    
    knows = EdgeTypeBuilder("KNOWS", "Person", "Person").build()
    edge_interp = TypeInterpretationBuilder("exact").addType(knows).build()
    edge_types = EdgeTypesBuilder().addInterpretation(edge_interp).build()
    
    graph_type = (
        GraphTypeBuilder()
        .withNodeTypes(node_types)
        .withEdgeTypes(edge_types)
        .build()
    )
    
    schema = (
        GraphSchemaBuilder("social_schema")
        .withGraphType(graph_type)
        .build()
    )
    
    # Create catalog
    catalog = (
        CatalogBuilder("my_catalog")
        .withIRI("http://example.com/catalogs/my_catalog")
        .addGraphSchema(schema)
        .build()
    )
    
    assert catalog.getPathName() == "my_catalog"
    assert catalog.getIRI() == "http://example.com/catalogs/my_catalog"
    assert len(catalog.getGraphSchemas()) == 1
    assert catalog.findGraphSchema("social_schema") is not None
    assert catalog.findGraphSchema("unknown") is None


if __name__ == "__main__":
    test_simple_node_type()
    test_simple_edge_type()
    test_node_type_with_inheritance()
    test_type_interpretation_exact()
    test_type_interpretation_with_subtypes()
    test_nested_type_interpretations()
    test_node_types_collection()
    test_edge_types_collection()
    test_graph_type()
    test_graph_schema()
    test_catalog()
    print("All tests passed!")
