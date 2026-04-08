import os
import re
import sys
from typing import Dict, List, Tuple


TEMPLATE_MAP = {
    'writer': 'assets/templates/writer-skill-template.md',
    'analyzer': 'assets/templates/analyzer-skill-template.md',
    'tool-wrapper': 'assets/templates/tool-wrapper-skill-template.md',
    'transformer': 'assets/templates/transformer-skill-template.md',
    'orchestrator': 'assets/templates/orchestrator-skill-template.md',
    'builder': 'assets/templates/builder-skill-template.md',
}


def parse_skill_yaml(path: str) -> Dict[str, object]:
    data = {
        'name': None,
        'type': None,
        'goal': None,
        'primary_input': None,
        'primary_output': None,
        'patterns': [],
        'boundaries': [],
        'output_sections': [],
        'fallback': {},
        'flow_steps': [],
    }
    section = None
    current_flow_step = None

    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip('\n')
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            if stripped in {'skill:', 'intent:', 'patterns:', 'flow:', 'fallback:', 'output:', 'boundaries:'}:
                section = stripped[:-1]
                continue

            if section == 'skill':
                m = re.match(r'^\s*(name|type):\s*(.+?)\s*$', line)
                if m:
                    key, value = m.group(1), m.group(2)
                    data[key] = value
            elif section == 'intent':
                m = re.match(r'^\s*(goal|primary_input|primary_output):\s*(.+?)\s*$', line)
                if m:
                    data[m.group(1)] = m.group(2)
            elif section == 'patterns':
                m = re.match(r'^\s*-\s*(.+?)\s*$', line)
                if m:
                    data['patterns'].append(m.group(1))
            elif section == 'flow':
                m_step = re.match(r'^\s*-\s*id:\s*(.+?)\s*$', line)
                if m_step:
                    current_flow_step = {'id': m_step.group(1)}
                    data['flow_steps'].append(current_flow_step)
                    continue
                m_attr = re.match(r'^\s*(condition|action):\s*(.+?)\s*$', stripped)
                if m_attr and current_flow_step is not None:
                    current_flow_step[m_attr.group(1)] = m_attr.group(2)
            elif section == 'fallback':
                m = re.match(r'^\s*([a-zA-Z0-9_-]+):\s*(.+?)\s*$', line)
                if m:
                    data['fallback'][m.group(1)] = m.group(2)
            elif section == 'boundaries':
                m = re.match(r'^\s*-\s*(.+?)\s*$', line)
                if m:
                    data['boundaries'].append(m.group(1))
            elif section == 'output':
                m = re.match(r'^\s*-\s*(.+?)\s*$', line)
                if m:
                    data['output_sections'].append(m.group(1))

    return data


def choose_template(skill_type: str) -> Tuple[str, str | None]:
    if skill_type in TEMPLATE_MAP:
        return TEMPLATE_MAP[skill_type], None
    return TEMPLATE_MAP['writer'], f'{skill_type} 无专用模板，已降级为 writer 模板。'


def render_skill_md(template_text: str, data: Dict[str, object]) -> str:
    name = data.get('name') or 'new-skill'
    rendered = template_text
    for placeholder in [
        '[writer-skill-name]',
        '[analyzer-skill-name]',
        '[tool-wrapper-skill-name]',
        '[transformer-skill-name]',
        '[orchestrator-skill-name]',
        '[builder-skill-name]',
    ]:
        rendered = rendered.replace(placeholder, name)

    goal = data.get('goal') or '[请补充技能目标]'
    primary_input = data.get('primary_input') or '[请补充核心输入]'
    primary_output = data.get('primary_output') or '[请补充核心输出]'
    rendered += '\n\n## 编译注记\n'
    rendered += f'- 目标: {goal}\n'
    rendered += f'- 核心输入: {primary_input}\n'
    rendered += f'- 核心输出: {primary_output}\n'

    rendered += '\n' + build_dynamic_sections(data)
    return rendered


def build_plan(data: Dict[str, object], template_path: str, downgrade_note: str | None) -> str:
    lines: List[str] = []
    lines.append('# Compile Plan')
    lines.append('')
    lines.append(f"- name: {data.get('name')}")
    lines.append(f"- type: {data.get('type')}")
    lines.append(f"- template: {template_path}")
    if downgrade_note:
        lines.append(f"- downgrade_note: {downgrade_note}")
    if data.get('goal'):
        lines.append(f"- goal: {data.get('goal')}")
    if data.get('primary_input'):
        lines.append(f"- primary_input: {data.get('primary_input')}")
    if data.get('primary_output'):
        lines.append(f"- primary_output: {data.get('primary_output')}")
    if data.get('patterns'):
        lines.append('- patterns:')
        for pattern in data['patterns']:
            lines.append(f'  - {pattern}')
    if data.get('flow_steps'):
        lines.append('- flow_steps:')
        for step in data['flow_steps']:
            lines.append(f"  - id: {step.get('id')}")
    if data.get('output_sections'):
        lines.append('- output_sections:')
        for section in data['output_sections']:
            lines.append(f'  - {section}')
    if data.get('boundaries'):
        lines.append('- boundaries:')
        for item in data['boundaries']:
            lines.append(f'  - {item}')
    return '\n'.join(lines)


