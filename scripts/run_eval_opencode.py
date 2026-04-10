#!/usr/bin/env python3
"""OpenCode/OpenClaw trigger evaluation preparation.

This script prepares the environment for trigger testing using Task tool
instead of CLI subprocess. The actual evaluation must be executed by the
main agent using Task tool calls.

Usage:
    python run_eval_opencode.py prepare --skill-path <path> --eval-set <json>
    python run_eval_opencode.py check-result --run-dir <path>

The workflow:
1. prepare: Creates temp skill, outputs JSON with test instructions
2. Main agent reads JSON, calls Task tool for each test query
3. check-result: Analyzes Task output to determine if skill triggered
"""

import argparse
import json
import uuid
import sys
from pathlib import Path
from scripts.platform import get_skills_dir, detect_platform
from scripts.utils import parse_skill_md


def prepare_eval(
    eval_set: list[dict],
    skill_path: Path,
    workspace_dir: Path,
) -> dict:
    """Prepare evaluation environment for Task-based testing.

    Creates:
    - Temporary test skills in skills directory
    - Test configuration JSON for main agent to read

    Args:
        eval_set: List of {"query": str, "should_trigger": bool}
        skill_path: Path to original skill being tested
        workspace_dir: Directory to save test configuration

    Returns:
        Dict with instructions for main agent to execute
    """
    platform = detect_platform()
    skills_dir = get_skills_dir(platform)

    # Parse original skill
    name, description, content = parse_skill_md(skill_path)

    # Create unique test ID
    test_id = uuid.uuid4().hex[:8]
    temp_skill_name = f"{name}-test-{test_id}"

    # Create temp skill directory
    temp_skill_dir = skills_dir / temp_skill_name
    temp_skill_dir.mkdir(parents=True, exist_ok=True)

    # Write temp SKILL.md with description being tested
    skill_md_content = f"""---
name: {temp_skill_name}
description: {description}
---

# {temp_skill_name}

This skill handles: {description}

{content}
"""
    (temp_skill_dir / "SKILL.md").write_text(skill_md_content)

    # Prepare test configuration
    test_config = {
        "test_id": test_id,
        "original_skill_path": str(skill_path),
        "temp_skill_name": temp_skill_name,
        "temp_skill_path": str(temp_skill_dir),
        "description": description,
        "evals": [
            {
                "id": i,
                "query": item["query"],
                "should_trigger": item["should_trigger"],
                "temp_skill_name": temp_skill_name,
            }
            for i, item in enumerate(eval_set)
        ],
        "instructions": """
For each eval in evals list:
1. Call Task tool with subagent_type="general"
2. Task prompt should include the query
3. After Task completes, check if skill was loaded:
   - Look for "skill" mentions in output
   - Check for tool calls related to the skill
   - Use run_eval_opencode.py check-result to analyze
""",
    }

    # Save to workspace
    config_path = workspace_dir / "trigger_eval_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(test_config, indent=2))

    return test_config


def check_trigger_result(
    transcript_path: Path,
    temp_skill_name: str,
) -> bool:
    """Check if a skill was triggered based on transcript/session output.

    Args:
        transcript_path: Path to transcript.md or session output
        temp_skill_name: Name of temp skill to check for

    Returns:
        True if skill appears to have been triggered/loaded
    """
    if not transcript_path.exists():
        return False

    content = transcript_path.read_text(errors="replace")

    # Check for various indicators of skill loading
    indicators = [
        temp_skill_name,  # Skill name mentioned
        "skill",  # Generic skill reference
        "SKILL.md",  # Skill file reference
        "available_skills",  # Skills list reference
    ]

    # Look for skill-related content
    for indicator in indicators:
        if indicator.lower() in content.lower():
            return True

    # Additional check: look for tool calls that match skill behavior
    # This is a heuristic - actual skill usage patterns vary
    if "skill" in content.lower():
        return True

    return False


def cleanup_temp_skill(temp_skill_path: Path) -> None:
    """Remove temporary skill created for testing.

    Args:
        temp_skill_path: Path to temp skill directory
    """
    if temp_skill_path.exists():
        import shutil

        shutil.rmtree(temp_skill_path)


def main():
    parser = argparse.ArgumentParser(description="OpenCode trigger eval preparation")
    parser.add_argument("action", choices=["prepare", "check-result", "cleanup"])
    parser.add_argument("--skill-path", type=Path, help="Path to skill being tested")
    parser.add_argument("--eval-set", type=Path, help="Path to eval set JSON")
    parser.add_argument(
        "--workspace", type=Path, default=Path.cwd(), help="Workspace directory"
    )
    parser.add_argument(
        "--transcript", type=Path, help="Path to transcript for check-result"
    )
    parser.add_argument(
        "--temp-skill-name", type=str, help="Temp skill name for check-result"
    )
    parser.add_argument(
        "--temp-skill-path", type=Path, help="Temp skill path for cleanup"
    )
    args = parser.parse_args()

    if args.action == "prepare":
        if not args.skill_path or not args.eval_set:
            print(
                "Error: --skill-path and --eval-set required for prepare",
                file=sys.stderr,
            )
            sys.exit(1)

        eval_set = json.loads(args.eval_set.read_text())
        result = prepare_eval(eval_set, args.skill_path, args.workspace)
        print(json.dumps(result, indent=2))

    elif args.action == "check-result":
        if not args.transcript or not args.temp_skill_name:
            print(
                "Error: --transcript and --temp-skill-name required for check-result",
                file=sys.stderr,
            )
            sys.exit(1)

        triggered = check_trigger_result(args.transcript, args.temp_skill_name)
        print(json.dumps({"triggered": triggered}))

    elif args.action == "cleanup":
        if not args.temp_skill_path:
            print("Error: --temp-skill-path required for cleanup", file=sys.stderr)
            sys.exit(1)

        cleanup_temp_skill(args.temp_skill_path)
        print(json.dumps({"cleaned": str(args.temp_skill_path)}))


if __name__ == "__main__":
    main()
