# Agent Skill 设计模式指南

当设计一个新技能时，选择合适的设计模式是关键。以下是五种核心设计模式及其使用指南。

---

## 核心设计模式概览

| 模式 | 核心问题 | 典型场景 |
|------|----------|----------|
| Tool Wrapper | "如何让 Agent 成为某库的专家？" | 框架规范、内部编码标准 |
| Generator | "如何保证输出结构一致？" | 文档生成、代码脚手架 |
| Reviewer | "如何系统性检查代码质量？" | PR 审查、安全审计 |
| Inversion | "如何确保收集完整需求？" | 项目规划、需求分析 |
| Pipeline | "如何防止步骤被跳过？" | 多阶段工作流、部署流程 |

---

## 模式 1: Tool Wrapper（工具封装）

### 核心理念

Tool Wrapper 让你的 Agent 按需获取特定库的上下文。不需要将 API 规范硬编码进系统提示词，而是打包成技能——Agent 只在真正使用该技术时才加载这些上下文。

### 关键特征

- **按需加载**: 规范存储在 `references/`，仅在需要时加载
- **单一职责**: 一个技能对应一个技术领域
- **规范即真理**: 外部文档是绝对权威

### 示例结构

```
skills/api-expert/
├── SKILL.md              # 路由指令，<100 行
└── references/
    └── conventions.md    # FastAPI 完整规范，500+ 行
```

### SKILL.md 模板

```markdown
---
name: api-expert
description: FastAPI development best practices and conventions. Use when building, reviewing, or debugging FastAPI applications, REST APIs, or Pydantic models.
metadata:
  pattern: tool-wrapper
  domain: fastapi
---

You are an expert in FastAPI development. Apply these conventions to the user's code or question.

## Core Conventions

Load 'references/conventions.md' for the complete list of FastAPI best practices.

## When Reviewing Code
1. Load the conventions reference
2. Check the user's code against each convention
3. For each violation, cite the specific rule and suggest the fix

## When Writing Code
1. Load the conventions reference
2. Follow every convention exactly
3. Add type annotations to all function signatures
4. Use Annotated style for dependency injection
```

### 适用场景

- 团队内部编码规范分发
- 特定框架最佳实践（React、FastAPI、Spring 等）
- 安全漏洞检查规则（OWASP Top 10）
- 代码风格指南（Google Style、Airbnb Style）

---

## 模式 2: Generator（生成器）

### 核心理念

Generator 通过"填空"流程确保输出结构一致。如果你发现 Agent 每次生成的文档结构都不同，Generator 可以解决这个问题。

### 关键特征

- **模板驱动**: 输出模板存储在 `assets/`
- **风格分离**: 格式规则存储在 `references/`
- **变量收集**: 主动询问缺失信息

### 示例结构

```
skills/report-generator/
├── SKILL.md                  # 编排指令
├── assets/
│   └── report-template.md    # 输出模板
└── references/
    └── style-guide.md        # 格式规范
```

### SKILL.md 模板

```markdown
---
name: report-generator
description: Generates structured technical reports in Markdown. Use when the user asks to write, create, or draft a report, summary, or analysis document.
metadata:
  pattern: generator
  output-format: markdown
---

You are a technical report generator. Follow these steps exactly:

Step 1: Load 'references/style-guide.md' for tone and formatting rules.

Step 2: Load 'assets/report-template.md' for the required output structure.

Step 3: Ask the user for any missing information needed to fill the template:
- Topic or subject
- Key findings or data points
- Target audience (technical, executive, general)

Step 4: Fill the template following the style guide rules. Every section in the template must be present in the output.

Step 5: Return the completed report as a single Markdown document.
```

### 适用场景

- API 文档生成
- 提交消息规范化
- 项目架构脚手架
- 配置文件模板

---

## 模式 3: Reviewer（审查器）

### 核心理念

Reviewer 分离"检查什么"和"如何检查"。检查清单存储在 `references/review-checklist.md`，Agent 动态加载并按严重程度分组输出。

### 关键特征

- **检查清单模块化**: 替换检查清单即可改变审查领域
- **严重程度分级**: error/warning/info 三级分类
- **结构化输出**: 统一的审查报告格式

### 示例结构

```
skills/code-reviewer/
├── SKILL.md                     # 审查协议
└── references/
    └── review-checklist.md      # 检查清单
```

### SKILL.md 模板

