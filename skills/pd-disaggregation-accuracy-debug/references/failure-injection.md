# Failure, lease and sustained-run experiments

Run injection only within authorized experiment scope. Use isolated test requests, recoverable instrumentation and original source hashes. Restore only this experiment's edits, preserving concurrent changes. An analysis-only task should produce the experiment design without executing it.

## Distinguish injection boundaries

| Injection | Example | What it covers |
|---|---|---|
| Request failure result | Skip READ for a test request and mark it failed | Scheduler/proxy/error propagation and release after failure reporting |
| Bucket execution failure | Raise inside the real submitted transfer future, or return a negative transport result | Exception capture, bucket-to-request attribution and failure reporting |
| Metadata/submission failure | Fail a selected handshake or partial submission | Engine-batch failure and draining already-submitted work |
| Notification/lease failure | Delay/drop test DONE or renewal; restart a test endpoint | Retry, expiry and incarnation handling, not physical device failure |
| In-flight cancellation/preemption | Cancel during a controlled DMA window | Allocation retention and isolation from old attempts/DMA |

Do not describe the first row as a network or exception-handling test. A DP4/TP1 experiment exercises four replicas, not cross-TP worker aggregation.

Use stable request selectors, such as SHA256 of a test ID, rather than Python's process-randomized `hash()` or independent worker RNG. Preserve complete internal IDs and log external-to-internal mappings. Verify that the selected request reaches the injection point; full prefix hits and masked automatic retries are not valid evidence of that path.

Keep healthy → failing → healthy controls and mixed healthy/failing batches. Record:

```text
external ID / attempt / P ID / D ID / worker
expected -> injected -> receive success/failure -> scheduler terminal state
-> HTTP/stream outcome -> P notification/release -> D cleanup -> next healthy request
```

Validate aggregation against all participating workers. A queued DONE is not proof of receipt; receipt is not proof of allocator release. After drain, inspect running/waiting requests, KV use and request bookkeeping, distinguishing intended cache retention from leaks.

## Leases and accumulation

Check renewal while D queues, long forward interference, and isolation from slow endpoints. Host heartbeat success does not prove the NPU or transfer data path healthy. An expired address remaining readable does not establish ownership of its current content.

Sample host RSS/PSS, request-ID sets, early/finished/delayed queues, metadata caches and device KV separately; record process incarnation and restarts. Growing finished-ID sets do not by themselves prove KV leakage. Deleting deduplication records can redirect late notifications into another unbounded set.

Use the user's workload and failure conditions to choose duration, concurrency and stop criteria. Do not turn historical duration, request-count or memory-utilization thresholds into universal defaults.
