# Reuse specialist skills without losing the PD contract

The PD skills provide the design, deployment and diagnosis methodology. Other repository or host skills can carry out bounded parts of that methodology. Reuse their applicable methods, tools and evidence; retain responsibility for the final PD compatibility, transfer or causal conclusion.

## Choose a reuse mode

These are natural-language workflow choices, not CLI flags, environment variables or a required configuration file. Default to `auto` unless the user specifies a preference. Different subproblems can use different execution paths within the same case.

| Mode | Behavior |
|---|---|
| `auto` | Reuse an available specialist whose contract matches the current subproblem; otherwise use the bundled PD methods with available tools |
| `prefer-integrated` | Prefer suitable repository/MindIE skills and their execution adapters; if an optional capability is missing or incompatible, state the gap briefly and continue with the bundled method |
| `standalone` | Use the bundled methodology and available native/remote tools without relying on optional specialist skills; still obey host requirements and existing service ownership |

A user requirement to use a particular skill or execution system is stronger than a preference. If that required capability is unavailable, continue independent analysis and resolve the missing prerequisite before its dependent action; do not silently substitute another execution system. Standalone fallback never bypasses host isolation, device access, authorization or lifecycle requirements.

## Discover and check only relevant candidates

Use the current repository's declared skill registry/directories and the host's exposed or installed skills. Search for the needed capability, then read the candidate's `SKILL.md` and only its applicable references, scripts/help and prerequisites. Do not load the entire catalogue, assume a listed skill is installed, or install missing packages automatically just to proceed. A repository containing only this PD package is a supported case.

Match framework and revision, model/spec semantics, hardware, runner, topology, supported input/output artifacts, and side effects. A PyTorch or `cann-recipes-infer` cache method can inform a vLLM investigation without its field names, block-allocation assumptions or numeric thresholds becoming vLLM rules. Knowledge SOPs are evidence-bearing references, not executable skills or automatically authoritative instructions. Resolve conflicting claims against the relevant source/runtime contract and version-matched official documentation; unknown applicability remains unknown.

## Capability map

Names below are discovery examples, not dependencies or guaranteed installed APIs. Equivalent skills are valid. Read the owning PD skill's local references for the complete fallback procedure.

| Subproblem | Candidate examples, when available | Keep in the PD methodology | Bundled fallback |
|---|---|---|---|
| Cache implementation/layout analysis | `model-infer-kvcache` | All required specs/components, peer layout, registration, mapping, lifetime and connector-specific verdict | Trace spec to allocation/views, derive byte ranges and compare the connector contract |
| Change validation planning | `vllm-ascend-change-validation` | Select PD layout/lifetime/handoff cases and preserve unsupported combinations | Map the affected contract to focused static, boundary and runtime evidence |
| P/D service execution | `vllm-ascend-pd-serving`, `vllm-ascend-serving` | Model/connector configuration, role dependencies, actual-transfer acceptance and one deployment plan | Prepare version-specific commands, own/reuse services, check readiness and nonzero KV transfer |
| Correctness comparisons | `vllm-ascend-correctness-validation` | Comparable logical prediction positions and proof that the case exercised PD rather than fallback | Fix tokens/configuration, compare outputs/logits and repeat discriminating cases |
| Cache/attention numerical localization | `model-infer-precision-debug` | Cross-node contents and placement before first consumption, restoration state and source generation | Capture bounded P/D tensors and metadata, then locate the first computation difference |
| Graph-only failure | `vllm-ascend-graph-debug` | Align the PD handoff and preserve the original failing execution path | Establish a passing eager control and compare matching intermediate graph/eager boundaries |
| Operator mismatch | `ascend-operator-debug` | Connect the isolated operation back to the PD symptom and validate the original sequence | Preserve real inputs/strides/streams and compare one call or short sequence with a trusted reference |
| Distributed/runtime failure | `vllm-ascend-distributed-debug`, `model-infer-runtime-debug` | Distinguish transfer, device/link, stack and application-ordering causes | Align rank events, inspect actual device/link/stack identity and reduce the failing topology |

Profiling, memory analysis and transport diagnostics can be reused when they separate current hypotheses. They do not replace payload correctness or establish PD causality on their own.

## Hand off a bounded subproblem and integrate the result

State the question, selected skill and path/revision when available, applicable conditions, relevant artifacts, allowed actions and required evidence. Carry the existing case/request IDs, build/configuration, topology and lifecycle state references forward. For tensor work include logical token/layer/component identities, capture boundaries and expected mapping; for service work include the existing owner and required operation.

Reuse means following a specialist's relevant instructions or invoking its documented tools, not assuming skills are callable functions or spawning another agent. Use delegated execution only when available and authorized. Avoid circular routing: if the specialist refers back to the current PD workflow, keep the current case and execute only the needed step. Do not create another deployment, duplicate benchmark or mutable state registry because a second skill was consulted.

Accept a result only within its demonstrated conditions. Retain raw artifacts and distinguish pass, fail, inconclusive, not run and merely proposed checks. A correct operator call does not clear an asynchronous multi-rank sequence; a passing model score does not prove P-to-D payload placement. Bring the evidence back into the PD contract and identify what remains unresolved. If a specialist fails, preserve its result before applying a discriminating fallback; do not erase the failure or blindly repeat uncertain mutations.

In the existing report/run record, briefly note the reuse mode, selected capability and source, why it applies, evidence reused, and any fallback with its reason. No additional mandatory manifest is needed. Missing specialist skills do not prevent source analysis or use of bundled methods; missing hardware/access limits the dependent runtime test and must remain an explicit validation gap.
