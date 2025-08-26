---
name: "Auto-commit Spec Changes"
description: "Automatically commit changes to any files in the .kiro/specs directory"
trigger:
  type: "file_save"
  pattern: ".kiro/specs/**/*"
---

# Auto-commit Spec Changes

When any file in the .kiro/specs directory is saved, automatically commit the changes to Git.

## Instructions

1. Check if there are changes to any files in .kiro/specs/
2. If changes exist, add all changed spec files to Git staging
3. Create a commit with a descriptive message including the changed files
4. Push the changes to the remote repository

## Commands to execute

```bash
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
```