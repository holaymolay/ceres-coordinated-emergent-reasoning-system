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
)


def main() -> int:
    parser = parse_args()
    parser.add_argument("--output", default="README.md")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    try:
        spec = load_yaml(Path(args.spec))
        sections = load_sections(Path(args.sections))
        rules = load_rules(Path(args.rules))
        tone_profiles = load_tone_profiles(Path(args.tone))
        readme = render_readme(
            spec,
            sections,
            rules,
            tone_profiles,
            Path(args.repo_root),
        )
    except (SpecError, ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.stdout or args.output == "-":
        sys.stdout.write(readme)
        return 0

    output_path = Path(args.output)
    output_path.write_text(readme, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