```markdown
---
name: code-reviewer
description: Reviews Python code for quality, style, and common bugs. Use when the user submits code for review, asks for feedback on their code, or wants a code audit.
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

You are a Python code reviewer. Follow this review protocol exactly:

Step 1: Load 'references/review-checklist.md' for the complete review criteria.

Step 2: Read the user's code carefully. Understand its purpose before critiquing.

Step 3: Apply each rule from the checklist to the code. For every violation found:
- Note the line number (or approximate location)
- Classify severity: error (must fix), warning (should fix), info (consider)
- Explain WHY it's a problem, not just WHAT is wrong
- Suggest a specific fix with corrected code

Step 4: Produce a structured review with these sections:
- **Summary**: What the code does, overall quality assessment
- **Findings**: Grouped by severity (errors first, then warnings, then info)
- **Score**: Rate 1-10 with brief justification
- **Top 3 Recommendations**: The most impactful improvements
```

### 适用场景

- PR 代码审查自动化
- 安全漏洞扫描
- 性能检查清单
- 代码质量审计

---

## 模式 4: Inversion（反转）

### 核心理念

Agent 的本能是"立即生成"。Inversion 反转这个动态：Agent 作为面试官，先收集信息再行动。

### 关键特征

- **门控指令**: 明确的 "DO NOT...until..." 约束
- **顺序提问**: 一次一个问题，等待回答
- **阶段划分**: 明确的 Phase 1/Phase 2/Phase 3

### 示例结构

```
skills/project-planner/
├── SKILL.md               # 多阶段面试流程
└── assets/
    └── plan-template.md   # 最终输出模板
```

### SKILL.md 模板

```markdown
---
name: project-planner
description: Plans a new software project by gathering requirements through structured questions before producing a plan. Use when the user says "I want to build", "help me plan", "design a system", or "start a new project".
metadata:
  pattern: inversion
  interaction: multi-turn
---

You are conducting a structured requirements interview. DO NOT start building or designing until all phases are complete.

## Phase 1 — Problem Discovery (ask one question at a time, wait for each answer)

Ask these questions in order. Do not skip any.

- Q1: "What problem does this project solve for its users?"
- Q2: "Who are the primary users? What is their technical level?"
- Q3: "What is the expected scale? (users per day, data volume, request rate)"

## Phase 2 — Technical Constraints (only after Phase 1 is fully answered)

- Q4: "What deployment environment will you use?"
- Q5: "Do you have any technology stack requirements or preferences?"
- Q6: "What are the non-negotiable requirements? (latency, uptime, compliance, budget)"

## Phase 3 — Synthesis (only after all questions are answered)

1. Load 'assets/plan-template.md' for the output format
2. Fill in every section of the template using the gathered requirements
3. Present the completed plan to the user
4. Ask: "Does this plan accurately capture your requirements? What would you change?"
5. Iterate on feedback until the user confirms
```

### 适用场景

- 项目需求收集
- 系统架构设计
- 产品规划
- 技术选型咨询

---

## 模式 5: Pipeline（流水线）

### 核心理念

对于复杂任务，不能容忍步骤被跳过。Pipeline 通过明确的硬性检查点强制顺序执行。

### 关键特征

- **显式步骤编号**: Step 1, Step 2, Step 3...
- **硬性检查点**: `**[硬性检查点]**: 等待用户确认后进入下一阶段`
- **失败处理**: 明确说明某步骤失败时的行为

### 示例结构

```
skills/doc-pipeline/
├── SKILL.md                      # 流水线定义
├── assets/
│   └── api-doc-template.md       # 输出模板
└── references/
    ├── docstring-style.md        # 文档字符串格式
    └── quality-checklist.md      # 质量检查清单
```

### SKILL.md 模板

```markdown
---
name: doc-pipeline
description: Generates API documentation from Python source code through a multi-step pipeline. Use when the user asks to document a module, generate API docs, or create documentation from code.
metadata:
  pattern: pipeline
  steps: "4"
---

You are running a documentation generation pipeline. Execute each step in order. Do NOT skip steps or proceed if a step fails.

## Step 1 — Parse & Inventory
Analyze the user's Python code to extract all public classes, functions, and constants. Present the inventory as a checklist. Ask: "Is this the complete public API you want documented?"

## Step 2 — Generate Docstrings
For each function lacking a docstring:
- Load 'references/docstring-style.md' for the required format
- Generate a docstring following the style guide exactly
- Present each generated docstring for user approval

**[硬性检查点]**: 等待用户确认所有 docstring 后，再进入 Step 3。

## Step 3 — Assemble Documentation
Load 'assets/api-doc-template.md' for the output structure. Compile all classes, functions, and docstrings into a single API reference document.

## Step 4 — Quality Check
Review against 'references/quality-checklist.md':
- Every public symbol documented
- Every parameter has a type and description
- At least one usage example per function

Report results. Fix issues before presenting the final document.
```

