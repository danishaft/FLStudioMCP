# fLMCP fork — Gap Analysis vs FL Studio Pilot (fls-pilot)

Date: 2026-08-14
Base: geezoria/FLStudioMCP v0.3.0 (159 tools, TCP bridge, 68 tests passing on our fork)
Target: thunderdew-dawn/fls-pilot v3.0.0-beta.3 (rollback-first production assistant)

## Verdict
fLMCP wins on reach (159 raw tools, full-cycle control). fls-pilot wins on
safety and agent ergonomics. This fork keeps fLMCP's reach and adds fls-pilot's
guardrails. Priority order below.

## P0 — Must have before an agent touches a real project

### 1. Rollback-first write layer
- fls-pilot: every persistent mutation routes through snapshot -> write ->
  readback -> changelog -> rollback (`fl_rollback_last_change`, named rollback
  units). FL's native Ctrl+Z is unreliable for API scripts.
- fLMCP: nothing. Agent writes are one-way.
- Plan: wrap mutating bridge calls with a before-state snapshot
  (channels.mixer/pattern state), persist to a JSONL changelog, add
  `rollback` CLI command that restores the last N snapshots.

### 2. Knowledgebase-backed parameter ranges
- fls-pilot: `kb_get_conversion` — dB/Hz mappings and verified safe ranges
  checked before writes; kills knob-value hallucination (150% on a 100% knob).
- fLMCP: plugins.get/set param passes raw values through.
- Plan: embed a compact JSON knowledgebase of known FL plugin param ranges
  (vol/pan dB scale, tempo bounds, mixer gain limits) + a `--check` flag on
  set commands that rejects out-of-range values.

### 3. Agent briefing resource
- fls-pilot: `fl://agent-briefing` — tool selection, safety gates, stop rules,
  API boundaries read before live work.
- fLMCP: no orientation resource; agents discover tools blindly.
- Plan: `flmcp brief` CLI command + MCP resource that prints the operating
  contract: what the API can/can't do, safety gates, error semantics.

## P1 — Ergonomics

### 4. Honest API-boundary mapping
- fls-pilot documents in plain language: cannot load plugins, cannot render
  audio, cannot push notes directly (needs armed MCP_Apply), no deep audio-clip
  params. Generates manual checklists instead of claiming success.
- fLMCP: renders + plugin loading attempted via bridge; failures are opaque.
- Plan: audit each of our 159 tools against FL 25.2.5 API and mark
  verified / attemptable / impossible in a capability table (like fl-mcp's
  verified-vs-attemptable split). CLI `flmcp audit` prints it.

### 5. Consolidated domain tools
- fls-pilot: folded dozens of single-purpose tools into `fl_transport`,
  `fl_mixer`, `fl_channel`, `fl_effect`, `fl_batch` — less tool-selection
  noise, more context for the agent.
- fLMCP: 159 fine-grained tools = context bloat.
- Plan: keep raw tools (reach) but add domain facades in the CLI: `flmcp
  mixer get/set vol|pan|mute|solo|route`, `flmcp transport play|stop`, etc.

## P2 — Nice to have

### 6. Push notifications
- fls-pilot: polls live peak meters (Mix Doctor). fLMCP already has push events
  (transport.tick, refresh, projectLoad) — keep and surface in CLI `flmcp watch`.

### 7. Preflight / health checks
- fls-pilot: `fl_check_project_preflight` export-readiness report (mix review +
  routing review + cleanup).
- Plan: `flmcp preflight` — gather project metadata, mixer levels, routing
  state, ungrouped/unrouted channels, and print a readiness report.

## What fLMCP already has that fls-pilot lacks (keep)
- TCP bridge — no loopMIDI/IAC dependency, Wine-friendly, push events.
- Generators (beats/chords/basslines/arps/melodies) — 14 tools.
- Voice-to-MIDI (mono + polyphonic via Basic Pitch).
- Audio analysis (tempo/key/onsets/melody) + DnB flip.
- Render + project save/undo/redo tooling.
- 109 tests (68 passing here; 15 upstream baseline grew via hardening).

## Implementation order
1. Rollback layer + changelog (P0-1)
2. CLI: domain facades + brief + audit (P0-3, P1-5, P1-4)
3. Knowledgebase param checking (P0-2)
4. Preflight (P2-7)
5. Re-test suite green after each step.
