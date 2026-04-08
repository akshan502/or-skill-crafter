from typing import List
import os


REQUIRED_SECTIONS = [
    '## 适用场景',
    '## 不适用场景',
    'Fallback',
    '边界约束',
]


def validate_semantics(skill_dir: str) -> List[str]:
    errors = []
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    if not os.path.exists(skill_md):
        return ['缺少 SKILL.md，无法做语义检查']

    with open(skill_md, 'r', encoding='utf-8') as f:
        md = f.read()

    if '## 适用场景' not in md:
        errors.append('缺少适用场景')
    if '## 不适用场景' not in md:
        errors.append('缺少不适用场景')
    if 'Fallback' not in md and '失败兜底' not in md:
        errors.append('缺少失败兜底')
    if '边界约束' not in md and 'Hard Constraints' not in md:
        errors.append('缺少边界约束')
    if '输入不足' not in md and '补问' not in md:
        errors.append('缺少输入不足时的补问机制')

    return errors
