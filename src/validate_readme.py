import sys
from pathlib import Path

from engine import (
    SpecError,
    load_rules,
    load_sections,
    load_tone_profiles,
    load_yaml,
    parse_args,
    validate_readme,
)


def main() -> int:
    parser = parse_args()
    parser.add_argument("--readme", default="README.md")
    args = parser.parse_args()

    try:
        spec = load_yaml(Path(args.spec))
        sections = load_sections(Path(args.sections))
        rules = load_rules(Path(args.rules))
        tone_profiles = load_tone_profiles(Path(args.tone))
        readme_text = Path(args.readme).read_text(encoding="utf-8")
        errors = validate_readme(
            readme_text,
            spec,
            sections,
            rules,
            tone_profiles,
            Path(args.repo_root),
        )
    except (SpecError, ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        print("FAIL: README does not match spec")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: README matches spec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
