#!/usr/bin/env python3
"""
Update JSON Schema to implement the new type interpretation design
"""
import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path, 'r') as f:
    schema = json.load(f)

print("Updating JSON Schema with new type interpretation design...")
print()

# 1. Update typeInterpretationMode enum values
if 'PropertyGraphDataModel' in schema['$defs']:
    pgdm = schema['$defs']['PropertyGraphDataModel']
    if 'properties' in pgdm and 'typeInterpretationMode' in pgdm['properties']:
        mode_prop = pgdm['properties']['typeInterpretationMode']
        old_enum = mode_prop.get('enum', [])
        mode_prop['enum'] = ['exactlyOf', 'subtypesOf', 'properSubtypesOf']
        mode_prop['default'] = 'exactlyOf'
        print(f"✓ Updated typeInterpretationMode enum:")
        print(f"  Old: {old_enum}")
        print(f"  New: {mode_prop['enum']}")
        print()

# 2. Replace all occurrences of old terms with new terms in the entire schema
def replace_in_dict(obj, replacements):
    """Recursively replace keys and string values in a dictionary"""
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            # Replace key if it matches
            new_key = replacements.get(key, key)
            # Recursively process value
            new_value = replace_in_dict(value, replacements)
            new_obj[new_key] = new_value
        return new_obj
    elif isinstance(obj, list):
        return [replace_in_dict(item, replacements) for item in obj]
    elif isinstance(obj, str):
        # Replace string values if they match
        return replacements.get(obj, obj)
    else:
        return obj

replacements = {
    'allowSubtypesOf': 'subtypesOf',
    'abstractSupertype': 'abstract',
    'abstractSupertypes': 'abstract',
    'exactlyOfThisType': 'exactlyOf',
    'anySubtypeOf': 'subtypesOf',
    'anyProperSubtypeOf': 'properSubtypesOf',
}

print("Replacing terms throughout schema:")
for old, new in replacements.items():
    print(f"  {old} → {new}")
print()

schema = replace_in_dict(schema, replacements)

# 3. Update descriptions to reflect new terminology
def update_descriptions(obj):
    """Update description strings to use new terminology"""
    if isinstance(obj, dict):
        if 'description' in obj and isinstance(obj['description'], str):
            desc = obj['description']
            # Update common phrases
            desc = desc.replace('Allow subtypes', 'Subtypes')
            desc = desc.replace('allow subtypes', 'subtypes')
            desc = desc.replace('Abstract supertype', 'Abstract')
            desc = desc.replace('abstract supertype', 'abstract')
            obj['description'] = desc
        
        for value in obj.values():
            update_descriptions(value)
    elif isinstance(obj, list):
        for item in obj:
            update_descriptions(item)

update_descriptions(schema)

# Save updated schema
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print(f"✓ Schema saved to {schema_path}")
print()
print("Schema update complete!")
