---
name: github-large-file-push
description: >
  Push large files (>1MB) to GitHub via the Git Data API when MCP tools or `git push` fail (sandbox network restriction or file size limits).
  This skill should be used when: (1) `mcp__github__push_files` truncates large files, (2) `git push` cannot connect to github.com from sandbox, or (3) the file exceeds GitHub Contents API's 1MB limit.
  Triggered by: GitHub push failure on large files, "file too large for GitHub MCP", "can't push to GitHub from sandbox".
agent_created: true
scripts:
  - push_via_git_api.py
