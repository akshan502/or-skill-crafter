import os
import re
import sys


def analyze_legacy_skill(skill_md_path: str):
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sections = {
        'references_candidates': [],
        'assets_candidates': [],
        'pipeline_candidates': [],
        'boundary_candidates': [],
    }

    for line in text.splitlines():
        low = line.lower()
        if 'checklist' in low or 'rubric' in low or '规范' in line or '方法' in line:
            sections['references_candidates'].append(line)
        if 'template' in low or '示例' in line or '输出' in line:
            sections['assets_candidates'].append(line)
        if 'step' in low or 'pipeline' in low or '阶段' in line:
            sections['pipeline_candidates'].append(line)
        if '禁止' in line or '约束' in line or '不得' in line:
            sections['boundary_candidates'].append(line)

    return text, sections


def infer_type_and_patterns(text: str):
    low = text.lower()
    if 'api' in low or 'mcp' in low or 'cli' in low or '浏览器' in text:
        return 'tool-wrapper', ['inversion', 'tool-wrapper', 'pipeline']
    if '评审' in text or '审查' in text or '评分' in text or '诊断' in text:
        return 'analyzer', ['inversion', 'reviewer', 'generator']
    if '生成' in text or '撰写' in text or '文档' in text:
        return 'writer', ['inversion', 'generator']
    return 'builder', ['inversion', 'pipeline', 'generator']


def normalize_name(name: str) -> str:
    clean_name = re.sub(r'[^a-z0-9-]', '-', name.lower())
    clean_name = re.sub(r'-+', '-', clean_name).strip('-')
    return clean_name or 'legacy-skill'


def build_skill_yaml(detected_name: str, inferred_type: str, patterns):
    lines = []
    lines.append('skill:')
    lines.append(f'  name: {normalize_name(detected_name)}')
    lines.append('  version: v3')
    lines.append(f'  type: {inferred_type}')
    lines.append('  user_invocable: true')
    lines.append('')
    lines.append('intent:')
    lines.append('  goal: [migrated from legacy skill; refine manually]')
    lines.append('  primary_input: [to be confirmed]')
    lines.append('  primary_output: [to be confirmed]')
    lines.append('  constraints:')
    lines.append('    - ask clarifying questions when context is insufficient')
    lines.append('')
    lines.append('patterns:')
    for pattern in patterns:
        lines.append(f'  - {pattern}')
    lines.append('')
    lines.append('flow:')
    lines.append('  - id: clarify')
    lines.append('    condition: missing_context')
    lines.append('    action: ask_questions')
    lines.append('')
    lines.append('fallback:')
    lines.append('  insufficient_info: ask_more')
    lines.append('  out_of_scope: refuse')
    lines.append('')
    lines.append('output:')
    lines.append('  format: markdown')
    lines.append('  sections:')
    lines.append('    - summary')
    lines.append('')
    lines.append('boundaries:')
    lines.append('  - do not write runtime data back into the skill directory')
    return '\n'.join(lines)


def build_report(skill_md_path: str, text: str, sections):
    inferred_type, patterns = infer_type_and_patterns(text)
    detected_name = os.path.basename(os.path.dirname(os.path.abspath(skill_md_path))) or 'unknown-skill'

    report = []
    report.append('# Migration Report')
    report.append('')
    report.append('## Legacy Skill')
    report.append(f'- path: {skill_md_path}')
    report.append(f'- detected_name: {detected_name}')
    report.append('')
    report.append('## Proposed v3 Type')
    report.append(f'- type: {inferred_type}')
    report.append('- rationale: based on legacy wording and dominant task shape')
    report.append('')
    report.append('## Proposed Patterns')
    for pattern in patterns:
        report.append(f'- {pattern}')
    report.append('')
    report.append('## Extraction Summary')
    for key, values in sections.items():
        report.append(f'### {key}')
        if not values:
            report.append('- (none)')
        else:
            for item in values[:10]:
                report.append(f'- {item}')
        report.append('')
    report.append('## Proposed Directory Split')
    report.append('- `SKILL.md`: 保留角色、适用范围、Pipeline、边界')
    report.append('- `skill.yaml`: 抽取 type / intent / patterns / flow / fallback / output / boundaries')
    report.append('- `references/`: 放 rubric / checklist / 规则 / 方法说明')
    report.append('- `assets/`: 放模板 / 示例 / 输出格式')
    report.append('- `scripts/`: 放初始化、验证、迁移辅助脚本')
    report.append('- `evals/`: 按需加入行为样例')
    report.append('')
    report.append('## Risks / Manual Review Needed')
    report.append('- 旧 skill 中的隐式约束可能未被自动识别')
    report.append('- 需要人工确认是否存在环境专属依赖')
    report.append('- 需要人工确认哪些内容属于 few-shot 示例而非规则')
    return '\n'.join(report)


def main(skill_md_path: str):
    if not os.path.exists(skill_md_path):
        print(f'❌ 文件不存在: {skill_md_path}', file=sys.stderr)
        return 1

    text, sections = analyze_legacy_skill(skill_md_path)
    inferred_type, patterns = infer_type_and_patterns(text)
    detected_name = os.path.basename(os.path.dirname(os.path.abspath(skill_md_path))) or 'unknown-skill'

    report = build_report(skill_md_path, text, sections)
    report_path = os.path.join(os.path.dirname(os.path.abspath(skill_md_path)), 'migration-report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    skill_yaml_draft = build_skill_yaml(detected_name, inferred_type, patterns)
    skill_yaml_path = os.path.join(os.path.dirname(os.path.abspath(skill_md_path)), 'skill.yaml.draft')
    with open(skill_yaml_path, 'w', encoding='utf-8') as f:
        f.write(skill_yaml_draft)

    print(f'✅ 已生成迁移报告: {report_path}')
    print(f'✅ 已生成 skill.yaml 草案: {skill_yaml_path}')
    print(report)
    return 0


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'SKILL.md'
    raise SystemExit(main(target))
