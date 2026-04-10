# Pipeline 模式完整示例

本文档展示 Pipeline 模式的完整可运行示例：API 文档生成流水线。

---

## 技能结构

```
skills/doc-pipeline/
├── SKILL.md                      # 流水线定义
├── assets/
│   └── api-doc-template.md       # 输出模板
└── references/
    ├── docstring-style.md        # 文档字符串格式
    └── quality-checklist.md      # 质量检查清单
```

---

## SKILL.md

```markdown
---
name: doc-pipeline
description: Generates API documentation from Python source code through a multi-step pipeline. Use when user asks to "document a module", "generate API docs", "create documentation from code", "add docstrings". Trigger keywords: document, api docs, docstring, documentation, python docs.
metadata:
  pattern: pipeline
  steps: "4"
  depends_on:
    assets:
      - api-doc-template.md
    references:
      - docstring-style.md
      - quality-checklist.md
---

# API Documentation Pipeline

You are running a documentation generation pipeline. Execute each step IN ORDER.

## Execution Rules

- Do NOT skip steps
- Do NOT proceed if a step fails
- Stop at hard checkpoints and wait for user confirmation

---

## Step 1 — Parse & Inventory

### Action
Analyze the user's Python code to extract:
- All public classes
- All public functions/methods
- All public constants

### Output
Present inventory as a checklist:

```
## API Inventory

### Classes
- [x] ClassName
  - [ ] method_one
  - [ ] method_two

### Functions
- [ ] function_name
- [ ] helper_function

### Constants
- [ ] MAX_SIZE
- [ ] DEFAULT_VALUE
```

### Question
Ask: "Is this the complete public API you want documented? Should I exclude anything?"

**[硬性检查点]**: Wait for user to confirm the inventory before proceeding to Step 2.

---

## Step 2 — Generate Docstrings

### Action
For each item lacking a docstring:
1. Load `references/docstring-style.md` for format requirements
2. Generate a docstring following the style guide
3. Present each docstring individually

### Output Format
```
## Docstring for function_name

```python
def function_name(param1: str, param2: int) -> bool:
    """
    [Generated docstring following style guide]
    
    Args:
        param1: [Description]
        param2: [Description]
        
    Returns:
        [Description]
        
    Raises:
        [Exception types if applicable]
    """
```

Does this docstring capture the function's behavior correctly?
```

### Process
- Generate docstrings one by one
- Get user approval for each
- Mark approved docstrings in inventory

**[硬性检查点]**: After all docstrings generated, ask: "All docstrings approved. Proceed to assembly?"

DO NOT proceed to Step 3 until user confirms.

---

## Step 3 — Assemble Documentation

### Action
1. Load `assets/api-doc-template.md` for output structure
2. Compile all classes, functions, and docstrings into single document
3. Apply formatting from style guide

### Output
Present the assembled API reference document.

Ask: "Does this structure look correct? Any sections to add/remove?"

---

## Step 4 — Quality Check

### Action
Load `references/quality-checklist.md` and verify:

| Check | Status |
|-------|--------|
| Every public symbol documented | [ ] |
| Every parameter has type and description | [ ] |
| Every return value documented | [ ] |
| At least one usage example per function | [ ] |
| Docstrings follow style guide | [ ] |

### Report Findings
- List any quality issues
- Severity: error (missing required element), warning (incomplete), info (enhancement possible)

### Fix Issues
- Fix errors automatically
- Ask user about warnings (fix or accept as-is)

### Final Output
Present the quality-checked, finalized API documentation.

---

## Failure Handling

| Step | If Fails | Recovery |
|------|----------|----------|
| Step 1 | Cannot parse code | Ask user to provide readable code or specify format |
| Step 2 | Cannot determine behavior | Ask user to explain function purpose |
| Step 3 | Template mismatch | Adjust template or ask user preference |
| Step 4 | Quality issues found | Fix errors, negotiate warnings |

---

## Hard Constraints

- NEVER skip a step
- NEVER proceed past checkpoint without user confirmation
- NEVER fabricate docstring content (ask if unclear)
- NEVER output final doc before Step 4 completes
```

---

## assets/api-doc-template.md

```markdown
# API Reference: [Module Name]

**Version**: [Version]  
**Generated**: [Date]

---

## Overview

[Brief description of the module purpose]

---

## Classes

### ClassName

**Purpose**: [One-line summary]

```python
class ClassName:
    """[Full docstring]"""
```

#### Methods

##### method_name

```python
def method_name(self, param: Type) -> ReturnType:
    """[Docstring]"""
```

**Example**:
```python
obj = ClassName()
result = obj.method_name(value)
```

---

## Functions

### function_name

**Purpose**: [One-line summary]

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """[Full docstring]"""
```

**Parameters**:
| Name | Type | Description |
|------|------|-------------|
| param1 | Type1 | [Description] |
| param2 | Type2 | [Description] |

