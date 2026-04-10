# ADK Skill 最终防错审查表 (Review Checklist)

在向用户输出最终生成的 Skill 文件代码前，AI 必须对照此清单自检：

- [ ] **命名极其严格**：YAML 的 `name` 是否**全部且仅为小写字母、数字和连字符(-)**？必须与文件夹名完全一致。
- [ ] **合法的元数据**：YAML 头部是否**绝对清除了** `triggers` 等不支持的字段？（仅允许使用 `name`, `description`, `user-invocable`, `metadata` 等）。
- [ ] **保持 SKILL.md 精简**：新技能的主提示词是否干净？是否有把复杂的代码规则或模板剥离并提示用户存入 `references/` 或 `assets/` 目录？
- [ ] **门控机制生效**：新技能的 Pipeline 中，是否设计了防止 AI 直接一口气跑到终点、强迫它“暂停并等待用户输入”的门控指令（Gate Conditions）？