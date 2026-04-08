# Pattern Selection Rules v3

v3 的核心不是模板优先，而是 **pattern 优先**。

## 可选 pattern

### inversion
含义：在执行前先补问、先收集上下文，而不是直接产出。

触发信号：
- 用户需求含糊
- 明确提到“先问”“先澄清”“信息不足时不要继续”
- 风险较高、边界不明确

最小要求：
- 至少 2~5 个关键澄清问题
- 明确“哪些信息不足时必须暂停”

### generator
含义：输出必须结构化、格式统一、可复用。

触发信号：
- 用户要求模板化、规范化、标准输出
- 输出是文档、清单、卡片、报告、skill 文件

最小要求：
- 定义输出结构
- 提供模板、字段约束或示例骨架

### reviewer
含义：生成和审查分离，使用独立 checklist / rubric 进行复核。

触发信号：
- 用户要求评分、审查、评估、诊断
- 任务本身容易“看起来对，其实不稳”

最小要求：
- 具备评审依据
- 具备 checklist / rubric / 审查步骤

### pipeline
含义：任务必须分阶段推进，而不是一步到底。

触发信号：
- 任务明确包含多个阶段
- 涉及规划、生成、确认、执行等链路
- 涉及高风险外部写操作或环境修改

最小要求：
- 显式 Step 划分
- 至少一个可判断的硬性检查点

### tool-wrapper
含义：把工具/API/MCP/CLI 封装成技能，而不是只描述“去调工具”。

触发信号：
- 用户要求对接 API、CLI、MCP、浏览器自动化
- 输出目标本质上依赖外部工具能力

最小要求：
- 明确输入参数
- 明确输出格式
- 明确失败处理与权限边界

## 组合规则

常见组合：
- writer = inversion + generator
- analyzer = inversion + reviewer + generator
- orchestrator = inversion + pipeline + reviewer
- tool-wrapper = inversion + tool-wrapper + pipeline
- builder = inversion + pipeline + generator + reviewer

## 约束

- 不要为了显得高级而堆满全部 pattern。
- 没有必要的 pattern 不应加入。
- 若选择某个 pattern，最终产物必须体现其结构证据：
  - inversion → 澄清步骤
  - generator → 输出模板
  - reviewer → checklist / rubric
  - pipeline → 阶段划分与门控
  - tool-wrapper → 工具边界与参数说明
