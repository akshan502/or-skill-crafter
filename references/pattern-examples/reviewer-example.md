# Reviewer 模式完整示例

本文档展示 Reviewer 模式的完整可运行示例：Python 代码审查器。

---

## 技能结构

```
skills/python-reviewer/
├── SKILL.md                      # 审查协议
└── references/
    └── review-checklist.md       # 检查清单
```

---

## SKILL.md

```markdown
---
name: python-reviewer
description: Reviews Python code for quality, style, security, and common bugs. Use when the user submits code for review, asks for feedback, requests a code audit, or says "review my code". Trigger keywords: review, code review, audit, feedback, check my code, python code.
metadata:
  pattern: reviewer
  severity-levels: error, warning, info
  depends_on:
    references:
      - review-checklist.md
---

# Python Code Reviewer

You are a Python code reviewer following a systematic review protocol.

## Step 1: Load Checklist

Load `references/review-checklist.md` for the complete review criteria.

## Step 2: Understand Context

Before critiquing:
1. Read the code completely
2. Identify the file/module purpose
3. Note any imports and dependencies
4. Understand the expected behavior

Ask the user if context is unclear:
- "What is the main purpose of this code?"
- "Are there specific areas you want me to focus on?"

## Step 3: Apply Rules

For each rule in the checklist:
1. Check if the code satisfies it
2. For violations found:
   - Note file and line number (approximate if needed)
   - Classify severity: error | warning | info
   - Explain WHY it's problematic
   - Suggest specific fix with code example

## Step 4: Generate Report

Produce structured output:

### Summary
- Overall purpose and quality (1-2 sentences)
- Major themes of issues found

### Findings by Severity

#### Errors (must fix)
[List all errors with: file:line, rule violated, explanation, suggested fix]

#### Warnings (should fix)
[List all warnings with: file:line, rule violated, explanation, suggested fix]

#### Info (consider)
[List suggestions with: description, rationale]

### Score

Rate 1-10 with brief justification:
- 9-10: Excellent, minor suggestions only
- 7-8: Good, some improvements needed
- 5-6: Acceptable, notable issues
- 3-4: Needs work, significant problems
- 1-2: Major issues, requires rewrite

### Top 3 Recommendations

List the most impactful improvements in priority order.

## Hard Constraints

- NEVER give a score without justification
- ALWAYS cite the specific rule from checklist
- NEVER make vague suggestions ("improve readability")
- ALWAYS provide specific fixes with code
- Group findings by severity, not by file
```

---

## references/review-checklist.md

```markdown
# Python Code Review Checklist

## 1. Code Quality

### 1.1 Function Length
**Rule**: Functions should be < 50 lines.

**Check**: Count lines per function. Flag functions > 50 lines.

**Severity**: warning

---

### 1.2 Naming Conventions
**Rule**: Use snake_case for functions/variables, PascalCase for classes.

**Check**: Scan for camelCase or PascalCase used incorrectly.

**Severity**: warning

---

### 1.3 Docstrings
**Rule**: Public functions must have docstrings.

**Check**: For each public function, verify docstring exists.

**Severity**: info

---

## 2. Type Safety

### 2.1 Type Annotations
**Rule**: Functions must have type annotations for parameters and return.

**Check**: Check each function signature. Flag missing annotations.

**Severity**: warning

---

### 2.2 Optional Handling
**Rule**: Optional types must be handled (None check or early return).

**Check**: Find Optional parameters/returns. Verify None handling.

**Severity**: error

---

## 3. Error Handling

### 3.1 Exception Specificity
**Rule**: Catch specific exceptions, not bare `except:`.

**Check**: Search for `except:` or `except Exception:` without specific type.

**Severity**: error

---

### 3.2 Exception Messages
**Rule**: Raised exceptions should have descriptive messages.

**Check**: Find `raise Exception` without message or with generic message.

**Severity**: warning

---

## 4. Security

### 4.1 SQL Injection
**Rule**: NEVER use string concatenation for SQL queries.

**Check**: Find SQL strings with + or f-string interpolation.

**Severity**: error

---

### 4.2 Hardcoded Secrets
**Rule**: NO hardcoded passwords, API keys, tokens.

**Check**: Search for common secret patterns (password=, api_key=, token=).

**Severity**: error

---

### 4.3 Input Validation
**Rule**: Validate user input before processing.

**Check**: Find input sources (request.body, argv, stdin). Verify validation.

**Severity**: warning

---

## 5. Performance

### 5.1 List Comprehension vs Loop
**Rule**: Prefer list comprehension for simple transformations.

**Check**: Find simple for-loops building lists. Suggest comprehension.

**Severity**: info

---

### 5.2 Large Data in Memory
**Rule**: Avoid loading large datasets into memory at once.

**Check**: Find file.read() on potentially large files. Suggest streaming.

**Severity**: warning

---

## 6. Maintainability

### 6.1 Magic Numbers
**Rule**: Named constants instead of magic numbers.

**Check**: Find numeric literals > 1 (excluding 0, 1, -1). Suggest naming.

**Severity**: info

---

### 6.2 Dead Code
**Rule**: Remove unused imports, functions, variables.

**Check**: Check import usage, function calls, variable references.

**Severity**: warning
```

