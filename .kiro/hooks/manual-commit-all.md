---
name: "Manual Commit All Changes"
description: "Manually commit all current changes with a custom message"
trigger:
  type: "manual"
inclusion: "manual"
---

# Manual Commit All Changes

Manually commit all current changes to the repository with a descriptive message.

## Instructions

1. Check the current status of the repository
2. Show what files have changed
3. Add all changes to staging
4. Create a commit with a descriptive message
5. Push to remote repository

## Commands to execute

```bash
# Show current status
echo "Current repository status:"
git status

# Check if there are any changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "Files to be committed:"
    git status --porcelain
    
    # Add all changes
    git add .
    
    # Create commit with timestamp and summary
    CHANGED_COUNT=$(git status --porcelain | wc -l | tr -d ' ')
    git commit -m "Manual commit: $CHANGED_COUNT files updated - $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Push to remote
    git push origin main
    
    echo ""
    echo "All changes committed and pushed to GitHub"
else
    echo "No changes to commit"
fi
```