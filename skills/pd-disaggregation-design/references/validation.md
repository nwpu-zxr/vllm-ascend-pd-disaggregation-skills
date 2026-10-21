# Validation and claim boundaries

Choose cases at the boundary of the changed contract. Do not require an exhaustive matrix for a small change or use mocks that merely repeat the implementation.

| Changed contract | Priority cases |
|---|---|
| New spec/layout compatibility | Concrete spec overrides and instantiated sizing, grouping/dispatch, same-shaped but semantically distinct specs, complete required component coverage |
| Descriptor/registration | Actual legacy and modern fields, nonzero offsets, last page, shared storage, stacked K/V, stride different from payload |
| Topology/mapping | Unequal TP, replicated heads, different main/draft heads, nonzero token offsets, CP interleaving, per-spec routing |
| Completion/lease | Duplicate/late DONE, reachable early DONE, expiry races, cancellation, restart, bounded state cleanup |
| Failure handling | Request-result injection, bucket exception, negative transfer return, partial submission, healthy requests in the same batch, P/D release |
| Layer/chunk transfer | Intermediate/final chunks, boundary lengths, late D registration, shared slots, cancellation during DMA, eager/graph |

A mock with modern fields does not validate a legacy descriptor. PCP=1 formula degeneration does not validate a changed wire schema. DP4/TP1 does not validate TP4 completion aggregation.

For block, window, compression and interleaving boundaries, test B-1, B and B+1 plus repeated reuse as relevant. First translate B into the current spec's logical token unit; the same integer length can exercise different boundaries across specs.

## Execution evidence

Use a device environment for Torch/NPU execution and the host project's supported remote tools. Local text, syntax and standard-library checks are useful but cannot validate NPU events, visibility or collective behavior. Verify actual imports and source identity before device execution. Follow the host's isolation and run-record requirements; standalone use needs no particular manifest library.

Record revisions, dirty diff/hash, commands, configuration, requests, raw artifacts and results. Explicitly list unexecuted cases. One smoke test does not establish statistical accuracy or a performance regression result.

Confirm that requests actually traverse the target connector: correlate request identities, remote tokens/blocks, worker transfer outcome and D execution/failure. HTTP 200, low TTFT or a transfer-plan log alone is insufficient.

Measure registration startup separately from steady-state entries/bytes/latency and end-to-end performance. Fewer registration regions can coexist with more padding bytes. Coalescing requires both source and destination continuity and valid ownership/lifetimes.

Report the strongest evidence obtained: source reasoning, focused unit validation, measured layout/addresses, actual KV transfer, synchronized payload equality, model correctness, or statistical accuracy. Each claim needs its exact applicability.
