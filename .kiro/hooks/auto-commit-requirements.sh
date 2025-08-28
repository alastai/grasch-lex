#!/bin/bash
# Auto-commit Requirements Changes  
# Trigger: file_save on .kiro/specs/property-graph-schema/requirements.md

echo "Auto-commit requirements hook triggered..."

# Check if there are changes
git diff --quiet .kiro/specs/property-graph-schema/requirements.md
if [ $? -ne 0 ]; then
    # Add the file to staging
    git add .kiro/specs/property-graph-schema/requirements.md
    
    # Create commit with timestamp
    git commit -m "Update requirements.md - $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Push to remote
    git push origin main
    
    echo "Requirements changes committed and pushed to GitHub"
else
    echo "No changes to requirements.md"
fi