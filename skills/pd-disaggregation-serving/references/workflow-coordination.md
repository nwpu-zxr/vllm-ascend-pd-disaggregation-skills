# Coordinate overlapping deployment workflows

Use one deployment plan and one lifecycle controller per service. A controller is the actual tool, script or service manager responsible for start/status/stop and its authoritative state; a skill supplies instructions and does not itself provide a process lock. Multiple skills can contribute advice to the same plan without independently launching it.

## Select the workflow and execution owners

Inspect the skills and tool versions actually available, existing deployment records, jobs and live endpoints. Catalogue membership does not establish installation, and similar skill names do not establish compatibility or selection priority. Read a candidate's relevant references and command help, not just its description.

| Situation | Action |
|---|---|
| User explicitly selects this skill | Lead PD configuration and acceptance here; use compatible existing controllers for actual lifecycle operations |
| Another workflow already manages this deployment | Keep it in charge; use this skill for PD-specific review and missing evidence, and submit changes through the existing workflow |
| Multiple applicable skills, no existing deployment | Choose one workflow based on user intent and actual environment; record that choice and use the others only for scoped advice or execution steps |
| No suitable host controller | Use the authorized standalone tools and record ownership; no MindIE/VAWS installation is required |

For an overlapping skill such as `vllm-ascend-pd-serving`, reuse its controller only if its actual prerequisites, topology, startup/rollback semantics and proxy scope fit. A Session Group requirement cannot be satisfied by inventing IDs or snapshots. If that workflow is optional and does not fit, choose a compatible standalone path; if the host or user requires it, resolve its prerequisites rather than bypassing them. Keep useful configuration advice separate from an inapplicable execution contract.

Delegation is a scoped operation, such as starting a specified role through its controller, not a second invocation of the entire deployment workflow. If a consulted skill routes back here, retain the selected plan and continue at the needed step rather than following the referral recursively. Selecting a different skill does not implicitly migrate running services to another controller.

## Record ownership in the existing run record

Use the host's existing manifest/state schema. Where none exists, a compact deployment record is sufficient; do not require a new state format. Retain:

- Selected workflow, intended configuration/revision and role startup dependencies.
- For each P/D/proxy service: endpoint, devices/ports, lifecycle controller, authoritative state location, and available run/job/session/process identities.
- Whether each service was reused, created or changed in this attempt, and the authorized restart/rollback scope. When changing an existing service, retain its prior configuration and intended recovery action.
- Whether the proxy is externally managed or owned by this deployment, plus the available health/status and stop operations.

Refer to controller state instead of maintaining a competing mutable PID/job registry. Immediately retain returned identities before waiting; reconcile any host-required progress record with those identities. A transport tool that executes a controller command is not a second controller. For concurrent agents, use the host's applicable locks/leases or serialize changes through the existing owner; Markdown instructions alone do not enforce mutual exclusion.

## Execute, resume and clean up through the same owners

1. Query controller state and correlate endpoint, process/command identity and device/port ownership before start. Reuse an appropriate live service. An existing incompatible configuration requires an in-scope change through its owner, not a second listener or blind replacement.
2. Send a lifecycle action once through the selected controller. Do not additionally issue raw `vllm serve`, a second launcher or a sibling skill's whole `start` workflow for the same role.
3. On timeout, disconnection or interruption, inspect the recorded job/controller state and actual process before retrying. A tool error does not prove no process was launched. If ownership or outcome remains ambiguous, continue read-only diagnosis and leave dependent mutations pending; ask only for missing information that cannot be recovered. Controller unavailability is not permission to start a replacement with another mechanism.
4. Keep an existing externally managed proxy under its owner. Check its health/routing and request any in-scope configuration change through that owner. When a new proxy is needed, choose and record its controller separately; a P/D controller that accepts only a proxy URL cannot be assumed to manage the proxy process.
5. Inspect rollback behavior before launch, including whether it would stop pre-existing roles. On partial failure, observe any controller rollback already performed, then clean up remaining attempt-owned changes through their owners in dependency-safe order. Restore changed services according to the recorded recovery plan; preserve unaffected reused roles, external proxies and resources belonging to other runs. Do not apply a second blanket rollback.
6. Reuse health, routing and KV-transfer evidence only when it matches the current service incarnation, configuration and request. Collect missing evidence in the same deployment. A changed configuration can require a new smoke request, but loading another skill does not require another deployment. If a separate diagnostic control is needed, give it distinct ownership and isolated resources.

An intentional controller migration requires a concrete handoff: reconcile the old state, stop or adopt through supported operations, verify the result, and update the authoritative owner before further mutations. Unrelated skill installation or discovery never triggers this migration.

## Review scenarios

These are workflow review cases, not claims of runtime validation:

| Case | Required decision |
|---|---|
| Both serving skills match a fresh direct-endpoint request | Select one compatible plan; do not manufacture a Session Group or run both launch workflows |
| P/D already run under a host controller | Review/reuse them and use that controller for any requested change |
| P is reused, new D fails, proxy is external | Check rollback results; preserve P and proxy; clean up only attempt-owned changes |
| Start timed out after remote launch | Query the recorded job and actual process before any retry |
| Another skill sends the request back here | Continue the selected plan at the scoped step; do not recurse or reinitialize state |
| Configuration unchanged and current smoke evidence is sufficient | Reuse that evidence; do not create a second deployment |
