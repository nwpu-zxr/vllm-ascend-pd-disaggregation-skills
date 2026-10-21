# Device, interconnect and software-stack attribution

Use this branch early when device/collective errors exist, failures follow a device, or synchronization changes the result. Do not require a full platform sweep before investigating an already localized wrong address.

For an active HIXL path, follow [official-docs.md](official-docs.md) to check the deployed API, protocol/resource configuration and relevant Wiki guidance. Correlate both endpoints' earliest low-level errors and effective settings with payload evidence. Separate connection, transfer and consumer-visibility failures; do not diagnose a hardware or CANN defect from a generic wrapper error or a similar Wiki example alone.

## Separate four hypotheses

| Hypothesis | Discriminating evidence | Insufficient evidence |
|---|---|---|
| Device/interconnect fault | Same inputs/software fail on one physical device/link and pass on a known-good equivalent; matching ECC/link/driver evidence or independent collective/data-integrity reproduction | One logical rank has NaNs; a host ping succeeds |
| CANN/driver/torch_npu/HCCL/operator stack defect | Minimal reproduction follows a controlled stack/build change on the same hardware; supported baseline passes; relevant loaded-library identity and logs | Installing a new image changes several libraries; launch blocking hides the symptom |
| Application ordering/lifetime defect | First bad buffer follows missing event/wait, reused staging/workspace, premature publication or allocation reuse | Error disappears after adding global synchronization |
| Numerical nondeterminism | Stable finite inputs, bounded repeated-run variation and sensitivity to supported reduction-order controls | Any NaN/Inf, stale block or gross corruption classified as rounding |

Device association is not causation: map logical rank to physical device/Die, peer path and NUMA/container visibility. Collect current health, topology, ECC and link/error counters with installed tools and version-appropriate commands (`npu-smi`, `hccn_tool`, device logs, `asys`/`msnpureport` when available). Do not reset devices or alter a shared fabric merely to diagnose accuracy.

Reproduce the relevant collective or transfer with known input and an independent expected result when authorized. Exercise the actual device pair, transport, dtype, shape and topology; a host-network test does not validate HCCS/RoCE device transfer. A memory copy test does not validate a reduction kernel. Preserve asynchronous error provenance: a later synchronization may surface an earlier fault.

## Synchronization and determinism experiments

For a supported eager debug run, `ASCEND_LAUNCH_BLOCKING=1` is a useful controlled change. Verify it is read by the installed torch_npu process and compatible with the chosen execution mode. Do not inject it blindly into graph capture; if eager is required, first establish the eager non-blocking control and then enable blocking. It changes scheduling and can mask races or runtime issues; it is not a production fix or a hardware-health certificate.

Test `HCCL_DETERMINISTIC` and, for paths actually using it, `LCCL_DETERMINISTIC` separately using values supported by the installed versions. Communicator-level settings and hardware can override environment variables; some devices/paths are already deterministic. Deterministic reduction does not verify link integrity and does not make all model kernels batch invariant. `HCCL_DETERMINISTIC` is distinct from a version-specific HCCL blocking-wait option.

Check initialization that rewrites these settings, including batch-invariant mode. Such a mode can also change weight layout and operator algorithms, so toggling it is not a communication-only experiment. Source inspection of vLLM/Ascend cannot by itself establish whether an installed torch_npu/CANN build honors a launch-blocking variable or whether the loaded transfer library uses HIXL; obtain effective runtime/library evidence.

Keep a small comparison table: original, eager control if needed, launch-blocking only, deterministic-communication only, and a combined case only if it resolves an outstanding question. Pair every change with selected tensor dumps before/after the suspect operation. Record performance/timing perturbation and whether the same failing request was actually exercised.

For async-scheduling/DSpark NaNs, keep both stack and application-ordering hypotheses open. A previously fixed stack issue does not establish the cause of a new incident. Require the current build pair, first divergent tensor, reproducer and fix/version evidence before attributing the failure to CANN or another component.

## Stack comparison

Record actual shared-library search paths and loaded builds, not just container tags. Host drivers may remain unchanged when the image changes; mounted CANN directories and `LD_LIBRARY_PATH` can mix releases. Compare a known-supported stack with the failing stack on the same model/input and hardware without replacing a shared installation. If only a complete compatible stack can be changed, attribute to that stack until a narrower component is isolated.

Inspect operator input/output dumps at the earliest divergent layer. Reduce to an operator or short sequence when feasible: fused MC2/MegaMoE dispatch-compute-combine, scatter→attention with real cache strides, or draft/target verification. Preserve dtype, stride, offset, scale, masks, shapes, device events and workspace reuse. An isolated eager call passing does not clear an async/graph/multi-rank sequence.

Use installed graph/operator/distributed debugging skills when available; otherwise perform the same bounded reduction directly. A root cause requires a violated contract and a controlled fix/replay. Report an unresolved stack-versus-ordering ambiguity rather than choosing one from a flag toggle.

## Authoritative starting points

Check the deployed release rather than assuming these pages match it:

- [Ascend PyTorch synchronous-launch variable](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/800alpha003/apiref/envref/envref_07_0058.html).
- [CANN deterministic reduction reference](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920beta2/commlib/hcclug/docs/zh/user_guide/hccl_env/HCCL_DETERMINISTIC.md).
- [vllm-ascend FAQs](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/faqs.md) and [configuration reference](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/user_guide/configuration/additional_config.md).
