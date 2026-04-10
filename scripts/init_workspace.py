import os
import sys
import re

def get_skills_directory():
    """获取 skills 目录路径（脚本位于 skills/skill-crafter/scripts/）"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.dirname(os.path.dirname(script_dir))
    return skills_dir

def create_skill_structure(raw_name):
    """为新技能创建符合 ADK 规范的目录结构，强制转换为规范命名"""
    # 强制将名称转换为仅包含小写字母、数字和连字符的格式
    clean_name = re.sub(r'[^a-z0-9-]', '-', raw_name.lower())
    clean_name = re.sub(r'-+', '-', clean_name).strip('-')
    
    if not clean_name:
        clean_name = "new-agent-skill"

    skills_dir = get_skills_directory()
    base_dir = os.path.join(skills_dir, clean_name)
    directories =[
        os.path.join(base_dir, 'scripts'),
        os.path.join(base_dir, 'references'),
        os.path.join(base_dir, 'assets')
    ]
    
    try:
        os.makedirs(base_dir, exist_ok=True)
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            # 创建 .gitkeep 占位符确保目录结构完整
            with open(os.path.join(directory, '.gitkeep'), 'w') as f:
                pass
        print(f"✅ 成功初始化 ADK 技能目录: {base_dir}")
        print("📁 包含子目录: scripts/, references/, assets/")
    except Exception as e:
        print(f"❌ 创建目录失败: {e}", file=sys.stderr)

if __name__ == "__main__":
    target_name = sys.argv[1] if len(sys.argv) > 1 else "new-agent-skill"
    create_skill_structure(target_name)