# CLI

## Generate

```bash
python src/generate_readme.py --spec README_SPEC.yaml --output README.md
```

Optional flags:
- `--sections spec/sections.yaml`
- `--rules spec/rules.yaml`
- `--tone spec/tone.yaml`
- `--repo-root .`
- `--stdout` (print to stdout)

## Validate

```bash
python src/validate_readme.py --spec README_SPEC.yaml --readme README.md
```

Validation returns exit code 0 on pass and 1 on fail.

## Diff

```bash
python src/diff_readme.py --spec README_SPEC.yaml --readme README.md
```

The diff is semantic (section-aware) and compares README.md to the regenerated README.
