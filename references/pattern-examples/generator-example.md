# Generator 模式完整示例

本文档展示 Generator 模式的完整可运行示例：技术报告生成器。

---

## 技能结构

```
skills/report-generator/
├── SKILL.md                      # 编排指令
├── assets/
│   └── report-template.md        # 输出模板
└── references/
    └── style-guide.md            # 格式规范
```

---

## SKILL.md

```markdown
---
name: report-generator
description: Generates structured technical reports in Markdown. Use when the user asks to write, create, draft, or generate a report, summary, analysis, or documentation. Trigger keywords: report, summary, analysis, document, technical report, write report.
metadata:
  pattern: generator
  output-format: markdown
  depends_on:
    assets:
      - report-template.md
    references:
      - style-guide.md
---

# Technical Report Generator

You are a technical report generator. Follow these steps exactly to produce consistent, well-structured reports.

## Step 1: Load Style Guide

Load `references/style-guide.md` for:
- Tone requirements (technical vs executive)
- Formatting rules (headings, lists, code blocks)
- Citation style
- Length guidelines

## Step 2: Load Template

Load `assets/report-template.md` for the required output structure.

## Step 3: Collect Variables

Ask the user for missing information. Collect ONE variable at a time, wait for each answer:

Required variables:
1. **topic**: What is the subject of the report?
2. **audience**: Technical, executive, or general?
3. **key_points**: List 3-5 main findings or data points
4. **format_preference**: Full report or executive summary?

Optional variables (ask if not provided):
- **deadline**: Is there a time constraint?
- **length**: Approximate word count preference?
- **sources**: Any specific sources to reference?

## Step 4: Fill Template

Using the collected variables:
1. Apply tone from style-guide based on audience
2. Fill every section in the template
3. Ensure structure matches template exactly (no missing sections)
4. Apply formatting rules from style-guide

## Step 5: Validate Output

Check against template:
- Every section header present
- Formatting matches style-guide
- Required variables are used in content

## Step 6: Return Report

Present the completed report as a single Markdown document.

Ask: "Does this report meet your requirements? What should be adjusted?"
Iterate based on feedback.

## Hard Constraints

- NEVER skip a section from the template
- NEVER change section headers
- ALWAYS match tone to declared audience
- NEVER fabricate data (ask user if missing)
```

---

## assets/report-template.md

```markdown
# [topic]

**Report Type**: Technical Analysis  
**Target Audience**: [audience]  
**Generated**: [date]

---

## Executive Summary

[2-3 paragraph overview of the key findings, suitable for the declared audience]

---

## Background

[Context and problem statement. What led to this analysis?]

---

## Key Findings

### Finding 1: [Title]

[Description, evidence, implications]

### Finding 2: [Title]

[Description, evidence, implications]

### Finding 3: [Title]

[Description, evidence, implications]

---

## Analysis

[Detailed analysis of findings, correlations, patterns]

---

## Recommendations

### Recommendation 1

[Actionable suggestion with rationale]

### Recommendation 2

[Actionable suggestion with rationale]

### Recommendation 3

[Actionable suggestion with rationale]

---

## Appendix

### Data Sources

[List of sources referenced]

### Methodology

[How the analysis was conducted]

### Limitations

[What constraints or gaps exist in this analysis]

---

*Report generated using technical-report-generator skill*
```

---

## references/style-guide.md

```markdown
# Report Style Guide

## Tone Requirements

### Technical Audience
- Use precise technical terminology
- Include relevant metrics and specifications
- Assume reader understands domain concepts
- Can include code snippets, diagrams, formulas

### Executive Audience
- Use business-focused language
- Lead with business impact and ROI
- Minimize technical jargon (explain when used)
- Focus on actionable outcomes
- Keep sections concise (bullet points preferred)

### General Audience
- Use plain language
- Explain technical concepts with analogies
- Avoid acronyms without explanation
- Focus on practical implications

---

## Formatting Rules

### Headings
- Use ATX style (# Heading)
- Maximum heading depth: 3 levels (###)
- Heading text should be descriptive

### Lists
- Use - for unordered lists
- Use 1. for ordered lists
- Nested lists: indent 2 spaces

### Code Blocks
- Use triple backticks with language tag
- ```python for Python code
- ```bash for shell commands
- Keep code snippets < 20 lines

### Emphasis
- **Bold** for key terms, section headers
- *Italic* for terms being defined
- NEVER use both simultaneously

---

## Citation Style

- Use inline citations: [Source Name]
- List full sources in Appendix
- NEVER fabricate citations

---

## Length Guidelines

| Section | Target Length |
|---------|---------------|
| Executive Summary | 150-300 words |
| Background | 200-400 words |
| Each Finding | 100-250 words |
| Analysis | 300-500 words |
| Each Recommendation | 50-150 words |
| Total Report | 1500-3000 words |
```

---

## 使用示例

### 用户触发

```
用户: "帮我写一份关于我们系统性能瓶颈的技术报告"
```

### Agent 行为

1. 检测到 "报告" 关键词 → 触发 report-generator
2. 加载 `references/style-guide.md` 和 `assets/report-template.md`
3. 逐个收集变量：
   - Q: "报告的主题是？" → 用户: "系统性能瓶颈分析"
   - Q: "目标读者是技术人员还是管理层？" → 用户: "技术团队"
   - Q: "关键发现有哪些（3-5点）？" → 用户: "1. 数据库查询慢 2. API响应时间长 3. 内存泄漏..."
   - Q: "需要完整报告还是执行摘要？" → 用户: "完整报告"
4. 使用 Technical tone 填充模板的每个部分
5. 输出完整的 Markdown 报告

---

## 模式合规检查点

| 检查项 | 要求 |
|--------|------|
| 模板文件 | `assets/report-template.md` 存在 |
| 模板填充步骤 | SKILL.md 包含 step-by-step 填充指令 |
| 结构保持 | 输出的每个 section 都在模板中定义 |
| 变量收集 | 明确列出需要的变量并逐个询问 |
| 风格规范 | `references/style-guide.md` 存在并被加载 |