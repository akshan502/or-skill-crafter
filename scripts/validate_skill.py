import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from validators import validate_patterns, validate_semantics, validate_structure


def fail(message: str):
    print(f'❌ {message}', file=sys.stderr)


def ok(message: str):
    print(f'✅ {message}')


def validate_skill_dir(skill_dir: str) -> int:
    errors = []
    errors.extend(validate_structure(skill_dir))
    errors.extend(validate_semantics(skill_dir))
    errors.extend(validate_patterns(skill_dir))

    if errors:
        for err in errors:
            fail(err)
        return 1

    ok('结构 / 语义 / pattern 一致性校验通过')
    return 0


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    raise SystemExit(validate_skill_dir(target))