### 硬性检查点语法

使用以下格式标记必须等待用户确认的检查点：

```markdown
**[硬性检查点]**: 描述必须完成的条件。等待用户确认后进入下一阶段。
```

### 适用场景

- 代码文档生成
- 多阶段部署流程
- 数据处理流水线
- 自动化测试流程

---

## 模式选择决策树

```
用户需要什么？
│
├─ "让 Agent 了解某个库/框架的规范"
│   └─ → Tool Wrapper
│
├─ "生成结构一致的文档/代码"
│   └─ → Generator
│
├─ "审查代码/输出质量"
│   └─ → Reviewer
│
├─ "规划项目/收集需求"
│   └─ → Inversion
│
├─ "执行多步骤工作流"
│   ├─ 步骤可跳过？
│   │   ├─ 否 → Pipeline
│   │   └─ 是 → 考虑组合模式
│   │
│   └─ 需要人工确认？
│       ├─ 是 → Pipeline + 硬性检查点
│       └─ 否 → Pipeline（自动执行）
│
└─ "复杂场景"
    └─ → 组合模式（见下文）
```

---

## 组合模式

这些模式可以组合使用。以下是常见组合：

### 组合 1: Pipeline + Reviewer

**场景**: 文档生成后自动审查质量

```yaml
metadata:
  pattern: composite
  components:
    - pipeline
    - reviewer
```

```markdown
## Step 3 — Generate Documentation
...生成文档...

**[硬性检查点]**: 文档生成完成，准备质量审查。

## Step 4 — Quality Review
Load 'references/quality-checklist.md' and apply Reviewer pattern:
- Check every section against the checklist
- Report severity-based findings
- Do NOT proceed to Step 5 if any errors found
```

### 组合 2: Inversion + Generator

**场景**: 收集需求后生成架构图

```yaml
metadata:
  pattern: composite
  components:
    - inversion
    - generator
```

```markdown
## Phase 1 — Requirements Gathering (Inversion)
...收集需求...

## Phase 2 — Generate Architecture (Generator)
1. Load 'assets/architecture-template.md'
2. Fill template with gathered requirements
3. Ask user to confirm or iterate
```

### 组合 3: Tool Wrapper + Reviewer

**场景**: 按特定框架规范审查代码

```yaml
metadata:
  pattern: composite
  components:
    - tool-wrapper
    - reviewer
```

```markdown
## When Reviewing Code
1. Load 'references/react-conventions.md' (Tool Wrapper)
2. Load 'references/security-checklist.md' (Reviewer)
3. Apply both rule sets to the code
4. Group findings: convention violations vs security issues
```

---

## 渐进式披露原则

无论使用哪种模式，都应遵循渐进式披露原则：

### 三层加载机制

```
┌─────────────────────────────────────────────────────────────┐
│ 第一层: 元数据 (常驻内存)                                      │
│ ─────────────────────────────────────────────────────────────│
│ YAML Frontmatter: name + description                         │
│ 用途: 技能发现与触发                                          │
│ 大小: < 100 词                                                │
└─────────────────────────────────────────────────────────────┘
                            ↓ 触发加载
┌─────────────────────────────────────────────────────────────┐
│ 第二层: 指令 (触发加载)                                       │
│ ─────────────────────────────────────────────────────────────│
│ SKILL.md 正文                                                 │
│ 用途: 角色定义、Pipeline 路由、硬性检查点                      │
│ 大小: < 5000 词                                               │
└─────────────────────────────────────────────────────────────┘
                            ↓ 按需加载
┌─────────────────────────────────────────────────────────────┐
│ 第三层: 资源 (按需挂载)                                       │
│ ─────────────────────────────────────────────────────────────│
│ references/ → 长篇规范、检查清单                              │
│ assets/     → 输出模板、格式定义                              │
│ scripts/    → 可执行脚本                                      │
│ 大小: 无限制                                                  │
└─────────────────────────────────────────────────────────────┘
```

### 关键规则

1. **SKILL.md 保持精简**: 仅作为路由中心，不内嵌长篇规范
2. **外部化长内容**: > 100 行的内容必须放入 `references/` 或 `assets/`
3. **延迟加载**: 使用 "Load 'references/xxx.md' when..." 指令

---

## 完整示例参考

每种模式的完整可运行示例见 `references/pattern-examples/` 目录：

- `tool-wrapper-example.md` — FastAPI 专家技能
- `generator-example.md` — 技术报告生成器
- `reviewer-example.md` — Python 代码审查器
- `inversion-example.md` — 项目规划面试官
- `pipeline-example.md` — API 文档流水线
- `composite-example.md` — Pipeline + Reviewer 组合