# PD accuracy case record

Keep this compact and link large artifacts. Mark fields unknown when evidence is missing.

## Symptom and applicability

- Observed failure, reproducible case IDs, frequency and first failing step:
- P/D revisions and dirty hashes; actual imported paths:
- Model/tokenizer/draft/quantization; device IDs and rank mapping:
- CANN/driver/firmware/torch_npu/HCCL/transport/custom-kernel versions:
- Exact request token IDs, sampling, output limits, load and evaluation method:
- Original failing configuration and nearest passing control:
- Investigation direction (top-down, bottom-up or mixed) and reason:
- Handoff ledger: prompt length, P processed/published position, D computed-token count and first input, per-spec state position, first output-token/logprob owner:
- Official model/PD/transport pages and sections, documentation revision or Wiki HEAD, access date and discrepancies with the effective configuration:

## Configuration and experiments

| Hypothesis | Single controlled change | Effective dispatch proof | Passing/failing result and repetitions | Artifact |
|---|---|---|---|---|
| Configuration mismatch | | | | |
| PD × feature interaction | | | | |
| Device/link or software stack | | | | |

Record why any stage was skipped. Include the PD on/off × feature on/off table where valid; note when disabling a feature also changes topology or implementation and the factors cannot be fully separated.

For bottom-up validation, record the effective eager/blocking/determinism baseline, required features retained, and covered block/spec boundaries, speculative steps, P/D prefix and external-pool hit combinations, concurrency and measured dirty-block reuse. Report omitted or unsupported cases and zero-transfer/recompute fallbacks explicitly.

For additional methods, record the skill/tool or source used (or label a reasoning-derived hypothesis), why the method discriminates between the remaining explanations, expected outcomes, actual observations and limitations. Link specialized reports and primary sources while preserving the same request/build identities. Keep externally reported findings separate from locally reproduced evidence.

## First divergent boundary

| Boundary | Aligned request/token/layer/rank | Synchronization and ownership | Comparison/result | Artifact |
|---|---|---|---|---|
| P segment after its relevant writers | | | | |
| Intended P/D ranges and mapping | | | | |
| D after transfer visibility | | | | |
| D after required restoration, before the component's first consumer | | | | |
| First divergent operation/logits/logprobs | | | | |

Distinguish byte equality, logical-value equality and numerical tolerances. Include positions, block tables, lengths, ring/compression state and accepted-token state, not only KV bytes. Record instrumentation-induced timing changes.

Record concrete capture hooks and their role/runner implementation. For per-layer loading, distinguish model-entry from layer-ready evidence. Map transfer destinations through any legitimate Mamba/copy-on-write/staging relocation to the final consumer locations. Record partial-hit, replay or failure-fallback changes to the expected scheduled interval.

State separately whether all required valid data matched and whether it occupied D's expected consumer locations. Record cache provenance and whether protected live prefixes, neighboring requests and hybrid aliases remained correct through transfer and reuse.

## Causal conclusion

- Classification: direct PD defect / PD-feature interaction / model path missing PD adaptation / independent device or stack issue / invalid comparison / unresolved.
- Minimal failing condition:
- First divergent artifact and violated contract:
- Mechanism connecting the contract violation to the symptom:
- Controlled remedy or counterfactual and replay evidence:
- Alternative explanations excluded and remaining uncertainty:

## Validation and handoff

- Original failure replay without diagnostic perturbations:
- Relevant boundary/repeated/concurrent tests:
- Static checks, device reproduction and statistical accuracy results, separately:
- Untested scope and next discriminating experiment:
- Process/instrumentation cleanup and artifact locations:

A mitigation that only hides the symptom is not a confirmed fix. Stop at the supported conclusion rather than assigning a PD cause by elimination.
