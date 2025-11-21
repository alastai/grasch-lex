#!/bin/bash

# Update all import paths to use imports/ directory

cd src/grasch/examples

# Update defaults imports
for file in *.yaml; do
  if [ -f "$file" ]; then
    # Update unquoted imports
    sed -i.bak 's|import: lex-2026.0.3.2-graph-type-defaults\.yaml|import: imports/lex-2026.0.3.2-graph-type-defaults.yaml|g' "$file"
    # Update quoted imports
    sed -i.bak 's|import: "lex-2026.0.3.2-graph-type-defaults\.yaml"|import: "imports/lex-2026.0.3.2-graph-type-defaults.yaml"|g' "$file"
    # Update snb-types paths
    sed -i.bak 's|import: lex-2026.0.3.2-snb-types/|import: imports/snb-types/|g' "$file"
    # Update snb_types paths (if any)
    sed -i.bak 's|import: snb_types/|import: imports/snb-types/|g' "$file"
    sed -i.bak 's|import: "snb_types/|import: "imports/snb-types/|g' "$file"
    # Remove backup files
    rm -f "$file.bak"
  fi
done

echo "Import paths updated successfully"
