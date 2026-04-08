# or-skill-crafter v3 alpha 状态说明

## 当前定位

当前仓库已从 v2 风格的目录型 skill 模板器，推进到 **v3 alpha：pattern-aware skill compiler skeleton**。

## 已完成能力

### 1. 类型系统（taxonomy）
已支持：
- writer
- analyzer
- transformer
- orchestrator
- tool-wrapper
- builder

### 2. Pattern 选择
已显式支持：
- inversion
- generator
- reviewer
- pipeline
- tool-wrapper

### 3. DSL
已定义 `skill.yaml` 初版规范，支持：
- `skill`
- `intent`
- `patterns`
- `flow`
- `fallback`
- `output`
- `boundaries`

### 4. 模板体系
已提供 6 类模板：
- writer
- analyzer
- transformer
- orchestrator
- tool-wrapper
- builder

### 5. 编译骨架
`scripts/compile_skill.py` 当前可：
- 读取 `skill.yaml`
- 根据 `type` 选模板
- 生成 `compile-plan.md`
- 生成 `SKILL.generated.md`
- 生成 `compile-review.md`
- 生成 `references/recommended-files.md`
- 生成 `assets/recommended-files.md`
- 生成一批 `references/*.md` / `assets/*.md` stub 草案

### 6. 验证能力
`scripts/validate_skill.py` 已聚合：
- 结构检查
- 语义检查
- pattern 一致性检查

### 7. 迁移骨架
`scripts/migrate_skill.py` 当前可：
- 分析 legacy `SKILL.md`
- 生成 `migration-report.md`
- 生成 `skill.yaml.draft`

### 8. 工作流文档
已补充：
- DSL → 产物映射规则
- Migration → Compile Workflow
- Compile Merge Guide

## 当前仍未完成

### 1. compile 产物仍偏草案
- `SKILL.generated.md` 仍需要人工收敛
- references/assets 仍以骨架为主，不是完整业务规则

### 2. migration 仍非全自动
- `skill.yaml.draft` 需要人工修订
- 还不会自动生成最终 `skill.yaml`

### 3. 验证仍偏静态
- 还缺 smoke test
- 还缺更强的行为级回归验证

## 适合现在验证的内容

建议重点验证：
1. `compile_skill.py` 是否能按 type 选模板
2. `compile_skill.py` 是否会按 pattern / type 生成合理的 references/assets 草案
3. `migrate_skill.py` 是否能为旧 skill 产出有价值的 `migration-report.md` 与 `skill.yaml.draft`
4. `validate_skill.py` 是否能拦住明显结构/语义错误

## 结论

当前仓库可以视为：
**v3 alpha，可验证、可演进、可继续工程化，但尚未到生产级自动生成器。**
