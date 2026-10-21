# vLLM Ascend PD Disaggregation Skills

[English](README.md) | [简体中文](README.zh-CN.md)

Agent skills for vLLM Ascend prefill/decode disaggregation: connector design, KV-cache spec/layout compatibility, deployment, and evidence-based accuracy diagnosis.

The collection contains three independently usable English skills. They turn model, runtime and transport evidence into scoped engineering conclusions. They do not provide a universal launch command or a fixed model-support matrix.

Their primary role is PD methodology: define the question, choose the evidence and reach a scoped conclusion. Suitable repository or host skills can supply specialist analysis and execution; the bundled procedures remain usable when those skills are absent.

| Skill | Use it for | Deliverable |
|---|---|---|
| [pd-disaggregation-design](skills/pd-disaggregation-design/SKILL.md) | Connector design/review and new KV-cache spec/layout assessment | Contract analysis, per-component compatibility verdicts, adaptation gaps and validation plan |
| [pd-disaggregation-serving](skills/pd-disaggregation-serving/SKILL.md) | Preparing or launching P/D/proxy services | Reproducible configuration, readiness, actual-transfer evidence and cleanup instructions |
| [pd-disaggregation-accuracy-debug](skills/pd-disaggregation-accuracy-debug/SKILL.md) | Numerical divergence, corrupted KV, NaNs, repetition and speculative acceptance changes | First-divergence evidence, controlled experiments and causal classification |

## Install and use

Get the collection:

```bash
git clone https://github.com/nwpu-zxr/vllm-ascend-pd-disaggregation-skills.git
cd vllm-ascend-pd-disaggregation-skills
```

Copy the complete directory of each desired skill from `skills/` into the skill search directory supported by your agent. Retain its references, scripts, license and optional `agents/openai.yaml` metadata. Each package works without installing its siblings. Agents without a skill loader can read the selected `SKILL.md` directly and follow its referenced workflow.

Example requests:

- Use `pd-disaggregation-design` to evaluate this new cache spec and all P/D tensor shapes, strides, sizes and aliases against the specified Mooncake connector revision. Report supported conditions, unknowns and adaptation gaps.
- Use `pd-disaggregation-serving` to prepare a minimal P/D/proxy deployment for this model and these endpoints. Check the official model recipe and actual transport, then validate a request with real remote KV transfer.
- Use `pd-disaggregation-accuracy-debug` to isolate this PD accuracy regression. Preserve the failing setup, test feature interactions and locate the first difference between P output, transferred KV, D input and computation.

Analysis-only requests remain analysis-only. Device experiments use an authorized matching runtime. Host-side package checks and output audits require Python 3.10 or newer and no third-party Python packages.

## What the workflows cover

Design follows spec definitions through grouping, allocation, runtime views, registration, peer metadata, token/head mapping, transfer and lifetime. A matching shape or successful memory registration is insufficient to establish compatibility.

Serving separates script validation, service readiness, routing, actual KV transfer and cleanup. It reuses the environment's service and remote-development tools instead of installing a second process manager.

Accuracy diagnosis can proceed top-down from configuration/features or bottom-up from tensor evidence. Its core check aligns each completed P segment with the contents and locations D consumes after required loading/restoration and before that component's first consumer. This can be a per-layer boundary inside forward. The handoff ledger covers N-1 where applicable, partial hits and bounded replay. A controlled eager/blocking/deterministic baseline can establish this contract before features are reintroduced. Coverage includes block/spec boundaries, speculative steps, P/D prefix and external-pool hits, concurrency and measured dirty-block reuse. Device/stack and first-computation evidence complete the causal analysis. Fast probes have explicit limits: a missing reasoning tag is not an accuracy verdict, and a successful transfer return does not prove payload correctness.

The diagnostic methods are intentionally open-ended. Use relevant skills available in MindIE Agent or another host, internet research grounded in primary sources, and general debugging knowledge to select additional discriminating experiments. Preserve source attribution, version applicability and controlled evidence; neither a recalled explanation nor a matching issue report establishes the current root cause.

