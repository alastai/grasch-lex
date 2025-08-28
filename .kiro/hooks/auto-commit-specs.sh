#!/bin/bash
# Auto-commit Spec Changes
# Trigger: file_save on .kiro/specs/**/*

echo "Auto-commit specs hook triggered..."

# Check if there are changes in the specs directory
if [ -n "$(git status --porcelain .kiro/specs/)" ]; then
    # Get list of changed files
    CHANGED_FILES=$(git status --porcelain .kiro/specs/ | awk '{print $2}' | tr '\n' ' ')
    
    # Add all changed spec files to staging
    git add .kiro/specs/
    
    # Create commit with changed files list
    git commit -m "Update spec files: $CHANGED_FILES - $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Push to remote
    git push origin main
    
    echo "Spec changes committed and pushed to GitHub: $CHANGED_FILES"
else
    echo "No changes to spec files"
fi