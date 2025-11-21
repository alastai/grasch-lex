#!/usr/bin/env python3
"""Test with exact structure from preprocessed file"""
import json
from jsonschema import Draft202012Validator

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))
validator = Draft202012Validator(schema)

# Load the actual preprocessed data
actual_data = json.load(open('preprocessed_minimal.json'))

# Test it
errors = list(validator.iter_errors(actual_data))
print(f"Actual preprocessed data: {len(errors)} errors")

# Now create a simplified version step by step
# Start with just graphSchema + pathName + graphType with empty propertyGraphDataModel
test1 = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {}
        }
    }
}

errors = list(validator.iter_errors(test1))
print(f"Test 1 (minimal structure): {len(errors)} errors")

# Add the full propertyGraphDataModel from actual data
test2 = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": actual_data['graphSchema']['graphType']['propertyGraphDataModel']
        }
    }
}

errors = list(validator.iter_errors(test2))
print(f"Test 2 (with full propertyGraphDataModel): {len(errors)} errors")

# Add nodeTypes
test3 = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": actual_data['graphSchema']['graphType']['propertyGraphDataModel'],
            "nodeTypes": actual_data['graphSchema']['graphType']['nodeTypes']
        }
    }
}

errors = list(validator.iter_errors(test3))
print(f"Test 3 (+ nodeTypes): {len(errors)} errors")

# Add edgeTypes
test4 = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": actual_data['graphSchema']['graphType']['propertyGraphDataModel'],
            "nodeTypes": actual_data['graphSchema']['graphType']['nodeTypes'],
            "edgeTypes": actual_data['graphSchema']['graphType']['edgeTypes']
        }
    }
}

errors = list(validator.iter_errors(test4))
print(f"Test 4 (+ edgeTypes): {len(errors)} errors")

# Use actual pathName
test5 = {
    "graphSchema": {
        "pathName": actual_data['graphSchema']['pathName'],
        "graphType": actual_data['graphSchema']['graphType']
    }
}

errors = list(validator.iter_errors(test5))
print(f"Test 5 (exact graphSchema): {len(errors)} errors")

# Check if there are any extra keys
print(f"\nActual data keys: {list(actual_data.keys())}")
print(f"graphSchema keys: {list(actual_data['graphSchema'].keys())}")
