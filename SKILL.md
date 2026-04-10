---
name: skill-crafter
description: 创建新技能、修改和改进现有技能，并测量技能性能。触发短语：创建技能/写一个新skill、改进/优化技能、测试/评估技能、基准测试技能性能、优化技能描述。支持 Claude Code、OpenCode 和 OpenClaw 平台。
metadata:
  pattern: composite
  components:
    - generator
    - reviewer
    - pipeline
  depends_on:
    references:
      - adk-patterns.md
      - schemas.md
      - review-checklist.md
    assets:
      - skill-template.md
      - eval_review.html
    scripts:
      - run_eval_opencode.py
      - package_skill.py
      - aggregate_benchmark.py
---

# Skill Crafter

一个跨平台的技能创建和迭代改进工具。

## 平台支持

本技能支持多个 AI 助手平台：

| 平台 | 支持功能 |
|------|----------|
| Claude Code | 完整支持（CLI 评估、浏览器查看器） |
| OpenCode | 核心功能（Task 工具用于评估、静态查看器） |
| OpenClaw | 核心功能（Task 工具用于评估、静态查看器） |

技能会自动检测你的平台并调整行为。

---

## 高层工作流

1. **确定**技能应该做什么以及大致如何实现
2. **编写**技能（SKILL.md + 打包资源）
3. **测试**使用真实提示词
4. **评估**输出（定性和定量）
5. **改进**基于反馈
6. **重复**直到满意

---

## 创建技能

### Step 1: 捕获意图

理解用户想要什么。如果存在上下文，从对话历史中提取。

**关键问题：**
1. 这个技能应该实现什么功能？
2. 何时应该触发？（用户短语/上下文）
3. 预期的输出格式是什么？
4. 是否需要设置测试用例？（有可验证输出的技能适合测试）
5. **哪种设计模式最合适？**（参见 `references/adk-patterns.md`）

**设计模式选择：**

加载 `references/adk-patterns.md` 查看完整模式指南。快速参考：

| 模式 | 适用场景 |
|------|----------|
| Tool Wrapper | Agent 需要按需获取库/框架的专业知识 |
| Generator | 需要从模板生成一致的输出结构 |
| Reviewer | 系统性的代码/输出质量检查 |
| Inversion | 必须在行动前收集需求 |
| Pipeline | 带有硬性检查点的多步骤工作流 |
| Composite | 上述模式的组合 |

### Step 2: 访谈和研究

询问边界情况、输入/输出格式、成功标准、依赖关系。

**模式针对性问题：**

根据 Step 1 选择的设计模式，提出针对性问题：

**Tool Wrapper:**
- 哪些规范/文档需要外部化到 `references/`？
- Agent 应该何时加载这些上下文？（触发时、首次使用时等）

**Generator:**
- 需要什么输出模板？→ 创建 `assets/template.md`
- 应用什么格式规则？→ 创建 `references/style-guide.md`
- 必须从用户收集哪些变量？

**Reviewer:**
- 应该检查哪些维度？（质量、安全、性能）
- 如何分类严重程度？（error/warning/info 阈值）
- `references/review-checklist.md` 应包含哪些检查项？

**Inversion:**
- 必须在行动前收集什么信息？
- 分几个阶段？每个阶段有哪些问题？
- 需要什么明确的"DO NOT proceed until..."门控？

**Pipeline:**
- 有哪些编号步骤？
- 硬性检查点应该放在哪里？使用：`**[硬性检查点]**: 条件`
- 如果某步骤失败会发生什么？

**Composite:**
- 组合了哪些模式？
- 它们之间如何过渡？

如果有用，检查可用的 MCP 进行研究。

### Step 3: 编写 SKILL.md

基于访谈，填写：

- **name**: 技能标识符（仅小写、数字、连字符）
- **description**: 何时触发 + 做什么。包含具体上下文。
- **metadata.pattern**: 声明设计模式（tool-wrapper、generator、reviewer、inversion、pipeline、composite）
- **metadata.depends_on**: 列出所需的 references/assets/scripts
- **body**: 遵循模式骨架的详细指令

#### 使用模式骨架

加载 `assets/skill-template.md` 获取模式特定的骨架。每种模式有预定义结构：

```
# Tool Wrapper → 聚焦于引用加载 + 应用规则
# Generator   → 逐步模板填充流程
# Reviewer    → 检查清单加载 + 严重程度分组输出
# Inversion   → 阶段门控的面试流程
# Pipeline    → 带硬性检查点的编号步骤
# Composite   → 声明组件 + 组合模式
```

#### 技能结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter (name、description、metadata.pattern 必需)
│   └── Markdown 指令（模式骨架）
└── 打包资源（模式依赖）
    ├── scripts/    - 可执行代码
    ├── references/ - 按需加载的文档（Tool Wrapper、Reviewer）
    └── assets/     - 模板（Generator、Inversion、Pipeline）
```

#### 渐进式披露

技能使用三层加载系统：
1. **元数据**（name + description）- 始终在上下文中
2. **SKILL.md 正文**- 技能触发时在上下文中
3. **打包资源**- 按需加载

**关键模式：**
- 保持 SKILL.md 少于 500 行
- 从 SKILL.md 清晰引用文件
- 对于大文件（>300 行），包含目录
- **绝不将长规范内联在 SKILL.md 中** → 移到 `references/`

### Step 4: 测试用例

创建 2-3 个真实的测试提示词。保存到 `evals/evals.json`：

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的任务提示词",
      "expected_output": "预期结果的描述",
      "files": []
    }
  ]
}
```

