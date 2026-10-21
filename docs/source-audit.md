# Source audit of the PD disaggregation skills

Audit date: 2026-10-21. This is a source review and workflow walkthrough, not a device validation or a universal connector support matrix.

## Audited source identity

| Repository | Local checkout commit | Worktree at review |
|---|---|---|
| vLLM | `7913c96894cacc348397a377411acde96b63e68a` | Clean |
| vLLM Ascend | `b61c9b207f72e7765bf096a5dff2fc928a19b03f` | Clean |

Paths below are relative to the named repository. They identify the inspected checkouts; they do not assert that these commits belong to an upstream release or that a remote service imports them. Re-resolve symbols and active dispatch on other revisions. No vLLM or vLLM Ascend source was changed by this audit.

## Findings and skill changes

### 1. Capture before consumption, which can occur inside forward

The vLLM connector interface separates `start_load_kv`, `wait_for_layer_load`, `save_kv_layer` and `wait_for_save` in `vllm/distributed/kv_transfer/kv_connector/v1/base.py:333`. Layer loads can complete inside attention execution. Ascend's concrete `AscendStoreConnector.wait_for_layer_load` in `vllm_ascend/distributed/kv_transfer/kv_pool/ascend_store/ascend_store_connector.py:360` waits and then performs the relevant Mamba copy. `AscendMultiConnector.wait_for_layer_load` in `vllm_ascend/distributed/kv_transfer/ascend_multi_connector.py:97` composes child load/reuse waits and deferred state copies.

A method name does not establish that behavior: `kv_p2p/mooncake_layerwise_connector.py:2153` has a no-op worker load hook, while `kv_p2p/sfa_pd_rd2h/connector.py:222` uses the hook for P reuse protection and documents a separate D load manager. These paths must not be conflated.

**Correction:** the accuracy skill now selects the actual component's first-consumer boundary after its load and required restoration. A global D model-entry dump cannot diagnose missing data in all layerwise paths. P snapshots likewise follow the readiness of each published segment, including all writers of that segment, without requiring unrelated layers to complete. Design and serving handoffs use the same wording.

### 2. Transfer destination can differ from final state location

`vllm_ascend/worker/model_runner_v1.py:2661` places Mamba alignment copy after KV loading, with deferred per-layer copies where required. `vllm_ascend/worker/v2/model_states/mamba_hybrid.py:102` prepares deferred copies; its `preprocess_state` at line 197 runs the ordinary copy only when a connector has not taken over the layerwise operation.

**Correction:** record transfer destination, legitimate relocation/copy-on-write/staging, and final consumer location separately. Correct post-transfer bytes followed by changed locations are not sufficient evidence of trampling. The failure classification and case report now require the expected restored state to be checked.

### 3. N-1 is a scoped handoff, not a universal scheduler assertion

In vLLM, `vllm/v1/core/sched/scheduler.py:3194` defines bounded prefix replay. `_update_waiting_for_remote_kv` at line 3218 subtracts the replay interval when needed; only its subsequent full-hit branch rewinds exactly one token. Partial hits and failed loads have different paths. At lines 1380-1404 the request can already carry a computed-token count while waiting for remote data.

Ascend's `kv_p2p/mooncake_connector.py:1885` derives the state prefill count. `_truncate_request_for_prefill` and `on_new_request` at lines 1892 and 1918 apply guarded producer truncation before local prefix lookup; N <= 1 is explicitly excluded. This is evidence for that connector, not a blanket instruction to truncate every model or proxy request.

**Correction:** the accuracy workflow distinguishes intended full-hit N-1, partial hits, SWA replay, single-token guards and failure fallback. Computed-token accounting is not receive-completion evidence. Serving acceptance rejects a recompute fallback being reported as successful transport.

### 4. Spec capabilities constrain the test matrix

`vllm/v1/kv_cache_interface.py:917` defines `CircularBufferSpec` as one block per request, with no ordinary prefix-cache or slot-mapping participation. `MambaSpec` at line 1043 distinguishes content bytes from padded page bytes, TP replication and state residency; an align-mode block-table row can grow with the sequence while only a bounded set of physical states remains resident. `KVCacheTensor` at line 1419 describes placement with offset, layer stride and block stride.

Ascend's `vllm_ascend/core/kv_cache_interface.py:205` and `:309` add MLA/indexer sizing and layout fields. Shape equality does not replace these semantics.

**Correction:** design now explicitly examines prefix-cacheability, slot mapping, token alignment, replication and row length versus resident blocks. Accuracy selects per-component hit cases and verifies how non-cacheable state is restored when other components hit. It does not require an impossible circular-state prefix hit.

### 5. Independent strides are connector- and branch-specific

V2 publishes physical stride separately from payload length in `vllm_ascend/distributed/kv_transfer/kv_p2p/mooncake/base_worker.py:272`. In `mooncake/pull_worker.py:1102`, address construction uses each side's stride. The whole-block branch at line 1183 checks tensor count, circular shape where applicable, equal payload length, and merges consecutive blocks only when both strides equal the transfer length. Head-sliced transfers at line 1323 impose their own head-length and coalescing conditions.

