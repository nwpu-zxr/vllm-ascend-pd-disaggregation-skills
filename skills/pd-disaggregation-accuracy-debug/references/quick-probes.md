# Fast probes and their limits

Use these to narrow a reproduced case, not as automatic production changes.

## Destination sentinel and write coverage

Purpose: detect missing writes to the D region that the transfer contract says must be replaced.

1. Use an isolated diagnostic request/allocation. Derive the expected write mask from logical tokens, head shards and valid state, independently of the generated transfer entries; otherwise a missing entry can disappear from both the plan and the test oracle.
2. After allocation and before transfer, fill only that request's exclusively owned destination elements with a recognizable sentinel. Preserve existing prefix-hit tokens, live hybrid aliases, valid recurrent/ring state, padding the kernel may read, and other requests' data. If ownership is uncertain, do not fill the shared storage; use a safe test allocation or payload snapshots.
3. Choose a dtype-aware sentinel. A representable NaN is useful for a floating-point diagnostic cache, using `isnan`, not equality. FP8, integer and packed/quantized formats need verified format-specific values or a shadow write-coverage mechanism; do not reinterpret arbitrary bytes as a portable NaN. Keep scales and valid-state metadata intact unless explicitly included in the test contract.
4. Synchronize the fill before submitting the transfer. Check after transfer visibility and again before the first consumer. Report expected-written elements retaining the sentinel, written elements outside the expected range, and untouched guard regions that changed.
5. If required valid elements retain poison, capture evidence and stop that diagnostic forward rather than knowingly feeding poison into the model. Restore/discard the test allocation and instrumentation afterward.

A retained sentinel supports a missing-write/visibility hypothesis only if the source is not legitimately the same sentinel and no later writer restored it. Sentinel disappearance alone does not prove correct source, offset, request identity or values. Compare P payload too. Changing allocation initialization/timing can mask races; a passing poisoned run does not clear the original path.

For cross-request trampling, prefer request/generation-specific shadow ownership records and snapshots. Canaries belong only to genuinely unused, allocated and protected ranges; never write beyond an allocation or into an intentional alias to create a guard.

## Reasoning-tag and output audit

Normalize each complete response attempt into JSONL with unique `id`, generated `text`, and optional `output_tokens`, `max_output_tokens`, `finish_reason`, and boolean `correct`. `text` must be the generated surface being compared, not the prompt or service log; consistently reconstruct reasoning/content if the API separates them. Exclude failed retries from a successful-attempt aggregate or label each attempt explicitly.

Run the bundled standard-library helper on the host:

```bash
python3 scripts/audit_outputs.py normalized.jsonl --expect-think-close > output-audit.json
```

The path is relative to this skill directory. Omit `--expect-think-close` if the output contract does not require `</think>`. The report counts samples with zero/one/multiple closing tags, explicit or suspected length limits, replacement characters, adjacent repeated text spans and correctness when supplied. It does not calculate model tokens or infer answer correctness. Repetition detection is a bounded heuristic; structured answers and quotations can be legitimate.

The repetition probe inspects the first and last 8192 characters, retaining overlap when the output is shorter than 16384 characters. It can miss a repeated span split across a window boundary or confined to an unscanned middle region. `repetition_characters_scanned` counts unique covered characters, not total regex work. IDs and metadata remain in the report even though generated text is omitted.

Compare rates over the same sample IDs, inspect suspicious outputs and distinguish short premature termination from long truncation. Never treat tag count alone as a pass/fail accuracy metric.

## Small tensor and operation probes

Before dumping the whole model, compare one request, layer/component and valid token/head interval at the boundaries in [evidence-ladder.md](evidence-ladder.md). Include metadata and synchronization; min/max alone is insufficient.

For a suspect scatter/attention, fused MC2/MegaMoE, reduction or recurrent operator, retain real inputs, shapes, strides, offsets, scales, workspace lifetime, streams and execution mode. Compare with a trusted reference. If a single call passes, replay the shortest original sequence, such as scatter→attention, target→draft or overlapping collective→consumer. Reinitialize or preserve state exactly as the original contract requires.

Validate on matching authorized hardware. Static Python checks or a mock output cannot establish CANN/operator correctness. A passing single-rank eager probe does not validate multi-rank or graph behavior.
