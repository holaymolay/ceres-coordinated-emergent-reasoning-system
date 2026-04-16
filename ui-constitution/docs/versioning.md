# Versioning

The Visual Constitution uses semantic versioning (MAJOR.MINOR.PATCH).

- MAJOR: breaking changes to constraints (removal of allowed values, tighter limits, renamed fields).
- MINOR: additive changes that preserve existing constraints (new optional fields, added roles that do not invalidate existing documents).
- PATCH: documentation updates or clarifications with no schema changes.

The top-level `version` field in a constitution document must match the repository release tag for that version.
