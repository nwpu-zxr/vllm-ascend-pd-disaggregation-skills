# Official model and transport documentation lookup

Use this workflow when model/platform settings or transport behavior affect PD design, layout compatibility, deployment or accuracy diagnosis. Reuse already-read evidence for the same revisions; refresh when the model, hardware, stack or disputed configuration changes. Read the relevant pages, not just search snippets or a site landing page.

## Official starting points

- [vLLM Ascend documentation](https://docs.vllm.ai/projects/ascend/en/latest/index.html): model tutorials, supported models/features, PD examples, configuration reference, FAQs and release notes.
- [HIXL official repository](https://gitcode.com/cann/hixl) and [documentation index](https://gitcode.com/cann/hixl/blob/master/docs/README.md): development guides, API contracts, examples and source.
- [HIXL Wiki](https://gitcode.com/cann/hixl/wiki/Home.md): platform setup, Mooncake integration, LocalCommRes, troubleshooting and performance guidance. Follow the current index because page names and organization can change.

`latest` and `master` are discovery entry points, not evidence that a deployed release supports a setting. Select the documented release/tag or source commit matching the installed build. Record when only newer or undated documentation is available. Documentation may contain examples for different hardware or validation scopes on the same page; read the applicable section and limitations.

## Select the model recipe

1. Identify the actual model family, architecture/config, checkpoint variant, main/draft model, quantization, hardware generation, runner and P/D topology. Do not select a recipe by an approximate model-name match alone.
2. Open the matching model tutorial from the official index. Cross-check supported models/features, framework/plugin pairing and release notes. If no exact recipe exists, mark the gap and use nearby documentation only for explicitly shared components.
3. Follow the recipe's relevant configuration and feature links: attention/cache format, CP, expert parallelism, fused operators, graph, asynchronous scheduling, speculation, offload, tokenizer/template/parser and output limits. Separate prerequisites and correctness constraints from optional performance settings.
4. Compare the documented recipe with the actual parser, dispatch and effective P/D process configuration. A renamed option, ignored environment variable or automatic fallback is a concrete discrepancy. Resolve conflicting documentation/source/runtime evidence explicitly instead of copying the most recent command.
5. Preserve role-specific differences and user constraints. A colocated recipe is not a complete PD recipe; combine it with the selected connector's PD contract and supported topology. A user-provided known-good configuration is a valuable control, with its exact environment and success criteria.

Produce a small configuration-difference table before applying changes. Do not import every tuning option from an example into a minimal reproduction.

## Identify whether HIXL is on the actual path

Trace connector -> transfer engine/backend -> loaded library/API -> device/host memory -> selected protocol. A Mooncake or NIXL class name does not prove that this run uses HIXL. Read build/runtime selections, actual library paths and initialization logs. Distinguish HIXL Engine, HIXL CS, legacy paths and other transports where relevant; configuration ownership and API contracts may differ.

If HIXL is active or under consideration, consult its official repository and Wiki for that path and hardware. If it is absent, record that finding and consult the active dependency's documentation instead of applying unrelated HIXL options.

| Topic | Evidence to retrieve and compare |
|---|---|
| Software/hardware support | Loaded HIXL/CANN/driver and transport builds, supported device generation, required APIs and protocol/memory-direction support |
| Configuration ownership | Connector options, wrapper environment, HIXL initialization options and defaults; precedence, parse timing, exact schema and which endpoint consumes each value |
| Communication resources | Actual protocol and host/device placement, device/rank mapping, advertised endpoints, network namespaces, topology and LocalCommRes when required |
| Ports and timing | Host control versus device transport ports, expanded listener ranges, connection/transfer timeouts and their units; do not substitute a scheduler lease timeout |
| Memory operations | Register/deregister rules, alignment and address/length limits, H2D/D2H/D2D applicability, READ/WRITE direction and source/destination lifetime |
| Async completion | Submission versus completion/status semantics, failure propagation, stream/visibility dependencies and cleanup of partial transfers |
| Diagnosis | Relevant Wiki signature, both endpoints' earliest errors, low-level logs, same-path data-integrity example and version-aligned source locations |

Search the selected revision for keys such as `GlobalResourceConfig`, `LocalCommRes`, `ASCEND_GLOBAL_RESOURCE_CONFIG`, `comm_resource_config.protocol_desc` and `comm_resource_config.listen_port` only where the active API/wrapper uses them. They are lookup terms, not a universal environment recipe. Preserve literal dotted JSON keys versus nested objects, value types, defaults and wrapper-specific restrictions. A low-level API may accept values that the connector deliberately rejects. Confirm effective settings in the initiating/receiving process and channel, not just exported shell variables.

Do not infer the protocol from an IP prefix or infer a device model from a loose marketing name. Establish the actual device and path. Treat Wiki diagnoses and suggested workarounds as hypotheses requiring version and symptom evidence. Reading a guide does not authorize changing shared fabric, routes, TLS policy or installed software; use the existing task scope for any experiment or repair.

## Apply findings to the current skill

- **Design/layout assessment:** include the transport's real registration, segmentation, memory-type and completion constraints in the per-component compatibility matrix. Transport support cannot compensate for missing model/spec mapping in the connector.
- **Serving:** derive the launch configuration, endpoint/port plan and stack prerequisites from the matched model and transport documents. Verify settings reach the service processes and selected backend before the real-transfer smoke test.
- **Accuracy diagnosis:** use documented constraints during configuration review and feature A/B selection. If evidence points below the connector, correlate both endpoints' transport logs and payload boundaries with the active HIXL API. A passing standalone transport example narrows the hypothesis but does not validate model integration; a timeout or successful return alone does not establish corruption or payload correctness.

For a claimed known bug or fixed release, require a matching issue/fix and precise build applicability. A Wiki keyword match or newer master implementation cannot prove the installed version is affected or repaired.

## Retrieve real content and handle access failures

Prefer an available official-service connector; otherwise use web tools or authorized read-only HTTP/Git access. Verify the returned body contains the intended document. HTTP 200 with a login page, JavaScript shell or error payload is not a successful read.

Useful public fallbacks verified during package maintenance:

- Repository file pages can be read through the official raw host, for example [HIXL docs index as Markdown](https://raw.gitcode.com/cann/hixl/raw/master/docs/README.md). Substitute the verified revision and discovered path for version-specific use; validate content type/body rather than trusting a `.md` suffix.
- If the Wiki web page is a frontend shell, its public Git endpoint is `https://gitcode.com/cann/hixl.wiki.git`. Clone into a task-local untracked directory, record HEAD, then read `Home.md` and linked Markdown. The Wiki has its own commit history; its HEAD is not the HIXL library version.
- In either route, follow actual index links. Resolve relative links against the correct repository/ref or Wiki root; do not treat Wiki paths into the main source repository as locally existing files.

For example, from a chosen untracked artifact directory:

```bash
git clone --depth 1 https://gitcode.com/cann/hixl.wiki.git hixl-wiki
git -C hixl-wiki rev-parse HEAD
```

Use an unused destination or inspect an existing checkout before reuse. Do not overwrite user files or force an update of a modified checkout. Fetching documentation does not require executing upstream setup scripts, installing an upstream skill or cloning every dependency. Keep upstream documentation as referenced evidence rather than copying it into this package.

If these routes fail, state which page/path was inaccessible and continue with applicable local versioned docs or user-provided excerpts. Ask for an excerpt/export only when the unavailable fact determines the next step. Do not bypass authentication or claim support from a search snippet. Record direct-read, indexed-content, local-snapshot and unavailable evidence distinctly.

## Evidence to retain

| Question/setting | Official page and section | Documentation revision/access date | Runtime value and consuming component | Applicability/discrepancy | Next check |
|---|---|---|---|---|---|

Link the actual supporting page, not just the home page. Record source commit or Wiki HEAD when using Git, missing evidence, and any mismatch with the deployed version. Keep the record in the task's existing run/report artifacts. The access check proves documentation retrieval, not successful deployment or model accuracy.
