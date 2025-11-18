---
name: "Auto-commit All Changes"
description: "Automatically commit file changes (max once per hour) and push to remote (max once per 4 hours)"
trigger:
  type: "file_save"
  pattern: "**/*"
---

# Auto-commit All Changes

When any file in the repository is saved, automatically commit the changes to Git if the last commit was more than 1 hour ago. Push to remote only if the last push was more than 4 hours ago.

## Instructions

1. Check if there are any changes in the repository
2. Check if the last commit was more than 1 hour ago
3. If yes, add all changed files to Git staging and create a commit
4. Check if the last push was more than 4 hours ago
5. If yes (or if there are unpushed commits), push to remote; otherwise, defer the push

## Commands to execute

```bash
# Check if there are any changes
if [ -n "$(git status --porcelain)" ]; then
    # Check if last commit was more than 1 hour ago
    LAST_COMMIT_TIME=$(git log -1 --format="%ct" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    ONE_HOUR=$((60 * 60))
    
    if [ -n "$LAST_COMMIT_TIME" ]; then
        TIME_SINCE_COMMIT=$((CURRENT_TIME - LAST_COMMIT_TIME))
        
        if [ "$TIME_SINCE_COMMIT" -lt "$ONE_HOUR" ]; then
            echo "Changes detected but commit deferred (last commit was less than 1 hour ago)"
            exit 0
        fi
    fi
    
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
    
    echo "Changes committed: $TOTAL_CHANGES files"
    
    # Check if we should push (only if last push was more than 4 hours ago)
    SHOULD_PUSH=false
    LAST_PUSH_TIME=$(git log --branches --not --remotes --format="%ct" | head -1)
    
    if [ -z "$LAST_PUSH_TIME" ]; then
        # No unpushed commits, check last push time from remote
        LAST_REMOTE_COMMIT=$(git log origin/main -1 --format="%ct" 2>/dev/null)
        if [ -n "$LAST_REMOTE_COMMIT" ]; then
            TIME_DIFF=$((CURRENT_TIME - LAST_REMOTE_COMMIT))
            FOUR_HOURS=$((4 * 60 * 60))
            
            if [ "$TIME_DIFF" -gt "$FOUR_HOURS" ]; then
                SHOULD_PUSH=true
            fi
        else
            # Can't determine last push time, push anyway
            SHOULD_PUSH=true
        fi
    else
        # There are unpushed commits, always push
        SHOULD_PUSH=true
    fi
    
    if [ "$SHOULD_PUSH" = true ]; then
        git push origin main
        echo "Pushed to GitHub"
    else
        echo "Push deferred (last push was less than 4 hours ago)"
    fi
else
    echo "No changes to commit"
fi
```