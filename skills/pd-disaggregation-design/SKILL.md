---
name: pd-disaggregation-design
description: Design, review, implement, or refactor vLLM and vLLM Ascend PD disaggregation connectors. Assess a new KV-cache layout against a specified connector using cache spec definitions, all cache shapes, strides, sizes, storage and semantic contracts; identify compatibility gaps and adaptation options. Covers version-specific lifecycle, topology, Mooncake, NIXL and layerwise/chunkwise transfer. PD methodology with optional specialist-skill reuse and standalone fallback.
license: MIT
---

# PD Disaggregation Design

Use the active source and runtime contracts. Historical implementations suggest checks; they do not establish current support. Honor analysis-only scope and preserve already-authorized implementation work without repeatedly requesting permission.

This skill owns the PD design methodology and final compatibility verdict. Follow [skill-reuse.md](references/skill-reuse.md) to reuse suitable repository/host skills for cache implementation analysis or change validation. Default to automatic capability-based reuse; `prefer-integrated` and `standalone` are optional workflow preferences. Without matching skills, use the spec/layout, lifecycle, mapping and validation methods bundled here. A specialist's cache verdict does not establish connector compatibility.

## Identify the actual path

Record relevant P/D framework/plugin/connector revisions and dirty changes, imported classes, hardware, runner, backend, model/draft, concrete cache specs and TP/PP/DP/PCP/DCP/KVPP topology.

Distinguish upstream Mooncake, Ascend V1/V2/Hybrid/Layerwise/Store/RD2H and NIXL. Determine READ versus WRITE, allocation/publication order, and completion/release ownership instead of assuming all PD is D-initiated pull.

Preserve the requested reference commit, supported versions and exclusions. Do not add obsolete compatibility because an older task needed it. Consult current documentation and implementation; missing support evidence means unknown.

Use [official-docs.md](references/official-docs.md) to select the model/hardware recipe from the official vLLM Ascend documentation and, when the actual or proposed backend uses HIXL, read its official repository/API documentation and Wiki. Match revisions, verify readable content and trace documented configuration to its runtime consumer. Include transport constraints in design and layout verdicts rather than assuming all connector backends share them.

Read [runtime-integration.md](references/runtime-integration.md) for standalone or optional MindIE execution. This skill does not require a particular repository layout, personal history, private endpoint or sibling skill.

## Assess a new KV-cache layout

When the user supplies a layout and asks whether a connector supports it, follow [layout-compatibility.md](references/layout-compatibility.md). Start from the concrete cache spec definitions and their derived sizing/grouping semantics, then trace allocation and runtime views. Inventory every cache component and alias on both sides, normalize shape/stride/size units, derive valid physical segments, and compare them with the specified connector's actual spec dispatch, descriptor, registration, handshake, mapping, transfer and lifetime capabilities. Matching tensor layouts do not establish matching spec semantics.

Return a per-component compatibility matrix and an overall verdict: supported by the current implementation within stated conditions, requires adaptation, incompatible under fixed constraints, or insufficient evidence. Separate static feasibility from runtime validation. For each gap, identify the failing contract and smallest adaptation direction, with worked address examples and validation cases. Shape equality or successful registration alone cannot establish support; a layout-only assessment does not authorize code changes or device experiments.

## Prove separate contracts

| Contract | Question | Reference |
|---|---|---|
| Lifecycle | When is data readable, D runnable and storage reusable? How do failures terminate? | [lifecycle.md](references/lifecycle.md) |
| Layout and addresses | How do descriptors become storage, views, registration and transmitted bytes? | [cache-layout.md](references/cache-layout.md) |
| Topology and mapping | Which replica/head/sequence owner provides each logical interval? | [topology-mapping.md](references/topology-mapping.md) |
| Execution and validation | Do events, aggregation, errors and coalescing preserve these contracts? | [validation.md](references/validation.md) |

Trace the affected chain to its consumers:

```text
descriptor -> allocation/reshape -> runtime views -> registration
-> handshake aggregation/serialization -> request metadata
-> layer/owner selection -> token/block mapping -> byte ranges
-> device readiness -> transfer -> completion/failure -> reuse/release
```

Do not audit every module for a small change, but do not infer complete model support from registration alone. Data changes require payload evidence; completion changes extend through scheduler/proxy termination and resource release.

## Design and implement

1. Describe current and intended behavior, applicability and minimal edit scope. Separate inherent constraints, implementation limitations, historical observations and hypotheses.
2. Preserve model/planner semantics. Do not alter `layer_stride=0`, invent head counts, remove backend guards or force equal strides merely to fit a connector assumption.
3. Keep the current metadata representation internally consistent. For layer-aligned arrays, verify outer/nested indexes and serialization consumers. A single outer metadata class is one design choice, not a universal requirement.
4. Attribute failures to actual submitted buckets and request dependencies. Drain or reliably isolate in-flight accesses before releasing storage; cleanup must not publish failed payload as usable.
5. Select sufficient boundary validation. Report static checks, unit tests, device E2E, fault injection and accuracy/performance evidence separately.

For a full numerical investigation, use `pd-disaggregation-accuracy-debug` if installed; otherwise follow the same source/transfer/restoration/first-consumption evidence boundaries, per layer when required. For deployment use `pd-disaggregation-serving` if installed, or the environment's existing lifecycle tools. These are optional specializations, not installation prerequisites.

## Deliverable

Provide the conclusion and exact applicability, source locations, useful timing/address examples, changes, validation and unresolved conditions. Briefly identify reused specialist evidence or standalone fallback where relevant. Treat legacy rules in [design-pitfalls.md](references/design-pitfalls.md) as counterexamples to overgeneralization, not a support matrix.
