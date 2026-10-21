# Assess a new KV-cache layout against a connector

Use this workflow for user-provided tensor descriptions, allocator/reshape code, runtime dumps or a proposed layout. Assess the named connector and revision; if several are requested, compare each explicitly. Do not substitute a related connector's capabilities. Static analysis can establish feasibility and concrete gaps without requiring a device launch.

Use [official-docs.md](official-docs.md) for the model's documented cache/backend constraints and the active transport's registration, memory-direction and completion contracts. Read HIXL API/Wiki material only for the HIXL path under assessment. Check these constraints against the actual connector adaptation; backend API support alone does not establish layout support.

## 1. Establish the complete input contract

Build an inventory for **every** distinct cache component, not just a representative attention layer. Identical layers may share one row only after proving equivalent layout and ownership. Include K/V, MLA components, indexer, scale/zero-point, draft/MTP, convolution/SSM, circular/recurrent state and any metadata needed to interpret them. Mark components as transferred, reconstructed locally, intentionally unused, or unknown, with reasons.

| Input | Required interpretation |
|---|---|
| Identity | P/D role, layer/group/spec/component, main/draft, framework and connector revisions, backend and hardware |
| Spec definition | Concrete class and inheritance, constructor/runtime field values, overridden properties/methods, grouping/merge behavior and connector dispatch |
| Logical meaning | Axis names/order, token/head/state ownership, logical block size, compression, CP interleave, valid window/tail and state cursor |
| Tensor view | Shape, dtype/packing, element size, stride of every axis with units, storage offset, actual block axis and view base |
| Size | Distinguish element count, logical tensor bytes, valid payload bytes per block, bounding address span, physical block/page stride, allocation bytes and registered bytes |
| Storage | Allocation identity/base/size, descriptor offsets, view aliases, shared groups/layers, padding, alignment and allocator block-ID policy |
| Execution | Writers, publication readiness, consumer interpretation, copy direction, staging/reuse rules, P/D topology and completion ownership |

If only one side's layout is given, distinguish same-layout P/D feasibility from conversion to another layout. State a conditional same-layout assumption when useful; do not invent the peer layout, block axis, dtype or byte units. Ask for missing values only when they determine the verdict, and continue evaluating independent components. Shape/stride/size alone cannot establish token order, sharing lifetime or model-state restoration.

For a proposed layout without runtime pointers, use symbolic allocation bases and offsets. For an existing implementation, reconcile the proposal with allocator/reshape code and measured views. A mismatch between supplied values is an input inconsistency to resolve, not something to silently normalize away.

### Read the spec definition before interpreting tensor dimensions

Read the concrete spec class on each side, its base classes and relevant overrides, and the code constructing its actual values. A class name or printed shape alone is insufficient. Field names vary by framework revision; record the actual definitions rather than assuming every spec implements the same API.

Trace:

```text
spec definition + instantiated values
-> grouping/merge + memory sizing + block manager selection
-> tensor descriptors + allocation + reshape/views
-> connector spec dispatch + peer metadata + request mapping
-> transmitted components + consumer interpretation/restoration
```

Check the following against code, retaining exact units:

- **Sizing:** logical block size versus kernel/physical block size; heads, head dimensions, dtype, quantized scales, padding/alignment, state planes and derived page bytes. Reconcile the spec's size formula with descriptor allocation, runtime strides and the allocator's number of blocks. Do not infer physical stride from payload bytes alone or assume a single spec's size owns an entire shared allocation.
- **Grouping and sharing:** equality/merge rules, grouping keys, shared-by/layer descriptors, page-size unification and layer/block stride. Determine which distinctions survive grouping and which must still be represented per layer/component. Equal page sizes do not make two specs semantically interchangeable.
- **Block/state semantics:** block-manager selection, null/evicted/window blocks, compression units, accepted versus speculative state, ring wrap/cursor and whether block IDs grow with tokens. Establish exactly which data and metadata D must restore and at what logical position.
- **Capabilities and residency:** read prefix-cacheability, slot-mapping participation, block-table token alignment and replication/sharding properties when present. Distinguish the number of block-table entries from simultaneously resident physical blocks. A Mamba row can span the sequence while old entries are null; a circular component can have one persistent block and no ordinary prefix-cache/slot-mapping semantics. Derive hit/replay tests per component instead of assuming all components share the attention contract.
- **Connector recognition:** `isinstance` branches, exact-type checks, registries, unsupported-spec guards and generic fallbacks, including inherited behavior. Determine whether the new spec is rejected, silently treated as a parent spec, or handled with its actual semantics. A matching branch is not proof that its formulas remain valid.
- **Peer compatibility:** determine which spec-derived values reach the peer or are safely reconstructed. Class names alone are not a wire contract. Same-named specs from different revisions can differ; differently named specs may be compatible after a proven mapping.

