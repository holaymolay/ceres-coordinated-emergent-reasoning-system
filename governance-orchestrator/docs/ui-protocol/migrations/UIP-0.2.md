# UIP-0.2 Migration Guide (Template)

**Status:** Template (do not treat as an active migration)

## 1. Summary of changes
- <List key changes introduced in UIP-0.2>

Example:
- Added `schemaVersion` to UIEvent payloads
- Clarified adapter pattern selection rules

## 2. Motivation / observed failures
- <Describe why UIP-0.1 requires evolution>

Example:
- UIP-0.1 lacked explicit versioning for UIEvent, causing inconsistent adapters

## 3. Compatibility matrix (UIP-0.1 ↔ UIP-0.2)
| Artifact | UIP-0.1 | UIP-0.2 | Compatibility |
| --- | --- | --- | --- |
| UIIntent | <v0.1> | <v0.2> | <compatible/incompatible> |
| UIEvent | <v0.1> | <v0.2> | <compatible/incompatible> |
| Adapter | <v0.1> | <v0.2> | <compatible/incompatible> |

## 4. Required actions

### Skill authors
- <Required updates for skills emitting UIIntent>

Example:
- Update emitters to output schemaVersion 0.2.0

### Adapter authors
- <Required updates for adapters>

Example:
- Update pattern registry to accept new intent fields

### Renderer authors
- <Required updates for renderers>

Example:
- Emit UIEvent schemaVersion 0.2.0 on output

## 5. Breaking vs additive change classification
- <Classify each change as breaking or additive>

Example:
- Breaking: UIEvent requires schemaVersion
- Additive: new optional UIIntent metadata

## 6. Sunset policy for prior versions
- <Define deprecation timeline and retirement date>

Example:
- UIP-0.1 supported for 90 days after UIP-0.2 release

## 7. CI enforcement changes
- <List new or modified checks>

Example:
- Enforce UIEvent schemaVersion in UIP compliance checks

## 8. Versioning rules
- Minor version: additive, backward compatible changes
- Major version: breaking changes, requires explicit migration