Each skill includes a model-specific lookup workflow for the [official vLLM Ascend docs](https://docs.vllm.ai/projects/ascend/en/latest/index.html). For an active or proposed HIXL path, it also consults the [official HIXL repository](https://gitcode.com/cann/hixl) and [Wiki](https://gitcode.com/cann/hixl/wiki/Home.md). Documentation must match the actual build and hardware; `latest` and `master` are discovery entry points.

## Runtime integration

Standalone use requires no VAWS installation, private session history or fixed workspace path. In an existing workspace, follow its isolation, code-parity, service lifecycle and run-record rules. MindIE Agent remote-dev, knowledge, diagnostics and coordinator tools are optional adapters discovered from the current harness.

Choose a reuse preference in ordinary language; no configuration file or new CLI option is needed:

| Preference | Behavior |
|---|---|
| `auto` (default) | Reuse a relevant, available specialist skill after checking applicability; otherwise use the bundled methods |
| `prefer-integrated` | Prefer suitable repository/MindIE skills; report missing optional capabilities and continue with a bundled fallback |
| `standalone` | Use the bundled methodology and available tools without optional specialist-skill dependencies |

For example: “Use `pd-disaggregation-accuracy-debug` in `prefer-integrated` mode; reuse available correctness, graph and operator skills, and use the bundled methods for uncovered steps.” Explicit requirements to use a particular system and mandatory host rules remain binding in every mode.

The [capability map and reuse contract](skills/pd-disaggregation-design/references/skill-reuse.md) cover cache/layout analysis, deployment, correctness comparisons and numerical/distributed debugging. Each package includes its own copy. Skills are selected by their actual framework/version/input contracts, not name alone. Keep the same request/build evidence across steps and return specialist findings to the PD conclusion; a local check passing does not establish end-to-end PD correctness.

When another serving skill is available, use one deployment plan and one lifecycle controller per service. An existing workflow retains its services; these skills can supply PD configuration review, diagnosis and missing acceptance evidence without launching a second deployment. New deployments use compatible host controllers or a standalone path. Record proxy ownership separately, reconcile uncertain launches before retrying, and preserve reused services during rollback. See [workflow coordination](skills/pd-disaggregation-serving/references/workflow-coordination.md). These instructions guide the agent; actual concurrency protection depends on the host's locks/leases and controller behavior.

See [catalogue integration](docs/catalogue-integration.md) for registering the published source with Awesome MindIE Skills. That catalogue indexes source definitions; it does not host this source package.

## Output audit helper

Normalize complete response attempts into JSONL with unique string `id` and generated `text`. Optional fields are `output_tokens`, `max_output_tokens`, `finish_reason` and boolean `correct`.

```bash
python3 skills/pd-disaggregation-accuracy-debug/scripts/audit_outputs.py outputs.jsonl --expect-think-close > output-audit.json
```

Use `--expect-think-close` only when the output contract requires that tag. The helper reports heuristic candidates, length-limit indicators and supplied correctness labels. It omits generated text but retains IDs and metadata. See [probe limitations](skills/pd-disaggregation-accuracy-debug/references/quick-probes.md).

## Validate this repository

```bash
python3 scripts/validate.py
```

This checks package structure, frontmatter, local links, standalone boundaries, shared reference consistency and the output-audit regression suite. It requires no model, Torch, NPU, network access or user-specific skill validator.

These checks do not validate a model, connector or hardware combination. Runtime support and accuracy claims require their own versioned evidence. See [CONTRIBUTING.md](CONTRIBUTING.md) for maintenance expectations.

The [2026-10-21 source audit](docs/source-audit.md) records the inspected vLLM/Ascend commits, code evidence, corrected assumptions and manual workflow cases. It separates source review from unexecuted device and service validation.

## License

[MIT](LICENSE). Individual skill copies include the same license. Referenced upstream documentation retains its own licensing and is not bundled here.
