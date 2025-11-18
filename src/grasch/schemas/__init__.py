"""
Grasch Schema Validation

This module contains JSON Schema definitions for validating graph schema configurations
that conform to the GQL (Graph Query Language) standard descriptors.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

# Get the directory containing this module
_SCHEMAS_DIR = Path(__file__).parent

def load_gql_descriptors_schema() -> Dict[str, Any]:
    """
    Load the LEX-2026 JSON Schema for validating graph schema configurations.
    
    Returns:
        Dict containing the JSON Schema for LEX-2026 specifications
    """
    schema_path = _SCHEMAS_DIR / "lex-2026.0.3.2.schema.json"
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_schema_path(schema_name: str) -> Path:
    """
    Get the path to a schema file.
    
    Args:
        schema_name: Name of the schema file (with or without extension)
        
    Returns:
        Path to the schema file
    """
    if schema_name == "gql-descriptors" or schema_name == "gql_descriptors":
        return _SCHEMAS_DIR / "lex-2026.0.3.2.schema.json"
    elif schema_name == "lex-2026" or schema_name == "lex_2026":
        return _SCHEMAS_DIR / "lex-2026.0.3.2.schema.json"
    elif not schema_name.endswith('.json'):
        return _SCHEMAS_DIR / f"{schema_name}.schema.json"
    else:
        return _SCHEMAS_DIR / schema_name

# Export the main schema loader
__all__ = ['load_gql_descriptors_schema', 'get_schema_path']