For example, a circular-state spec with a fixed physical page may need cursor/wrap restoration even though its tensor has an ordinary block axis. A sliding-window spec may need eviction/window alignment despite sharing an attention cache's shape. A compressed spec changes token-to-block units even when page bytes match. Judge each from its definition and consumers, not the example's name.

If a spec definition or its instantiation is unavailable, report shape-level feasibility separately and mark semantic compatibility unresolved. Request the minimal class/property/constructor or block-manager evidence needed rather than declaring support from tensors alone.

## 2. Derive physical addresses and valid transfer segments

Apply [cache-layout.md](cache-layout.md). For an ordinary byte-addressable strided tensor, normalize element strides to bytes and write:

```text
address(index) = allocation_base + view_offset_bytes
                 + sum(index[axis] * byte_stride[axis])
logical_bytes = product(shape) * element_size
```

For a nonempty view, the minimum addressed offset relative to its view base is `sum(min(0, (shape[i]-1)*byte_stride[i]))`; the exclusive maximum is `sum(max(0, (shape[i]-1)*byte_stride[i])) + element_size`. Check both against the allocation. Handle empty dimensions separately. Negative/zero strides and overlapping views require explicit backend/connector support, not just a mathematically valid bound. For sub-byte or packed formats, derive addresses from the actual packing contract instead of assuming one element occupies an independent byte range.

Derive contiguous valid segments for the same logical token/head/state region on P and D independently. Identify holes, padding, inactive tails and shared components. The enclosing span is not the payload and does not authorize copying intervening bytes. Verify segment correspondence, coverage and unintended overlap; prove both bounds at the first and last blocks and at nonzero subview offsets.

Distinguish four cases:

- Equal internal byte order with different block strides: potentially compatible through per-block segments if the implementation carries independent peer strides.
- Noncontiguous components: potentially compatible through supported segment lists or pack/unpack; a single contiguous-copy interface may need adaptation.
- Different internal token/head order, dtype or packing: requires proven segment remapping or conversion, even when shape and total bytes match.
- Shared-page copying: requires a true page base, compatible component placement, complete readiness and permission to overwrite every copied destination byte. A scale subview is not automatically the page base.

Example: `shape=[N,4,8]`, FP16, byte strides `[128,16,2]` contains 64 valid bytes per block, but the block stride is 128 bytes. Its bounding span is `(N-1)*128+64`, not `N*64`. A peer with block stride 64 can receive 64-byte block copies if peer strides are modeled independently. Copying 128 bytes from each producer block would include a hole and can overrun the final destination block. This example proves arithmetic only; it does not prove that the named connector generates those entries.

## 3. Audit the connector end to end

For each row, record the layout requirement, actual implementation capability, evidence location, and gap. Read relevant code paths and their callers; do not infer capability from a class name or transport library alone.

