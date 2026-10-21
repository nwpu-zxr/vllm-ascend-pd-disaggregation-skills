# Standalone and MindIE Agent integration

The skill is portable Markdown plus bundled resources. It has no mandatory plugin, private history, fixed checkout path, sibling skill, remote session manager or Python package dependency. Read only the references relevant to the task.

## Standalone execution

1. Identify the available repository, runtime, endpoint and authorization from current context. Discover version-specific code and documentation.
2. Use native file/search/command tools for local work and the host's approved mechanism for remote work. Do not run NPU-dependent checks on a machine without the matching stack and devices.
3. Keep a compact case/run record: revisions and dirty hashes, actual imports, hardware/stack, effective configuration, input, hypothesis, controlled change, commands, observed result and artifacts. Mark missing evidence explicitly.
4. Keep transient state untracked and credentials out of reports. Existing host-project instructions govern isolation and artifact schemas.

Missing remote access blocks only the dependent runtime experiment. Continue useful static diagnosis and identify the exact evidence still required. Do not install an infrastructure stack simply to read or apply the skill.

## Optional MindIE capabilities

[MindIE Agent](https://github.com/mindie-agent/mindie-agent) documents a component-based ecosystem. Discover the tools exposed by the current harness and inspect their schemas; do not assume a universal MCP prefix, CLI alias, bootstrap script or service installed by this skill.

| Capability, when present | Use |
|---|---|
| Knowledge query/explain | Retrieve version-specific compatibility or failure evidence; read applicability, provenance and limitations before reusing a result |
| Remote development | Inspect files and runtime state, execute controlled commands/jobs, edit authorized instrumentation and collect artifacts |
| Diagnostics | Examine device/collective/system failures and correlate physical devices with rank-level symptoms |
| Coordinator | Coordinate resources only when shared/parallel work requires it; preserve existing allocations |
| Profiler | Collect timing evidence when needed; a profile does not replace correctness evidence |

Use available tools instead of duplicating their state management. Missing optional capabilities fall back to the standalone workflow, not an invented tool name. Do not publish knowledge, send external messages or allocate unrelated resources merely because a tool is available.

If the host workspace requires a particular run manifest, parity workflow or managed session, follow it there. Legacy VAWS manifests and `.remote-dev` state directories are host integration details, not requirements for other consumers.

## Catalogue distribution

[Awesome MindIE Skills](https://github.com/mindie-agent/awesome-mindie-skills) is a catalogue, not the source home of this package. Its source revision, license, maintainer, path and SHA256 must identify the actual published source. Definition review and hardware reproduction are separate claims. Do not claim a runtime validation based on this skill's examples or historical observations.

Retain the bundled MIT license and all references/scripts when copying a skill directory. `agents/openai.yaml` provides optional Codex interface metadata; the workflow remains in `SKILL.md`. Sibling skill names are routing suggestions with inline fallback behavior, not required imports.
