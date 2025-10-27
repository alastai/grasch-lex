"""
Grasch Examples

This module contains example graph schema configurations that demonstrate
the use of the Grasch library and GQL descriptors.
"""

from pathlib import Path

# Get the directory containing this module
_EXAMPLES_DIR = Path(__file__).parent

def get_snb_schema_path() -> Path:
    """
    Get the path to the SNB (Social Network Benchmark) example schema.
    
    Returns:
        Path to the SNB schema YAML file
    """
    return _EXAMPLES_DIR / "snb_schema.yaml"

def get_example_path(example_name: str) -> Path:
    """
    Get the path to an example file.
    
    Args:
        example_name: Name of the example file (with extension)
        
    Returns:
        Path to the example file
    """
    return _EXAMPLES_DIR / example_name

__all__ = ['get_snb_schema_path', 'get_example_path']