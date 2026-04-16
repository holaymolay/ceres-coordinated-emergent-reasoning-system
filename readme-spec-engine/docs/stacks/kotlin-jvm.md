# Stack Profile: Kotlin JVM (non-Spring)

Use this profile for Kotlin JVM services/CLIs that are not Spring-based (e.g., Ktor, Micronaut, plain Kotlin). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- JDK 21 (match project); build with Gradle (wrapper preferred).
- Lint/format: `ktlint`/`detekt`; format via `ktlintFormat`/`detekt` autofix when configured.
- Testing: `./gradlew test`; frameworks: JUnit5 + MockK.

## Project Layout
- `src/main/kotlin` and `src/test/kotlin`; resources under `src/main/resources`.
- Keep build outputs in `build/` (ignored).

## Development Commands
- `./gradlew clean build`
- `./gradlew test`
- `./gradlew ktlintCheck` / `./gradlew detekt`
- `./gradlew run` or framework-specific run tasks (e.g., `./gradlew run` for Ktor).

## Style & Naming
- Follow Kotlin style; prefer immutability; use coroutines as appropriate.
- Use structured logging (e.g., `kotlin-logging`, `slf4j`); avoid `println` in production code.

## Testing Guidance
- Use MockK for mocking; keep tests isolated; avoid external I/O in unit tests.
- Configure test resources under `src/test/resources`.

## Configuration & Ops
- Externalize config (HOCON/YAML/env); avoid hardcoded secrets.
- Pin tool versions in Gradle wrapper/plugins; use BOMs when available.
