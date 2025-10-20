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
    personContent = ContentRecordType("PersonContent")
    personContent.addLabelType(LabelType("Person"))
    personContent.addPropertyType(PropertyType("name", "STRING", not_null=True))
    
    companyContent = ContentRecordType("CompanyContent")
    companyContent.addLabelType(LabelType("Company"))
    companyContent.addPropertyType(PropertyType("name", "STRING", not_null=True))
    
    worksForContent = ContentRecordType("WorksForContent")
    worksForContent.addLabelType(LabelType("WORKS_FOR"))
    worksForContent.addPropertyType(PropertyType("position", "STRING"))
    
    # Create node types
    personType = NodeType("Person", personContent)
    companyType = NodeType("Company", companyContent)
    
    print("✓ Created NodeType instances")
    
    # Test NodeType inheritance from ElementType
    assert isinstance(personType, ElementType)
    assert personType.getElementKind() == "node"
    assert personType.identifyingContentType == personContent
    assert personType.name == "Person"
    
    print("✓ NodeType correctly inherits from ElementType")
    
    # Create undirected edge (no direction specified)
    undirectedEdge = EdgeType("KNOWS", personType, personType, worksForContent)
    
    # Create directed edges with explicit directions
    firstToSecondEdge = EdgeType("WORKS_FOR", personType, companyType, worksForContent, 
                                   EdgeDirection.firstToSecond())
    secondToFirstEdge = EdgeType("MANAGES", companyType, personType, worksForContent,
                                   EdgeDirection.secondToFirst())
    
    print("✓ Created EdgeType instances with different directions")
    
    # Test EdgeType inheritance from ElementType
    assert isinstance(firstToSecondEdge, ElementType)
    assert firstToSecondEdge.getElementKind() == "edge"
    assert firstToSecondEdge.identifyingContentType == worksForContent
    
    print("✓ EdgeType correctly inherits from ElementType")
    
    # Test undirected edge properties
    assert undirectedEdge.isUndirected
    assert not undirectedEdge.isDirected
    assert undirectedEdge.tailNodeType is None
    assert undirectedEdge.headNodeType is None
    
    print("✓ Undirected edge properties work correctly")
    
    # Test first-to-second directed edge
    assert firstToSecondEdge.isDirected
    assert not firstToSecondEdge.isUndirected
    assert firstToSecondEdge.tailNodeType == personType  # first
    assert firstToSecondEdge.headNodeType == companyType  # second
    
    print("✓ First-to-second direction works correctly")
    
    # Test second-to-first directed edge
    assert secondToFirstEdge.isDirected
    assert not secondToFirstEdge.isUndirected
    assert secondToFirstEdge.tailNodeType == personType  # second
    assert secondToFirstEdge.headNodeType == companyType  # first
    
    print("✓ Second-to-first direction works correctly")
    
    # Test backward compatibility properties
    # For undirected edges
    assert undirectedEdge.sourceType == personType  # first
    assert undirectedEdge.targetType == personType  # second (same in this case)
    
    # For directed edges
    assert firstToSecondEdge.sourceType == firstToSecondEdge.tailNodeType
    assert firstToSecondEdge.targetType == firstToSecondEdge.headNodeType
    
    print("✓ Backward compatibility properties work")
    
    # Test same node type with different directions
    selfFirstToSecond = EdgeType("MENTORS", personType, personType, worksForContent,
                                   EdgeDirection.firstToSecond())
    selfSecondToFirst = EdgeType("REPORTS_TO", personType, personType, worksForContent,
                                   EdgeDirection.secondToFirst())
    
    # Both should have same node types but different tail/head assignments
    assert selfFirstToSecond.tailNodeType == personType
    assert selfFirstToSecond.headNodeType == personType
    assert selfSecondToFirst.tailNodeType == personType
    assert selfSecondToFirst.headNodeType == personType
    
    # But the direction objects should be different
    assert selfFirstToSecond.direction.tailReference == "first"
    assert selfFirstToSecond.direction.headReference == "second"
    assert selfSecondToFirst.direction.tailReference == "second"
    assert selfSecondToFirst.direction.headReference == "first"
    
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