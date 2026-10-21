# Cache layout, registration and addresses

For a new layout versus a named connector, use [layout-compatibility.md](layout-compatibility.md) to inventory all components and produce compatibility verdicts and adaptation gaps. This reference supplies the shared address and storage rules.

## Separate four kinds of sharing

Distinguish scheduler block-ID allocation, Tensor/view aliasing, shared raw storage and physical contiguity of each transfer segment. Equal pointers may be intentional views with disjoint live group block IDs. Different view pointers may share one allocation. Prove overlap for live logical pages at the same time.

Trace allocation, reshape, writers and readers. Record descriptor fields, size/offset/layer_stride/block_stride, storage pointer/nbytes, view pointer/storage_offset, shape, dtype, per-axis byte strides, actual block axis, payload and padding.

- Legacy `shared_by` and modern `layers/layer_stride` are different contracts. An absent field is not a zero value. Support old descriptors only within the requested version scope.
- `layer_stride=0` may describe components in one physical page; interpret offsets and allocation semantics before calling it overlap or missing storage.
- Runtime cache values may be tensors, tuples or stacked K/V such as `[2,N,...]`. Axis zero is not universally the block dimension.
- An indexer may produce a compressed MLA spec. Main, draft, Mamba and indexer components can have different parallel semantics.

## Registration versus transmitted payload

Register the ranges actually accessed and keep allocation lifetime intact. Whole-storage, descriptor-span and merged-view registration are implementation/API choices. Preserve storage identity independently from per-view addresses.

`numel * element_size` excludes strided holes. For a nonempty view with nonnegative strides, an upper addressed bound is `view_ptr + sum((shape[i]-1)*byte_stride[i]) + element_size`; handle empty views separately. This bounding span does not imply every enclosed byte belongs to the view.

```text
P_addr = P_base + P_block_id * P_block_stride + P_inner_offset
D_addr = D_base + D_block_id * D_block_stride + D_inner_offset
length = corresponding contiguous valid bytes in this segment
```

Check each half-open interval against registration, storage bounds and semantic ownership. Include first/last blocks and nonzero inner offsets.

P stride=512B, D stride=256B and length=128B can be copied block by block. Independent block strides do not implement HND/NHD transposition, different internal head/token strides or dtype conversion. Inspect segment construction or an explicit conversion path.

## Three distinct coalescing operations

- Registration merging changes the registration table, not permission to overwrite intervening bytes. Strict overlap and adjacency rules depend on the helper/API and named reference behavior.
- Shared-page transfer needs a proven page base, physical stride, compatible peer layout and valid component spans. All included components must be ready with compatible lifetimes. Copying a full page from an inner scale-view pointer can overrun the final page.
- Transfer-entry merging requires source and destination continuity, compatible endpoint, ownership/generation and readiness. Consecutive block IDs alone are insufficient when stride exceeds payload length.

Delayed grouped-layer/chunk transfer can read a slot after a later layer overwrites it. Check independent storage, early flush, staging or reuse barriers before coalescing aliases.

A suspected shared-page optimization is a candidate for controlled A/B, not proof that all shared-page copying is wrong. Fewer registrations do not prove faster service: measure registration count/bytes/time separately from transfer entry count/bytes/latency.
