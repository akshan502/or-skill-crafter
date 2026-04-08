# or-skill-crafter

一个用于生成目录型技能（Directory-Based Skill）的母技能。  
它面向 OpenClaw / ADK 风格工作流，帮助你把“我想做个技能”这件事，收束成一套**可维护、可扩展、可审查**的标准过程。

> 中文为主，英文说明附后。  
> Chinese first, English summary included below.

---

## 这是什么

`or-skill-crafter` 不是普通技能，它是一个**用来创建其他技能的技能**。

它不鼓励把所有规则都塞进一个巨大的 prompt 里，而是通过一套分阶段流水线，帮助你生成更像“工程产物”而不是“提示词堆积物”的目录型技能。

它的目标很明确：

- 让技能更容易维护
- 让技能结构更清晰
- 减少提示词越写越乱的问题
- 让 references / assets / scripts 各归其位
- 在生成前先澄清，在交付前先自检
- 在 v3 中引入 **skill taxonomy + pattern selection + skill.yaml DSL**

---

## 核心理念

### 1）渐进式披露（Progressive Disclosure）
不要把所有约束、模板、说明、检查清单都堆在一个 `SKILL.md` 里。

推荐拆分为三层：

- **第一层：YAML Frontmatter**
  - `name`
  - `description`
- **第二层：SKILL.md 正文**
  - 角色定义
  - 适用/不适用场景
  - Pipeline
  - 边界约束
- **第三层：按需资源**
  - `references/`：规则、知识、方法说明、清单
  - `assets/`：模板、静态资源、示例骨架
  - `scripts/`：自动化脚本
  - `evals/`：评测样例（可选）

### 2）目录型技能优先
一个好的技能应该像一个小型工程目录，而不是一团越滚越大的提示词。

推荐结构如下：

```text
skill-name/
  SKILL.md
  references/
  assets/
  scripts/
  evals/      # 可选
```

### 3）门控优先于冲动执行
技能不应该从“模糊需求”直接一口气冲到“最终产物”。

`or-skill-crafter` 强制采用阶段式推进：

1. 先澄清需求
2. 再规划结构
3. 再生成文件
4. 最后做规范自检

在关键步骤设置 **[硬性检查点]**，要求暂停并等待用户确认。

### 4）运行时数据不属于 skill 本体目录
这是很重要的一条：

- 学习日志
- 用户偏好
- 缓存
- 状态文件
- 执行结果

这些都**不应写回 skill 目录**。  
`references/` 只该放静态知识与模板，不该混进运行时数据。

---

## 它能帮你做什么

使用 `or-skill-crafter`，你可以得到一套更规范的技能生成流程：

- 帮你先问对问题，而不是上来就瞎写
- 帮你规划 skill 目录结构
- 帮你生成 `SKILL.md` 草案
- 帮你生成配套的 `references/` / `assets/` 文件草案
- 在交付前按 checklist 做自检

适合这些场景：

- 你要批量构建技能
- 你希望技能目录结构统一
- 你不想再维护那种一眼看不完的大 prompt
- 你想把技能做成可持续迭代的工程资产

---

## 生成出来的技能应具备什么

一个由 `or-skill-crafter` 生成的技能，通常应该至少包含：

- 明确的角色定义
- 明确的适用场景
- 明确的不适用场景
- 清晰的执行步骤（Pipeline）
- 必要的硬性检查点
- 输入不足时的补问机制
- 失败兜底方案
- 输出要求
- 边界约束

同时，应尽量避免：

- 非法 YAML 字段
- 不规范命名
- 过于臃肿的单文件 prompt
- 把运行时状态写回 skill 目录
- 写死某个特定环境工具名（除非该技能本来就是环境专属）

---

## 仓库内容

当前目录包含：

- `SKILL.md`  
  主技能说明，定义 `or-skill-crafter` 自身的工作方式

- `assets/skill-template.md`  
  技能生成模板

- `references/adk-patterns.md`  
  技能设计规范与目录分层原则

- `references/review-checklist.md`  
  最终输出前的自检清单

