# Configuration review and feature isolation

Use [official-docs.md](official-docs.md) for model-specific lookup in the official vLLM Ascend docs and active-backend lookup in HIXL's repository/API docs and Wiki, including content-access fallbacks and version/evidence recording.

## Stage 1: verify what actually runs

Build one compact P/D comparison table from process arguments, effective runtime configuration, loaded module/library paths and model metadata. A launcher or `pip show` alone is insufficient.

Record framework/plugin commits and dirty changes; driver, firmware, CANN, torch_npu, HCCL and custom-operator builds; device model and rank-to-device mapping; main/draft checkpoint and tokenizer hashes; quantization and scale metadata; cache dtype/layout; attention and MoE backends; runner; TP/PP/DP/PCP/DCP/EP/KVPP; graph, asynchronous scheduling, prefix caching, chunking, offload and speculative settings. Record environment variables only when relevant; exclude secrets.

Use this order of authority:

1. Documentation, release compatibility matrix and model recipe matching the deployed revision and hardware.
2. The deployed configuration parser, validation and dispatch code, plus startup logs showing effective values.
3. A user-provided known-good configuration, with its environment and success criteria.

Resolve disagreements explicitly. A current `latest` recipe is not proof for an older release. A provided script is a comparison baseline, not proof that it was deployed. Ask only for missing information that changes the diagnosis.

Check weights versus quantization configuration, main versus draft compatibility, context/output limits, chat template and exact input token IDs, special/stop tokens, API/proxy field forwarding, sampling and benchmark postprocessing. Check P/D protocol compatibility and advertised endpoints as well as parallelism. A role-specific setting may legitimately differ; do not make every flag identical merely to simplify comparison.

For Ascend, search the selected vllm-ascend checkout's `docs/source/tutorials/models/`, configuration docs, FAQs and release notes. Configuration names move: for example, fused MC2 may be configured through additional configuration rather than an older environment variable. Confirm which operator actually executes and whether an automatic fallback/override changed another setting.

Inspect initialization side effects as well as the parser. Some revisions normalize `enable_fused_mc2` while retaining a separate MegaMoE capability flag; an effective scalar alone may not identify the selected operator. Batch-invariant mode can override weight layout, HCCL/LCCL settings and operator determinism together. Record values after these overrides and the dispatched operation; do not treat either example as a stable cross-version flag recipe.

**Exit evidence:** a reproducible baseline command/configuration for each role, its actual runtime identity, and any remaining unsupported or unknown combinations. Correct a concrete configuration mismatch and rerun the failing case before deep tensor instrumentation.

## Stage 2: test feature interactions

Preserve the original failing setup. Select one feature family that can affect the observed boundary, change one causal factor, restart only affected test services, and confirm the effective dispatch changed. A flag that does not alter runtime behavior is not a valid A/B test.

| Family | Useful comparison | Essential control |
|---|---|---|
| CP/sequence parallelism | PCP/DCP/sequence-parallel disabled or reduced versus original | Keep sufficient memory; record changed TP/head ownership, interleave, reduction and batch shape |
| Specialized communication/compute | fused MC2, MegaMoE, FlashComm or overlap path versus supported unfused/reference path | Check actual kernel/backend, weight dtype, EP topology and dispatch thresholds |
| Execution ordering | async scheduling, multistream overlap, graph versus supported synchronous/eager mode | Separate scheduler async from device async; target and draft graph modes are independent |
| Speculation | none, one draft step, original steps using the same target checkpoint | Track target verification, draft cache, accepted state and acceptance statistics |
| Cache lifecycle | prefix reuse, chunked prefill, SWA, offload/recompute versus permitted control | Preserve allocation/token semantics; test cold and repeated requests |
| Precision/layout | supported dtype/quantization/backend/layout alternatives | This changes the numerical reference; do not label any improvement a transport fix |

Disabling optional acceleration together is appropriate for the controlled [bottom-up baseline](bottom-up-validation.md), including supported eager execution, launch blocking and deterministic communication. Do not call that combined change a causal isolation result. After establishing content/placement correctness, re-enable features incrementally and bisect the interacting set. Preserve mandatory model/hardware settings and user exclusions. Mark a test inconclusive if it OOMs, takes a different model path or no longer reproduces the relevant workload.

Use a small factorial comparison when PD interaction is suspected:

| | Feature off | Feature on |
|---|---|---|
| Colocated/direct baseline | A | B |
| PD, same model and comparable execution | C | D |

- Only D fails reproducibly: evidence for a PD-by-feature interaction; locate its failing boundary before naming a component.
- C and D fail while A/B pass: investigate the PD-specific path, including model integration and different prefill topology.
- B and D fail: the feature can fail without PD; PD is not necessary in this tested setup.
- All pass or results fluctuate within baseline noise: this matrix has not reproduced the failure.

These are triage decisions, not proofs of absence. Compare repeated runs, the same logical positions and the original failing workload. A lower CP size also changes collectives and memory pressure; that confound must be recorded.

**Exit evidence:** a minimal failing combination and a nearby passing comparison, or a documented reason to move directly to platform/tensor investigation. Do not run an exhaustive Cartesian product without a discriminating hypothesis.