---

## 运行测试用例

本节是一个连续序列。

### Claude Code

使用 subprocess 运行加载了技能的 `claude -p`。

### OpenCode/OpenClaw

使用 Task 工具启动子代理。工作流程：

1. 读取 `scripts/run_eval_opencode.py` 获取设置说明
2. 为每个测试使用 Task 工具，设置 `subagent_type="general"`
3. 检查子代理输出中的技能使用情况

### Step 1: 启动运行

为每个测试用例启动子代理：

**带技能运行：**
```
Task: 使用 <skill-path> 的技能执行
Prompt: <eval 提示词>
输出保存到: <workspace>/iteration-N/eval-ID/with_skill/outputs/
```

**基线运行（不带技能或旧版本）：**
```
Task: 不带技能执行（或使用旧技能版本）
Prompt: <eval 提示词>
输出保存到: <workspace>/iteration-N/eval-ID/without_skill/outputs/
```

为每个测试创建 `eval_metadata.json`：

```json
{
  "eval_id": 0,
  "eval_name": "描述性名称",
  "prompt": "任务提示词",
  "assertions": []
}
```

### Step 2: 编写断言

在运行执行期间，编写量化断言。好的断言：
- 可客观验证
- 描述性命名
- 在基准查看器中清晰

### Step 3: 捕获计时

当 Task 完成时，保存计时数据：

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### Step 4: 评分并启动查看器

1. **评分每个运行** - 使用评分子代理或内联
2. **聚合为基准** - 运行：
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
3. **启动查看器**：
   ```bash
   # Claude Code（浏览器）
   python eval-viewer/generate_review.py <workspace>/iteration-N --skill-name "my-skill"
   
   # OpenCode/OpenClaw（静态 HTML）
   python eval-viewer/generate_review.py <workspace>/iteration-N --skill-name "my-skill" --static <output.html>
   ```

### Step 5: 读取反馈

完成后，读取 `feedback.json`：

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "评论内容"}
  ],
  "status": "complete"
}
```

---

## 改进技能

### 如何思考改进

1. **从反馈中泛化** - 不要过度拟合测试用例
2. **保持精简** - 移除不起作用的内容
3. **解释原因** - 帮助模型理解推理
4. **寻找重复工作** - 打包常见辅助脚本

### 迭代循环

1. 应用改进
2. 重新运行所有测试用例（新的 `iteration-N+1/` 目录）
3. 使用 `--previous-workspace` 启动查看器
4. 等待反馈
5. 重复直到满意

---

## 描述优化

**仅 Claude Code** - 优化技能描述以提高触发准确性。

### Step 1: 生成触发评估

创建 20 个评估查询（混合应该触发和不应触发）：

```json
[
  {"query": "用户提示词", "should_trigger": true},
  {"query": "另一个提示词", "should_trigger": false}
]
```

### Step 2: 与用户审查

使用 `assets/eval_review.html` 的 HTML 模板。

### Step 3: 运行优化（Claude Code）

```bash
python -m scripts.run_loop \
  --eval-set <trigger-eval.json> \
  --skill-path <skill-path> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

### Step 4: 应用结果

用 `best_description` 更新 SKILL.md frontmatter。

---

## 平台特定说明

### OpenCode/OpenClaw

- **评估运行**: 使用 Task 工具，不是 CLI subprocess
- **查看器**: 使用 `--static` 模式输出 HTML
- **描述优化**: 不可用（需要 CLI 评估）
- **打包**: 使用 `scripts/package_skill.py`

### Claude Code

- **完整功能**: CLI 评估、浏览器查看器、描述优化
- **使用 subprocess** 运行 `claude -p` 命令

---

## 参考文件

- `references/adk-patterns.md` - **设计模式指南，包含示例和决策树**
- `assets/skill-template.md` - **模式特定的骨架模板**
- `references/pattern-examples/` - **每种模式的完整可运行示例**
- `agents/grader.md` - 如何评估断言（包含模式合规检查）
- `agents/comparator.md` - 盲测 A/B 比较
- `agents/analyzer.md` - 分析基准结果
- `references/schemas.md` - JSON 结构

---

## 核心循环（重复）

```
理解意图 → 选择模式 → 编写/编辑技能 → 运行测试 → 评估 → 改进 → 重复 → 打包
```

始终使用 `eval-viewer/generate_review.py` 帮助用户在改进前审查输出。

---

## 模式合规检查

评估技能时，验证它正确遵循其声明的模式。加载 `agents/grader.md` 获取详细合规标准。

**快速检查：**

| 模式 | 必须包含 |
|------|----------|
| Tool Wrapper | 外部 `references/` 文件、动态加载指令 |
| Generator | `assets/template.md`、模板填充步骤 |
| Reviewer | `references/checklist.md`、严重程度分组 |
| Inversion | "DO NOT proceed until..." 门控、顺序提问 |
| Pipeline | 编号步骤、硬性检查点（`**[硬性检查点]**`） |
| Composite | 元数据中声明的组件 |