- `scripts/init_workspace.py`  
  初始化新技能目录骨架的辅助脚本

- `evals/evals.json`  
  最小评测样例，用于校验该母技能是否按预期工作

---

## 快速开始

### 方式一：作为技能使用

1. 将 `or-skill-crafter` 放入你的 skills 目录
2. 调用 `or-skill-crafter`
3. 描述你想创建的技能要解决什么问题
4. 回答它提出的澄清问题
5. 确认目录规划方案
6. 获取生成的 `SKILL.md` 与配套文件草案
7. 在最终交付前查看 review checklist

### 方式二：先初始化目录骨架

如果你已经知道要创建新技能，也可以先执行初始化脚本：

```bash
python scripts/init_workspace.py "your-skill-name"
```

它会：

- 规范化技能名
- 创建：
  - `scripts/`
  - `references/`
  - `assets/`
- 在缺失时创建基础 `SKILL.md`

`evals/` 默认不强制创建，按需添加。

---

## 一个最小示例

假设你想做一个“自动生成 PRD 的技能”。

`or-skill-crafter` 不会直接上来就生成一堆文件，而是会先问你：

1. 这个技能要解决什么痛点？
2. 用户如何调用它？
3. 有哪些不能违反的边界？

接着，它会帮你规划：

- `references/` 里放 PRD 规范、检查清单
- `assets/` 里放 PRD 模板
- `scripts/` 是否需要辅助脚本
- 是否需要 `evals/` 做回归校验

然后再生成正式 skill。

这就是它和“直接写一个 prompt”的区别。

---

## 为什么要做这个项目

因为很多技能写着写着，就会变成三种东西的混合体：

- 角色设定
- 业务规则
- 输出模板
- 脚本说明
- 历史补丁

最后没人敢动，也没人愿意看。

`or-skill-crafter` 想解决的，就是这个问题：

> 让技能重新像技能，而不是像一堆缠在一起的临时补丁。

---

## 设计哲学

一个好的技能，应该像一把小而利的工具。

不是越长越强，
不是越复杂越专业，
而是：

- 结构清楚
- 边界明确
- 依赖分层
- 默认安全
- 长期可维护

如果一个技能必须靠不断往主 prompt 上打补丁才能活，那它迟早会烂掉。

---

## v3 设计方向

`or-skill-crafter` 正在从“模板器”升级为 **Pattern-aware Skill Compiler**。

v3 首批重点包括：

- **Skill taxonomy**：先判断 skill 类型，再决定生成策略
- **Pattern selection**：显式选择 inversion / generator / reviewer / pipeline / tool-wrapper
- **`skill.yaml` DSL**：在需求分析与文件生成之间加入统一中间表示
- **目录职责清晰化**：把规则、模板、脚本、评测进一步拆清
- **validator / migration 预留**：为后续结构校验、语义校验、旧 skill 迁移打基础

当前仓库已补入的 v3 基础文件：

- `references/skill-taxonomy.md`
- `references/pattern-selection.md`
- `references/v3-roadmap.md`
- `references/dsl-to-artifacts-mapping.md`
- `references/migration-to-compile-workflow.md`
- `references/compile-merge-guide.md`
- `dsl-skill-schema.md`
- `assets/skill-yaml-example.yaml`
- `assets/file-responsibility-template.md`
- `assets/migration-report-template.md`
- `assets/templates/writer-skill-template.md`
- `assets/templates/analyzer-skill-template.md`
- `assets/templates/tool-wrapper-skill-template.md`
- `assets/templates/transformer-skill-template.md`
- `assets/templates/orchestrator-skill-template.md`
- `assets/templates/builder-skill-template.md`
- `validators/structure.py`
- `validators/semantics.py`
- `validators/patterns.py`
- `migrations/legacy-to-v3-plan.md`
- `scripts/migrate_skill.py`
- `scripts/compile_skill.py`
- `evals/v3-evals.json`
- `evals/compile-evals.json`

## 项目状态

当前仓库处于 **v2 → v3 迁移期**。

已经具备：

