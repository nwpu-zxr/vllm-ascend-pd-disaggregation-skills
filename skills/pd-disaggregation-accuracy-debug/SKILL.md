---
name: pd-disaggregation-accuracy-debug
description: Diagnose vLLM and vLLM Ascend PD accuracy failures using top-down feature isolation or bottom-up tensor evidence. Align completed P KV/state with D's contents and placement before each component's first consumption and verify the handoff position; cover block boundaries, speculative steps, prefix/pool hits and dirty-block reuse before attributing a cause. PD methodology with optional specialist-skill reuse and standalone fallback.
license: MIT
---

# PD Disaggregation Accuracy Diagnosis

Find the first divergent boundary and the mechanism that causes it. Distinguish a direct PD defect, a PD-by-feature interaction, a model path missing PD adaptation, an independent device/software-stack fault, and an invalid comparison. A lower benchmark score or a successful transfer return does not determine the category.

This skill owns the PD diagnosis methodology and causal conclusion. Follow [skill-reuse.md](references/skill-reuse.md) to reuse suitable repository/host correctness, cache/attention, graph, operator or distributed-debug skills for bounded subproblems. Default to automatic capability-based reuse; `prefer-integrated` and `standalone` are optional workflow preferences. Without matching skills, continue with the bundled top-down/bottom-up procedures and probes. Bring specialist results back to the cross-node handoff evidence rather than treating a local pass as proof of PD correctness.

The core PD check is whether the valid KV/state produced or retained by P is present with the right content at the positions D will actually consume, before each component's first consuming operation. This can be a model-entry boundary for a completed request-level load, or a per-layer boundary after that layer's load and required state relocation. Compare tensor dumps with block/slot tables, token positions and state metadata. Correct transfer entries or successful API returns alone do not satisfy this check.

## Choose the investigation direction

- **Top-down:** use the stages below when configuration, a feature interaction or a platform failure offers a cheaper discriminating lead. Narrow the symptom, then descend to the first divergent data/state boundary.
- **Bottom-up:** follow [bottom-up-validation.md](references/bottom-up-validation.md) when transfer integrity, layout/state adaptation, missing writes or cache trampling is in question. Establish an eager, launch-blocking, deterministic-communication baseline with optional acceleration disabled where supported; compare P's completed source with D's tensors and placement before consumption, exercise boundary/hit/reuse cases, then add features incrementally.

Select or switch direction from the actual failure and available evidence. Both paths begin with a preserved failing case and verified runtime identity, and converge on the same handoff contract and causal evidence. Do not run every stage mechanically. Honor analysis-only requests. Existing authorization to instrument or run experiments remains valid.

## Extend the investigation when useful

The stages and probes in this skill are starting points, not an exhaustive list of permitted diagnostic methods. Proactively use a more discriminating method when the evidence warrants it, or broaden the investigation when the current checks cannot explain the symptom. Methods supplied by the user are examples unless the user explicitly limits the scope.

- **Other skills and tools:** use the discovery, applicability and evidence-return contract in [skill-reuse.md](references/skill-reuse.md). Profiling, memory analysis and transport diagnostics can supplement the mapped specialist workflows when useful. Read only relevant capabilities; missing skills do not prevent applying the bundled method directly with available tools.
- **Internet research:** search beyond the starting links when a failure signature, API contract or version-specific behavior needs investigation. Use official documentation, source code, maintainer issues/PRs, release notes and relevant research papers as evidence. Broader search results can provide leads; verify technical claims against primary sources and the deployed implementation. Read the supporting content, record applicability and links, and distinguish a proposed workaround from a merged fix or reproduced result. Keep private prompts, tensors, credentials and identifying logs out of public queries.
- **Model knowledge and reasoning:** use general debugging and numerical-computing knowledge to propose additional methods, such as code/input bisection, differential or metamorphic checks, invariant checks, minimal reproductions and targeted ordering instrumentation. Treat recalled version-specific facts as unverified until checked. Label deductions and hypotheses explicitly; do not invent citations or present prior knowledge as measured evidence.

Choose the next experiment by the competing explanations it separates, expected outcomes, execution cost and perturbation of the original failure. Preserve useful controls and state what each outcome would establish. New methods follow the same evidence standard as the listed probes: connect the observation to a faulty contract, test the explanation, and replay the original case. A specialized skill's conclusion or a matching internet symptom is not automatically the root cause of this deployment.

## Execution context

This skill is self-contained. Read [runtime-integration.md](references/runtime-integration.md) for standalone execution or optional MindIE knowledge, remote-dev, diagnostics and coordinator tools. No private session store, fixed checkout path, VAWS installation, sibling skill or mandatory NPU allocation is required for static analysis. Hardware experiments need an authorized matching device environment.

## Stage 0 — Preserve the symptom and comparison

Capture a failing request or a small failing set before changing configuration: exact prompt token IDs, checkpoint/tokenizer, sampling, output limit, load, run order, service logs and observable failure. Distinguish first-request failure, boundary failure, repeated-run drift, concurrency dependence, graph-only failure, and speculative-decoding failure.

Keep the original failing configuration and a known-good comparison. Record missing evidence instead of converting a suspicion into a root cause. If no failure is reproducible, first improve case selection and observability.

## Stage 1 — Check configuration and compatibility

