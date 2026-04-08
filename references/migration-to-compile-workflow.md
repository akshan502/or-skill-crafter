# Migration → Compile Workflow

本文件定义 legacy skill 升级到 v3 的推荐链路。

## 标准路径

1. 旧 skill 输入
   - 输入对象通常是旧版 `SKILL.md`

2. 运行迁移分析
   - 执行 `scripts/migrate_skill.py <legacy-skill>/SKILL.md`
   - 产出：
     - `migration-report.md`
     - `skill.yaml.draft`

3. 人工修订 DSL 草案
   - 检查 `skill.yaml.draft`
   - 修正：
     - `type`
     - `patterns`
     - `goal`
     - `primary_input`
     - `primary_output`
     - `flow`
     - `fallback`
     - `boundaries`

4. 运行编译
   - 执行 `scripts/compile_skill.py <skill-dir>`
   - 产出：
     - `compile-plan.md`
     - `SKILL.generated.md`
     - `compile-review.md`
     - `references/*.md` 草案
     - `assets/*.md` 草案

5. 人工收敛
   - 对照 `compile-review.md`
   - 决定 `SKILL.generated.md` 是否替换正式 `SKILL.md`
   - 决定哪些 references/assets 保留、重写或删除

6. 运行验证
   - 执行 `scripts/validate_skill.py <skill-dir>`
   - 检查结构、语义、pattern 一致性

## 当前边界

- 迁移脚本目前生成的是 DSL 草案，不是最终 `skill.yaml`
- 编译脚本目前生成的是草案与 stub，不是完整定稿
- 最终收敛仍需要人工判断

## 推荐实践

- 不要让迁移脚本直接覆盖现有 `SKILL.md`
- 不要跳过 `compile-review.md`
- 不要把 stub 文件当成完整规则文档直接投入长期使用
