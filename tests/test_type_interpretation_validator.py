#!/usr/bin/env python3
"""
Tests for type interpretation validation logic.
Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 7.4, 7.5
"""

import pytest
from src.grasch.type_interpretation_validator import (
    TypeInterpretationValidator,
    AbstractTypeInstantiationError,
    ExactMatchViolationError
)
from src.grasch.type_interpretation import TypeInterpretation
from src.grasch.types import (
    NodeType, EdgeType, GraphType, ArcType,
    ContentRecordType, EdgeDirection
)


class TestAbstractTypeValidation:
    """Tests for abstract type validation (Task 5.1)."""
    
    def test_abstract_type_cannot_be_directly_instantiated(self):
        """Test that abstract types cannot be directly instantiated."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.subtypesAbstract('Vehicle')
        
        with pytest.raises(AbstractTypeInstantiationError) as exc_info:
            validator.validate_abstract_type_not_instantiated(interp, is_direct_instance=True)
        
        assert 'Vehicle' in str(exc_info.value)
    
    def test_abstract_type_allows_subtype_instances(self):
        """Test that abstract types allow subtype instances."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.subtypesAbstract('Vehicle')
        validator.validate_abstract_type_not_instantiated(interp, is_direct_instance=False)
    
    def test_concrete_type_allows_direct_instantiation(self):
        """Test that concrete types allow direct instantiation."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.exactlyConcrete('Car')
        validator.validate_abstract_type_not_instantiated(interp, is_direct_instance=True)


class TestExactMatchValidation:
    """Tests for exact match validation (Task 5.2)."""
    
    def test_exact_match_rejects_subtypes(self):
        """Test that exact match types reject subtypes."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.exactlyConcrete('Car')
        
        with pytest.raises(ExactMatchViolationError):
            validator.validate_exact_match(interp, 'Car', 'SportsCar')
    
    def test_exact_match_accepts_same_type(self):
        """Test that exact match types accept the same type."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.exactlyConcrete('Car')
        validator.validate_exact_match(interp, 'Car', 'Car')


class TestSubtypeMatchValidation:
    """Tests for subtype match validation (Task 5.3)."""
    
    def test_subtype_match_accepts_exact_type(self):
        """Test that subtype match accepts the exact type."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.subtypesConcrete('Vehicle')
        result = validator.validate_subtype_match(interp, 'Vehicle', 'Vehicle', is_subtype=False)
        assert result is True
    
    def test_subtype_match_accepts_subtypes(self):
        """Test that subtype match accepts subtypes."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.subtypesConcrete('Vehicle')
        result = validator.validate_subtype_match(interp, 'Vehicle', 'Car', is_subtype=True)
        assert result is True


class TestConcreteTypeValidation:
    """Tests for concrete type validation (Task 5.4)."""
    
    def test_concrete_type_can_be_instantiated(self):
        """Test that concrete types can be directly instantiated."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.exactlyConcrete('Car')
        result = validator.validate_concrete_type_instantiation(interp)
        assert result is True
    
    def test_abstract_type_cannot_be_instantiated(self):
        """Test that abstract types cannot be directly instantiated."""
        validator = TypeInterpretationValidator()
        interp = TypeInterpretation.subtypesAbstract('Vehicle')
        result = validator.validate_concrete_type_instantiation(interp)
        assert result is False


class TestConsistentValidation:
    """Tests for consistent validation across element types (Task 5.5)."""
    
    def test_node_type_validation(self):
        """Test validation for NodeType."""
        validator = TypeInterpretationValidator()
        content = ContentRecordType([], [], ['Node'])
        node_type = NodeType(content, interpretation=TypeInterpretation.subtypesAbstract('Node'))
        
        with pytest.raises(AbstractTypeInstantiationError):
            validator.validate_node_type(node_type, 'Node', is_direct_instance=True)
    
    def test_edge_type_validation(self):
        """Test validation for EdgeType."""
        validator = TypeInterpretationValidator()
        content = ContentRecordType([], [], ['Edge'])
        node_type = NodeType(content)
        edge_arc = ArcType(content)
        edge_type = EdgeType('Edge', node_type, node_type, edge_arc, 
                           EdgeDirection.firstToSecond(),
                           interpretation=TypeInterpretation.subtypesAbstract('Edge'))
        
        with pytest.raises(AbstractTypeInstantiationError):
            validator.validate_edge_type(edge_type, 'Edge', is_direct_instance=True)
    
    def test_graph_type_validation(self):
        """Test validation for GraphType."""
        validator = TypeInterpretationValidator()
        graph_type = GraphType('Graph', interpretation=TypeInterpretation.subtypesAbstract('Graph'))
        
        with pytest.raises(AbstractTypeInstantiationError):
            validator.validate_graph_type(graph_type, 'Graph', is_direct_instance=True)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
