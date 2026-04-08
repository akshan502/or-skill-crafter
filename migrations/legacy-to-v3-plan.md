# Legacy Skill → v3 Migration Plan

## 目标
把旧式“单文件大 prompt skill”迁移为 v3 的目录型 skill：
- `SKILL.md`
- `skill.yaml`
- `references/`
- `assets/`
- `scripts/`
- `evals/`（可选）

## 迁移步骤

### Step 1: 识别旧 skill 结构
扫描旧 `SKILL.md`，判断其中哪些内容分别属于：
- 角色定义
- 适用/不适用场景
- Pipeline
- checklist / rubric
- 输出模板
- few-shot 示例
- 环境耦合说明

### Step 2: 抽取为 v3 DSL
将旧 skill 抽取为：
- `skill.type`
- `intent`
- `patterns`
- `flow`
- `fallback`
- `output`
- `boundaries`

### Step 3: 拆分目录
迁移规则：
- 角色、范围、Pipeline、边界 → `SKILL.md`
- checklist / rubric / 方法说明 → `references/`
- 模板 / 示例 / few-shot → `assets/`
- 初始化 / 校验 / 辅助动作 → `scripts/`
- 行为样例 / 回归样例 → `evals/`

### Step 4: 校验一致性
检查：
- `skill.yaml` 与 `SKILL.md` 是否一致
- pattern 是否有结构证据
- 是否去除了运行时数据回写
- 是否消除了过度环境耦合

## 迁移输出物
- `migration-report.md`
- 新版 `skill.yaml`
- 新版目录结构建议
- 待人工确认的风险清单
