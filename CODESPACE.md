# Codespace Workflow

## What This Is

A cloud dev environment (Linux, free tier) where you build and test everything that
doesn't need FL Studio running. Git syncs work back to your local machine for
live FL testing.

## Quick Start

1. Open https://github.com/danishaft/FLStudioMCP
2. Code -> Codespaces -> Create codespace on main
3. Wait for setup (installs Python deps automatically via devcontainer)
4. Verify:
   ```bash
   python -c "import fl_studio_mcp; print('ok')"
   pytest -q          # 68+ tests, no FL needed
   ```

## What Works in Codespace

- Writing/editing all bridge handlers (src/fl_studio_mcp/tools/)
- Running the full test suite
- Building the CLI (install Go + clihub, run `clihub generate`)
- Layer 3 (PyFLP) offline .flp tools — no FL needed
- Writing Layer 2 (GUI) scripts — testable locally later

## What Needs Your Machine

- Live bridge testing against FL Studio (needs FL running)
- GUI automation against FL's window
- Audio recording / Edison verification

## Sync Loop

```
Codespace (build + test)  --git push-->  GitHub  --git pull-->  Local (FL verify)
      ^                                                              |
      +--------------------- git push <----------------------------+
```

## Agent / Memory Continuity

The repo carries the full agent context:

| Path in repo | Contents |
|---|---|
| `agent/merlin.md` | Merlin agent definition |
| `agent/merlin.toml` | Launch profile |
| `agent/brain/` | Memory system (MEMORY.md, lessons, patterns, journal) |
| `config/opencode/` | OpenCode config + agent wrapper |

To use Merlin in the Codespace, copy to home:
```bash
mkdir -p ~/.codex/agents/brain ~/.config/opencode/agent
cp agent/merlin.md ~/.codex/agents/
cp agent/merlin.toml ~/.codex/agent-roles/ 2>/dev/null || true
cp agent/brain/*.md ~/.codex/agents/brain/
cp config/opencode/opencode.json ~/.config/opencode/
cp config/opencode/agent/merlin.md ~/.config/opencode/agent/
```

## Local Sync After Codespace Work

```bash
# On your machine (Linux or Windows)
git pull
# Rebuild CLI if handlers changed
pip install -e '.[dev]'
# (Windows) run setup-windows.ps1 helpers as needed
```
