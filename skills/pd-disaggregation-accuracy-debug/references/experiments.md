# Controlled comparisons and causal conclusions

## Comparable observations

Fix checkpoint and tokenizer revision, exact prompt tokens, sampling/penalties, output limits, dataset, evaluator and answer extraction. A new DSpark checkpoint is not a one-factor replacement for MTP if target weights also changed. Same seed does not guarantee token identity under different asynchronous batching.

A colocated/direct-D reference may compute prefill with a different TP/CP/attention path from P. Record that difference; do not demand universal bitwise equality or dismiss all mismatches as rounding. Measure repeated-run noise within each path before selecting tolerances.

Prioritize one failing request over repeated full benchmarks while localizing. Cover actual block/window/compression/interleave boundaries, cold versus repeated requests, the original concurrency and state reuse. Respect explicitly excluded features and state the uncovered scope.

## Logits and logprobs

Align logical prediction position and vocabulary IDs. Compare raw target logits before temperature/penalties/filtering separately from processed sampling scores and normalized logprobs. Save selected-token identity, rank, top-k values, top1/top2 margin and nonfinite counts. Compute common-precision log-softmax for offline comparison when appropriate; constant logit shifts affect raw logits differently from normalized probabilities.

At the P/D handoff, record which side produces the first generated token and its logprob, which tokens are already represented in transferred KV, and the token/position consumed by D's first forward. Check the proxy's stitching and any replay of the last prompt or generated token against the active protocol. P's last prefill logits and D's first decode logits may predict different tokens; comparing them by local step number can create a false accuracy failure. Include handoff tokens in the teacher-forced alignment.

API logprobs may expose only selected/top-k tokens and may reflect a different processing stage. Equal top-k or equal output tokens do not establish full-logit equality. Once generated prefixes differ, later logits are for different contexts; teacher-force the same token sequence to continue localization. Synchronize captures and preserve target versus draft labels.

Draft quality primarily changes acceptance and efficiency. With a correct verification/rejection algorithm, poor drafts alone should not systematically damage the target distribution or greedy answer. Inspect target multi-token verification, draft-cache publication, rejected-state rollback, positions and shared RoPE/workspace when accuracy changes with speculation.

## Benchmark interpretation

Report correct/total, paired wrong-to-right/right-to-wrong transitions, answer-extraction failures, truncation, errors, output token-length distribution, repetition and reasoning-tag counts. Use the same tokenizer for token lengths; character counts are not token counts.

For reasoning models, missing or repeated `</think>` is a triage signal conditioned on the template and API output contract. A stripped reasoning field, maximum-output truncation or an intentional non-thinking mode can explain it. Match sample IDs and complete response attempts, not raw substring counts in a mixed log.

Use repeated paired evaluations when stochastic uncertainty matters. Three changed answers out of 198 are about 1.52 percentage points; a single such change does not prove corruption. Several passing rounds do not establish all-load correctness. Retain output morphology and first-divergence evidence alongside aggregate scores.

## Final attribution

| Classification | Required causal evidence |
|---|---|
| Direct PD path defect | Matching source and intended consumer semantics; a PD transfer/mapping/visibility/lifetime violation localized and corrected in a controlled replay |
| PD-by-feature interaction | PD/feature comparison isolates the combination, and evidence identifies the shared event, layout, state or operation contract that fails |
| Model path missing PD adaptation | Model-specific state/cursor/cache writer or consumer assumption conflicts with PD allocation, external tokens, publish order or restoration; repair changes that contract |
| Independent device/interconnect issue | Controlled physical-device/link comparison or independent integrity reproduction plus relevant hardware/driver evidence |
| Software-stack/operator issue | Controlled supported build comparison and minimal operator/sequence reproduction, or equivalent fix-level evidence |
| Comparison/evaluation artifact | Tokenization, checkpoint, sampling, truncation, retry or scoring mismatch explains the observed result under a corrected comparison |
| Unresolved | First known-good/known-bad boundary and remaining discriminating experiment; do not force another label |

These categories can coexist: a stack race may be exposed only by PD plus async speculation. Describe both the trigger and the faulty contract, not just a label.

A root-cause report includes reproducible inputs, the minimal failing combination, exact build/topology, first divergent tensor or state, the code/event/ownership violation, and a fix or controlled intervention that changes the outcome. Revalidate without sentinel fills, extra dumps, global blocking or unrelated feature removal unless that is the explicitly accepted mitigation. Distinguish a mitigation from a root-cause repair.
