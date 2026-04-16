# Stack Profile: Spec-Only (JSON Schema)

This repository is a spec-only artifact. It contains JSON Schema documents and supporting docs; no application runtime is included.

## Runtime & Tooling
- JSON Schema draft 2020-12 documents.
- No package manager, build system, or runtime required.
- Optional validation via third-party JSON Schema validators.

## Project Layout
- `constitution/` holds JSON Schema files for the Visual Constitution.
- `docs/` holds governance and constitution documentation.
- `specs/` holds task specs for governance traceability.
- Generated or cached artifacts should not be committed.

## Development Commands
- Install: n/a.
- Build: n/a.
- Lint/format: n/a (use editor defaults for Markdown/JSON).
- Test/coverage: n/a; validate schemas manually with a JSON Schema validator when needed.

## Style & Naming
- Use lowercase kebab-case filenames for schema documents.
- Keep schema IDs stable and versioned in semver.
- Avoid subjective language in schema descriptions.

## Testing Guidance
- Validate example JSON against the relevant schema using a standards-compliant validator.
- Keep examples in `docs/examples.md` and reference schema IDs.

## Configuration & Ops
- No environment variables or secrets.
- No runtime dependencies or migrations.
