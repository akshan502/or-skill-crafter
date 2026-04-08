# or-skill-crafter v3 Roadmap

## v3 定位

`or-skill-crafter` v3 = Pattern-aware Skill Compiler

它不是只会填模板的母 skill，而是：
- 先识别 skill 类型
- 再选择 pattern 组合
- 再生成目录型 skill 产物
- 再进行基础验证
- 最后给出迁移或落地建议

## 第一阶段（当前要先做）

1. taxonomy：定义 skill 类型
2. pattern selection：定义 pattern 选择规则
3. DSL：定义统一中间表示 `skill.yaml`
4. template refactor：按 skill 类型拆模板
5. validator：做结构/语义/pattern 一致性校验
6. migration：为旧 skill 提供迁移方案

## 第二阶段

1. 按 skill 类型扩展模板库
2. 增加更多 evals
3. 支持 legacy skill 拆分建议
4. 支持更细的 pattern 组合提示

## 第三阶段

1. 支持 tool-wrapper 脚手架
2. 支持最小 smoke test
3. 支持 migration diff 提示

## 明确不在 v3 首批范围内

- 不重造独立 runtime
- 不直接做“自进化”闭环
- 不默认修改用户环境或强制自动安装依赖

这些方向可以以后做，但不应先把当前项目拖进复杂度泥潭。
