# Request and storage lifecycle

## Trace one request

Associate external ID, P/D internal IDs, engine incarnation, worker endpoint and transfer/attempt ID. Do not substitute a D-local ID for the P release ID or guess identity by stripping suffixes. Connectivity and cache identity are distinct; restart must invalidate stale addresses and metadata.

Trace admission, allocation, writer readiness/publication, READ/WRITE submission, consumer visibility, state relocation, first consumption of each component, notification and reclamation. Identify which scheduler, worker, device stream or proxy owns each transition. Layerwise loading can finish inside D forward; streaming publication can precede completion of unrelated P layers. Read concrete hooks rather than assuming a whole-model barrier.

- Interpret `finished_recving`, `finished_sending`, DONE and ACK from the active protocol. D becoming runnable and P being allowed to release are separate state flows; an ACK may acknowledge a message before allocator reclamation.
- Fan-in counts the actual unique consumers required by each P endpoint, not heads, groups, fragments or DP world size.
- Scheduler-level and worker-level completion protocols both exist. Select according to source lifetime rather than treating either placement as universal.
- Cleanup may report that receiving ended, but must propagate failure so D cannot consume invalid KV or publish it into reusable cache.

## Early and duplicate completion

Prove whether early DONE is reachable. A synchronous delayed-free registration before publishing transfer parameters may make it impossible on the normal path. Other entrypoints, asynchronous registration and retry generations can require early-completion state.

Simply discarding completed IDs when dequeued may move late duplicates into an unbounded early set. Audit insertion/deletion, timeout, retry and generation reuse across all queues/sets. A finite TTL needs a protocol retry bound or generation isolation. CPU request-ID growth is distinct from unreleased device KV.

## Failure and leases

| Event | Required reasoning |
|---|---|
| Bucket exception/negative result | Attribute failure to the actual requests depending on that bucket |
| Partial submission | Drain or isolate submitted work before releasing any accessed page |
| Multi-group failure | Inspect current request-level `failed_recving` or invalid-block reporting and scheduler policy |
| Failed reception | No invalid forward; client termination and eventual P/D reclamation |
| Failed DONE | Current bounded retry or explicit fallback; queued notification is not delivery |
| Successful heartbeat | Lease/control-plane evidence, not payload/device-health/progress proof |
| Successful READ after expiry | The address may now hold another request; success is not ownership proof |
| Cancel/preempt/retry | Retain in-flight pages and isolate old notifications and DMA |

Do not preserve historical multi-group limitations without checking current upstream interfaces. Do not replace failure propagation with a warning followed by decode. Verify fail/recompute policy and preserve a product constraint against local D prefill.

Lease review includes tracking while D is queued, stop conditions, monotonic deadlines, no shortening or resurrection, out-of-order expiry scans and endpoint isolation. An independent heartbeat thread can survive scheduler stalls but also maintain a request with no progress indefinitely. State the policy; thread counts and historical timeout values are not universal requirements. Renewal-only behavior is not complete RAS.

## Layerwise and chunkwise transfer

Distinguish request-wise, final-chunk grouped-layer, incremental per-layer and completed-chunk cross-layer sending. Destination readiness and batching granularity are separate decisions.

- Prove valid complete-block ranges for intermediate chunks and final-tail handling. Avoid exposing a shared tail still being modified.
- Initialize transfer state before layer hooks; verify MRV1/MRV2 order and actual graph-replay hook behavior.
- One final event is sufficient only if it dominates every relevant write and has correct reuse/re-record semantics. Layer order alone does not prove cross-stream ordering.
- Prevent a shared slot from being overwritten while a sender still reads it. Deferring grouped transfer makes this especially important.
- Generation checks reject stale notifications but cannot undo issued DMA. Retain old source/destination allocations until safe completion.
- Bound backlog for late D registration and define timeout/fallback without double sending.

Replacing an RD2H transport must preserve its ready/done semantics, CPU/HBM destinations, slot reuse and allocator lifetime contract.
