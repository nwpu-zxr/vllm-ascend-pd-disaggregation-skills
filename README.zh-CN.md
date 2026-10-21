# vLLM Ascend PD Disaggregation Skills

[English](README.md) | [简体中文](README.zh-CN.md)

面向 vLLM Ascend Prefill/Decode 分离（PD 分离）的 Agent skills，覆盖 connector 设计、KV-cache spec/layout 兼容性评估、服务部署，以及基于证据的精度诊断。

本仓库包含三个可独立使用的英文 skill。它们指导 Agent 根据模型、源码、运行环境和传输证据完成具体工程任务，不提供适用于所有模型的启动命令或固定兼容性清单。

三个 skills 主要提供 PD 方法论：明确问题、选择证据并形成有适用范围的结论。具体专项分析和执行可以复用仓库或宿主中的合适 skills；没有这些 skills 时，仍可使用包内流程和方法继续。

| Skill | 使用场景 | 交付内容 |
|---|---|---|
| [pd-disaggregation-design](skills/pd-disaggregation-design/SKILL.md) | Connector 设计与审查；新 KV-cache spec/layout 适配评估 | 语义与实现分析、逐组件兼容性结论、适配缺口和验证计划 |
| [pd-disaggregation-serving](skills/pd-disaggregation-serving/SKILL.md) | 准备启动脚本，部署、检查和停止 P/D/proxy 服务 | 可复现配置、就绪检查、实际 KV 传输证据及清理方法 |
| [pd-disaggregation-accuracy-debug](skills/pd-disaggregation-accuracy-debug/SKILL.md) | 精度下降、KV 异常、NaN、重复输出、投机接受率异常 | 首个差异位置、受控对照实验、根因分类与验证证据 |

## 安装和使用

获取仓库：

```bash
git clone https://github.com/nwpu-zxr/vllm-ascend-pd-disaggregation-skills.git
cd vllm-ascend-pd-disaggregation-skills
```

将 `skills/` 下需要使用的完整目录复制到 Agent 支持的 skill 搜索目录，保留其中的引用文档、脚本、许可证和可选的 `agents/openai.yaml` 元数据。每个 skill 均可单独安装，无需安装另外两个。不支持 skill 自动加载的 Agent，也可以直接读取对应的 `SKILL.md` 并遵循其工作流。

示例请求：

- 使用 `pd-disaggregation-design`，根据这个新 cache spec 和 P/D 所有 cache 的 shape、stride、size、共享关系，评估指定版本 Mooncake connector 的兼容性，列出支持条件、未知项和适配缺口。
- 使用 `pd-disaggregation-serving`，根据这个模型和这些服务端点准备最小 P/D/proxy 部署；核对官方模型配置和实际传输后端，再验证存在真实远端 KV 传输的请求。
- 使用 `pd-disaggregation-accuracy-debug`，定位这次 PD 精度回退；保留失败现场，检查特性交互，找出 P 产生状态、KV 传输、D 输入和后续计算之间的首个差异。

仅分析的请求不会自动扩展成设备实验。硬件实验需要已授权、与目标环境匹配的运行环境。本地包检查和输出审计需要 Python 3.10 或更新版本，无需第三方 Python 包。

## 工作流覆盖范围

**设计与兼容性**：沿 spec 定义、分组、内存分配、运行时 tensor view、内存注册、对端元数据、token/head 映射、传输与生命周期逐项核对。检查所有必需的 cache 组件；shape 相同或注册成功本身不能证明兼容。

**服务部署**：区分脚本检查、服务就绪、请求路由、实际 KV 传输和资源清理。复用所在环境的服务管理与远程开发工具，无需另行安装一套进程管理系统。

**精度诊断**：可以从配置和特性向下定位，也可以从 tensor 证据向上验证。核心是对齐 P 已完成写入的有效 KV/state，与 D 完成必要加载和状态恢复后、对应组件首次消费前的数据内容及位置。逐层加载时，这个检查点可以位于整个 forward 内部。恢复位置按实际协议核对，覆盖适用的 N-1、部分命中及有限范围 replay。

从底向上的路线可以先建立支持的 eager、算子下发 blocking、确定性通信基线，再逐项恢复特性。针对性覆盖 block/spec 边界、投机步数、P/D prefix cache 与外部池命中、多并发，以及有实际写入和回收记录的脏 block 复用；结合设备、软件配套和首个计算差异完成归因。缺少 `</think>` 或传输接口返回成功，都不能单独作为精度结论。

