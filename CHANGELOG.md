# CHANGELOG

## v3-initial
- 新增 `references/skill-taxonomy.md`
- 新增 `references/pattern-selection.md`
- 新增 `references/v3-roadmap.md`
- 新增 `dsl-skill-schema.md`
- 新增 `assets/skill-yaml-example.yaml`
- 新增 `assets/file-responsibility-template.md`
- 更新 `SKILL.md`，引入 taxonomy + pattern selection + skill.yaml DSL 流程
- 更新 `README.md`，补充 v3 方向、文件职责表、DSL 示例
- 更新 `scripts/init_workspace.py`，初始化时同时生成 `skill.yaml`
- 新增 `scripts/validate_skill.py`，提供基础结构校验骨架

## v3-second-round
- 新增按类型拆分的模板：writer / analyzer / tool-wrapper
- 新增 `validators/structure.py`
- 新增 `validators/semantics.py`
- 新增 `validators/patterns.py`
- 更新 `scripts/validate_skill.py`，改为聚合分层 validator
- 新增 `migrations/legacy-to-v3-plan.md`
- 新增 `scripts/migrate_skill.py`
- 新增 `evals/v3-evals.json`
- 更新 `README.md`，同步第二轮进度

## v3-third-round
- 新增 `references/dsl-to-artifacts-mapping.md`
- 新增 `assets/migration-report-template.md`
- 更新 `SKILL.md`，明确按 `skill.type` 选择模板并声明降级策略
- 更新 `scripts/migrate_skill.py`，从预览输出升级为生成 `migration-report.md`
- 更新 `README.md`，补充映射规则与当前脚本能力说明

## v3-fourth-round
- 新增 `assets/templates/transformer-skill-template.md`
- 新增 `assets/templates/orchestrator-skill-template.md`
- 新增 `scripts/compile_skill.py`，提供最小编译骨架
- 新增 `evals/compile-evals.json`
- 更新 `scripts/migrate_skill.py`，额外生成 `skill.yaml.draft`
- 更新 `README.md`，同步 compile 与 migration 新能力

## v3-fifth-round
- 新增 `assets/templates/builder-skill-template.md`
- 更新 `scripts/compile_skill.py`，支持 builder 模板
- 更新 `scripts/compile_skill.py`，开始吃入 `intent / flow / fallback`
- 更新 `scripts/compile_skill.py`，生成 `references/recommended-files.md` 与 `assets/recommended-files.md`
- 更新 `evals/compile-evals.json`，覆盖 builder 与 flow/fallback 感知
- 更新 `README.md`，同步第五轮能力说明

## v3-sixth-round
- 更新 `scripts/compile_skill.py`，按 pattern / type 生成 `references/*.md` 与 `assets/*.md` stub 草案
- 更新 `scripts/compile_skill.py`，新增 `compile-review.md` 作为编译收敛说明
- 更新 `scripts/compile_skill.py`，将 flow / fallback / output 进一步写入动态章节
- 更新 `evals/compile-evals.json`，新增 stub 文件与 compile-review 覆盖
- 更新 `README.md`，同步第六轮能力说明

## v3-seventh-eighth-round
- 更新 `scripts/compile_skill.py`，将 stub 文件细化为类型化骨架内容
- 新增 `references/migration-to-compile-workflow.md`
- 新增 `references/compile-merge-guide.md`
- 新增 `final-status-v3-alpha.md` 作为阶段总结
- 更新 `README.md`，补充工作流文档与 alpha 状态入口