Follow [configuration-and-ab.md](references/configuration-and-ab.md). Compare effective P/D settings with documentation for the deployed vLLM/Ascend revision and hardware, implementation validation, and the user's known-good configuration. Verify actual imported code and loaded stack, model/draft/quantization compatibility, role topology, API/token semantics and evaluation settings.

Use [official-docs.md](references/official-docs.md) to find and read the exact model/hardware recipe in the official vLLM Ascend docs. Identify the real transport backend; for HIXL, consult its official repository/API docs and Wiki for applicable configuration, platform and completion constraints. Record the supporting pages and runtime discrepancies. Reuse this evidence in feature isolation and platform/transfer diagnosis; a Wiki symptom match is a hypothesis, not a root cause.

**Decision:** fix a demonstrated mismatch and replay the original case. If no mismatch explains it, retain the verified configuration table and proceed.

## Stage 2 — Isolate feature interactions

Compare relevant CP/sequence-parallel, fused MC2/MegaMoE, communication overlap, async scheduling, graph, speculation and cache-lifecycle features one factor at a time. Verify that dispatch actually changes. Use the PD on/off × feature on/off matrix in [configuration-and-ab.md](references/configuration-and-ab.md); do not disable all features and declare the cause found.

**Decision:** identify the smallest failing combination and its nearest passing control. A disappearing symptom selects the next boundary to inspect; it does not by itself prove a connector or operator defect.

## Stage 3 — Separate hardware, interconnect and software-stack effects

Use [platform-triage.md](references/platform-triage.md) when device/collective evidence, rank dependence, async symptoms or synchronization sensitivity warrant it. Check physical devices and links independently from CANN/driver/torch_npu/HCCL/custom-kernel builds. Compare launch-blocking and supported deterministic-communication modes with tensor evidence, recording their timing and graph effects.

**Decision:** a failure that follows a device/link or a controlled stack change takes that branch. A failure hidden by synchronization remains a timing/stack hypothesis until the violated event, buffer lifetime or operator contract is identified. Do not exclude PD merely because blocking helps.

## Stage 4 — Verify the PD data and lifetime path

Follow [evidence-ladder.md](references/evidence-ladder.md):

1. Establish the intended handoff and actual D `num_computed_tokens`, input tokens and positions. Check full-hit N-1, partial hits, bounded replay and fallback separately. Match P/D request identities, attempts, layers/specs, owners, logical token intervals and exact read/write byte ranges.
2. Capture each P source segment after its relevant cache writers finish, including any draft/MTP writers of that segment, while the published generation remains stable. Streaming publication need not wait for unrelated layers.
3. Capture D after transfer visibility, then again after required state relocation and immediately before that component's first consumer. Trace the active runner/connector hooks; a method named `wait_for_layer_load` can be a no-op or protect P reuse instead of loading D data.
4. Compare payload and consumer metadata independently: positions, seq_len, block/slot tables, compression/ring/accepted-state cursors.
5. Check cache trampling and hybrid aliasing using live physical ranges and ownership over time, not pointer equality alone.

**Decision:** localize source generation, mapping, transfer/visibility, overwrite/reuse, or consumer-state failure. Address correctness establishes only the transfer plan.

Use the boundary, speculative-step, P/D prefix-hit, external-pool-hit and dirty-block reuse matrix in [bottom-up-validation.md](references/bottom-up-validation.md) when a cold single-request copy is insufficient to exercise the failure.

## Stage 5 — Localize computation and sampling

With corresponding KV and metadata established, compare the first consuming forward and the earliest divergent layer. Align logical token positions and teacher-force the same prefix when free generation diverges. Compare target logits and selected-token/top-k logprobs with matching preprocessing and normalization; top-k agreement alone is incomplete evidence.

Separate draft quality, target multi-token verification, accept/reject state, sampling and proxy/postprocessing. Reduce the suspect operation to a single call or short sequence while preserving real dtype, stride, shape, workspace, streams and rank semantics. Use an installed operator/graph debugging skill if helpful; otherwise perform that reduction directly.

## Stage 6 — Establish cause and validate the remedy

Produce the causal classification in [experiments.md](references/experiments.md), including the minimal failing condition, first divergent artifact, violated contract and a controlled fix/replay. Re-run the original failing case, relevant boundaries, and repeated/concurrent behavior that initially exposed the issue. Remove diagnostic perturbations when validating the fix.

If the evidence stops at a hypothesis, say so and give the next discriminating experiment. Do not force a PD root cause after other checks pass.

## Targeted fast probes

Read [quick-probes.md](references/quick-probes.md) before sentinel-filling KV, checking `</think>` counts, comparing logits/logprobs, or reducing an operator. These probes have distinct coverage and false-positive conditions. [failure-injection.md](references/failure-injection.md) covers request failures, exceptions, leases and cleanup.

The optional standard-library [audit_outputs.py](scripts/audit_outputs.py) summarizes normalized benchmark JSONL without model dependencies. It finds candidates for inspection; it does not certify accuracy.

## Deliverable

Use [report-template.md](references/report-template.md) as a compact case record. State what was observed, controlled, inferred and still unknown; link configuration, raw evidence and exact revisions. Separate definition/static checks, runtime reproduction and statistical accuracy evidence. Never treat historical success as validation of the current build.
