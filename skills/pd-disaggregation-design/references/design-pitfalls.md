# Counterexamples to universal PD rules

These are reusable review questions, not a compatibility matrix. Verify each against the active revisions.

- **A class name does not identify a protocol.** Framework and plugin variants with similar names may have different cache descriptors, handshake schemas and completion ownership.
- **PCP=1 is not a universal requirement.** Some paths support PCP replicas. Conversely, formulas simplifying at PCP=1 do not prove compatibility after metadata nesting or head inference changes.
- **Replicas and shards differ.** A PCP implementation may partition Q while preserving full KV replicas. Worker-rank ordering and KVPP ownership ordering may differ. Select the right complete replica before shard routing.
- **Equal kernel block sizes do not prove all cache specs compatible.** Sliding-window, compressed and circular state have distinct logical-token and physical-transfer contracts.
- **Different physical strides do not automatically prohibit transfer.** Per-block copies can transfer the same payload between padded layouts. They do not convert different token orders within a block: one DCP rank's [0,2,4,6] cannot be copied as [0,1,2,3].
- **Registration success is not model support.** Circular state may register successfully while request mapping or address generation is missing.
- **Planner metadata is not a connector workaround.** Preserve meaningful `layer_stride=0` and shared-backing descriptors; reconstruct and validate physical pages rather than rewriting metadata to satisfy assumptions.
- **A finished request set is not automatically a KV leak.** Distinguish deduplication state, reachable early notifications, retained allocations and unbounded bookkeeping. Prove whether early DONE can occur under publication order before adding a new queue.
- **D completion and P release are different events.** Completion aggregation may require unique D senders per P endpoint and the P-side request ID. Confirm current code rather than preserving a fixed ACK route from an older connector.
- **Failure-result injection is not an exception test.** Directly adding a request to a failed set covers downstream handling, not transport exception capture or physical network faults.
- **Determinism improvements are not an accuracy pass.** Identical output tokens can coexist with materially different logprobs; deterministic collectives do not validate transfer payload or link integrity.
- **A heartbeat policy is a design choice.** Lease renewal, health detection, failover and request termination are separate contracts. Do not inherit all of them from an intermediate historical design.

When replacing a former skill, retire its version-specific prescriptions explicitly. Keep private source-session indexes and operational artifacts outside the distributable skill; publish only the supported reasoning and validation scope.
