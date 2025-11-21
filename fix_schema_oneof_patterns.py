#!/usr/bin/env python3
"""
Fix JSON Schema oneOf patterns to handle both pre-import and post-import structures.

The key insight: After preprocessing, import-only patterns become inline patterns.
So the schema needs to accept both:
- Before: {import: "file.yaml"} 
- After: <actual content from file>

For propertyGraphDataModel:
- Before: {import: "file.yaml"}
- After: {valueTypeSystemName: "...", graphPreferredName: "...", ...}

For nodeTypes/edgeTypes:
- Before: {import: "file.yaml"} OR [{import: "file.yaml"}, ...]
- After: [{nodeType: {...}}, ...] (just the array)

The fix: Ensure the "inline" option in oneOf patterns is flexible enough to match
the preprocessed output.
