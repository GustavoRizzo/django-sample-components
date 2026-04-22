---
name: Memory storage preference
description: User wants project memories saved locally in .claude/memory/ inside the project, not in the global ~/.claude/ folder
type: feedback
---

Save all project-specific memories to `.claude/memory/` inside this project directory.

**Why:** User explicitly prefers local, project-scoped memory over the global `~/.claude/` folder, keeping context close to the code.

**How to apply:** When creating or updating memory files for this project, always write to `/home/grizzo/projetos/django-sample-components/.claude/memory/` and maintain the MEMORY.md index there. Do not write to `~/.claude/projects/...`.
