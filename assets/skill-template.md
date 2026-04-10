---
name: [skill-name-in-lowercase-with-hyphens]
description: [50-100 词的高度凝练描述。明确说明：1) 解决什么问题 2) 何时触发 3) 预期输出]
metadata:
  pattern: [tool-wrapper|generator|reviewer|inversion|pipeline|composite]
  components: [仅 composite 模式需要，列出组合的模式]
  depends_on:
    references: [需要加载的外部规范文件]
    assets: [需要加载的模板文件]
    scripts: [需要执行的脚本]
---

# 角色定义

[定义此技能下 Agent 的角色定位和总体目标。字数控制在 500 词以内。]

## 外部资源引用

> 按需加载外部文件，遵循渐进式披露原则：

| 目录 | 用途 | 加载时机 |
|------|------|----------|
| `references/[文件名].md` | 规范/知识/检查清单 | 处理相关任务时动态加载 |
| `assets/[文件名].md` | 输出模板/格式定义 | 生成输出前加载 |
| `scripts/[脚本名]` | 自动化工具 | 需要执行时加载 |

---

## 执行流程

[根据选择的模式，使用以下对应的模板骨架]

---

# 模式骨架参考

## Pattern: Tool Wrapper

```markdown
## 规范加载

Load `references/[conventions].md` for [specific domain] best practices.

## 应用场景

### When Reviewing Code
1. Load the conventions reference
2. Check the user's code against each convention
3. For each violation, cite the specific rule and suggest the fix

### When Writing Code
1. Load the conventions reference
2. Follow every convention exactly
3. [Pattern-specific instructions]
```

**必需文件**:
- `references/[conventions].md` — 完整规范文档

---

## Pattern: Generator

```markdown
## 执行步骤

Step 1: Load `references/style-guide.md` for tone and formatting rules.

Step 2: Load `assets/[template].md` for the required output structure.

Step 3: Ask the user for any missing information needed to fill the template:
- [Variable 1]
- [Variable 2]
- [Variable 3]

Step 4: Fill the template following the style guide rules. Every section in the template must be present in the output.

Step 5: Return the completed document.
```

**必需文件**:
- `assets/[template].md` — 输出模板
- `references/style-guide.md` — 格式规范（可选）

---

## Pattern: Reviewer

```markdown
## 审查协议

Step 1: Load `references/review-checklist.md` for the complete review criteria.

Step 2: Read the user's code/output carefully. Understand its purpose before critiquing.

Step 3: Apply each rule from the checklist. For every violation found:
- Note the location (file:line or section)
- Classify severity: error (must fix) | warning (should fix) | info (consider)
- Explain WHY it's a problem, not just WHAT is wrong
- Suggest a specific fix

Step 4: Produce a structured review:
- **Summary**: Overall assessment
- **Findings**: Grouped by severity (errors → warnings → info)
- **Score**: Rate with justification
- **Top Recommendations**: Most impactful improvements
```

**必需文件**:
- `references/review-checklist.md` — 检查清单

**严重程度分级**:
- `error`: 必须修复
- `warning`: 应该修复
- `info`: 建议考虑

---

## Pattern: Inversion

```markdown
## 面试流程

You are conducting a structured requirements interview. DO NOT start [building/designing/executing] until all phases are complete.

## Phase 1 — [Phase Name] (ask one question at a time, wait for each answer)

Ask these questions in order. Do not skip any.

- Q1: "[Question 1]"
- Q2: "[Question 2]"
- Q3: "[Question 3]"

## Phase 2 — [Phase Name] (only after Phase 1 is fully answered)

- Q4: "[Question 4]"
- Q5: "[Question 5]"

## Phase 3 — Synthesis (only after all questions are answered)

1. Load `assets/[template].md` for the output format
2. Fill in every section using the gathered information
3. Present the result to the user
4. Ask: "Does this accurately capture your requirements? What would you change?"
5. Iterate on feedback until the user confirms
```

**关键要素**:
- 明确的 "DO NOT...until..." 门控指令
- 阶段顺序执行
- 逐个问题等待回答

---

## Pattern: Pipeline

```markdown
## 执行流水线

Execute each step in order. Do NOT skip steps or proceed if a step fails.

## Step 1 — [Step Name]
[Step 1 description and actions]

## Step 2 — [Step Name]
[Step 2 description and actions]

**[硬性检查点]**: [描述必须完成的条件]。等待用户确认后进入 Step 3。

## Step 3 — [Step Name]
[Step 3 description and actions]

## Step 4 — [Step Name]
[Step 4 description and actions]
```

**硬性检查点语法**:
```markdown
**[硬性检查点]**: [条件描述]。等待用户确认后进入 [下一阶段]。
```

**流水线设计原则**:
1. 每个步骤编号明确
2. 关键节点使用硬性检查点
3. 说明步骤失败时的处理方式

---

## Pattern: Composite

组合多个模式时，在 metadata 中声明 components：

```yaml
metadata:
  pattern: composite
  components:
    - inversion    # Phase 1-2: 收集需求
    - generator    # Phase 3: 生成输出
    - reviewer     # Phase 4: 质量检查
```

```markdown
## Phase 1 — Requirements (Inversion Pattern)
[Inversion 模式指令...]

**[硬性检查点]**: 等待用户确认需求完整。

## Phase 2 — Generate (Generator Pattern)
[Generator 模式指令...]

## Phase 3 — Review (Reviewer Pattern)
[Reviewer 模式指令...]
```

---

## 边界约束

- [绝对禁止做的事项 1]
- [绝对禁止做的事项 2]
- [其他硬性约束]

---

## 示例调用

```
用户: [触发该技能的典型提示词示例]
```

---

## 完整示例

参见 `references/pattern-examples/` 目录中的完整可运行示例。