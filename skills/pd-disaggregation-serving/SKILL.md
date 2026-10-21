---
name: pd-disaggregation-serving
description: Prepare scripts, launch, inspect, smoke-test and stop vLLM or vLLM Ascend PD disaggregation on explicit endpoints or managed environments. Covers P/D/proxy configuration, actual runtime code, port ranges, transfer evidence and cleanup. Use for service setup rather than numerical root-cause diagnosis. Supports standalone use and optional MindIE Agent tools.
license: MIT
---

# PD Disaggregation Serving

Deliver reproducible P/D/proxy configuration and verified results. For script-only requests, prepare and statically validate scripts. For an authorized launch, continue through health checks and a real PD request. Do not reuse historical addresses, device counts, ports or model paths as defaults.

## Resolve the target and execution context

Use current inventory, existing scripts and user instructions to determine endpoints, model/checkpoint, hardware, P/D devices, parallel topology, connector, proxy and source paths. Ask only for necessary information that cannot be recovered from available context.

Read [runtime-integration.md](references/runtime-integration.md). Use the environment's existing lifecycle tools or native authorized tools. MindIE remote-dev, knowledge, diagnostics and coordinator capabilities are optional. Do not force an existing endpoint into a new session framework or require VAWS to use this skill.

Preserve requested topology, quantization, backend, MTP and environment settings. For a basic deployment, avoid adding optional tuning features; retain model/hardware requirements and explain them. For an existing failure, record its original configuration before constructing a minimal control.

Follow [official-docs.md](references/official-docs.md) before deriving model/platform or transport settings: read the matching model recipe in the official vLLM Ascend docs, combine it with the relevant PD guide, and consult the official HIXL repository/API docs and Wiki if HIXL is on the selected path. Record version applicability, configuration ownership and effective values; use the documented retrieval fallback if GitCode returns only a frontend shell.

## Prepare and launch

1. Verify actual source imports, local/remote code identity, model and proxy entry points, visible devices/occupancy, reachable addresses and complete port ranges. When local edits must run remotely, synchronize and verify them using the available parity workflow. Preserve a remote-only failure snapshot before overwriting it.
2. Build version-specific P/D/proxy scripts and an untracked run-state directory. Validate shell syntax, JSON, paths and current CLI support. Use [launch-contract.md](references/launch-contract.md); there is no cross-version universal `vllm serve` recipe.
3. Start roles according to the connector's real allocation/handshake dependencies. Record process identity, logs and health at each stage. A D-allocation-first layerwise path need not share the start order of a conventional pull path.
4. Send a traceable request through the proxy. Verify actual KV transfer, complete output and request resource release with [acceptance.md](references/acceptance.md).
5. On failure, preserve the earliest error and all relevant rank evidence. Clean up processes started by this run as appropriate. If services should remain running, provide exact status and stop commands.

Use the host project's run-record schema when required. Without one, a compact record of environment, source identity, topology, commands, process IDs, configuration and artifacts is sufficient. Never introduce a mandatory import from a private workspace library.

## Deliverable

Provide script locations, role endpoints, devices/topology, current service state and smoke evidence. Distinguish scripts validated, services ready, actual transfer verified and numerical correctness tested. HTTP 200 is not proof of correct KV or accuracy.

Use `pd-disaggregation-accuracy-debug` if installed for numerical symptoms, or follow source/transfer/restoration/first-consumption boundaries directly, per layer when required. Distributed startup and graph failures can use specialized skills when available; siblings are not installation prerequisites.
