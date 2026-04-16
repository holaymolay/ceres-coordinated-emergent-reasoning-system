# Stack Profile: Java (Spring)

Use this profile for Java services built with Spring (Boot/MVC). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- JDK 21 (or project-specified LTS). Align local and CI toolchains.
- Build tool: Maven (`mvn`) or Gradle (`./gradlew`). Match the repo’s wrapper; prefer wrapper scripts over system installs.
- Lint/format: `spotless`/`checkstyle`/`google-java-format` per project config.
- Testing: JUnit 5; mocking with Mockito; integration tests via Spring Test.

## Project Layout
- Standard Spring Boot structure under `src/main/java` and `src/test/java`.
- Configuration in `src/main/resources`; test resources in `src/test/resources`.
- Keep generated artifacts in `target/` or `build/` and out of VCS.

## Development Commands
- Maven: `./mvnw clean verify` (or `./mvnw test`), `./mvnw spring-boot:run` for local run.
- Gradle: `./gradlew clean check`, `./gradlew bootRun` for local run.
- Format: `./mvnw spotless:apply` or `./gradlew spotlessApply` when configured.
- Dependency updates: prefer BOMs; avoid local SNAPSHOT drift unless intentional.

## Style & Naming
- Follow project checkstyle/format rules; keep package names lowercase.
- Components/services/repos annotated per Spring conventions; avoid circular deps.
- Use framework logging (`slf4j`/`Logback`); no `System.out.println` in production code.

## Testing Guidance
- Unit tests under `src/test/java`; use Spring’s `@SpringBootTest` sparingly—favor sliced tests (`@WebMvcTest`, etc.).
- Keep test data in resources or builders; avoid hitting real external services.
- Measure coverage via build tool reports (`jacoco`); watch thresholds if enforced.

## Configuration & Ops
- Externalize config via `application.yml`/`application.properties` with profile overlays; avoid hardcoded secrets.
- Use `local`/`dev`/`prod` Spring profiles; document new keys and defaults.
- Run dependency/security scans (e.g., `mvn -Psecurity verify`, `gradle dependencyCheckAnalyze`, or org-specific tools) and record waivers.
