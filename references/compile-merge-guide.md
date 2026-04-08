# Compile Merge Guide

本文件说明如何将编译产物收敛回正式 skill 目录。

## 推荐原则

### 1. `SKILL.generated.md` 默认视为草案
除非人工确认质量足够，否则不要直接覆盖正式 `SKILL.md`。

### 2. 先比对，再替换
建议比较：
- 角色定义是否更清楚
- 适用/不适用场景是否更具体
- Pipeline 是否更完整
- 边界约束是否被削弱
- fallback 是否被遗漏

### 3. references/assets 先看职责，再看内容
编译脚本生成的 references/assets 是骨架，不一定完整。
先判断：
- 该文件是否确实需要
- 文件职责是否正确
- 内容是否需要按 skill 类型继续补充

### 4. 优先保留人工沉淀内容
若旧文件中已有高质量规则、示例或 checklist，应优先保留人工沉淀，而不是盲目用新 stub 覆盖。

## 合并建议

### 适合直接采用的内容
- 目录结构建议
- 缺失文件的最小骨架
- 新增的 flow / fallback 提示

### 适合人工重写的内容
- 角色定义
- rubric / checklist 细节
- tool contract 细节
- output template 的业务字段

### 不应自动覆盖的内容
- 已长期使用且稳定的规则文档
- 含环境特定约束的工具规范
- 人工维护的 few-shot 示例
