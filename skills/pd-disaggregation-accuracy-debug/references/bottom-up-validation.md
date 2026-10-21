# Bottom-up PD handoff and cache integrity validation

Use this route to establish the data/state contract before reintroducing acceleration. It complements top-down configuration and feature isolation; choose the route that best separates the current hypotheses. A controlled baseline passing does not clear the original asynchronous or concurrent configuration.

## 1. Define the handoff being tested

Let the prompt contain N tokens indexed `0..N-1`. For the N-1 handoff, D starts from `num_computed_tokens = N-1`, with the preceding context represented by valid cache/state, and processes the token at position N-1 to obtain the next-token prediction. It must not silently recompute the entire prefix to make the test pass. Verify scheduler metadata, scheduled tokens and the actual model input rather than only the request's advertised external-token count.

P may execute the full prompt or stop at prompt-minus-one according to the model/spec and protocol. Distinguish how far P executed from the exact state that D must receive. Attention KV can contain an additional slot that D will recompute, whereas recurrent, convolution, compressed or circular state may represent a particular consumed-token count and cannot be rolled back merely by truncating a block list. Check the concrete spec's accepted/restorable state, compression units and cursors. Do not apply one N/N-1 clipping rule to every component.

Record this handoff ledger before comparing dumps:

| Quantity | Evidence |
|---|---|
| Prompt and output | Exact prompt token IDs and N; which side generates the first output token/logprob; proxy stitching |
| P execution | Actual processed interval, prefix/external hits, main and draft writers, published state position/generation |
| D resumption | Actual `num_computed_tokens`, scheduled input tokens, logical positions, existing local/pool state and required remote interval |
| Per-component restoration | Spec, logical token/state position, valid rows, block/slot mapping, scale metadata, ring/window/compression cursor and accepted/speculative state |

If the active protocol instead carries a P-generated token or resumes at a different position, derive and record that contract and align the comparison accordingly. Do not force N-1 into another protocol or use local forward-step numbers as token positions. For a bug in an intended N-1 handoff, the observed mismatch is evidence to investigate, not a reason to redefine the expected contract.

Distinguish a successful full-prompt load from partial hits, bounded SWA prefix replay and failed-load recomputation. A scheduler can deliberately rewind more than one token to rebuild a missing window; this is not by itself a PD failure. Trace the replay interval and the state available at its start. Include a single-token prompt when supported: producer truncation can explicitly guard N > 1, so do not assume an empty P execution is legal. A computed-token count assigned while waiting for remote KV is accounting state, not proof of arrival or permission to consume it.

## 2. Establish a deliberately simple baseline

Preserve the original failing setup. On an isolated authorized deployment, use eager execution for applicable target/draft paths, synchronous operator launch (`ASCEND_LAUNCH_BLOCKING=1` when supported), and supported HCCL determinism. Disable optional acceleration such as graph capture, scheduler/communication overlap, CP optimizations, fused communication/MoE paths and speculation where the model and memory constraints permit. Verify effective dispatch and both roles' environments using [configuration-and-ab.md](configuration-and-ab.md) and [platform-triage.md](platform-triage.md).

This combined configuration establishes a reference; it is deliberately a multi-factor change and cannot identify which disabled feature caused a difference. Keep required model/hardware settings, record unavailable controls and retain sufficient memory. Deterministic collectives do not establish whole-model bitwise invariance, and launch blocking does not replace the transport's visibility contract. Do not run an invalid configuration just to claim that all features are off.

Start with a cold, nonzero-transfer request and valid initial state. Once its contents and destination placement are established, expand to the cases below before treating the transport path as validated. A cold single-request pass is a narrow result.

## 3. Compare the completed producer state with the actual consumer input

Use [evidence-ladder.md](evidence-ladder.md) for capture and address rules. The primary pair is each P segment after its relevant writers complete, while its source generation is retained, versus D after required loading/restoration and immediately before that component's first consumer. For layerwise execution this can be inside the model forward. An additional D capture after transfer visibility distinguishes wrong reception from later restoration or overwrite; map legitimate state relocation explicitly.

Build the expected mapping from model/spec semantics and D's actual consumer metadata, independently of the connector's generated transfer list. For each valid logical element/state component, record:

```text
request / attempt / source generation / layer / component / token or state position
-> expected producer owner and logical value
-> expected D block, slot, head/sequence shard and physical byte segment
-> observed D value at that location immediately before consumption
```

