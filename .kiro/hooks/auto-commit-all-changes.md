---
name: "Auto-commit All Changes"
description: "Automatically commit and push any file changes in the repository"
trigger:
  type: "file_save"
  pattern: "**/*"
---

# Auto-commit All Changes

When any file in the repository is saved, automatically commit and push the changes to Git.

## Instructions

1. Check if there are any changes in the repository
2. If changes exist, add all changed files to Git staging
3. Create a commit with a descriptive message including the changed files
4. Push the changes to the remote repository

## Commands to execute

```bash
# Check if there are any changes
if [ -n "$(git status --porcelain)" ]; then
    # Get list of changed files (limit to first 5 for readability)
    CHANGED_FILES=$(git status --porcelain | head -5 | awk '{print $2}' | tr '\n' ' ')
    TOTAL_CHANGES=$(git status --porcelain | wc -l | tr -d ' ')
    
    # Add all changes to staging
    git add .
    
    # Create commit with changed files list
    if [ "$TOTAL_CHANGES" -le 5 ]; then
        git commit -m "Auto-commit: Update $CHANGED_FILES- $(date '+%Y-%m-%d %H:%M:%S')"
    else
        git commit -m "Auto-commit: Update $TOTAL_CHANGES files - $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    # Push to remote
    git push origin main
    
    echo "Changes committed and pushed to GitHub: $TOTAL_CHANGES files"
else
    echo "No changes to commit"
fi
```