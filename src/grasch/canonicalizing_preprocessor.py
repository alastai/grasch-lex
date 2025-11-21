#!/usr/bin/env python3
"""
YAML Import Preprocessor for LEX Schemas

This preprocessor resolves 'import' directives in YAML files recursively,
producing a flattened YAML structure suitable for JSON Schema validation.

Supported import patterns:
1. Whole graphSchema: graphSchema: {import: "schema.yaml"}
2. Defaults blrt patterns:
1. Whole graphSchema: graphSchema: {import: "schema.yaml"}
2. Defaults block: defaults: {import: "defaults.yaml"}
3. Type subsets: nodeTypes: [{import: "types.yaml"}, ...]
"""

import yaml
from pathlib import Path
from typing import Any, Dict, List, Union, Tuple, Optional
from enum import Enum


class SubtypeMatchingMode(Enum):
    """Subtype matching mode for type interpretation."""
    EXACTLY_OF = "exactlyOf"
    SUBTYPES_OF = "subtypesOf"


class Concreteness(Enum):
    """Concreteness for type interpretation."""
    CONCRETE = "concrete"
    ABSTRACT = "abstract"


class TypeInterpretationWrapper:
    """Represents a parsed type interpretation wrapper."""
    
    def __init__(
        self,
        subtype_matching: SubtypeMatchingMode,
        concreteness: Concreteness,
        wrapped_content: Any
    ):
        self.subtype_matching = subtype_matching
        self.concreteness = concreteness
        self.wrapped_content = wrapped_content
    
    def to_canonical_dict(self) -> Dict:
        """Convert to canonical two-level wrapper form."""
        return {
            self.subtype_matching.value: {
                self.concreteness.value: self.wrapped_content
            }
        }