| Contract | What to verify |
|---|---|
| Spec definition and dispatch | Concrete fields/overrides, derived sizes and grouping, block-manager semantics, exact/inherited matching and unsupported/generic paths |
| Descriptor and allocation | Spec-to-descriptor consistency, block axis, shared backing, allocation and memory-budget assumptions |
| Registration | Base/length/alignment, alias deduplication, noncontiguous spans, physical bounds and lifetime |
| Handshake | Peer-specific layout/stride/offset/dtype, version negotiation, per-layer/spec identity and topology survive serialization |
| Request mapping | Logical tokens to kernel blocks/pages, CP/head/replica ownership, prefix/window/tail, compression and state restoration |
| Transfer construction | Actual address/length formulas, segment-list support, whole-block/page assumptions, coalescing and conversion |
| Readiness and reuse | All included writers complete, aliases remain stable while read, D visibility before use, no in-flight reuse |
| Consumer and failure | Correct cache interpretation and metadata, failed/partial reception handling, retry/cancel/release behavior |

For hybrid layouts, evaluate cross-component interactions as well as each component alone. A whole-page copy can overwrite a valid alias even if all individual view bounds are correct. One unsupported required state component prevents a full-model support verdict. If a component is omitted from transfer, prove how D obtains its required state.

Trace readiness at the actual segment/layer boundary and final placement after any model-state relocation. Request-level receive completion, per-layer load waits and P-side slot-reuse barriers are different contracts even when method names resemble each other. Verify each hook's implementation and caller in the active runner, including composite connectors and pool/offload paths.

## 4. Report compatibility and adaptation gaps

Use one of the following verdicts per component and for the complete required cache set:

| Verdict | Meaning |
|---|---|
| Supported within stated conditions | Current implementation represents and executes all required contracts in the specified configuration; state whether this is static evidence or runtime-validated |
| Requires adaptation | A concrete implementation gap exists and a feasible change has been identified; current code is not supported for that case |
| Incompatible under fixed constraints | Required semantics cannot be preserved with the permitted protocol/layout/topology; explain which constraint would have to change |
| Insufficient evidence | Missing input or implementation evidence prevents a conclusion; list the smallest information needed |

Supply this compact result table:

| Component/spec and P/D layout | Valid bytes / physical stride / span | Connector contract and source evidence | Verdict and conditions | Gap and adaptation | Required validation |
|---|---|---|---|---|---|

Prioritize adaptation at the actual gap:

- Metadata/addressing: carry per-component peer strides/offsets and storage identity, fix block-axis assumptions, or reconstruct physical pages from valid descriptors.
- Spec integration: add explicit dispatch/capability checks and preserve spec-derived sizing, grouping and state semantics through descriptors and peer metadata. Fix a demonstrated spec/allocation inconsistency at its owner; do not relabel a new spec as an existing type merely to enter a supported branch.
- Mapping: add spec-specific logical-token/head/state mapping or supported sub-block scatter/gather; do not remove a topology guard without implementing the missing mapping.
- Data transformation: add a bounded staging pack/unpack or dtype/layout conversion when raw transfer cannot preserve the consumer representation. Account for extra memory, events, quantization metadata and numerical validation.
- Shared storage/lifetime: split transfers, flush before alias reuse, stage stable snapshots, or add correct readiness/reuse barriers. Do not change planner sharing semantics just to fit the connector.
- Protocol/model integration: extend versioned peer metadata, restore required cursors/state, and propagate completion/failure consistently. State compatibility implications for mixed versions.

Name affected implementation locations when source is available. Explain which changes are necessary versus optional optimizations, and include a worked failing address/mapping example. Segment count, padding traffic and staging memory are performance considerations to measure, not automatic reasons to declare incompatibility.

## 5. Validate the supported claim

Select cases from [validation.md](validation.md): instantiated spec size formulas and dispatch, same-shaped specs with different semantics, last-page bounds, nonzero offsets, padded/noncontiguous views, each distinct spec/alias group, topology mismatches, tails and repeated reuse. Validate payload and consumer metadata on the matching runtime when authorized. Verify shared-page copies do not alter unrelated live state, and conversion preserves logical values within justified tolerances.

An address derivation proves layout arithmetic; a focused unit test proves its tested contract; synchronized P/D payload and consuming-forward evidence establish a stronger runtime result. Keep those levels separate. If only static evidence is available, return the assessment and validation plan without claiming tested model accuracy.