诊断方法不局限于内置清单。Agent 可以使用 MindIE Agent 或其他宿主提供的相关 skills、基于官方文档和源码等一手来源的互联网检索，以及通用调试知识来设计更有区分力的实验。需要保留来源、版本适用范围和对照证据，不能把记忆中的解释或相似问题记录直接当作当前根因。

三个 skills 均包含按模型查阅 [vLLM Ascend 官方文档](https://docs.vllm.ai/projects/ascend/en/latest/index.html) 的流程。实际或拟议路径使用 HIXL 时，还会查阅 [HIXL 官方仓库](https://gitcode.com/cann/hixl) 和 [Wiki](https://gitcode.com/cann/hixl/wiki/Home.md)。文档应匹配实际构建和硬件，`latest`、`master` 仅作为查找入口。

## 运行环境与 MindIE Agent 集成

独立使用不依赖 VAWS 安装、私人 session 记录或固定工作区路径。在已有工作区内使用时，遵循该环境的隔离、代码一致性、服务生命周期和运行记录规范。MindIE Agent 的 remote-dev、知识查询、诊断及协调工具属于可选适配，按当前环境实际提供的能力使用。

可以用自然语言指定复用偏好，无需新增配置文件或命令行参数：

| 偏好 | 行为 |
|---|---|
| `auto`（默认） | 核对适用条件后复用可用的专项 skill；没有合适 skill 时使用包内方法 |
| `prefer-integrated` | 优先复用合适的仓库/MindIE skills；缺少可选能力时说明原因，并按包内方法继续 |
| `standalone` | 使用包内方法论和可用工具，不依赖可选专项 skills |

例如：“使用 `pd-disaggregation-accuracy-debug`，采用 `prefer-integrated` 模式；复用可用的正确性验证、graph 和算子 skills，未覆盖的步骤按包内方法处理。”用户明确要求使用的特定系统和宿主强制规则，在所有模式下都仍然有效。

[能力映射与复用约定](skills/pd-disaggregation-design/references/skill-reuse.md) 覆盖 cache/layout 分析、部署、正确性对照和数值/分布式诊断，每个 skill 包内均有独立副本。选择时核对实际框架、版本和输入约定，不仅按名称匹配；跨步骤保持相同请求、构建和证据标识，将专项结果汇总到 PD 结论，局部检查通过不代表 PD 端到端正确。

与其他部署 skill 同时使用时，遵循“一个部署计划、每个服务一个生命周期管理者”。已有工作流继续管理其服务，本仓库提供 PD 配置审查、诊断和缺失的验收证据，不另起一套重复部署。新部署选择适配的宿主管理工具或独立执行路径；单独记录 proxy 归属，启动结果不确定时先核实再重试，回滚时保留复用服务。详见 [工作流协作规则](skills/pd-disaggregation-serving/references/workflow-coordination.md)。这些规则用于指导 Agent，实际并发互斥仍依赖宿主锁、资源租约和管理工具的行为。

参见 [目录集成说明](docs/catalogue-integration.md)，了解如何将已发布版本登记到 Awesome MindIE Skills。该目录索引上游 skill 定义，本仓库保存实际源码；提供兼容说明不代表已被目录收录。

## 输出审计工具

将每次完整响应整理为 JSONL，每条记录包含唯一字符串 `id` 和生成文本 `text`。可选字段为 `output_tokens`、`max_output_tokens`、`finish_reason` 和布尔值 `correct`。

```bash
python3 skills/pd-disaggregation-accuracy-debug/scripts/audit_outputs.py outputs.jsonl --expect-think-close > output-audit.json
```

只有输出协议要求 `</think>` 时才使用 `--expect-think-close`。工具报告启发式异常候选、长度限制线索和用户提供的正确性标签，不自行判断答案对错。报告不包含生成文本，但保留 ID 和元数据。详见 [探针适用范围与限制](skills/pd-disaggregation-accuracy-debug/references/quick-probes.md)。

## 验证本仓库

```bash
python3 scripts/validate.py
```

检查内容包括包结构、frontmatter、本地链接、独立分发边界、共享引用一致性和输出审计回归测试。无需模型、Torch、NPU、网络或用户特定的 skill 校验器。

这些检查不能证明具体模型、connector 或硬件组合的正确性。运行时支持和精度结论需要独立、带版本信息的证据。维护要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。

[2026-10-21 源码审计报告](docs/source-audit.md) 记录了核对的 vLLM/Ascend commit、源码依据、修正的假设和人工流程检查案例，并明确区分静态审查与尚未执行的设备和服务验证。

## 许可证

采用 [MIT](LICENSE) 许可证，每个可独立分发的 skill 目录包含相同许可证。所引用的上游文档保留原有许可证，本仓库不打包这些文档。
