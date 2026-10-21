# Topology and block mapping

## Establish per-spec ownership

For each side identify `(DP engine, PP layer, PCP replica, TP/head piece, DCP sequence owner, KVPP layer owner)`. Worker flattening, endpoint indexing and layer ownership are distinct coordinate systems; derive them from the active implementation.

DP replicas generally serve independent requests; DP4/TP1 does not validate four-worker fan-in for one request. Match PP layers by stable identity, not local flattened spec indexes.

Some Ascend PCP implementations partition Q while replicating KV/cache. Select one complete producer replica in that contract; do not treat it as DCP sequence sharding. Historical worker and KVPP orderings have differed, for example `tp*PCP+pcp` versus `pcp*TP+tp`. These are examples to verify, not universal formulas. A handshake key omitting PCP may overwrite workers with the same PP/TP.

Compute KVPP owners separately from head shards/replicas. A restriction on KVPP+DCP within one side does not automatically prohibit cross-side P-KVPP/D-DCP. MLA, Mamba, GQA draft and replicated indexer can follow different CP/TP paths within one process.

## Head routing

Intersect local and remote intervals in each layer/spec's global KV-head space. Distinguish jointly required shards from interchangeable replicas. One head per rank does not distinguish eight independent heads from eight copies of one head. Main-model head counts need not apply to draft layers.

Filter topology candidates by layer owners, retaining a provider for every required shard. Cache only mappings with identical semantic dependencies: engine incarnation, layer/spec, final owners/candidates, CP/layout/scale and request offsets as applicable. Do not require one universal cache representation.

## Connect block tables through logical token positions

Keep original tokens, compressed tokens, manager blocks, kernel blocks and physical pages distinct. State units, origins, rounding and valid tails at every conversion.

1. Trace D matched/external tokens through allocation and post-allocation metadata to actual full/unhashed/null block tables.
2. Establish whether P publishes full, missed, windowed or final-state blocks. N versus N-1 depends on the scheduler/state-restoration contract, not a universal model rule.
3. Expand each side using its own scale, then align global logical token intervals. Different scales are neither automatically invalid nor automatically supported by equal kernel block sizes.
4. Explain prefix hits, windows, padding and speculative tails before truncation. `min(len(P),len(D))` must not hide unaccounted gaps, duplication or mismatches.

Example: eight compressed tokens per physical block and compression ratio four mean 32 original computed tokens skip one physical block, not four. Do not apply compression twice to a field already expressed in compressed units.

## DCP interleave

Verify backend interleave, per-rank token order and within-block continuity. Whole-block ownership formulas require demonstrated block-aligned sharding; divisibility restrictions also depend on the implementation.

Counterexample: block size four, producer DCP2, interleave one: rank zero stores `[0,2,4,6]`. A whole-block copy cannot produce the DCP1 consumer's `[0,1,2,3]`. Use supported sub-block scatter/gather or conversion, or reject that combination. Deleting a backend guard cannot provide conversion.

Do not copy upstream single-group limitations into Ascend V2, or claim upstream has Ascend's multi-group/PCP support. PCP=1 arithmetic degeneration does not prove compatibility of wire schema, head metadata or release behavior.

## Stateful and windowed caches

| Spec family | Evidence needed |
|---|---|
| FA/MLA | Token interval, compression/scale, head/sequence sharding, prefix offset |
| SWA/tail | Valid window, eviction/null blocks, peer logical sizes; when tail alignment equals list-offset alignment |
| Mamba/GDN | Accepted versus speculative state, align/none mode, conv/SSM shapes, TP slicing, restoration position |
| Circular/ring | Position/wrap, valid state planes and metadata when block IDs do not grow |
| Indexer/scale | Actual concrete spec, replication, effective DCP size, inner offsets and compression units |

Correct state bytes still require correct seq_len, slot mapping and state cursor. Assess support per spec, layout and protocol rather than model name alone.
