import sys
from pathlib import Path

from engine import (
    SpecError,
    load_rules,
    load_sections,
    load_tone_profiles,
    load_yaml,
    parse_args,
    render_readme,
    semantic_diff,
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
        expected = render_readme(
            spec,
            sections,
            rules,
            tone_profiles,
            Path(args.repo_root),
        )
        diff_text = semantic_diff(readme_text, expected)
    except (SpecError, ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if diff_text.strip() == "README Semantic Diff":
        print("README Semantic Diff")
        print("- No differences found")
        return 0

    sys.stdout.write(diff_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
