# Stack Profile: Flutter

Use this profile for Flutter apps. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Flutter stable channel (match `flutter --version` in repo); Dart SDK bundled.
- Package manager: `flutter pub`.
- Lint/format: `flutter format` or `dart format`; `flutter analyze`.
- Testing: `flutter test`; integration tests via `flutter test integration_test`.

## Project Layout
- Standard Flutter structure under `lib/`, `test/`, `integration_test/`, `android/`, `ios/`, `web/` (if enabled).
- Build artifacts under `build/` (ignored).

## Development Commands
- `flutter pub get`
- `flutter analyze`
- `flutter format lib test integration_test`
- `flutter test`
- `flutter test integration_test` (or `flutter drive`) for integration/E2E
- `flutter run -d <device>` for local run

## Style & Naming
- Follow Dart style; widgets PascalCase; prefer const constructors where possible.
- Avoid `print` in committed code; use logging packages as standardized.

## Testing Guidance
- Unit/widget tests in `test/`; integration tests in `integration_test/`.
- Mock platform channels/network; keep golden tests stable with controlled fonts/assets.

## Configuration & Ops
- Manage secrets via env/CI; keep keystores/provisioning profiles out of VCS.
- Pin Flutter channel/version in CI; run `flutter pub outdated` periodically.
