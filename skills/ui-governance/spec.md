# Design capability levels
This spec defines capability levels for UI rendering sessions.
It scopes how much design freedom is permitted per session.
Capabilities never bypass the intent protocol.
Patterns declare the minimum capability required to use them.

## Capability levels
### Utility
- Internal tools.
- Zero creativity.
- Strict canonical patterns only.

### Baseline
- Public-facing default.
- Restrained, modern, neutral.
- Limited pattern variation allowed.

### Expressive
- Designer-controlled interpretation.
- Expanded pattern selection.
- Tokens may be remapped.

### Custom
- Full override.
- Framework provides infrastructure only.

## Rules
- Capabilities do not bypass the intent protocol.
- Patterns declare minimum required capability.
- Lower levels cannot access higher-level patterns.