**Returns**: [Description]

**Example**:
```python
result = function_name(arg1, arg2)
```

---

## Constants

### CONSTANT_NAME

```python
CONSTANT_NAME: Type = value
```

**Purpose**: [Description]

---

## Exceptions

### CustomException

```python
class CustomException(Exception):
    """Raised when [condition]"""
```

---

*Generated by doc-pipeline skill*
```

---

## references/docstring-style.md

```markdown
# Docstring Style Guide

## Format: Google Style

Use Google-style docstrings for all Python code.

### Function Docstring Structure

```python
def function_name(param1: str, param2: int) -> bool:
    """One-line summary of what the function does.
    
    Extended description if needed. Explain behavior,
    edge cases, and important notes.
    
    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.
            Can extend to multiple lines for complex params.
        
    Returns:
        Description of return value. Include type if not
        obvious from signature.
        
    Raises:
        ValueError: If param1 is empty.
        TypeError: If param2 is not an integer.
        
    Example:
        >>> result = function_name("test", 5)
        >>> print(result)
        True
    """
```

### Class Docstring Structure

```python
class ClassName:
    """One-line summary of the class purpose.
    
    Extended description of the class behavior and usage.
    
    Attributes:
        attr1: Description of first attribute.
        attr2: Description of second attribute.
        
    Example:
        >>> obj = ClassName()
        >>> obj.method()
    """
```

## Requirements

| Element | Required | Notes |
|---------|----------|-------|
| One-line summary | Yes | < 80 chars, imperative mood |
| Args section | Yes | For functions with parameters |
| Returns section | Yes | For functions that return |
| Raises section | If applicable | Only if exceptions are raised |
| Example section | Recommended | Shows basic usage |

## Style Rules

- Use imperative mood for summary: "Calculate total", not "Calculates total"
- First word of summary should be capitalized
- No period at end of one-line summary
- Parameter descriptions start with lowercase, end without period
- Use "Optional" for optional parameters with defaults
```

---

## references/quality-checklist.md

```markdown
# Documentation Quality Checklist

## Required Elements

### 1. Coverage
- [ ] Every public function documented
- [ ] Every public class documented
- [ ] Every public constant has comment or docstring

### 2. Parameters
- [ ] Every parameter has type annotation
- [ ] Every parameter has description
- [ ] Optional parameters marked as Optional

### 3. Returns
- [ ] Return type annotated
- [ ] Return value described
- [ ] None return explicitly stated if function returns None

### 4. Exceptions
- [ ] All raised exceptions listed in Raises section
- [ ] Exception conditions described

### 5. Examples
- [ ] At least one example per function
- [ ] Example is runnable (valid syntax)
- [ ] Example shows typical use case

## Style Compliance

- [ ] Summary line < 80 characters
- [ ] Imperative mood used
- [ ] Consistent formatting throughout
- [ ] No markdown in docstrings (only in assembled docs)

## Severity Levels

| Level | Condition |
|-------|-----------|
| error | Missing required element (param type, return description) |
| warning | Incomplete element (param type present but no description) |
| info | Enhancement possible (example could be clearer) |
```

---

## 使用示例

### 用户触发

```
用户: "帮我为这个 Python 模块生成 API 文档"
[提交 calculator.py 文件]
```

### Step 1 执行

Agent 分析代码，输出：

```
## API Inventory

### Classes
- [x] Calculator
  - [ ] add
  - [ ] subtract
  - [ ] multiply

### Functions
- [ ] create_calculator
```

Agent: "Is this the complete public API? Should I exclude anything?"

用户: "是的，继续"

**[硬性检查点通过]**

### Step 2 执行

Agent 加载 docstring-style.md，逐个生成 docstring...

```
## Docstring for Calculator.add

```python
def add(self, a: float, b: float) -> float:
    """Add two numbers and return the result.
    
    Args:
        a: First number to add.
        b: Second number to add.
        
    Returns:
        Sum of a and b.
        
    Example:
        >>> calc = Calculator()
        >>> calc.add(1, 2)
        3.0
    """
```

Does this capture the function correctly?
```

用户逐个确认后...

Agent: "All docstrings approved. Proceed to assembly?"

用户: "继续"

**[硬性检查点通过]**

### Step 3 执行

加载模板，组装完整文档...

### Step 4 执行

加载质量检查清单，验证，输出最终文档。

---

## 模式合规检查点

| 检查项 | 要求 |
|--------|------|
| 步骤编号 | Step 1, Step 2, Step 3, Step 4 明确标注 |
| 硬性检查点 | 包含 `**[硬性检查点]**` 语法 |
| 检查点等待 | Agent 在检查点停止等待用户确认 |
| 顺序执行 | transcript 显示步骤按序执行 |
| 失败处理 | 定义各步骤失败时的恢复策略 |