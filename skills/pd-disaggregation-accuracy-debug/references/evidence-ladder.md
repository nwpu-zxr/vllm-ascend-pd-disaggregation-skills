# Transfer and tensor evidence

The decisive transfer check compares P's completed valid KV/state with the content at D's expected consumer locations immediately before each component's first consuming operation. For a bottom-up baseline and boundary/hit/reuse coverage, use [bottom-up-validation.md](bottom-up-validation.md). Tensor dumps must establish both values and placement under the actual handoff contract, including N-1 where applicable.

## Correlate one logical request

Track external ID, P/D internal IDs, engine incarnation, attempt/generation, worker endpoint, layer/spec/component and logical token interval. Internal ID suffixes may differ. Record actual rank-to-device and DP/PP/PCP/TP/DCP ownership, block size/scale/compression, full/unhashed/null block tables and source/destination segments.

Addresses need not match between P and D. Match their logical content, reconstructing head/sequence shards when necessary. Bound dumps to selected requests/layers/steps; keep raw prompts and tensors in the authorized local evidence store.

## Capture five boundaries

| Boundary | Evidence | Question answered |
|---|---|---|
| P writer complete, before publication/reuse | Valid KV/state, positions, relevant stream/event and generation | Was correct source content produced? |
| Transfer submission | Actual P/D byte segments, token/head mapping, endpoint, operation return/exception | Were the intended ranges submitted? |
| D transfer complete and visible | Corresponding destination payload and completion dependency | Did correct data arrive at this boundary? |
| D after required restoration, before the component's first consumer | Payload again, seq_len/positions/block/slot/state metadata | Is the data correct at the location actually consumed? |
| Forward and sampler | First divergent layer, target logits, draft/accepted/rejected tokens | Where did computation or output semantics diverge? |

“P writer complete” means every writer of the published segment has finished. A target-forward event may precede draft/MTP writes to that segment; a layer/chunk can also be published before unrelated layers finish. Capture each segment at its actual readiness boundary, without imposing a whole-model barrier on a streaming protocol. A transfer API return may not establish the consumer-stream dependency required by the backend. Inspect the actual event and transport contract. A debug `torch.npu.synchronize()` can help sample a boundary but is not universal proof of RDMA coherence. If instrumentation changes reproduction, retain that fact.

For request-level loads, a model-entry dump after completion and state restoration may suffice. For layerwise/pool loading, capture after the specific layer's receive wait and required Mamba/state copy, before the first operation that reads it; later layers can legitimately be absent at model entry. Trace the concrete implementation and role: `wait_for_layer_load` may be a no-op, a P-side reuse barrier, or a D-side load wait. Some paths load through a separate manager. A hook's name alone does not identify the capture point.

Keep transfer destination and final consumer location as separate mappings. Mamba align copies, copy-on-write, offload restoration or staging can legitimately relocate state after reception. Record source/destination IDs, valid state offsets and completion for each required transformation, and compare against the expected transformed state before diagnosing an overwrite.

Hold or snapshot the same source generation until its comparison is complete. Do not compare an earlier P dump with D data from a recycled allocation. Record device synchronization and event placement alongside each dump.

## Plan, registration and physical ownership

Trace descriptor → allocation/reshape → runtime views → registration → handshake → mapping → transfer → release. Record storage base/nbytes, view pointer/offset, shape, dtype, per-axis byte strides, actual block axis, payload length and padding.

For each contiguous segment, calculate independently:

```text
P_addr = P_base + P_block_id * P_stride + P_inner_offset
D_addr = D_base + D_block_id * D_stride + D_inner_offset
```

Check both half-open byte ranges against registrations, allocation bounds and logical ownership, including the last block and nonzero subview offsets. `numel * element_size` omits strided holes. Separate manager blocks, kernel blocks, compressed-token units and CP interleave. Explain missing ranges instead of silently truncating paired block lists.

Hybrid sharing requires four separate facts: scheduler block-ID allocation, Tensor/view aliasing, raw storage sharing, and physical contiguity. Equal pointers can be intentional aliases with disjoint live group block IDs; equal block IDs across different storage need not overlap. For the failing interval, compute actual occupied ranges over time, including main/MTP/indexer/scale, conv/SSM, ring state and speculative slots.

Look for an unexpected writer between D completion and first use: another request, old DMA, zeroing, allocator reuse, staging-buffer replay or graph update. Correlate it with release/DONE/lease events. A page still being registered does not mean its contents still belong to this request.

## Compare only semantically valid elements

For unchanged dtype/layout raw copies, compare valid byte segments or their hashes, then report the first mismatch. Exclude padding, unwritten tail tokens and inactive ring rows. Do not compare the whole backing allocation indiscriminately.

For quantized or converted layouts, include scale/zero-point metadata, reconstruct logical values and compare using justified atol/rtol, max/mean error, NaN/Inf counts and first divergent coordinates. Raw-byte inequality after conversion is not automatically wrong. Min/max/mean and absence of NaNs help localize but do not establish equality.

Compare cache contents and consumer metadata separately. Correct bytes with wrong positions, N/N-1 restoration, window offsets, compressed units, accepted Mamba state or ring cursor still yield wrong output.

## Route by the first difference

| Observation | Next investigation |
|---|---|
| P is wrong at the correct publication point | Producer computation, cache writer, allocation or draft readiness |
| Plan is out of bounds or maps wrong tokens/heads/ranks | Descriptor/topology/mapping contract |
| P is correct, plan is valid, synchronized D is wrong | Actual submitted segments, partial failure, source reuse/expiry, visibility and transport |
| D is correct after transfer but differs before consumption | First account for required state relocation/conversion; if the expected restored state is wrong, locate the restoration defect or unexpected overwrite, alias collision, old DMA, zeroing or release race |
| Payload is correct, consumer metadata differs | Scheduler/model adaptation and restored state |
| Payload and metadata match, computation diverges | Backend/operator/collective/graph inputs and first divergent layer |
| Target computation agrees, outputs differ | Sampling/RNG consumption, reject/accept state, stream termination, proxy retry or evaluation |

A log containing the expected block pair or a successful transfer status proves neither destination contents nor request ownership.
