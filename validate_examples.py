#!/usr/bin/env python3
"""
Validate all LEX-2026.0.3.2 example YAML files against the JSON Schema.
"""

import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

# Load the schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Files to validate
example_files = [
    "src/grasch/examples/lex-2026.0.3.2-minimal-test.yaml",
    "src/grasch/examples/lex-2026.0.3.2-all-import-patterns.yaml",
    "src/grasch/examples/lex-2026.0.3.2-complete-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-comprehensive-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-example-catalog-no-iri.yaml",
    "src/grasch/examples/lex-2026.0.3.2-example-catalog.yaml",
    "src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml",
    "src/grasch/examples/lex-2026.0.3.2-finbench-sf1-graph.yaml",
    "src/grasch/examples/lex-2026.0.3.2-minimal-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-mixed-import-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml",
    "src/grasch/examples/lex-2026.0.3.2-snb-special-identification-example.yaml",
    "src/grasch/examples/lex-2026.0.3.2-subtype-abstract-test.yaml",
    "src/grasch/examples/lex-2026.0.3.2-type-definition-syntax-examples.yaml",
]

results = {
    "valid": [],
    "invalid": [],
    "errors": {}
}

for file_path in example_files:
    path = Path(file_path)
    if not path.exists():
        print(f"⚠️  SKIP: {path.name} (file not found)")
        continue
    
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Validate
        errors = list(validator.iter_errors(data))
        
        if errors:
            results["invalid"].append(path.name)
            results["errors"][path.name] = []
            print(f"❌ INVALID: {path.name}")
            for error in errors:
                error_path = ".".join(str(p) for p in error.absolute_path)
                error_msg = f"  Path: {error_path} - {error.message}"
                print(error_msg)
                results["errors"][path.name].append(error_msg)
        else:
            results["valid"].append(path.name)
            print(f"✅ VALID: {path.name}")
    
    except yaml.YAMLError as e:
        results["invalid"].append(path.name)
        results["errors"][path.name] = [f"YAML parsing error: {e}"]
        print(f"❌ YAML ERROR: {path.name} - {e}")
    except Exception as e:
        results["invalid"].append(path.name)
        results["errors"][path.name] = [f"Unexpected error: {e}"]
        print(f"❌ ERROR: {path.name} - {e}")

# Summary
print("\n" + "="*60)
print("VALIDATION SUMMARY")
print("="*60)
print(f"Total files: {len(example_files)}")
print(f"Valid: {len(results['valid'])}")
print(f"Invalid: {len(results['invalid'])}")

if results["valid"]:
    print("\n✅ Valid files:")
    for name in results["valid"]:
        print(f"  - {name}")

if results["invalid"]:
    print("\n❌ Invalid files:")
    for name in results["invalid"]:
        print(f"  - {name}")

# Save detailed results
with open("SCHEMA-VALIDATION-RESULTS.md", "w") as f:
    f.write("# LEX-2026.0.3.2 Schema Validation Results\n\n")
    f.write(f"**Total files tested:** {len(example_files)}\n\n")
    f.write(f"**Valid:** {len(results['valid'])}\n\n")
    f.write(f"**Invalid:** {len(results['invalid'])}\n\n")
    
    if results["valid"]:
        f.write("## ✅ Valid Files\n\n")
        for name in results["valid"]:
            f.write(f"- {name}\n")
        f.write("\n")
    
    if results["invalid"]:
        f.write("## ❌ Invalid Files\n\n")
        for name in results["invalid"]:
            f.write(f"### {name}\n\n")
            if name in results["errors"]:
                for error in results["errors"][name]:
                    f.write(f"{error}\n")
            f.write("\n")

print("\nDetailed results saved to SCHEMA-VALIDATION-RESULTS.md")
