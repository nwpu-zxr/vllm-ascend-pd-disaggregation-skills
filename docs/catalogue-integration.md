# Awesome MindIE Skills integration

This repository is the source collection. [Awesome MindIE Skills](https://github.com/mindie-agent/awesome-mindie-skills) is a catalogue that pins upstream definitions. Follow its current [contribution guide](https://github.com/mindie-agent/awesome-mindie-skills/blob/main/CONTRIBUTING.md) and [format](https://github.com/mindie-agent/awesome-mindie-skills/blob/main/docs/catalog-format.md) when preparing a submission.

Source repository: [nwpu-zxr/vllm-ascend-pd-disaggregation-skills](https://github.com/nwpu-zxr/vllm-ascend-pd-disaggregation-skills). Catalogue inclusion is a separate submission; this guide does not claim an accepted entry.

| Skill | Source path | Suggested category | Execution | Role |
|---|---|---|---|---|
| `pd-disaggregation-design` | `skills/pd-disaggregation-design/SKILL.md` | `model-integration` | `depends-on-checks` | `task` |
| `pd-disaggregation-serving` | `skills/pd-disaggregation-serving/SKILL.md` | `serving` | `depends-on-checks` | `workflow` |
| `pd-disaggregation-accuracy-debug` | `skills/pd-disaggregation-accuracy-debug/SKILL.md` | `debugging` | `depends-on-checks` | `workflow` |

## Prepare a source entry

1. Publish the reviewed source to the chosen GitHub repository. Record its actual repository URL, maintainer, MIT license and full commit SHA. Local uncommitted files are not a publishable pinned revision.
2. Inspect each complete package at that revision and compute the exact `SKILL.md` SHA256. References and scripts are covered by the source commit, not by that definition-file hash alone.
3. Register the source project in `catalog/sources.yaml`; add one entry per skill under `catalog/skills/` with the source-relative paths above, bilingual summaries and definition-review evidence.
4. Use `validation.status: not-recorded` with empty cases unless that exact revision has a scoped runtime reproduction. Local package tests do not establish hardware support.
5. Render and validate the catalogue using its documented commands, including pinned remote hashes. Recheck its current schema before submission.

Do not guess a repository owner, fabricate a commit SHA or retain a stale hash after editing. Updating a shared source revision affects every catalogue entry that references it.

## Coexistence with existing serving entries

An entry such as `vllm-ascend-pd-serving` may overlap with this collection. Catalogue membership does not establish that it is installed, and registration does not give either skill precedence. Describe the actual integration as one selected deployment plan with one lifecycle controller per service, not two independent launch workflows.

Follow [workflow coordination](../skills/pd-disaggregation-serving/references/workflow-coordination.md): retain existing controllers and state, contribute scoped PD review or missing evidence, and use a standalone path for a new deployment only when appropriate to the host's requirements. Read the installed candidate's references to resolve Session Group, proxy and rollback boundaries. Do not claim transparent compatibility with every version or that the Markdown rules enforce process exclusion.

The coordination reference includes manual review scenarios for overlapping entrypoints, reused services, partial failure, uncertain launches, routing loops and shared acceptance evidence. Package checks validate distribution and links; they do not constitute a live MindIE deployment test.

## Reuse across design and diagnosis

These skills remain PD methodology entrypoints, with optional specialist execution. The bundled [reuse contract](../skills/pd-disaggregation-design/references/skill-reuse.md) defines `auto`, `prefer-integrated` and `standalone` preferences, capability discovery, applicability checks and evidence returned to the PD conclusion. Candidate names are navigation examples, not required installations or guaranteed cross-version integrations.

Review both paths: a matching specialist receives the existing case/build/state identities and returns scoped evidence; an absent or incompatible optional specialist falls back to the package's own methods. Check that a framework-specific cache recipe is not applied as a universal vLLM rule, and that missing hardware is reported as unexecuted runtime coverage rather than a successful fallback. Catalogue metadata must not turn optional reuse into a hard dependency.

## Suggested summaries

| Skill | English | Chinese |
|---|---|---|
| `pd-disaggregation-design` | Design and review PD connectors; assess new cache specs/layouts and identify compatibility gaps and adaptations. | 设计与审查 PD connector，评估新 cache spec 与 layout 的兼容性并给出适配方向。 |
| `pd-disaggregation-serving` | Prepare or launch P/D/proxy services and verify routing, actual KV transfer and cleanup. | 准备或拉起 P/D/proxy 服务，验证路由、真实 KV 传输和资源回收。 |
| `pd-disaggregation-accuracy-debug` | Diagnose PD accuracy top-down or bottom-up, aligning completed P KV/state with D's content and placement before each component's first consumption under the actual handoff contract. | 从上而下或从底而上诊断 PD 精度，按实际交接语义对齐 P 完成的 KV/state 与 D 对应组件首次消费前的内容和位置。 |

The catalogue's own metadata license does not replace this repository's MIT license. Optional MindIE tool integration is described inside each skill; catalogue inclusion does not imply those tools or a device environment are installed.
