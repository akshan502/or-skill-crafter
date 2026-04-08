# DSL → Artifacts Mapping (v3)

本文件定义 `skill.yaml` 如何映射为目录型 skill 产物。

## 1. `skill.type` → 模板选择

- `writer` → `assets/templates/writer-skill-template.md`
- `analyzer` → `assets/templates/analyzer-skill-template.md`
- `tool-wrapper` → `assets/templates/tool-wrapper-skill-template.md`
- `transformer` → 暂按 writer 模板降级，并在交付中说明
- `orchestrator` → 暂按 analyzer + pipeline 结构降级，并在交付中说明
- `builder` → 暂按 analyzer 模板降级，并在交付中说明

## 2. `intent` → 主体目标表达

`intent.goal`、`intent.primary_input`、`intent.primary_output` 应映射到：
- `SKILL.md` 的角色定义
- 适用场景
- 输出要求

## 3. `patterns` → 必要结构证据

若声明以下 pattern，则最终产物必须包含对应结构：

- `inversion` → 澄清问题 / 输入不足先补问 / 明确暂停条件
- `generator` → 输出模板 / 输出结构 / 格式要求
- `reviewer` → checklist / rubric / review step
- `pipeline` → 显式 Step 划分 / 硬性检查点
- `tool-wrapper` → 输入参数 / 输出结果 / 权限边界 / 失败处理

## 4. `flow` → Pipeline 章节

`flow` 中每个 step 应映射为 `SKILL.md` 中的一个步骤描述，至少体现：
- step id
- 进入条件（若有）
- 主要动作
- 所依赖的 references / assets

## 5. `fallback` → 失败兜底

`fallback` 中的键值对必须映射为 `SKILL.md` 的失败兜底段落，不得遗漏。

## 6. `output` → 输出要求

`output.format` 与 `output.sections` 必须映射为输出格式与章节要求。

## 7. `boundaries` → 边界约束

`boundaries` 中的每一条都应体现在 `SKILL.md` 的硬性约束中。

## 8. `references/` / `assets/` / `scripts/` / `evals/`

若 DSL 或 flow 中引用到外部文件，则目录规划与交付时必须显式列出：
- 哪些文件属于 `references/`
- 哪些文件属于 `assets/`
- 哪些文件属于 `scripts/`
- 是否需要 `evals/`

## 9. 降级策略

当某 skill type 尚无专门模板时：
- 必须明确告知用户“当前使用降级模板”
- 不得假装已有完整模板支持
- 应在后续建议中指出该类型值得补充专门模板
