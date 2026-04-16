# Versioning

Versioning keeps schema evolution and pattern changes predictable.

## Registry versions
- The repository follows semver. Initial release: `v0.1.0` (package version `0.1.0`).
- Tag releases in git (e.g., `v0.1.0`) after validation passes and docs are updated.
- Breaking schema changes require a major bump; additive fields land in minors.

## Schema versions
- `schema_version` in each pattern references the schema release (currently `0.1.0`).
- Schema updates must be reflected in `schemas/pattern.schema.json` plus validation tooling and tests.

## Pattern versions
- Each pattern carries its own `version` and `status` (`draft`, `stable`, `deprecated`).
- Increment a pattern’s `version` when its structure, roles, or constraints change.
- Deprecate patterns in-place before removal so adapters can migrate safely.

## Change process
1. Propose schema/pattern updates under a new spec or todo entry.
2. Update definitions and validation tests; rerun `npm run validate` and `npm test`.
3. Refresh docs and handover notes; bump repository/package version when cutting a release.
4. Tag the release and note it in `CHANGELOG.md`.
