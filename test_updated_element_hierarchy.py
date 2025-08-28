#!/usr/bin/env python3
"""
Test script for the updated ElementType hierarchy with new direction model
"""

from src.grasch.types import (
    ElementType, NodeType, EdgeType, ContentRecordType, 
    LabelType, PropertyType, EdgeDirection
)

def test_updated_element_type_hierarchy():
    """Test the updated ElementType hierarchy implementation"""
    
    # Create content record types
    person_content = ContentRecordType("PersonContent")
    person_content.add_label_type(LabelType("Person"))
    person_content.add_property_type(PropertyType("name", "STRING", not_null=True))
    
    company_content = ContentRecordType("CompanyContent")
    company_content.add_label_type(LabelType("Company"))
    company_content.add_property_type(PropertyType("name", "STRING", not_null=True))
    
    works_for_content = ContentRecordType("WorksForContent")
    works_for_content.add_label_type(LabelType("WORKS_FOR"))
    works_for_content.add_property_type(PropertyType("position", "STRING"))
    
    # Create node types
    person_type = NodeType("Person", person_content)
    company_type = NodeType("Company", company_content)
    
    print("✓ Created NodeType instances")
    
    # Test NodeType inheritance from ElementType
    assert isinstance(person_type, ElementType)
    assert person_type.get_element_kind() == "node"
    assert person_type.identifying_content_type == person_content
    assert person_type.name == "Person"
    
    print("✓ NodeType correctly inherits from ElementType")
    
    # Create undirected edge (no direction specified)
    undirected_edge = EdgeType("KNOWS", person_type, person_type, works_for_content)
    
    # Create directed edges with explicit directions
    first_to_second_edge = EdgeType("WORKS_FOR", person_type, company_type, works_for_content, 
                                   EdgeDirection.first_to_second())
    second_to_first_edge = EdgeType("MANAGES", company_type, person_type, works_for_content,
                                   EdgeDirection.second_to_first())
    
    print("✓ Created EdgeType instances with different directions")
    
    # Test EdgeType inheritance from ElementType
    assert isinstance(first_to_second_edge, ElementType)
    assert first_to_second_edge.get_element_kind() == "edge"
    assert first_to_second_edge.identifying_content_type == works_for_content
    
    print("✓ EdgeType correctly inherits from ElementType")
    
    # Test undirected edge properties
    assert undirected_edge.is_undirected
    assert not undirected_edge.is_directed
    assert undirected_edge.tail_node_type is None
    assert undirected_edge.head_node_type is None
    
    print("✓ Undirected edge properties work correctly")
    
    # Test first-to-second directed edge
    assert first_to_second_edge.is_directed
    assert not first_to_second_edge.is_undirected
    assert first_to_second_edge.tail_node_type == person_type  # first
    assert first_to_second_edge.head_node_type == company_type  # second
    
    print("✓ First-to-second direction works correctly")
    
    # Test second-to-first directed edge
    assert second_to_first_edge.is_directed
    assert not second_to_first_edge.is_undirected
    assert second_to_first_edge.tail_node_type == person_type  # second
    assert second_to_first_edge.head_node_type == company_type  # first
    
    print("✓ Second-to-first direction works correctly")
    
    # Test backward compatibility properties
    # For undirected edges
    assert undirected_edge.source_type == person_type  # first
    assert undirected_edge.target_type == person_type  # second (same in this case)
    
    # For directed edges
    assert first_to_second_edge.source_type == first_to_second_edge.tail_node_type
    assert first_to_second_edge.target_type == first_to_second_edge.head_node_type
    
    print("✓ Backward compatibility properties work")
    
    # Test same node type with different directions
    self_first_to_second = EdgeType("MENTORS", person_type, person_type, works_for_content,
                                   EdgeDirection.first_to_second())
    self_second_to_first = EdgeType("REPORTS_TO", person_type, person_type, works_for_content,
                                   EdgeDirection.second_to_first())
    
    # Both should have same node types but different tail/head assignments
    assert self_first_to_second.tail_node_type == person_type
    assert self_first_to_second.head_node_type == person_type
    assert self_second_to_first.tail_node_type == person_type
    assert self_second_to_first.head_node_type == person_type
    
    # But the direction objects should be different
    assert self_first_to_second.direction.tail_reference == "first"
    assert self_first_to_second.direction.head_reference == "second"
    assert self_second_to_first.direction.tail_reference == "second"
    assert self_second_to_first.direction.head_reference == "first"
    
    print("✓ Same node type with different directions works correctly")
    
    # Test EdgeDirection validation
    try:
        EdgeDirection("invalid", "second")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be 'first' or 'second'" in str(e)
    
    try:
        EdgeDirection("first", "invalid")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be 'first' or 'second'" in str(e)
    
    print("✓ EdgeDirection validation works correctly")
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED!")
    print("✓ Updated ElementType hierarchy implemented correctly")
    print("✓ NodeType and EdgeType inherit from ElementType")
    print("✓ EdgeDirection as ordered pair (tail, head) works")
    print("✓ No default direction - None means undirected")
    print("✓ Flexible tail/head mapping based on direction")
    print("✓ Backward compatibility maintained")
    print("="*60)

if __name__ == "__main__":
    test_updated_element_type_hierarchy()