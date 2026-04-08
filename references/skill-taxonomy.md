# Skill Taxonomy v3

`or-skill-crafter` v3 将技能先归类，再组合 pattern，而不是直接套一个通用模板。

## 1. writer
适合：文档生成、说明文、PRD、周报、邮件草稿。

默认 pattern：
- inversion
- generator

典型特征：
- 输入是主题、素材、约束
- 输出是结构化文本或文档
- 常依赖模板与输出格式

## 2. analyzer
适合：审查、评分、评估、诊断、复盘。

默认 pattern：
- inversion
- reviewer
- generator

典型特征：
- 输入是待分析对象
- 输出是结论、问题列表、评分、建议
- 需要 rubric、checklist 或评审框架

## 3. transformer
适合：改写、提取、翻译、结构化转换、摘要。

默认 pattern：
- inversion
- generator

典型特征：
- 输入输出之间有明显映射
- 强依赖格式与约束
- 常需要 few-shot 示例

## 4. orchestrator
适合：多阶段任务编排、子步骤分发、阶段式执行。

默认 pattern：
- inversion
- pipeline
- reviewer

典型特征：
- 存在多个阶段
- 每阶段有明确进入条件与退出条件
- 常需要硬性检查点

## 5. tool-wrapper
适合：把 API、MCP、CLI、浏览器流程封装成可复用技能。

默认 pattern：
- inversion
- tool-wrapper
- pipeline

典型特征：
- 明确的输入参数与输出结果
- 有工具边界、失败处理、权限/风险约束
- 不应把环境细节硬编码到模板里，除非它就是环境专属技能

## 6. builder
适合：生成其他技能、配置、模板或项目骨架。

默认 pattern：
- inversion
- pipeline
- generator
- reviewer

典型特征：
- 输出是目录、文件、脚手架或结构化产物
- 必须说明哪些内容是草案，哪些内容可直接使用
- 应避免变成职责失控的“万能构建器”

## 选型原则

优先回答三个问题：
1. 这个技能的主输出是什么？
2. 它更像“写”“审”“改”“调工具”还是“编排流程”？
3. 它是否需要强制补问、评分框架、分阶段门控？

若一个需求同时命中多种类型，优先选择主类型，并把次级能力下沉为 pattern，而不是把 skill 类型写成混合怪。
