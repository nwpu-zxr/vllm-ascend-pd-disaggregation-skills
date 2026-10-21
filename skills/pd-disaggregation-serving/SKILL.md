---
name: pd-disaggregation-serving
description: Prepare, launch, inspect and stop vLLM or vLLM Ascend PD services, with model-specific P/D/proxy configuration and actual KV-transfer evidence. Reuse an existing deployment workflow and lifecycle controllers when present; use standalone execution otherwise. Use for PD service setup or review, not numerical root-cause diagnosis.
license: MIT
---

# PD Disaggregation Serving

Deliver reproducible P/D/proxy configuration and verified results. For script-only requests, prepare and statically validate scripts. For an authorized launch, continue through health checks and a real PD request. Do not reuse historical addresses, device counts, ports or model paths as defaults.

This skill owns the PD deployment methodology and acceptance criteria. Follow [skill-reuse.md](references/skill-reuse.md) to reuse suitable repository/host serving skills for bounded execution steps. Default to automatic capability-based reuse; `prefer-integrated` and `standalone` are optional workflow preferences. Without matching skills, use the bundled launch and acceptance methods with available tools. In every mode, retain one deployment plan and one lifecycle controller per service.

## Resolve the target and execution context

Use current inventory, existing scripts and user instructions to determine endpoints, model/checkpoint, hardware, P/D devices, parallel topology, connector, proxy and source paths. Ask only for necessary information that cannot be recovered from available context.

Read [runtime-integration.md](references/runtime-integration.md). Use the environment's existing lifecycle tools or native authorized tools. MindIE remote-dev, knowledge, diagnostics and coordinator capabilities are optional. Do not force an existing endpoint into a new session framework or require VAWS to use this skill.

Before service mutations, choose one deployment plan and one lifecycle controller per service. If another workflow already manages the deployment, use this skill for PD configuration review and missing acceptance evidence, and execute changes through that workflow. If this skill leads, reuse compatible host controllers for execution. Explicit user choices determine the requested workflow but do not silently transfer ownership of existing processes. Read [workflow-coordination.md](references/workflow-coordination.md) when another serving skill/controller is present, when reusing services, or when recovering an interrupted launch. Loading multiple skills must not start multiple deployment workflows.

Preserve requested topology, quantization, backend, MTP and environment settings. For a basic deployment, avoid adding optional tuning features; retain model/hardware requirements and explain them. For an existing failure, record its original configuration before constructing a minimal control.

Follow [official-docs.md](references/official-docs.md) before deriving model/platform or transport settings: read the matching model recipe in the official vLLM Ascend docs, combine it with the relevant PD guide, and consult the official HIXL repository/API docs and Wiki if HIXL is on the selected path. Record version applicability, configuration ownership and effective values; use the documented retrieval fallback if GitCode returns only a frontend shell.

## Prepare and launch

1. Verify actual source imports, local/remote code identity, model and proxy entry points, visible devices/occupancy, reachable addresses and complete port ranges. When local edits must run remotely, synchronize and verify them using the available parity workflow. Preserve a remote-only failure snapshot before overwriting it.
2. Prepare version-specific P/D/proxy configuration for the selected controllers; generate scripts only where needed. Reuse their authoritative state records and link them from the deployment plan. Validate shell syntax, JSON, paths and current CLI support as applicable. Use [launch-contract.md](references/launch-contract.md); there is no cross-version universal `vllm serve` recipe.
3. Inspect existing role state and start only required roles through their selected controllers, in the connector's real allocation/handshake order. Record returned job/process identity before waiting. A D-allocation-first layerwise path need not share the start order of a conventional pull path. A pending or uncertain launch must be reconciled before retrying.
4. Reuse applicable current smoke evidence or send a traceable request through the proxy to collect what is missing. Verify actual KV transfer, complete output and request resource release with [acceptance.md](references/acceptance.md).
5. On failure, preserve the earliest error and all relevant rank evidence. Check the controller's rollback result before further cleanup; roll back only changes within this attempt's scope and preserve unaffected reused services and externally managed proxies. If services should remain running, provide exact status and stop commands through their owning controllers.

Use the host project's run-record schema when required. Without one, a compact record of environment, source identity, topology, commands, process IDs, configuration and artifacts is sufficient. Never introduce a mandatory import from a private workspace library.

## Deliverable

Provide configuration/script locations, role endpoints, devices/topology, each lifecycle controller and authoritative state reference, current service state and smoke evidence. Reuse evidence from the same deployment/configuration instead of launching a second deployment for another skill. Distinguish scripts validated, services ready, actual transfer verified and numerical correctness tested. HTTP 200 is not proof of correct KV or accuracy.

Use `pd-disaggregation-accuracy-debug` if installed for numerical symptoms, or follow source/transfer/restoration/first-consumption boundaries directly, per layer when required. Distributed startup and graph failures can use specialized skills when available; siblings are not installation prerequisites.
