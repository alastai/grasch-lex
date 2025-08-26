---
name: "Auto-commit Requirements Changes"
description: "Automatically commit changes to requirements.md when it's modified"
trigger:
  type: "file_save"
  pattern: ".kiro/specs/property-graph-schema/requirements.md"
---

# Auto-commit Requirements Changes

When the requirements.md file is saved, automatically commit the changes to Git with a descriptive message.

## Instructions

1. Check if there are changes to the requirements.md file
2. If changes exist, add the file to Git staging
3. Create a commit with a descriptive message including the timestamp
4. Push the changes to the remote repository

## Commands to execute

```bash
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
```