Verify content and placement separately. Correct values copied into the wrong valid block are a failure; matching flat dumps without the consumer mapping are insufficient. Different TP/CP layouts may require reconstruction into common logical coordinates. Raw, unchanged-format transfers require exact valid-byte equality. For intentional conversion, compare the documented logical transformation, including scales and justified tolerances. Do not require arbitrary padding or inactive rows to match.

For every required D interval, also identify its provenance: local prefix cache, external pool, newly transferred P data, or a legitimate local state reconstruction. Reused intervals must remain correct while missing intervals are filled. If P itself hits cached/pool data, capture its valid retained generation or the authoritative source snapshot rather than assuming all P tensors were newly written by this forward.

If all required content and placement agree but decoding diverges, inspect consumer positions/state, first-forward computation and sampling. Correct P-to-D copying alone does not prove P computed the right values; compare the producer with a trusted computation reference when source correctness is in question.

## 4. Exercise boundaries, hits and dirty reuse

Select cases that stress the suspected contract; do not run a Cartesian product without a reason. State actual coverage and exclusions.

| Dimension | Targeted cases | Required evidence |
|---|---|---|
| Block boundaries | Valid short lengths and lengths around kB-1, kB, kB+1 for several k; consider both N and N-1 | First/last valid slot, full/partial blocks, offsets and expected copy coverage |
| Spec-specific boundaries | Compressed-block, SWA window/replay, ring wrap and recurrent-state boundaries | Translate B into original/compressed tokens or state steps; verify each spec separately |
| Configured block sizes | Relevant supported P/D block-size/scale combinations, especially the failing combination | Distinguish changing `block_size` from changing prompt length around a fixed block size |
| Speculative steps | Disabled baseline, small supported count and original failing count; acceptance/rejection and rollback | Main/draft ownership, accepted state, speculative slots and restored positions |
| P/D prefix hits | Neither hits, P-only, D-only, both; partial and boundary-aligned hits where valid | Actual hit lengths and block IDs, retained ranges, missing remote ranges and prompt-end handling |
| External/pool hits | P or D external hits, partial hit plus remote fill, and supported local/pool/PD combinations | Source/generation provenance, hit offset, completion order and preservation of existing valid state |
| Concurrency | Overlapping requests with distinguishable content, different lengths/hits, allocation churn | Live ownership, per-request block maps, in-flight transfer and release order |
| Sustained dirty reuse | Repeated varied requests until the relevant physical cache blocks have been written and recycled | Actual allocation/write/reuse coverage and generation changes, not elapsed time alone |

For a zero-transfer/full-hit case, verify correct preservation and handoff, but label it as no transport coverage and include a separate nonzero-transfer case. A local recompute fallback must not masquerade as successful external transfer.

Select hit cases per spec and connector capability. A non-prefix-cacheable circular component can still need restoration or replay when other model components hit; do not require a prefix hit for that component or assume the attention hit count proves its state exists. Check slot-mapping participation, null blocks and per-group valid state rather than applying a dense-attention table to every cache.

Exercise dirty reuse through legitimate requests and allocator transitions. Track which relevant valid block/component ranges were written, released and reused; submitting more tokens than cache capacity does not by itself prove every physical block was exercised. Avoid requiring initialization of padding that has no semantic role. Use distinguishable request data so stale content is detectable. Do not reset or zero caches between all trials and thereby remove the reuse condition being tested.

For suspected trampling, snapshot protected live ranges of neighboring requests or intentional hybrid aliases before/after the target transfer and before consumption. Correlate any change with legitimate writers, ownership generations and in-flight DMA; shared pointers alone are not a violation. Check partial tails, previously hit prefixes, main/draft sharing and release/reallocation races. Sentinel probes from [quick-probes.md](quick-probes.md) can reveal missing writes, but must not overwrite live shared/prefix/state data.

## 5. Reintroduce features and establish causality

After the controlled baseline passes the selected content/placement cases, add back one feature or a necessary coupled group at a time. Preserve failing input identities and retain targeted dumps at the same semantic boundaries. Separately remove diagnostic synchronization/dumps so a timing-sensitive defect is not permanently hidden.

If a feature introduces a mismatch, use the PD on/off comparison where feasible and identify the first changed boundary: producer generation, mapping, transfer visibility, destination overwrite, restored metadata or computation. Record topology, batching and allocation changes caused by the feature. Passing the baseline plus failure after feature enablement identifies a trigger; the faulty contract still requires evidence.

Report the exact handoff, tested topology/features, case matrix, valid-payload equality, correct placement, protected-state preservation and remaining runtime gaps. Do not generalize a controlled single-rank test to asynchronous multi-rank or long-running service correctness.
