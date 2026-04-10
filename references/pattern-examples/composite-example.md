# Composite 模式完整示例

本文档展示 Composite 模式的完整可运行示例：Pipeline + Reviewer 组合。

---

## 技能结构

```
skills/doc-pipeline-reviewed/
├── SKILL.md                      # 组合流水线
├── assets/
│   └── api-doc-template.md       # 输出模板
└── references/
    ├── docstring-style.md        # 文档字符串格式
    ├── review-checklist.md       # 审查清单 (Reviewer 组件)
    └── quality-checklist.md      # 质量检查清单
```

---

## SKILL.md

```markdown
---
name: doc-pipeline-reviewed
description: Generates API documentation through a pipeline with integrated quality review. Use when user wants thoroughly reviewed documentation from Python code. Trigger keywords: document, api docs, reviewed docs, quality documentation.
metadata:
  pattern: composite
  components:
    - pipeline
    - reviewer
  steps: "5"
  depends_on:
    assets:
      - api-doc-template.md
    references:
      - docstring-style.md
      - review-checklist.md
      - quality-checklist.md
---

# API Documentation Pipeline with Review

This skill combines Pipeline (structured workflow) + Reviewer (quality assessment).

Execute each step IN ORDER. Do NOT skip. Stop at checkpoints.

---

## Step 1 — Parse & Inventory (Pipeline)

Analyze Python code to extract public API.

Present inventory checklist.

Ask: "Is this the complete API to document?"

**[硬性检查点]**: Wait for confirmation.

---

## Step 2 — Generate Docstrings (Pipeline)

For each undocumented item:
1. Load `references/docstring-style.md`
2. Generate docstring
3. Present for approval

**[硬性检查点]**: Wait for all docstrings approved.

---

## Step 3 — Assemble Documentation (Pipeline)

Load `assets/api-doc-template.md`.

Compile all elements into single document.

Present assembled document.

Ask: "Structure correct? Proceed to review?"

---

## Step 4 — Quality Review (Reviewer)

**Now applying Reviewer pattern within the pipeline.**

### 4.1 Load Checklist

Load `references/review-checklist.md` for review criteria.

### 4.2 Apply Checks

For each rule in the checklist, verify the assembled documentation:

| Check | Rule Reference | Status |
|-------|----------------|--------|
| Coverage completeness | §1.1 | [ ] |
| Parameter descriptions | §2.2 | [ ] |
| Return documentation | §3.1 | [ ] |
| Example presence | §5.1 | [ ] |
| Style compliance | §6.1 | [ ] |

### 4.3 Generate Findings

Group findings by severity:

#### Errors (must fix before final)
- [Finding with rule citation and fix suggestion]

#### Warnings (should fix)
- [Finding with rule citation]

#### Info (consider)
- [Enhancement suggestion]

### 4.4 Fix and Iterate

**For errors**: Fix automatically. Re-run check.

**For warnings**: Ask user:
- "Found [issue]. Fix automatically or accept as-is?"

**[硬性检查点]**: All errors fixed and warnings resolved before Step 5.

---

## Step 5 — Final Output (Pipeline)

Present quality-reviewed, finalized documentation.

Ask: "Final documentation ready. Any last adjustments?"

---

## Component Mapping

| Step | Pattern Used |
|------|--------------|
| 1-3 | Pipeline — sequential execution with checkpoints |
| 4 | Reviewer — checklist-based quality assessment |
| 5 | Pipeline — final assembly and delivery |

---

## Hard Constraints

From Pipeline component:
- Steps execute in order
- Checkpoints block progression
- No skipping

From Reviewer component:
- Checklist must be loaded
- Findings grouped by severity
- Errors must be fixed

Combined:
- Reviewer step (4) is mandatory checkpoint in Pipeline
- Cannot reach Step 5 with unresolved errors
```

---

## references/review-checklist.md (Reviewer 组件)

```markdown
# Documentation Review Checklist

## 1. Coverage

### 1.1 Symbol Coverage
**Rule**: Every public symbol (class, function, constant) has documentation.

**Check**: Compare inventory from Step 1 against assembled doc.

**Severity**: error

### 1.2 Method Coverage
**Rule**: Every public method of documented classes has docstring.

**Check**: For each class in doc, verify all methods present.

**Severity**: error

---

## 2. Parameter Documentation

### 2.1 Type Annotations
**Rule**: Every parameter has type in signature and docstring.

**Check**: Cross-reference function signature with Args section.

**Severity**: warning

### 2.2 Parameter Descriptions
**Rule**: Every parameter has a meaningful description (not just name).

**Check**: Args section should have descriptions, not empty placeholders.

**Severity**: error

---

## 3. Return Documentation

### 3.1 Return Type
**Rule**: Return type documented in signature and Returns section.

**Check**: Verify Returns section exists for functions returning values.

**Severity**: warning

### 3.2 Return Description
**Rule**: Return value described, not just type.

**Check**: Returns section has meaningful description.

**Severity**: warning

---

## 4. Exception Documentation

### 4.1 Exception Listing
**Rule**: All raised exceptions listed in Raises section.

**Check**: Find raise statements in code. Verify in doc.

**Severity**: warning

---

## 5. Examples

### 5.1 Example Presence
**Rule**: Every function has at least one usage example.

**Check**: Each function section contains Example block.

**Severity**: info

### 5.2 Example Validity
**Rule**: Examples are syntactically valid Python.

**Check**: Parse example code blocks.

**Severity**: error

---

## 6. Style Compliance

### 6.1 Summary Line
**Rule**: One-line summary, < 80 chars, imperative mood.

**Check**: First line of each docstring.

**Severity**: info
```

---

## 使用示例流程

### 用户触发

```
用户: "生成并审查 calculator.py 的 API 文档"
```

### Step 1-3 (Pipeline)

按 pipeline 流程执行，同 pipeline-example.md...

### Step 4 (Reviewer 嵌入)

Agent:
```
## Step 4 — Quality Review

Loading `references/review-checklist.md`...

### Checks Applied

| Check | Status |
|-------|--------|
| Symbol Coverage | ✓ All 4 symbols documented |
| Parameter Descriptions | ⚠ 2 params missing description |
| Return Documentation | ✓ All returns documented |
| Example Presence | ✓ Examples present for all functions |
| Style Compliance | ✓ Google style followed |

### Findings

#### Warnings (should fix)

**Calculator.add:param2** — Rule 2.2: Parameter "b" has empty description
Current:
```
Args:
    a: First operand.
    b: 
```
Fix:
```
Args:
    a: First operand.
    b: Second operand to add.
```

---

Fix automatically or accept as-is?
```

用户: "自动修复"

Agent 修复后重新检查...

**[硬性检查点通过]**

### Step 5 (Final)

输出最终文档。

---

## 模式合规检查点

| 检查项 | 组件 | 要求 |
|--------|------|------|
| 元数据声明 | Composite | `metadata.components` 列出 pipeline + reviewer |
| Pipeline 检查 | Pipeline | 步骤编号、检查点语法、顺序执行 |
| Reviewer 检查 | Reviewer | 检查清单加载、severity 分组、规则引用 |
| 组件过渡 | Composite | Step 4 明确标注 "(Reviewer)" |
| 组合检查点 | Composite | Reviewer 结果作为 Pipeline 检查点 |