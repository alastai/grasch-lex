"""
Schema Validation for Grasch

This module provides validation functionality for graph schema configurations
using the GQL Descriptors JSON Schema.
"""

from typing import Dict, Any, List, Optional, Union
import json
import yaml
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

from .schemas import load_gql_descriptors_schema


class ValidationError(Exception):
    """Raised when schema validation fails."""
    
    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message)
        self.errors = errors or []


class SchemaValidator:
    """
    Validates graph schema configurations against the GQL Descriptors JSON Schema.
    """
    
    def __init__(self):
        if not JSONSCHEMA_AVAILABLE:
            raise ImportError(
                "jsonschema library is required for validation. "
                "Install with: pip install jsonschema"
            )
        
        self._schema = load_gql_descriptors_schema()
        self._validator = Draft202012Validator(self._schema)
    
    def validate_dict(self, data: Dict[str, Any]) -> bool:
        """
        Validate a dictionary against the GQL Descriptors schema.
        
        Args:
            data: Dictionary to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        errors = list(self._validator.iter_errors(data))
        if errors:
            error_messages = [
                f"Path: {'.'.join(str(p) for p in error.absolute_path)} - {error.message}"
                for error in errors
            ]
            raise ValidationError(
                f"Schema validation failed with {len(errors)} error(s)",
                error_messages
            )
        return True
    
    def validate_yaml_file(self, file_path: Union[str, Path]) -> bool:
        """
        Validate a YAML file against the GQL Descriptors schema.
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If validation fails
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValidationError(f"Invalid YAML syntax: {e}")
        
        return self.validate_dict(data)
    
    def validate_json_file(self, file_path: Union[str, Path]) -> bool:
        """
        Validate a JSON file against the GQL Descriptors schema.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If validation fails
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON syntax: {e}")
        
        return self.validate_dict(data)
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the loaded GQL Descriptors schema.
        
        Returns:
            The JSON Schema dictionary
        """
        return self._schema


def validate_graph_schema(data: Union[Dict[str, Any], str, Path]) -> bool:
    """
    Convenience function to validate graph schema data.
    
    Args:
        data: Dictionary, YAML file path, or JSON file path to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If validation fails
    """
    validator = SchemaValidator()
    
    if isinstance(data, dict):
        return validator.validate_dict(data)
    elif isinstance(data, (str, Path)):
        path = Path(data)
        if path.suffix.lower() in ['.yaml', '.yml']:
            return validator.validate_yaml_file(path)
        elif path.suffix.lower() == '.json':
            return validator.validate_json_file(path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")