# `skill.yaml` DSL 初版规范（v3）

## 目标

`skill.yaml` 是 `or-skill-crafter` v3 的统一中间表示。

用途：
- 在“需求分析”和“文件生成”之间插一层可验证结构
- 让 skill 生成、校验、迁移使用同一份语义骨架
- 避免把所有逻辑都揉进主模板

## 顶层结构

```yaml
skill:
intent:
patterns:
flow:
fallback:
output:
boundaries:
```

## 字段说明

### `skill`
描述技能自身元数据。

```yaml
skill:
  name: prd-reviewer
  version: v3
  type: analyzer
  user_invocable: true
```

字段约束：
- `name`：仅允许小写字母、数字、连字符
- `version`：当前推荐 `v3`
- `type`：writer / analyzer / transformer / orchestrator / tool-wrapper / builder
- `user_invocable`：布尔值

### `intent`
描述技能要解决的问题。

```yaml
intent:
  goal: review PRD quality
  primary_input: PRD text
  primary_output: score + issues + suggestions
  constraints:
    - ask clarifying questions when context is missing
```

### `patterns`
列出该技能使用的 pattern。

```yaml
patterns:
  - inversion
  - reviewer
  - generator
```

### `flow`
声明阶段式步骤。

```yaml
flow:
  - id: clarify
    condition: missing_context
    action: ask_questions

  - id: analyze
    references:
      - references/prd-rubric.md
```

字段建议：
- `id`：步骤名
- `condition`：进入条件（可选）
- `action`：主要动作（可选）
- `references`：依赖的规则/知识（可选）
- `assets`：依赖的模板/示例（可选）

### `fallback`
声明失败兜底。

```yaml
fallback:
  insufficient_info: ask_more
  tool_unavailable: manual_mode
  out_of_scope: refuse
```

### `output`
声明输出结构。

```yaml
output:
  format: markdown
  sections:
    - summary
    - issues
    - suggestions
```

### `boundaries`
声明硬性边界。

```yaml
boundaries:
  - do not fabricate missing evidence
  - do not modify external systems without confirmation
```

## 最小可用示例

见：`assets/skill-yaml-example.yaml`

## 设计原则

1. 轻 DSL，不发明复杂语法
2. 先解决表达与校验，不追求华丽抽象
3. DSL 是中间层，不替代 `SKILL.md`
4. 若 pattern 被声明，最终产物中必须能找到相应结构证据
