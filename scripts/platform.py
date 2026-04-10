#!/usr/bin/env python3
"""Platform detection module for skill-crafter.

Detects the current execution environment to choose appropriate implementation:
- claude-code: Claude Code CLI (claude command available)
- opencode: OpenCode CLI (opencode command available)
- openclaw: OpenClaw workspace environment
"""

import os
import subprocess
from pathlib import Path


def detect_platform() -> str:
    """Detect current platform environment.

    Returns:
        "claude-code" - Claude Code CLI available, CLAUDECODE env exists, or .claude/ directory
        "opencode"    - OpenCode CLI available, OPENCODE env exists, or .opencode context
        "openclaw"    - OpenClaw workspace (sandbox structure, skills/ in workspace)
    """
    cwd = Path.cwd()

    # Priority 1: Environment variables (most reliable)
    if os.environ.get("CLAUDECODE"):
        return "claude-code"
    if os.environ.get("OPENCODE"):
        return "opencode"

    # Priority 2: Directory structure markers
    if (cwd / ".claude").exists():
        return "claude-code"
    if (cwd / ".opencode").exists():
        return "opencode"

    # Check for OpenClaw workspace structure
    for parent in [cwd, *cwd.parents]:
        if (parent / "sandboxes").exists() or (parent / "skills").exists():
            # Additional check: if .claude also exists, prefer claude-code
            if (parent / ".claude").exists():
                return "claude-code"
            return "openclaw"

    # Priority 3: CLI availability
    if is_cli_available("claude"):
        return "claude-code"
    if is_cli_available("opencode"):
        return "opencode"

    # Default fallback
    return "opencode"


def is_cli_available(cli_name: str) -> bool:
    """Check if a CLI tool is available in PATH.

    Args:
        cli_name: Name of the CLI tool (e.g., "claude", "opencode")

    Returns:
        True if CLI is available, False otherwise
    """
    try:
        subprocess.run(
            [cli_name, "--version"],
            capture_output=True,
            check=True,
            timeout=5,
        )
        return True
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        return False


def get_skills_dir(platform: str) -> Path:
    """Get the appropriate skills directory for the platform.

    Args:
        platform: Platform name from detect_platform()

    Returns:
        Path to skills directory
    """
    cwd = Path.cwd()

    if platform == "claude-code":
        # Claude Code uses .claude/commands/ for skill-like commands
        for parent in [cwd, *cwd.parents]:
            if (parent / ".claude").exists():
                return parent / ".claude" / "commands"
        return cwd / ".claude" / "commands"

    elif platform == "opencode":
        # OpenCode uses ~/.config/opencode/skills/
        config_dir = Path.home() / ".config" / "opencode" / "skills"
        if config_dir.exists():
            return config_dir
        # Fallback: check current project
        for parent in [cwd, *cwd.parents]:
            if (parent / "skills").exists():
                return parent / "skills"
        return config_dir

    elif platform == "openclaw":
        # OpenClaw uses workspace/skills/ or sandbox/skills/
        for parent in [cwd, *cwd.parents]:
            if (parent / "skills").exists():
                return parent / "skills"
        return cwd / "skills"

    else:
        return cwd / "skills"


def get_project_root(platform: str) -> Path:
    """Get the project root directory for the platform.

    Args:
        platform: Platform name from detect_platform()

    Returns:
        Path to project root
    """
    cwd = Path.cwd()

    if platform == "claude-code":
        # Claude Code project root: find .claude/ directory
        for parent in [cwd, *cwd.parents]:
            if (parent / ".claude").exists():
                return parent
        return cwd

    elif platform == "opencode":
        # OpenCode project root
        for parent in [cwd, *cwd.parents]:
            if (parent / ".opencode").exists() or (parent / "opencode.json").exists():
                return parent
        return cwd

    elif platform == "openclaw":
        # OpenClaw workspace root
        for parent in [cwd, *cwd.parents]:
            if (parent / "sandboxes").exists():
                return parent
        return cwd

    else:
        return cwd


def supports_cli_eval(platform: str) -> bool:
    """Check if platform supports CLI-based evaluation (claude -p style).

    Args:
        platform: Platform name from detect_platform()

    Returns:
        True if platform supports CLI eval, False if needs Task tool
    """
    return platform == "claude-code"


if __name__ == "__main__":
    platform = detect_platform()
    print(f"Detected platform: {platform}")
    print(f"Skills directory: {get_skills_dir(platform)}")
    print(f"Project root: {get_project_root(platform)}")
    print(f"Supports CLI eval: {supports_cli_eval(platform)}")
