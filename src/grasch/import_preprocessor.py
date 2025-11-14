#!/usr/bin/env python3
"""
YAML Import Preprocessor for LEX Schemas

This preprocessor resolves 'import' directives in YAML files recursively,
producing a flattened YAML structure suitable for JSON Schema validation.

Supported import patterns:
1. Whole graphSchema: graphSchema: {import: "schema.yaml"}
2. Defaults block: defaults: {import: "defaults.yaml"}
3. Type subsets: nodeTypes: [{import: "types.yaml"}, ...]
"""

import yaml
from pathlib import Path
from typing import Any, Dict, List, Union


class ImportPreprocessor:
    """Preprocesses YAML files by resolving import directives."""
    
    def __init__(self, base_path: Path):
        """
        Initialize preprocessor with base path for resolving relative imports.
        
        Args:
            base_path: Base directory for resolving relative import paths
        """
        self.base_path = base_path
        self.imported_files = set()  # Track to prevent circular imports
    
    def load_yaml(self, file_path: Path) -> Any:
        """Load a YAML file."""
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    def resolve_import(self, import_spec: Union[str, Dict], current_path: Path) -> Any:
        """
        Resolve an import specification.
        
        Args:
            import_spec: Either a string path or dict with 'import' key
            current_path: Path of the file containing the import
            
        Returns:
            The loaded and processed content from the imported file
        """
        # Extract import path
        if isinstance(import_spec, dict) and 'import' in import_spec:
            import_path = import_spec['import']
        elif isinstance(import_spec, str):
            import_path = import_spec
        else:
            return import_spec
        
        # Resolve relative to current file's directory
        if current_path:
            import_file = current_path.parent / import_path
        else:
            import_file = self.base_path / import_path
        
        # Check for circular imports
        import_file_abs = import_file.resolve()
        if import_file_abs in self.imported_files:
            raise ValueError(f"Circular import detected: {import_file}")
        
        self.imported_files.add(import_file_abs)
        
        # Load and process the imported file
        content = self.load_yaml(import_file)
        processed = self.process(content, import_file)
        
        self.imported_files.remove(import_file_abs)
        
        return processed
    
    def process(self, data: Any, current_path: Path = None) -> Any:
        """
        Recursively process data structure, resolving imports.
        
        Args:
            data: The data structure to process
            current_path: Path of the current file being processed
            
        Returns:
            Processed data with all imports resolved
        """
        if isinstance(data, dict):
            # Check if this is an import directive
            if 'import' in data and len(data) == 1:
                return self.resolve_import(data, current_path)
            
            # Process each key-value pair
            result = {}
            for key, value in data.items():
                if key == 'import':
                    # Standalone import key - resolve and merge
                    imported = self.resolve_import(value, current_path)
                    if isinstance(imported, dict):
                        result.update(imported)
                    else:
                        return imported
                else:
                    result[key] = self.process(value, current_path)
            return result
        
        elif isinstance(data, list):
            # Process list items, flattening imported lists
            result = []
            for item in data:
                if isinstance(item, dict) and 'import' in item and len(item) == 1:
                    # Import directive in list
                    imported = self.resolve_import(item, current_path)
                    if isinstance(imported, list):
                        result.extend(imported)
                    else:
                        result.append(imported)
                else:
                    result.append(self.process(item, current_path))
            return result
        
        else:
            # Primitive value, return as-is
            return data
    
    def process_file(self, file_path: Path) -> Any:
        """
        Process a YAML file, resolving all imports.
        
        Args:
            file_path: Path to the YAML file to process
            
        Returns:
            Fully resolved data structure
        """
        self.imported_files.clear()
        data = self.load_yaml(file_path)
        return self.process(data, file_path)


def preprocess_yaml_with_imports(file_path: Union[str, Path]) -> Any:
    """
    Convenience function to preprocess a YAML file with imports.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Fully resolved data structure
    """
    file_path = Path(file_path)
    preprocessor = ImportPreprocessor(file_path.parent)
    return preprocessor.process_file(file_path)


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python import_preprocessor.py <yaml_file>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    try:
        result = preprocess_yaml_with_imports(input_file)
        
        # Output as YAML
        print("# Preprocessed YAML (imports resolved)")
        print(yaml.dump(result, default_flow_style=False, sort_keys=False))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
