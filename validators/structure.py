import os
import re
from typing import List


def validate_structure(skill_dir: str) -> List[str]:
    errors = []
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    skill_yaml = os.path.join(skill_dir, 'skill.yaml')

    if not os.path.exists(skill_md):
        errors.append('缺少 SKILL.md')
    if not os.path.exists(skill_yaml):
        errors.append('缺少 skill.yaml')

    if errors:
        return errors

    with open(skill_md, 'r', encoding='utf-8') as f:
        md = f.read()

    folder_name = os.path.basename(os.path.abspath(skill_dir))
    match = re.search(r'^name:\s*([a-z0-9-]+)\s*$', md, re.M)
    if not match:
        errors.append('SKILL.md 中缺少合法的 name')
    else:
        skill_name = match.group(1)
        if skill_name != folder_name:
            errors.append(f'name 与目录名不一致: {skill_name} != {folder_name}')

    return errors