class ImportPreprocessor:
    """Preprocesses YAML files by resolving import directives and canonicalizing type interpretation wrappers."""
    
    # Wrapper keywords
    SUBTYPE_MATCHING_KEYWORDS = {'exactlyOf', 'subtypesOf'}
    CONCRETENESS_KEYWORDS = {'abstract', 'concrete'}
    ONE_LEVEL_WRAPPER_KEYWORDS = {'abstract', 'concrete', 'properSubtypesOf'}
    ALL_WRAPPER_KEYWORDS = SUBTYPE_MATCHING_KEYWORDS | CONCRETENESS_KEYWORDS | {'properSubtypesOf'}
    
    # Keys that can have wrappers
    WRAPPABLE_PROPERTIES = {'nodeType', 'edgeType', 'graphType'}
    WRAPPABLE_ARRAYS = {'nodeTypes', 'edgeTypes'}
    EDGE_COMPONENTS = {'from', 'to', 'tail', 'head', 'src', 'dst', 'dest', 'source', 'destination', 'between', 'and', 'via', 'arc'}
    
    def __init__(self, base_path: Path, canonicalize_wrappers: bool = True):
        """
        Initialize preprocessor with base path for resolving relative imports.
        
        Args:
            base_path: Base directory for resolving relative import paths
            canonicalize_wrappers: Whether to canonicalize type interpretation wrappers
        """
        self.base_path = base_path
        self.imported_files = set()  # Track to prevent circular imports
        self.canonicalize_wrappers = canonicalize_wrappers
    
    def load_yaml(self, file_path: Path) -> Any:
        """Load a YAML file."""
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    def detect_wrapper(self, data: Any) -> Optional[Tuple[str, Any]]:
        """
        Detect if data is a wrapper structure.
        
        Returns:
            Tuple of (wrapper_keyword, wrapped_content) if wrapper detected, None otherwise
        """
        if not isinstance(data, dict):
            return None
        
        # Check for wrapper keywords
        wrapper_keys = [k for k in data.keys() if k in self.ALL_WRAPPER_KEYWORDS]
        
        if len(wrapper_keys) == 1:
            wrapper_key = wrapper_keys[0]
            return (wrapper_key, data[wrapper_key])
        
        return None
    
    def parse_wrapper(self, data: Any, context: str = "") -> Optional[TypeInterpretationWrapper]:
        """
        Parse a wrapper structure into TypeInterpretationWrapper.
        
        Args:
            data: The data to parse
            context: Context string for error messages
            
        Returns:
            TypeInterpretationWrapper if valid wrapper found, None otherwise
            
        Raises:
            ValueError: If wrapper nesting or invalid structure detected
        """
        if not isinstance(data, dict):
            return None
        
        # Detect first level wrapper
        first_wrapper = self.detect_wrapper(data)
        if not first_wrapper:
            return None
        
        first_key, first_content = first_wrapper
        
        # Check for nested wrapper
        second_wrapper = self.detect_wrapper(first_content)
        
        if first_key in self.ONE_LEVEL_WRAPPER_KEYWORDS:
            # One-level wrapper
            if second_wrapper:
                # Check if it's a valid two-level pattern
                second_key, second_content = second_wrapper
                
                # Valid two-level: subtype matching → concreteness → property
                # Check order: first must be subtype matching, second must be concreteness
                if first_key in self.SUBTYPE_MATCHING_KEYWORDS and second_key in self.CONCRETENESS_KEYWORDS:
                    # Valid two-level wrapper
                    subtype_matching = SubtypeMatchingMode(first_key) if first_key != 'properSubtypesOf' else SubtypeMatchingMode.SUBTYPES_OF
                    concreteness = Concreteness(second_key)
                    
                    # Check for triple nesting (invalid)
                    third_wrapper = self.detect_wrapper(second_content)
                    if third_wrapper:
                        raise ValueError(
                            f"Type interpretation wrappers cannot be nested more than two levels. "
                            f"Found {first_key}: {second_key}: {third_wrapper[0]}: at {context}"
                        )
                    
                    return TypeInterpretationWrapper(subtype_matching, concreteness, second_content)
                
                # Invalid order
                elif first_key in self.CONCRETENESS_KEYWORDS and second_key in self.SUBTYPE_MATCHING_KEYWORDS:
                    raise ValueError(
                        f"Invalid wrapper order at {context}. "
                        f"Wrappers must be ordered: subtype matching mode (exactlyOf/subtypesOf), "
                        f"then concreteness (concrete/abstract), then property. "
                        f"Found: {first_key}: {second_key}:"
                    )
                
                # Both are same type (invalid nesting)
                else:
                    raise ValueError(
                        f"Type interpretation wrappers cannot be nested. "
                        f"Found {first_key} wrapper containing {second_key} wrapper at {context}"
                    )
            
            # One-level wrapper without nesting - will be canonicalized
            # Map one-level wrappers to their canonical two-level form
            if first_key == 'properSubtypesOf':
                return TypeInterpretationWrapper(
                    SubtypeMatchingMode.SUBTYPES_OF,
                    Concreteness.ABSTRACT,
                    first_content
                )
            elif first_key == 'concrete':
                return TypeInterpretationWrapper(
                    SubtypeMatchingMode.EXACTLY_OF,
                    Concreteness.CONCRETE,
                    first_content
                )
            elif first_key == 'abstract':
                return TypeInterpretationWrapper(
                    SubtypeMatchingMode.SUBTYPES_OF,
                    Concreteness.ABSTRACT,
                    first_content
                )
        
        elif first_key in self.SUBTYPE_MATCHING_KEYWORDS:
            # Two-level wrapper starting with subtype matching
            if not second_wrapper:
                # No second wrapper - this is incomplete, but might be valid in some contexts
                # Return None to let it be processed as regular dict
                return None
            
            second_key, second_content = second_wrapper
            
            # Check order
            if second_key not in self.CONCRETENESS_KEYWORDS:
                # Not a valid two-level wrapper - might be nested content
                # Return None to let it be processed as regular dict
                return None
            
            # Valid two-level wrapper - already canonical
            subtype_matching = SubtypeMatchingMode(first_key)
            concreteness = Concreteness(second_key)
            
            # Check for triple nesting (invalid)
            third_wrapper = self.detect_wrapper(second_content)
            if third_wrapper:
                raise ValueError(
                    f"Type interpretation wrappers cannot be nested more than two levels. "
                    f"Found {first_key}: {second_key}: {third_wrapper[0]}: at {context}"
                )
            
            return TypeInterpretationWrapper(subtype_matching, concreteness, second_content)
        
        return None
    
    def canonicalize_wrapper(self, data: Any, parent_key: str = None, context: str = "") -> Any:
        """
        Canonicalize type interpretation wrappers in data structure.
        
        Args:
            data: The data to canonicalize
            parent_key: The parent key (to determine if wrappers are valid here)
            context: Context string for error messages
            
        Returns:
            Data with wrappers canonicalized to two-level form
        """
        if not self.canonicalize_wrappers:
            return data
        
        # Try to parse as wrapper
        wrapper = self.parse_wrapper(data, context)
        
        if wrapper:
            # This is a wrapper - check if it's already canonical
            # A wrapper is canonical if it's two-level with correct order
            first_wrapper = self.detect_wrapper(data)
            if first_wrapper:
                first_key, first_content = first_wrapper
                # Check if this is already a two-level canonical wrapper
                if first_key in self.SUBTYPE_MATCHING_KEYWORDS:
                    second_wrapper = self.detect_wrapper(first_content)
                    if second_wrapper:
                        second_key, second_content = second_wrapper
                        if second_key in self.CONCRETENESS_KEYWORDS:
                            # Already canonical - just recursively process the content
                            processed_content = second_content
                            if isinstance(processed_content, dict):
                                result_content = {}
                                for key, value in processed_content.items():
                                    result_content[key] = self.canonicalize_wrapper(value, key, f"{context}.{key}")
                                processed_content = result_content
                            
                            return {
                                first_key: {
                                    second_key: processed_content
                                }
                            }
            
            # Not already canonical - canonicalize it
            canonical = wrapper.to_canonical_dict()
            
            # Recursively canonicalize the wrapped content
            wrapped_content = wrapper.wrapped_content
            if isinstance(wrapped_content, dict):
                result_content = {}
                for key, value in wrapped_content.items():
                    result_content[key] = self.canonicalize_wrapper(value, key, f"{context}.{key}")
                wrapped_content = result_content
            
            # Reconstruct canonical form with canonicalized content
            return {
                wrapper.subtype_matching.value: {
                    wrapper.concreteness.value: wrapped_content
                }
            }
        
        # Not a wrapper - check if it's a structure that might contain wrappers
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                # Recursively canonicalize
                result[key] = self.canonicalize_wrapper(value, key, f"{context}.{key}" if context else key)
            return result
        
        elif isinstance(data, list):
            # Canonicalize each item in the list
            return [self.canonicalize_wrapper(item, parent_key, f"{context}[{i}]") for i, item in enumerate(data)]
        
        else:
            # Primitive value or zero-level wrapper (bare reference)
            # Check if this is a bare type reference that should be canonicalized
            if parent_key in self.WRAPPABLE_PROPERTIES and isinstance(data, (str, int, list)):
                # Bare reference - canonicalize to exactlyOf: concrete:
                return {
                    SubtypeMatchingMode.EXACTLY_OF.value: {
                        Concreteness.CONCRETE.value: {
                            parent_key: data
                        }
                    }
                }
            
            return data
    
    def canonicalize_edge_type(self, edge_data: Dict, context: str = "") -> Dict:
        """
        Canonicalize an edge type structure, handling component-level wrappers.
        
        The canonicalizer is "dumb" - it doesn't parse or understand what a 
        <node type for endpoint> is. It just checks if a type interpretation 
        wrapper exists, and if not, inserts the default exactlyOf: concrete: 
        wrapper around the ENTIRE value.
        
        Args:
            edge_data: The edge type data (should contain 'directed' or 'undirected')
            context: Context string for error messages
            
        Returns:
            Canonicalized edge type data
        """
        if not isinstance(edge_data, dict):
            return edge_data
        
        result = {}
        
        for key, value in edge_data.items():
            if key in {'directed', 'undirected'}:
                # Process edge type components
                if isinstance(value, dict):
                    edge_components = {}
                    for comp_key, comp_value in value.items():
                        if comp_key in self.EDGE_COMPONENTS:
                            # This is an edge component - check for wrappers
                            wrapper = self.parse_wrapper(comp_value, f"{context}.{key}.{comp_key}")
                            if wrapper:
                                # Already has a wrapper - canonicalize it
                                edge_components[comp_key] = wrapper.to_canonical_dict()
                            else:
                                # No wrapper - insert default exactlyOf: concrete: wrapper
                                # around the ENTIRE value (the <node type for endpoint>)
                                # Don't try to understand what the value is - just wrap it
                                edge_components[comp_key] = {
                                    SubtypeMatchingMode.EXACTLY_OF.value: {
                                        Concreteness.CONCRETE.value: comp_value
                                    }
                                }
                        else:
                            # Not an edge component - recursively process
                            edge_components[comp_key] = self.canonicalize_wrapper(
                                comp_value, comp_key, f"{context}.{key}.{comp_key}"
                            )
                    result[key] = edge_components
                else:
                    result[key] = value
            else:
                result[key] = self.canonicalize_wrapper(value, key, f"{context}.{key}")
        
        return result
    
    def resolve_import(self, import_spec: Union[str, Dict], current_path: Path, parent_key: str = None) -> Any:
        """
        Resolve an import specification.
        
        Args:
            import_spec: Either a string path or dict with 'import' key
            current_path: Path of the file containing the import
            parent_key: The key under which this import appears (for wrapper stripping)
            
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
        
        # Strip wrapper if the imported content has the same key as parent
        # Example: If importing into "nodeTypes:" and file contains "nodeTypes: [...]"
        # then strip the wrapper and return just the array
        if parent_key and isinstance(processed, dict) and parent_key in processed and len(processed) == 1:
            processed = processed[parent_key]
        
        self.imported_files.remove(import_file_abs)
        
        return processed
    
    def process(self, data: Any, current_path: Path = None, parent_key: str = None) -> Any:
        """
        Recursively process data structure, resolving imports and canonicalizing wrappers.
        
        Args:
            data: The data structure to process
            current_path: Path of the current file being processed
            parent_key: The key under which this data appears
            
        Returns:
            Processed data with all imports resolved and wrappers canonicalized
        """
        if isinstance(data, dict):
            # Check if this is an import-only directive
            if 'import' in data and len(data) == 1:
                imported = self.resolve_import(data, current_path, parent_key)
                # Canonicalize after import resolution
                return self.canonicalize_wrapper(imported, parent_key, f"imported:{parent_key}")
            
            # Check if this has import mixed with other keys
            if 'import' in data:
                # Mixed pattern: import + other keys
                # Resolve import first, then merge with other keys
                imported = self.resolve_import(data['import'], current_path, parent_key)
                result = {}
                if isinstance(imported, dict):
                    result.update(imported)
                # Add other keys
                for key, value in data.items():
                    if key != 'import':
                        result[key] = self.process(value, current_path, key)
                # Canonicalize the merged result
                return self.canonicalize_wrapper(result, parent_key, f"merged:{parent_key}")
            
            # Check for edge type structure
            if 'directed' in data or 'undirected' in data:
                # This is an edge type - handle component-level canonicalization
                processed = {}
                for key, value in data.items():
                    processed[key] = self.process(value, current_path, key)
                return self.canonicalize_edge_type(processed, f"edgeType:{parent_key}")
            
            # Check if this dict is already a wrapper before processing
            if self.detect_wrapper(data):
                # This is a wrapper - canonicalize it directly without processing keys first
                return self.canonicalize_wrapper(data, parent_key, f"{parent_key}" if parent_key else "root")
            
            # Process each key-value pair normally
            result = {}
            for key, value in data.items():
                result[key] = self.process(value, current_path, key)
            
            # Canonicalize after processing (but this won't double-wrap because we check above)
            return self.canonicalize_wrapper(result, parent_key, f"{parent_key}" if parent_key else "root")
        
        elif isinstance(data, list):
            # Process list items, flattening imported lists
            result = []
            for item in data:
                if isinstance(item, dict) and 'import' in item and len(item) == 1:
                    # Import directive in list
                    imported = self.resolve_import(item, current_path, parent_key)
                    if isinstance(imported, list):
                        result.extend(imported)
                    else:
                        result.append(imported)
                else:
                    processed_item = self.process(item, current_path, parent_key)
                    result.append(processed_item)
            
            # Don't double-canonicalize - items are already processed
            return result
        
        else:
            # Primitive value
            return data
    
    def process_file(self, file_path: Path) -> Any:
        """
        Process a YAML file, resolving all imports and canonicalizing wrappers.
        
        Args:
            file_path: Path to the YAML file to process
            
        Returns:
            Fully resolved and canonicalized data structure
        """
        self.imported_files.clear()
        data = self.load_yaml(file_path)
        return self.process(data, file_path)


def preprocess_yaml_with_imports(file_path: Union[str, Path], canonicalize_wrappers: bool = True) -> Any:
    """
    Convenience function to preprocess a YAML file with imports.
    
    Args:
        file_path: Path to the YAML file
        canonicalize_wrappers: Whether to canonicalize type interpretation wrappers
        
    Returns:
        Fully resolved and canonicalized data structure
    """
    file_path = Path(file_path)
    preprocessor = ImportPreprocessor(file_path.parent, canonicalize_wrappers=canonicalize_wrappers)
    return preprocessor.process_file(file_path)


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python import_preprocessor.py <yaml_file> [--no-canonicalize]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    canonicalize = '--no-canonicalize' not in sys.argv
    
    try:
        result = preprocess_yaml_with_imports(input_file, canonicalize_wrappers=canonicalize)
        
        # Output as YAML
        print("# Preprocessed YAML (imports resolved, wrappers canonicalized)")
        print(yaml.dump(result, default_flow_style=False, sort_keys=False))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
