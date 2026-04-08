import os
import sys
import re


def get_skills_directory():
    """获取 skills 目录路径（脚本位于 skills/or-skill-crafter/scripts/）"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.dirname(os.path.dirname(script_dir))
    return skills_dir


def normalize_skill_name(raw_name: str) -> str:
    """将名称转换为仅包含小写字母、数字和连字符的格式"""
    clean_name = re.sub(r'[^a-z0-9-]', '-', raw_name.lower())
    clean_name = re.sub(r'-+', '-', clean_name).strip('-')
    return clean_name or "new-agent-skill"


def write_file_if_missing(path: str, content: str = ""):
    """仅当文件不存在时写入，避免覆盖用户已有内容"""
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


def create_skill_structure(raw_name):
    """为新技能创建符合 ADK 规范的目录结构，强制转换为规范命名"""
    clean_name = normalize_skill_name(raw_name)

    skills_dir = get_skills_directory()
    base_dir = os.path.join(skills_dir, clean_name)
    directories = [
        os.path.join(base_dir, 'scripts'),
        os.path.join(base_dir, 'references'),
        os.path.join(base_dir, 'assets')
    ]

    try:
        os.makedirs(base_dir, exist_ok=True)
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            write_file_if_missing(os.path.join(directory, '.gitkeep'))

        skill_stub = f"""---
name: {clean_name}
description: [在此处填写 50-100 词内的高度凝练描述。明确说明该技能用于解决什么具体问题、何时使用、何时不使用。]
user-invocable: true
---

# 角色定义
[定义此技能下 Agent 的角色定位、目标与工作原则]

## 适用场景
- [场景 1]
- [场景 2]

## 不适用场景
- [不应使用此技能的场景 1]
- [不应使用此技能的场景 2]

## 外部依赖 (Resource References)
- **规范/知识**: `references/[文件名].md`
- **模板/格式**: `assets/[文件名].md`
- **自动化工具**: `scripts/[脚本名]`
- **评测样例（可选）**: `evals/[文件名].json`

## 执行步骤 (Pipeline)
### Step 1: 分析阶段
...动作描述...
**[硬性检查点]：完成分析后停止，等待用户确认分析结果，再进入下一步。**

### Step 2: 执行阶段
...动作描述...

## 失败兜底 (Fallback)
- [当工具不可用时怎么办]
- [当输入不足时怎么办]

## 输出要求
- [输出物 1]
- [输出物 2]

## 边界约束 (Hard Constraints)
- [绝对禁止做的事项 1]
- [绝对禁止做的事项 2]
- [禁止把运行时数据写回 skill 本体目录]
"""
        skill_yaml_stub = f"""skill:
  name: {clean_name}
  version: v3
  type: writer
  user_invocable: true

intent:
  goal: [该技能的核心目标]
  primary_input: [核心输入]
  primary_output: [核心输出]
  constraints:
    - [关键约束]

patterns:
  - inversion
  - generator

flow:
  - id: clarify
    condition: missing_context
    action: ask_questions

fallback:
  insufficient_info: ask_more
  out_of_scope: refuse

output:
  format: markdown
  sections:
    - [section-name]

boundaries:
  - do not write runtime data back into the skill directory
"""
        write_file_if_missing(os.path.join(base_dir, 'SKILL.md'), skill_stub)
        write_file_if_missing(os.path.join(base_dir, 'skill.yaml'), skill_yaml_stub)

        print(f"✅ 成功初始化 ADK 技能目录: {base_dir}")
        print("📁 包含子目录: scripts/, references/, assets/")
        print("📝 已创建基础 SKILL.md 与 skill.yaml（若原文件不存在）")
        print("ℹ️ evals/ 为可选目录，按需手动添加")
    except Exception as e:
        print(f"❌ 创建目录失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    target_name = sys.argv[1] if len(sys.argv) > 1 else "new-agent-skill"
    create_skill_structure(target_name)
