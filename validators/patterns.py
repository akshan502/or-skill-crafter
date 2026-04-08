import os
import re
from typing import List


PATTERN_TO_EVIDENCE = {
    'inversion': ['clarify', '补问', '澄清'],
    'generator': ['output', '输出要求', 'template'],
    'reviewer': ['review', 'checklist', 'rubric', '审查'],
    'pipeline': ['step', 'pipeline', '硬性检查点'],
    'tool-wrapper': ['tool', '参数', '权限', '调用'],
}


def validate_patterns(skill_dir: str) -> List[str]:
    errors = []
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    skill_yaml = os.path.join(skill_dir, 'skill.yaml')

    if not os.path.exists(skill_md) or not os.path.exists(skill_yaml):
        return ['缺少 SKILL.md 或 skill.yaml，无法做 pattern 检查']

    with open(skill_md, 'r', encoding='utf-8') as f:
        md = f.read().lower()
    with open(skill_yaml, 'r', encoding='utf-8') as f:
        yml = f.read().lower()

    for pattern, evidences in PATTERN_TO_EVIDENCE.items():
        if re.search(rf'^\s*-\s*{re.escape(pattern)}\s*$', yml, re.M):
            if not any(e.lower() in md or e.lower() in yml for e in evidences):
                errors.append(f'声明了 pattern `{pattern}`，但未发现对应结构证据')

    return errors
