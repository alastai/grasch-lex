#!/usr/bin/env python3
"""
Transform LEX-2026.0.3.1 files to use simplified pathName syntax.
Replaces locallyQualifiedObjectName and globallyQualifiedObjectName with pathName.
"""

import re
import sys
from pathlib import Path

def transform_identifier(content: str) -> str:
    """Transform identifier syntax from locallyQualifiedObjectName/globallyQualifiedObjectName to pathName and remove identifier wrapper."""
    
    # Pattern 1: identifier:\n  locallyQualifiedObjectName: "/path"
    # Becomes: pathName: "/path"
    content = re.sub(
        r'identifier:\s*\n\s+locallyQualifiedObjectName:\s*(["\']?)(/[^"\'\n]+)\1',
        r'pathName: \1\2\1',
        content
    )
    
    # Pattern 2: identifier:\n  globallyQualifiedObjectName: "iri|/path"
    # Becomes: pathName: "iri|/path"
    content = re.sub(
        r'identifier:\s*\n\s+globallyQualifiedObjectName:\s*(["\']?)([^"\'\n]+\|/[^"\'\n]+)\1',
        r'pathName: \1\2\1',
        content
    )
    
    # Pattern 3: Inline identifier: {locallyQualifiedObjectName: "/path"}
    content = re.sub(
        r'identifier:\s*\{\s*locallyQualifiedObjectName:\s*(["\']?)(/[^"\'\n}]+)\1\s*\}',
        r'pathName: \1\2\1',
        content
    )
    
    # Pattern 4: Inline identifier: {globallyQualifiedObjectName: "iri|/path"}
    content = re.sub(
        r'identifier:\s*\{\s*globallyQualifiedObjectName:\s*(["\']?)([^"\'\n}]+\|/[^"\'\n}]+)\1\s*\}',
        r'pathName: \1\2\1',
        content
    )
    
    return content

def transform_file(filepath: Path) -> bool:
    """Transform a single file. Returns True if changes were made."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        transformed_content = transform_identifier(original_content)
        
        if transformed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(transformed_content)
            print(f"✓ Transformed: {filepath}")
            return True
        else:
            print(f"  No changes: {filepath}")
            return False
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}", file=sys.stderr)
        return False

def main():
    """Transform all relevant files."""
    
    # Files to transform
    files_to_transform = [
        "src/grasch/examples/snb-lex-2026.0.3.1-schema.yaml",
        "src/grasch/examples/finbench-lex-2026.0.3.1-schema.yaml",
        "src/grasch/examples/example-catalog-no-iri-lex-2026.0.3.1.yaml",
        "src/grasch/examples/complete_import_example.yaml",
        "src/grasch/examples/graph-schema-type-interpretation-example.yaml",
        "src/grasch/examples/element-type-interpretation-example.yaml",
        "src/grasch/examples/mixed_import_example.yaml",
        "src/grasch/examples/all_import_patterns.yaml",
        "ancillary docs/LEX -- GraphAr separation.yml",
    ]
    
    transformed_count = 0
    for filepath_str in files_to_transform:
        filepath = Path(filepath_str)
        if filepath.exists():
            if transform_file(filepath):
                transformed_count += 1
        else:
            print(f"  File not found: {filepath}")
    
    print(f"\n{transformed_count} file(s) transformed")

if __name__ == "__main__":
    main()
