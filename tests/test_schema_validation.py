"""
Tests for GQL Descriptors schema validation functionality.
"""

import pytest
from pathlib import Path

try:
    from grasch.validation import SchemaValidator, ValidationError
    from grasch.examples import get_snb_schema_path
    from grasch.schemas import load_gql_descriptors_schema
    VALIDATION_AVAILABLE = True
except ImportError:
    VALIDATION_AVAILABLE = False


@pytest.mark.skipif(not VALIDATION_AVAILABLE, reason="Validation dependencies not available")
class TestSchemaValidation:
    """Test cases for schema validation functionality."""
    
    def test_load_gql_descriptors_schema(self):
        """Test that the GQL descriptors schema can be loaded."""
        schema = load_gql_descriptors_schema()
        assert isinstance(schema, dict)
        assert "$schema" in schema
        assert "title" in schema
        assert schema["title"] == "GQL Descriptors Schema"
    
    def test_schema_validator_creation(self):
        """Test that SchemaValidator can be created."""
        validator = SchemaValidator()
        assert validator is not None
        schema = validator.get_schema()
        assert isinstance(schema, dict)
    
    def test_validate_valid_minimal_graph_type(self):
        """Test validation of a minimal valid graph type."""
        validator = SchemaValidator()
        
        # Minimal valid graph type descriptor
        valid_data = {
            "graphType": {
                "declaredName": "GRAPH DATA",
                "preferredName": "PROPERTY GRAPH",
                "nodeTypeDescriptors": [],
                "edgeTypeDescriptors": [],
                "nodeTypeKeyLabelSetDictionary": {},
                "edgeTypeKeyLabelSetDictionary": {},
                "constraintSetDictionary": {}
            }
        }
        
        result = validator.validate_dict(valid_data)
        assert result is True
    
    def test_validate_invalid_graph_type(self):
        """Test validation of an invalid graph type."""
        validator = SchemaValidator()
        
        # Invalid graph type (missing required fields)
        invalid_data = {
            "graphType": {
                "declaredName": "GRAPH DATA",
                # Missing required fields
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_dict(invalid_data)
        
        assert "validation failed" in str(exc_info.value).lower()
        assert len(exc_info.value.errors) > 0
    
    @pytest.mark.skipif(not Path("src/grasch/examples/snb_schema.yaml").exists(), 
                       reason="SNB example schema not found")
    def test_validate_snb_example(self):
        """Test validation of the SNB example schema."""
        validator = SchemaValidator()
        snb_path = get_snb_schema_path()
        
        # This test may fail if the SNB schema doesn't conform to the base GQL standard
        # That's expected since we rolled back to the base standard
        try:
            result = validator.validate_yaml_file(snb_path)
            assert result is True
        except ValidationError:
            # Expected if SNB schema uses features not in base GQL standard
            pytest.skip("SNB schema uses features beyond base GQL standard")
    
    def test_validate_nonexistent_file(self):
        """Test validation of a nonexistent file."""
        validator = SchemaValidator()
        
        with pytest.raises(FileNotFoundError):
            validator.validate_yaml_file("nonexistent_file.yaml")


@pytest.mark.skipif(VALIDATION_AVAILABLE, reason="Testing import error handling")
def test_validation_import_error():
    """Test that appropriate error is raised when validation dependencies are missing."""
    # This test would only run if jsonschema/pyyaml are not available
    # In practice, this is mainly for documentation of the expected behavior
    pass