The inspected Hybrid pull loop in `kv_p2p/mooncake_hybrid_connector.py:750` instead uses a locally selected stride for both address lists. Therefore V2's independent-stride property cannot be used as evidence that this Hybrid branch accepts arbitrary unequal peer strides. This observation does not prove a deployed failure: the reachable layout and peer constraints still need inspection.

**Retained:** the design skill's per-connector, per-spec compatibility verdict, independent P/D address arithmetic, physical bounds and no implicit block-internal conversion. The audit confirms why these boundaries are necessary.

### 6. Launch configuration can be normalized or overridden

`vllm_ascend/ascend_config.py:657` normalizes fused-MC2 configuration and separately tracks MegaMoE capability. `vllm_ascend/batch_invariant.py:102` overrides weight layout, HCCL/LCCL environment settings and operator determinism together.

**Correction:** feature A/B tests now record configuration after initialization and the actual dispatched operation. Batch-invariant mode must not be described as a communication-only toggle. These source examples are not cross-version launch recipes.

### 7. Proxy token ownership must be traced

`examples/disaggregated_prefill_v1/load_balance_proxy_server_example.py:819` builds a P request with one output token and explicit transfer parameters. At line 973 it propagates returned transfer metadata into the D request. A one-token P generation limit by itself does not establish that the P token must be appended to D input.

**Correction:** serving now traces P construction, returned metadata, D construction, first output-token/logprob ownership and budgets together. It warns against changing prompt tokens solely from the P output limit.

### 8. External stack behavior remains a runtime evidence requirement

`vllm_ascend/distributed/kv_transfer/utils/mooncake_transfer_engine.py:11` imports the installed `mooncake.engine.TransferEngine` and selects the `ascend` backend. That Python wrapper does not establish the loaded transport implementation or HIXL build. Launch-blocking behavior likewise belongs to the installed torch_npu/runtime stack, not just these two source trees.

**Retained and clarified:** official model/HIXL documentation lookup, loaded-library identification, supported debug settings and device-versus-stack attribution remain required where applicable. This audit does not certify HIXL settings, hardware links, CANN correctness, RDMA visibility or launch-blocking behavior.

## Source-based usability walkthroughs

These are manual workflow checks against the code, not executed inference cases or independent agent evaluations.

| Case | Expected action using the revised skills |
|---|---|
| Full prompt remotely restored, no replay | Verify final-token recomputation and actual D input; retain nonzero-transfer and completion evidence |
| Missing SWA window triggers bounded replay | Derive replay interval/state; do not diagnose a defect merely because D starts before N-1 |
| Layerwise external pool with Mamba alignment | Capture after the specific load and state copy, then before its first consumer |
| Nominal layerwise hook is a no-op or protects P reuse | Find the real D load/visibility path and instrument that boundary |
| Equal payload lengths but unequal physical block strides | Trace the named connector's metadata and address branch; do not borrow V2 support for Hybrid |
| Attention prefix hit with a non-cacheable circular component | Prove component restoration/replay separately from attention hit length |
| Successful HTTP response after failed receive | Identify fallback/retry and decline to count it as successful PD transport |
| Fused-MC2 or determinism flag changed | Confirm post-initialization settings and operator dispatch before interpreting the A/B result |

Existing source tests were also inspected as evidence of intended contracts:

- `tests/ut/kv_offload/mooncake_v2/test_pull_worker.py:1212`: `test_whole_block_mla_address_generation_uses_independent_stride`, with independent 256/512-byte strides and 128-byte entries.
- `tests/ut/distributed/ascend_store/test_ascend_store_connector.py:648` and `:695`: V1/V2 Mamba load-before-copy ordering tests.

These tests were read, not run. No local Torch/torch_npu execution was attempted.

## Validation and remaining scope

Completed host-only validation:

- `python3 scripts/validate.py`: passed package structure, links, independent distribution and shared-reference checks; all seven output-audit regression tests passed.
- `quick_validate.py` from the installed skill-creator package: all three entrypoints passed.
- Workspace, personal and publication copies: all 32 package files matched byte-for-byte after synchronization; prior personal packages were backed up outside the publication repository.
- `git diff --check`: passed for the workspace and publication repository. The package validator also checked untracked distribution files for trailing whitespace and Python syntax. Both audited source submodule worktrees remained clean.

The source audit supports the revised workflow's applicability to the inspected paths and removes the identified misleading assumptions. It does not prove complete coverage of every connector, runner, model, topology or future revision. NIXL internals, live MindIE tool invocation, remote launch, real P/D dumps, device/stack A/B tests and sustained dirty-block/concurrency tests were not executed in this audit. Those remain case-specific validation work on a matching authorized runtime.