def write_stub(path: str, title: str, bullets: List[str]):
    if os.path.exists(path):
        return
    lines = [f'# {title}', '']
    for bullet in bullets:
        lines.append(f'- {bullet}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def build_reference_stub(name: str, data: Dict[str, object]) -> Tuple[str, List[str]]:
    skill_type = str(data.get('type') or '')
    if name == 'rubric.md':
        return 'Rubric', [
            '评审维度：正确性 / 完整性 / 清晰度 / 可执行性',
            '每个维度建议采用 1-5 分评分',
            f'当前 skill type: {skill_type}',
        ]
    if name == 'review-checklist.md':
        return 'Review Checklist', [
            '是否先做了必要澄清',
            '是否给出了依据而不是只有结论',
            '是否区分必须修改与可优化项',
        ]
    if name == 'tool-contract.md':
        return 'Tool Contract', [
            '输入参数：名称 / 类型 / 是否必填 / 示例',
            '输出结果：成功结构 / 失败结构',
            '权限边界：哪些操作必须确认后执行',
        ]
    if name == 'parameter-spec.md':
        return 'Parameter Spec', [
            '参数名',
            '类型',
            '默认值',
            '校验规则',
        ]
    if name == 'workflow-rules.md':
        return 'Workflow Rules', [
            '阶段顺序',
            '阶段进入条件',
            '阶段退出条件',
        ]
    if name == 'gate-rules.md':
        return 'Gate Rules', [
            '哪些情况必须暂停等待确认',
            '哪些情况允许继续',
            '高风险动作的二次确认条件',
        ]
    if name == 'transformation-rules.md':
        return 'Transformation Rules', [
            '保留哪些信息',
            '丢弃哪些信息',
            '如何处理无法映射的部分',
        ]
    if name == 'field-mapping.md':
        return 'Field Mapping', [
            '源字段 → 目标字段',
            '一对多 / 多对一映射说明',
            '缺失字段处理策略',
        ]
    if name == 'build-rules.md':
        return 'Build Rules', [
            '哪些文件为必需',
            '哪些文件为可选',
            '哪些内容只能生成草案不能假装最终完成',
        ]
    if name == 'layout-guide.md':
        return 'Layout Guide', [
            '根目录文件职责',
            'references/、assets/、scripts/、evals/ 的边界',
            '运行时数据不得写回 skill 目录',
        ]
    return name.replace('.md', '').replace('-', ' ').title(), [
        '由 compile_skill.py 生成的参考文件草案',
        '请根据具体 skill 继续补充规则、rubric 或方法说明',
    ]


def build_asset_stub(name: str, data: Dict[str, object]) -> Tuple[str, List[str]]:
    skill_type = str(data.get('type') or '')
    if name == 'output-template.md':
        sections = data.get('output_sections') or ['summary']
        return 'Output Template', [
            '建议输出结构：',
            *[f'[{section}]' for section in sections],
            f'当前 skill type: {skill_type}',
        ]
    if name == 'question-prompts.md':
        return 'Question Prompts', [
            '这个技能要解决的核心问题是什么？',
            '核心输入和期望输出分别是什么？',
            '有哪些不能违反的边界或风险？',
        ]
    return name.replace('.md', '').replace('-', ' ').title(), [
        '由 compile_skill.py 生成的资产文件草案',
        '请根据具体 skill 继续补充模板、示例或提示片段',
    ]


def write_recommended_files(skill_dir: str, data: Dict[str, object]):
    references_dir = os.path.join(skill_dir, 'references')
    assets_dir = os.path.join(skill_dir, 'assets')
    os.makedirs(references_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    references_path = os.path.join(references_dir, 'recommended-files.md')
    assets_path = os.path.join(assets_dir, 'recommended-files.md')

    references_lines = ['# Recommended Reference Files', '']
    assets_lines = ['# Recommended Asset Files', '']

    ref_stubs = []
    asset_stubs = []

    for pattern in data.get('patterns', []):
        if pattern == 'reviewer':
            references_lines.append('- references/review-checklist.md')
            references_lines.append('- references/rubric.md')
            ref_stubs.extend(['review-checklist.md', 'rubric.md'])
        if pattern == 'tool-wrapper':
            references_lines.append('- references/tool-contract.md')
            references_lines.append('- references/parameter-spec.md')
            ref_stubs.extend(['tool-contract.md', 'parameter-spec.md'])
        if pattern == 'generator':
            assets_lines.append('- assets/output-template.md')
            asset_stubs.append('output-template.md')
        if pattern == 'inversion':
            assets_lines.append('- assets/question-prompts.md')
            asset_stubs.append('question-prompts.md')

    if data.get('type') == 'orchestrator':
        references_lines.append('- references/workflow-rules.md')
        references_lines.append('- references/gate-rules.md')
        ref_stubs.extend(['workflow-rules.md', 'gate-rules.md'])
    if data.get('type') == 'transformer':
        references_lines.append('- references/transformation-rules.md')
        references_lines.append('- references/field-mapping.md')
        ref_stubs.extend(['transformation-rules.md', 'field-mapping.md'])
    if data.get('type') == 'builder':
        references_lines.append('- references/build-rules.md')
        references_lines.append('- references/layout-guide.md')
        ref_stubs.extend(['build-rules.md', 'layout-guide.md'])

    with open(references_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(dict.fromkeys(references_lines)))
    with open(assets_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(dict.fromkeys(assets_lines)))

    for name in dict.fromkeys(ref_stubs):
        title, bullets = build_reference_stub(name, data)
        write_stub(os.path.join(references_dir, name), title, bullets)
    for name in dict.fromkeys(asset_stubs):
        title, bullets = build_asset_stub(name, data)
        write_stub(os.path.join(assets_dir, name), title, bullets)


def build_dynamic_sections(data: Dict[str, object]) -> str:
    lines: List[str] = []

    if data.get('patterns'):
        lines.append('## Pattern 映射')
        for pattern in data['patterns']:
            lines.append(f'- {pattern}')
        lines.append('')

    if data.get('flow_steps'):
        lines.append('## Pipeline 细化')
        for i, step in enumerate(data['flow_steps'], start=1):
            line = f"### Step {i}: {step.get('id')}"
            lines.append(line)
            if step.get('condition'):
                lines.append(f'- condition: {step.get("condition")}')
            if step.get('action'):
                lines.append(f'- action: {step.get("action")}')
        lines.append('')

    if data.get('fallback'):
        lines.append('## Fallback 细化')
        for key, value in data['fallback'].items():
            lines.append(f'- {key}: {value}')
        lines.append('')

    if data.get('output_sections'):
        lines.append('## 输出章节映射')
        for section in data['output_sections']:
            lines.append(f'- {section}')
        lines.append('')

    return '\n'.join(lines)


def write_compile_review(skill_dir: str, data: Dict[str, object], template_rel: str, downgrade_note: str | None):
    review_path = os.path.join(skill_dir, 'compile-review.md')
    lines = ['# Compile Review', '']
    lines.append(f"- selected_template: {template_rel}")
    lines.append(f"- detected_type: {data.get('type')}")
    if downgrade_note:
        lines.append(f"- downgrade_note: {downgrade_note}")
    lines.append('')
    lines.append('## Review Questions')
    lines.append('- `SKILL.generated.md` 是否可直接替代现有 `SKILL.md`，还是仅作为草案？')
    lines.append('- `references/` 与 `assets/` 草案文件名是否合理？')
    lines.append('- 是否需要根据实际场景补更多专用模板或规则文件？')
    lines.append('- DSL 的 flow / fallback / output 是否已被正确反映？')
    with open(review_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def main(skill_dir: str):
    skill_yaml = os.path.join(skill_dir, 'skill.yaml')
    if not os.path.exists(skill_yaml):
        print(f'❌ 缺少 skill.yaml: {skill_yaml}', file=sys.stderr)
        return 1

    data = parse_skill_yaml(skill_yaml)
    if not data.get('name') or not data.get('type'):
        print('❌ skill.yaml 缺少 name 或 type', file=sys.stderr)
        return 1

    template_rel, downgrade_note = choose_template(str(data['type']))
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(repo_root, template_rel)
    if not os.path.exists(template_path):
        print(f'❌ 模板不存在: {template_path}', file=sys.stderr)
        return 1

    with open(template_path, 'r', encoding='utf-8') as f:
        template_text = f.read()

    compiled_skill = render_skill_md(template_text, data)
    compiled_path = os.path.join(skill_dir, 'SKILL.generated.md')
    with open(compiled_path, 'w', encoding='utf-8') as f:
        f.write(compiled_skill)

    plan = build_plan(data, template_rel, downgrade_note)
    plan_path = os.path.join(skill_dir, 'compile-plan.md')
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(plan)

    write_recommended_files(skill_dir, data)
    write_compile_review(skill_dir, data, template_rel, downgrade_note)

    print(f'✅ 已生成编译计划: {plan_path}')
    print(f'✅ 已生成草案文件: {compiled_path}')
    print(f'✅ 已生成推荐资源文件: {os.path.join(skill_dir, "references", "recommended-files.md")}')
    print(f'✅ 已生成推荐资源文件: {os.path.join(skill_dir, "assets", "recommended-files.md")}')
    print(f'✅ 已生成编译审阅说明: {os.path.join(skill_dir, "compile-review.md")}')
    if downgrade_note:
        print(f'ℹ️ {downgrade_note}')
    return 0


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    raise SystemExit(main(target))
