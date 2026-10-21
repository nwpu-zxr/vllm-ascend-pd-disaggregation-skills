# Launch contract

Select the official model and transport documents with [official-docs.md](official-docs.md). Retain a version-scoped configuration-difference table, including HIXL settings only when the selected backend uses them.

## Actual code and environment

In the target runtime, record framework/plugin/connector `__file__`, `__path__` or `find_spec()`, source revisions/dirty hashes, Python environment, CANN, torch_npu, transfer library and backend. An editable flag in `pip show` does not prove that imports resolve to the intended checkout.

For a missing `acl` module, inspect the installed CANN environment and pyACL before choosing a package fix. Check the service process environment; an interactive shell loading CANN does not imply a noninteractive service does. Avoid printing credentials or broad environment dumps.

Matching P/D versions are a normal baseline. An explicitly requested mixed-version experiment instead needs wire-schema, capability, layout and failure-policy verification; do not silently prohibit it or claim compatibility. Record hardware, runner and quantization differences.

Read documentation and examples from the deployed revision, then inspect its parser and effective configuration. A flag accepted by the CLI may be ignored, deprecated or overridden; verify dispatch. Do not copy tuning flags from a newer release into an older deployment.

## Endpoint and port table

For each role and DP engine, list API, DP RPC, connector metadata/control, transfer engine, proxy and collective/bootstrap ports. Derive expanded rank ranges from the current code and communication library. Check actual listeners and host/container network namespaces.

- A wildcard bind address such as `0.0.0.0` is not a usable advertised peer address.
- P/D on separate devices of one host can still collide on communication ports. Distinguish API-port and collective-port failures.
- Historical base ports or range widths are not defaults. Validate the installed HCCL version and topology; changing system-wide reserved ports requires appropriate scope and preservation of existing settings.
- Record timeout units and owners separately: HTTP, connect, collective, execution, connector retention/lease and heartbeat I/O. Longer timeouts cannot repair deadlock, stale ownership or wrong addresses.

## Request API and proxy

Verify model names, tokenizer/chat template, raw-token API, transfer parameters and the route of remote engine/request IDs. Accepted JSON fields do not prove connector consumption.

Trace P request construction, returned transfer metadata and D request construction together. A proxy can request one P output token to obtain transfer metadata without forwarding that token as an extra D prompt token. Identify which role owns the first returned token/logprob and how output budgets are preserved. Do not append P output or globally truncate the prompt without confirming this protocol and the model/spec's state handoff. Trace any prompt-minus-one mutation in the connector and replay adjustment in the scheduler.

Proxy startup, health and retries are separate concerns. Inspect streaming finish/error behavior, client cancellation, P/D ID correlation and whether retries hide a failed attempt. Recompute/retry must preserve token semantics; avoid applying a chat template twice or decode→encode round trips that alter token IDs.

Reuse the target revision's maintained proxy/example where appropriate. Do not rewrite an existing proxy merely to launch it. Remove irrelevant example settings and private addresses when preparing reusable scripts.

## Optional execution adapters

Discover current tool schemas before invoking MindIE remote-dev or another companion backend. Prefer structured execution, file, job and artifact tools when available. Use the host project's authorized native mechanism otherwise; no specific MCP name is guaranteed.

If an existing managed orchestrator is selected, inspect its help and requirements first: isolation/session IDs, snapshot identity, device assignment, startup order and proxy ownership. Reuse it only when the deployment meets its actual contract. Do not fabricate ready state or snapshot identity to satisfy validation.

Record commands and process ownership so restart and cleanup target the exact deployment. Keep transient state outside tracked skill files and never embed endpoint credentials in a reusable package.
