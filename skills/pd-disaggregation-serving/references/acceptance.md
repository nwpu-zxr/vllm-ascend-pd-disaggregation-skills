# Launch acceptance

Select evidence levels appropriate to the request. Do not expand a script-only request into a device experiment.

Before starting, choose explicit per-phase readiness and request deadlines appropriate to the model and known load time. Distinguish weight loading, graph preparation, connector readiness and proxy readiness; a live PID is not a ready service. Keep retries bounded and preserve each attempt's failure. On deadline expiry, inspect the current progress and earliest error before deciding whether an extension is justified; do not silently restart or wait forever. Do not increase a transport timeout to conceal a service-readiness failure.

| Level | Evidence | Does not establish |
|---|---|---|
| Scripts validated | Shell/JSON checks, model and entry-point existence, CLI compatibility, port plan | Processes started |
| Services ready | P/D engines and proxy healthy, process logs | Requests traverse PD |
| Routing works | External request correlated with P/D internal IDs, complete proxy response | KV was transferred |
| Actual KV transfer | Nonzero remote tokens/blocks, matching worker transfer outcome, D execution/failure | Numerical payload correctness |
| Cleanup works | P completion/release, D termination and relevant active state draining | No leaks under every sustained workload |

Avoid a full prefix hit yielding an empty-transfer smoke case. Choose input known to require remote KV and verify counters/path. If prefix cache must remain enabled, preserve it and use suitable fresh input rather than silently disabling it.

Remote-token accounting can be set before arrival. Confirm completion and the scheduled D interval as well as nonzero transfer work; reject a supposed transfer-success result that actually used failed-load recomputation. Partial-hit or bounded-replay execution can legitimately start earlier than N-1, so compare with the active scheduler/spec contract rather than a fixed token-count assertion.

Check HTTP status, content, stream termination/finish reason, P/D errors/timeouts and block lifecycle. Record each retry attempt; a final success must not erase an earlier failure.

For repeated/concurrent acceptance, distinguish cold startup, repeated runs in one instance, identical/different input and block reuse. Do not add a full benchmark automatically to basic launch work.

Preserve the earliest failing rank, context and effective settings. Async HCCL errors can become visible at a later synchronization point. Query an available verified knowledge source for the observed signature before repeating diagnosis, but verify applicability to this version and topology. Missing knowledge is unknown, not proof of support or a reason to stop ordinary investigation.

Cleanup and rollback target only this run's processes, containers and files. Verify PID and command identity instead of broad process-name killing. Keep raw logs and reproducible launch/status/stop commands. Whether services remain running follows the user's requested outcome.
