# Context Continuity Guidelines

## Session Initialization Protocol

**CRITICAL: Always consult the latest version of CONTEXT-SUMMARIES at the start of a new session. Find the latest summary document at the head of that document. Read it, but do not act or change anything, just add this into your understanding of the transferred context.**

### Purpose

This document ensures proper context continuity across session boundaries when conversations are reset due to length limitations and context is transferred via summarization.

### Mandatory First Action

When starting any new session where context has been transferred:

1. **Immediately read CONTEXT-SUMMARIES.md** - This file contains chronological summaries of work completed
2. **Identify the latest summary** - Look for the most recent entry at the top of the document
3. **Integrate the information** - Add the latest summary details to your understanding of the current state
4. **Do not take action** - Only read and understand; do not make changes or execute commands based on this information alone

### Why This Matters

- Context transfer summaries may be incomplete or outdated
- Critical analysis and decisions from recent work may not be fully captured in the basic context transfer
- The CONTEXT-SUMMARIES document provides the most accurate and complete picture of recent progress
- This prevents repeating work or missing important context about what has already been accomplished

### Implementation

- This check should happen automatically at session start
- The assistant should acknowledge having read the latest context summary
- Any discrepancies between transferred context and the summary should be noted
- The user should be informed if additional context was found that affects the current understanding
- **Analyze discrepancies**: If there are differences between the context transfer summary and the CONTEXT-SUMMARIES head document, explicitly analyze and explain these discrepancies to understand what information may have been lost or incomplete in the transfer

This protocol ensures continuity and prevents the frustration of having to re-explain completed work or analysis.