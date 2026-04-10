---
name: Antigravity — Editor Identity & Marketplace
description: Antigravity is Google's VS Code fork; uses OpenVSX not Microsoft marketplace — affects extension availability
type: project
---

Antigravity (v1.107.0, author: Google) is Jackson's primary editor — a VS Code fork that pulls extensions from OpenVSX, not Microsoft's marketplace.

**Why:** Microsoft-exclusive extensions won't appear in Antigravity's extension search. If an extension is missing, it's likely not on OpenVSX.

**How to apply:** When recommending or installing extensions for Antigravity, verify they exist on OpenVSX. Install via `antigravity --install-extension <id>` not `code --install-extension`. Extensions installed via `code` go to VS Code only, not Antigravity.

**Current extensions installed:**

- anthropic.claude-code (panel mode)
- eamodio.gitlens (→ Claude Sonnet 4.6)
- esbenp.prettier-vscode
- davidanson.vscode-markdownlint
- yzhang.markdown-all-in-one
- usernamehw.errorlens
- gruntfuggly.todo-tree
- christian-kohler.path-intellisense

**User data:** `C:/Users/jacks/AppData/Roaming/Antigravity/`
**Executable:** `C:/Users/jacks/AppData/Local/Programs/Antigravity/Antigravity.exe`
**CLI:** `antigravity` (on PATH)