- 目录型技能生成
- 渐进式披露
- 门控式流水线
- 更严格的自检机制
- 初步的 v3 taxonomy / pattern / DSL 基础

后续仍需继续完善：

- validator 深化（更多规则与 smoke test）
- compile 链路从“生成草案 + 推荐文件 + stub 文件”走向“正式生成目录产物”
- migration（从报告 + `skill.yaml.draft` 走向自动拆分建议）
- 更强的评测样例
- tool-wrapper 类型的更细契约模板
- compile 结果与现有 `SKILL.md` 的差异比对机制
- compile 输出的 references/assets 内容继续细化到业务级模板

阶段总结见：`final-status-v3-alpha.md`

---

## 文件职责表（v3）

### 根目录
- `SKILL.md`：主行为定义，保持精简，只放角色、适用范围、Pipeline、门控、边界。
- `skill.yaml`：统一的中间表示（DSL），供生成、校验、迁移使用。
- `CHANGELOG.md`：版本变更记录。

### `references/`
放规则、知识、rubric、checklist、方法说明。

### `assets/`
放输出模板、示例骨架、few-shot 示例、格式模板。

### `scripts/`
放初始化、验证、迁移等辅助自动化脚本。

目前已有：
- `scripts/init_workspace.py`
- `scripts/validate_skill.py`
- `scripts/migrate_skill.py`
- `scripts/compile_skill.py`

### `evals/`
放行为样例、对抗样例、回归样例。

### 不该放进 skill 目录的内容
- 日志
- 缓存
- 用户偏好
- 临时状态
- 执行结果

这些应放到独立数据目录，而不是 skill 本体目录。

## `skill.yaml` DSL 初版示例

```yaml
skill:
  name: prd-reviewer
  version: v3
  type: analyzer
  user_invocable: true

intent:
  goal: review PRD quality and provide actionable feedback
  primary_input: PRD text or document content
  primary_output: score, issues, and revision suggestions
  constraints:
    - ask clarifying questions when context is insufficient

patterns:
  - inversion
  - reviewer
  - generator
  - pipeline

flow:
  - id: clarify
    condition: missing_context
    action: ask_questions

  - id: analyze
    references:
      - references/prd-rubric.md

  - id: score
    assets:
      - assets/score-template.md

fallback:
  insufficient_info: ask_more
  tool_unavailable: manual_mode
  out_of_scope: refuse

output:
  format: markdown
  sections:
    - summary
    - issues
    - suggestions

boundaries:
  - do not fabricate missing product context
  - do not write runtime data back into the skill directory
```

完整说明见：`dsl-skill-schema.md`

补充映射规则见：`references/dsl-to-artifacts-mapping.md`

当前已经有一个最小编译骨架：`scripts/compile_skill.py`
- 读取 `skill.yaml`
- 根据 `skill.type` 选择模板
- 吃入 `intent / flow / fallback / boundaries / output.sections`
- 生成 `compile-plan.md`
- 生成 `SKILL.generated.md`
- 生成 `references/recommended-files.md`
- 生成 `assets/recommended-files.md`
- 按 pattern / type 生成一批 `references/*.md` 与 `assets/*.md` 草案
- 生成 `compile-review.md` 作为收敛与人工确认说明

## English Summary

`or-skill-crafter` is a meta-skill for generating directory-based skills in an OpenClaw / ADK-style workflow.

Instead of encouraging one giant prompt, it helps structure a skill into:

- `SKILL.md`
- `references/`
- `assets/`
- `scripts/`
- `evals/` (optional)

It enforces a staged workflow:

1. clarify the use case
2. plan the directory structure
3. generate the skill files
4. review the result before delivery

Its main design goals are:

- cleaner skill structure
- progressive disclosure
- safer defaults
- explicit boundaries
- easier long-term maintenance

It also treats runtime data carefully:
logs, preferences, cache, and state files should not be written back into the skill directory.

If you are building lots of skills and want them to stay readable, reviewable, and reusable, this project is for you.

---

## License

请在此处补充你的开源许可证，例如 MIT / Apache-2.0 / GPL-3.0。