---

## 使用示例

### 用户触发

```
用户: "帮我审查这段代码"
[用户提交代码文件]
```

### Agent 行为

1. 检测到 "审查" 关键词 → 触发 python-reviewer
2. 加载 `references/review-checklist.md`
3. 读取并理解代码
4. 逐项检查：
   - 代码质量：函数长度、命名、docstring
   - 类型安全：类型注解、Optional 处理
   - 错误处理：异常 specificity、消息
   - 安全：SQL 注入、硬编码密钥、输入验证
   - 性能：列表推导、大数据加载
   - 可维护性：魔数、死代码
5. 按 severity 分组输出 findings
6. 给出评分和 Top 3 建议

---

## 输出格式示例

```markdown
## Summary

This module implements user authentication with JWT tokens. 
Overall quality is acceptable (6/10) with notable security concerns 
and missing type annotations.

## Findings

### Errors (must fix)

**auth.py:45** — Rule 4.1: SQL Injection Risk
```python
query = "SELECT * FROM users WHERE email = '" + email + "'"
```
Why: String concatenation allows SQL injection.
Fix:
```python
query = "SELECT * FROM users WHERE email = ?"
cursor.execute(query, (email,))
```

**auth.py:12** — Rule 3.1: Bare Exception
```python
except:
    pass
```
Why: Silently catches all exceptions including system exits.
Fix:
```python
except ValueError as e:
    logger.error(f"Invalid input: {e}")
```

### Warnings (should fix)

**auth.py:23** — Rule 2.1: Missing Type Annotations
```python
def authenticate(email, password):
```
Fix:
```python
def authenticate(email: str, password: str) -> Optional[User]:
```

### Info (consider)

**auth.py:30** — Rule 1.3: Missing Docstring
Consider adding docstring for public function `authenticate`.

## Score: 6/10

Justification: Core logic works but security vulnerabilities 
(SQL injection, bare except) and missing type safety are significant issues.

## Top 3 Recommendations

1. Replace SQL string concatenation with parameterized queries (security)
2. Add type annotations to all function signatures (maintainability)
3. Add specific exception handling with logging (robustness)
```

---

## 模式合规检查点

| 检查项 | 要求 |
|--------|------|
| 检查清单文件 | `references/review-checklist.md` 存在 |
| Severity 分组 | 输出包含 error/warning/info 分组 |
| 规则引用 | 每个 finding 引用 checklist 具体规则 |
| 评分输出 | 包含 1-10 评分和理由 |
| 具体修复建议 | 每个 finding 包含代码修复示例 |